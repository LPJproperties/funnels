# Migration checklist

Copies of the three campaigns are in this repository. The live pages are unchanged and keep serving the old URLs until you switch them yourself.

Old pages:

- https://txasc.github.io/DONNA-M/ (redirects to Home Valuation)
- https://txasc.github.io/DONNA-M/home-valuation/
- https://txasc.github.io/DONNA-M/hna/
- https://beardedventures.github.io/boo-tiful-home-basket/

New pages, after GitHub Pages is enabled and `main` has been deployed:

- https://lpjproperties.github.io/funnels/
- https://lpjproperties.github.io/funnels/home-valuation/
- https://lpjproperties.github.io/funnels/hna/
- https://lpjproperties.github.io/funnels/boo-basket/

The CORS origin is the host with no path: `https://lpjproperties.github.io`.

## Before any public link changes

- [ ] Merge the funnel copy to `main`.
- [ ] Confirm **Check site** passes. The Pages workflow also requires these checks before it can publish.
- [ ] In **Settings → Pages → Build and deployment**, set **Source** to **GitHub Actions**. A workflow file cannot change this setting. If the first Actions run fails because Pages is not enabled yet, turn the setting on and re-run **Deploy to GitHub Pages**.
- [ ] Open the four new URLs above and confirm each page paints, images load, and the form is on the page.
- [ ] Import `n8n/home-valuation-lead.json` and `n8n/hna-membership.json` into the existing n8n instance. The workflow ids are still `donnaHomeValLead1` and `donnaHnaMember1`, so import updates those workflows.
- [ ] Re-attach the SMTP credential on each Email node (see Secrets). The JSON does not include it.
- [ ] Confirm each webhook's Allowed Origins is exactly `https://txasc.github.io,https://lpjproperties.github.io` with no space after the comma. The old origin stays so the current sites can still submit.
- [ ] Upgrade n8n to **1.109.0 or newer** if it is older. Before that version, a webhook with several allowed origins answered every browser with the first origin only. The old origin is listed first, so the TXASC pages keep working on an older n8n, and the new pages fall through to the email fallback until the upgrade.
- [ ] Activate both workflows.
- [ ] On the Boo Basket workflow that already serves the path `boo-tiful-home-basket`, add `https://lpjproperties.github.io` the same way and leave `https://txasc.github.io` in the list. That workflow was not in the source repo, so it was not copied.
- [ ] Submit one test from each **old** URL and confirm it arrives (Home Valuation email, HNA email, Boo Basket entry). The old pages must still succeed.
- [ ] Submit one test from each **new** URL after the import. Home Valuation and HNA show "thank you" on success. A CORS or network failure opens the visitor's email app instead. Boo Basket shows "You're in" on success, and "We couldn't submit your entry" when the webhook rejects the browser.
- [ ] Leave printed QR codes and the QR generator's default URL on the old addresses until you decide to reprint. Inventory is below.
- [ ] Switch public links only after the tests above pass. This repo cannot redirect `txasc.github.io` or `beardedventures.github.io`. After the tests pass, a later edit in those repositories (a short redirect page) or a reprint of the QR codes is what moves traffic. Until then, existing print keeps opening the old pages.

## QR codes

Decoded from the copied image files. The files were not edited and were not regenerated.

| File | Encoded URL today | URL after you choose to switch |
|------|-------------------|--------------------------------|
| `home-valuation/assets/home-valuation-qr.png` | https://txasc.github.io/DONNA-M/home-valuation/ | https://lpjproperties.github.io/funnels/home-valuation/ |
| `home-valuation/assets/home-valuation-qr.svg` | https://txasc.github.io/DONNA-M/home-valuation/ | https://lpjproperties.github.io/funnels/home-valuation/ |
| `hna/assets/hna-qr.png` | https://txasc.github.io/DONNA-M/hna/ | https://lpjproperties.github.io/funnels/hna/ |
| `hna/assets/hna-qr.svg` | https://txasc.github.io/DONNA-M/hna/ | https://lpjproperties.github.io/funnels/hna/ |

