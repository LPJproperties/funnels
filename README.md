# LPJ funnel engine

Static campaign pages for LPJ Properties. Each top-level folder is one funnel, with its own HTML, CSS, scripts, and images. GitHub Pages serves the repository as a project site at `https://lpjproperties.github.io/funnels/` once Pages is set to GitHub Actions. See [MIGRATION.md](MIGRATION.md) before any public link changes.

The pages that are live today stay where they are. This repository is a copy. It does not change [TXASC/DONNA-M](https://github.com/TXASC/DONNA-M) or [BeardedVentures/boo-tiful-home-basket](https://github.com/BeardedVentures/boo-tiful-home-basket).

## Layout

| Path | What it is |
|------|------------|
| `index.html` | Directory of the funnels. The old DONNA-M root redirected only to Home Valuation; that redirect was not copied, because this site hosts three campaigns. |
| `home-valuation/` | Home valuation landing page, print QR assets, and the in-browser QR generator. Copied from TXASC/DONNA-M at `b76de809bb0c5e0b5bdf6e3a7eb5e35b4cb33679`. |
| `hna/` | Highlands Neighborhood Association 2027 membership page and QR assets. Same DONNA-M commit. |
| `boo-basket/` | Boo-tiful Home Basket giveaway. Static files, no build. Copied from BeardedVentures/boo-tiful-home-basket at `7c08612c131b9e2cf0091e2c064b93a323cadd70`. |
| `n8n/` | Workflow exports for Home Valuation and HNA. CORS in these copies allows both the old Pages host and `https://lpjproperties.github.io`. |
| `shared/` | Notes only. Duplicated logos and similar form patterns are listed in [shared/README.md](shared/README.md) and were left inside each funnel. |
| `.github/workflows/check.yml` | Checks links, migration invariants, secrets, source hashes, and the vendored QR browser build on pull requests and non-main branch pushes. |
| `.github/workflows/pages.yml` | Runs the same checks, then deploys the repository root to GitHub Pages on every push to `main`. |
| `.nojekyll` | Already in the repo. Pages Actions upload the files as they are. |

Image, stylesheet, and script links inside each funnel are already relative (`assets/...`, `styles.css`, `src/app.mjs`). Those were left as relative paths. Absolute URLs that point at a campaign page were left pointing at the old site so printed QR codes and the QR generator keep their current target. The full list is in [MIGRATION.md](MIGRATION.md).

## Run a funnel locally

From the repository root:

```bash
python3 -m http.server 8080
```

Then open:

- http://127.0.0.1:8080/
- http://127.0.0.1:8080/home-valuation/
- http://127.0.0.1:8080/home-valuation/qr.html
- http://127.0.0.1:8080/hna/
- http://127.0.0.1:8080/boo-basket/

Run the same checks used by pull requests and the Pages workflow:

```bash
python3 -m unittest discover -s tests -p 'check_*.py' -v
node --test tests/qr_vendor.test.mjs
```

Boo Basket loads an ES module. Use a static server. A `file://` URL will not run it. On localhost, `http://127.0.0.1:8080/boo-basket/?preview=1` mocks the submit and does not email anyone.

## Add a funnel

1. Add a new top-level folder with a short hyphenated name. Put `index.html` and that campaign's assets inside it. Point images, CSS, and scripts at relative paths in that folder.
2. Add a link to the folder from the root `index.html`.
3. Write a `README.md` in the folder. If the funnel was copied, name the source repository and the commit SHA. If it is new, say what the page is for.
4. If the page submits a form, keep the endpoint in one place (a `config.js` or a single constant) and commit the workflow export under `n8n/`. Set Allowed Origins to `https://txasc.github.io,https://lpjproperties.github.io` with no space after the comma, for as long as the old host should keep working.
5. Keep passwords, API keys, and webhook URLs that contain a secret token out of git. Use a placeholder such as `YOUR_WEBHOOK_URL` and record the file and the kind of secret in `MIGRATION.md`.
6. Serve the repo locally and confirm the new page, its assets, and its form all load.
7. Merge to `main`. The Pages workflow publishes the folder at `https://lpjproperties.github.io/funnels/<folder>/`.

## Pages

Publishing is `.github/workflows/pages.yml`. In the GitHub repo, set **Settings → Pages → Build and deployment → Source** to **GitHub Actions**. The workflow runs when `main` changes. The public origin for CORS is `https://lpjproperties.github.io`. The pages themselves live under `/funnels/` because the repository name is `funnels`.
