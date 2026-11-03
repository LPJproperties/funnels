import hashlib
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
FUNNELS = ("home-valuation", "hna", "boo-basket")
ORIGINS = "https://txasc.github.io,https://lpjproperties.github.io"


class ReferenceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.remote_assets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for attr in ("href", "src"):
            value = attrs.get(attr)
            if value:
                self.references.append((tag, attr, value))
        if tag == "script" and attrs.get("src"):
            self.remote_assets.append((tag, attrs["src"]))
        if tag == "link" and attrs.get("href") and "stylesheet" in attrs.get("rel", ""):
            self.remote_assets.append((tag, attrs["href"]))


def html_parsers():
    for path in ROOT.rglob("*.html"):
        parser = ReferenceParser()
        parser.feed(path.read_text(encoding="utf-8"))
        yield path, parser


def local_target(source, reference):
    clean = unquote(reference.split("#", 1)[0].split("?", 1)[0])
    if not clean:
        return None
    parsed = urlparse(clean)
    if parsed.scheme or clean.startswith("//"):
        return None
    target = (source.parent / clean).resolve()
    if clean.endswith("/"):
        target /= "index.html"
    return target


class SiteChecks(unittest.TestCase):
    def test_01_three_funnels_are_present(self):
        for funnel in FUNNELS:
            self.assertTrue((ROOT / funnel / "index.html").is_file(), funnel)

    def test_02_root_index_links_each_funnel(self):
        text = (ROOT / "index.html").read_text(encoding="utf-8")
        for funnel in FUNNELS:
            self.assertRegex(text, rf'href=["\']{re.escape(funnel)}/["\']')

    def test_03_local_references_resolve(self):
        missing = []
        for path, parser in html_parsers():
            for _, _, reference in parser.references:
                if reference.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
                    continue
                target = local_target(path, reference)
                if target is not None and not target.exists():
                    missing.append(f"{path.relative_to(ROOT)} -> {reference}")
        for path in ROOT.rglob("*.css"):
            for reference in re.findall(r"url\([\"']?([^\"')]+)", path.read_text(encoding="utf-8")):
                target = local_target(path, reference)
                if target is not None and not target.exists():
                    missing.append(f"{path.relative_to(ROOT)} -> {reference}")
        for path in ROOT.rglob("*.mjs"):
            text = path.read_text(encoding="utf-8")
            for reference in re.findall(r"(?:from\s+|import\s*)[\"'](\.[^\"']+)[\"']", text):
                target = local_target(path, reference)
                if target is not None and not target.exists():
                    missing.append(f"{path.relative_to(ROOT)} -> {reference}")
        self.assertEqual([], missing)

    def test_04_no_root_absolute_asset_paths(self):
        bad = []
        for path, parser in html_parsers():
            for _, _, reference in parser.references:
                if reference.startswith("/") and not reference.startswith("//"):
                    bad.append(f"{path.relative_to(ROOT)} -> {reference}")
        for path in ROOT.rglob("*.css"):
            for reference in re.findall(r"url\([\"']?([^\"')]+)", path.read_text(encoding="utf-8")):
                if reference.startswith("/") and not reference.startswith("//"):
                    bad.append(f"{path.relative_to(ROOT)} -> {reference}")
        self.assertEqual([], bad)

    def test_05_external_scripts_and_styles_are_allowlisted(self):
        bad = []
        allowed = {"fonts.googleapis.com", "fonts.gstatic.com"}
        for path, parser in html_parsers():
            for _, reference in parser.remote_assets:
                host = urlparse(reference).hostname
                if host and host not in allowed:
                    bad.append(f"{path.relative_to(ROOT)} -> {reference}")
        self.assertEqual([], bad)

    def test_06_form_webhooks_stay_on_existing_jarvis_host(self):
        files = [ROOT / "home-valuation/index.html", ROOT / "hna/index.html", ROOT / "boo-basket/config.js"]
        found = []
        for path in files:
            urls = re.findall(r"https://[^\"'\s]+/webhook/[^\"'\s]+", path.read_text(encoding="utf-8"))
            self.assertEqual(1, len(urls), path.relative_to(ROOT))
            found.extend(urls)
        self.assertEqual(3, len(found))
        self.assertTrue(all(urlparse(url).hostname == "jarvis.tailb14d90.ts.net" for url in found))

    def test_07_n8n_ids_paths_and_origins(self):
        expected = {
            "home-valuation-lead.json": ("donnaHomeValLead1", "home-valuation"),
            "hna-membership.json": ("donnaHnaMember1", "hna-membership"),
        }
        for name, (workflow_id, webhook_path) in expected.items():
            data = json.loads((ROOT / "n8n" / name).read_text(encoding="utf-8"))
            self.assertEqual(workflow_id, data["id"])
            webhooks = [node for node in data["nodes"] if node["type"] == "n8n-nodes-base.webhook"]
            self.assertEqual(1, len(webhooks))
            params = webhooks[0]["parameters"]
            self.assertEqual(webhook_path, params["path"])
            self.assertEqual(ORIGINS, params["options"]["allowedOrigins"])

    def test_08_n8n_exports_contain_no_credentials(self):
        for path in (ROOT / "n8n").glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertNotIn("credentials", data)
            for node in data.get("nodes", []):
                self.assertNotIn("credentials", node, f"credential in {path.name}/{node.get('name')}")

    def test_09_source_manifest_matches_unchanged_files(self):
        manifest = json.loads((ROOT / "tests/source_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(19, len(manifest["files"]))
        self.assertEqual(3, sum("edited" in item for item in manifest["files"].values()))
        for relative, item in manifest["files"].items():
            path = ROOT / relative
            self.assertTrue(path.is_file(), relative)
            if "sha256" in item:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                self.assertEqual(item["sha256"], digest, relative)

    def test_10_no_secret_patterns(self):
        patterns = {
            "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
            "GitHub token": re.compile(r"\b(?:gh[opsu]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
            "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
            "generic secret assignment": re.compile(r"(?i)\b(?:api[_-]?key|client[_-]?secret|password|bearer[_-]?token)\b\s*[:=]\s*[\"'][^\"']{12,}[\"']"),
        }
        bad = []
        suffixes = {".html", ".js", ".mjs", ".json", ".md", ".yml", ".yaml"}
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in suffixes or "vendor" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            for label, pattern in patterns.items():
                if pattern.search(text):
                    bad.append(f"{path.relative_to(ROOT)}: {label}")
        self.assertEqual([], bad)


if __name__ == "__main__":
    unittest.main()