Boo Basket's source has no QR image. Its payload `source` field is `boo-tiful-home-basket-qr`, so a printed code may exist outside the repo. Anything printed for the old site still points at https://beardedventures.github.io/boo-tiful-home-basket/ . The new page would be https://lpjproperties.github.io/funnels/boo-basket/ .

`home-valuation/qr.html` is a generator, not a print file. Its text field is prefilled with the old Home Valuation URL. Downloading a PNG from that page today still encodes the old URL.

## Hardcoded absolute URLs

In-page images, CSS, and scripts already use relative paths. Those were left relative.

| URL in the copy | File | What to use when you switch |
|-----------------|------|------------------------------|
| `https://txasc.github.io/DONNA-M/home-valuation/` | `home-valuation/qr.html` (default value of the URL field) | `https://lpjproperties.github.io/funnels/home-valuation/` |
| `https://txasc.github.io` (kept) and `https://lpjproperties.github.io` (added) | `n8n/home-valuation-lead.json`, `n8n/hna-membership.json` | Drop the TXASC origin only after the old pages no longer submit here |
| `https://jarvis.tailb14d90.ts.net/webhook/home-valuation` | `home-valuation/index.html` | Same endpoint. This is the n8n webhook, not a Pages URL |
| `https://jarvis.tailb14d90.ts.net/webhook/hna-membership` | `hna/index.html` | Same endpoint |
| `https://jarvis.tailb14d90.ts.net/webhook/boo-tiful-home-basket` | `boo-basket/config.js` | Same endpoint |
| `https://fonts.googleapis.com` and the Great Vibes / Playfair / Lato stylesheet | `hna/index.html` | Leave. Third-party fonts |
| `assets/vendor/qrcode-1.4.4.min.js` | `home-valuation/qr.html` | Vendored from qrcode 1.4.4 because the previously copied qrcode 1.5.3 jsDelivr build URL returned 404. The pinned hash and license are beside the file. The print PNG and SVG in `assets/` are unaffected. |
| `https://www.google.com/maps/search/?api=1&query=` plus the lead's address | inside the email HTML built by both workflow files | Leave. Map link in the notification email |

Email fallbacks, if the webhook cannot be reached:

| Funnel | Fallback |
|--------|----------|
| Home Valuation | `mailto:mallorya@kw.com` |
| HNA | `mailto:president@highlandshna.com` |
| Boo Basket | `mailto:mallorya@kw.com` (from `boo-basket/config.js`) |

## Secrets

Every copied text file, SVG, and image was scanned for API keys, bearer tokens, private keys, passwords, and webhook paths that contain a secret token. None of those values are in the sources, so nothing was replaced with a placeholder.

| Kind | Where it belongs | In git? |
|------|------------------|---------|
| n8n SMTP credential named `Mallory Gmail SMTP` (Gmail app password for the Home Valuation and HNA email nodes) | n8n credential store. Re-attach after import | No |
| Boo Basket workflow credential, if that workflow sends mail | n8n, on the workflow that was not in the source repo | No |

The webhook URLs above are public path names already shipped in the live pages (`/webhook/home-valuation`, `/webhook/hna-membership`, `/webhook/boo-tiful-home-basket`). They have no token segment, and the forms need them, so they were copied. Workflow ids (`donnaHomeValLead1`, `donnaHnaMember1`) and the webhook node ids were kept so import updates the existing workflows.

## Redirects from the old URLs

- [ ] Home Valuation QR and `https://txasc.github.io/DONNA-M/home-valuation/` stay on TXASC until you reprint or replace that page with a redirect to `https://lpjproperties.github.io/funnels/home-valuation/`.
- [ ] `https://txasc.github.io/DONNA-M/` currently redirects to Home Valuation inside the DONNA-M repo. Leave it until you edit that repo.
- [ ] HNA QR and `https://txasc.github.io/DONNA-M/hna/` stay on TXASC until you reprint or replace that page with a redirect to `https://lpjproperties.github.io/funnels/hna/`.
- [ ] `https://beardedventures.github.io/boo-tiful-home-basket/` stays on BeardedVentures until you replace that page with a redirect to `https://lpjproperties.github.io/funnels/boo-basket/`.
- [ ] Do that replacement in the old repositories, in a separate change, after the form tests on the new URLs succeed. This repository does not push to those remotes.
