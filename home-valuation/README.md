# Home valuation

History-free copy from [TXASC/DONNA-M](https://github.com/TXASC/DONNA-M) at commit `b76de809bb0c5e0b5bdf6e3a7eb5e35b4cb33679`.

The page that is live today, and the URL encoded in the print QR code, is still:

https://txasc.github.io/DONNA-M/home-valuation/

| File | What it is |
|------|------------|
| `index.html` | Landing page and lead form. Image paths are relative (`assets/...`). |
| `qr.html` | In-browser QR generator. Its default URL is still the TXASC address above. The jsDelivr script it loads currently returns 404, so the canvas does not draw; the print files in `assets/` are the codes in use. |
| `assets/home-valuation-qr.png` and `.svg` | Print QR codes. Left unchanged. |
| `assets/kw-logo-white.png`, `assets/mallory-headshot.webp` | Brand images for this page. |

The form posts to the existing n8n webhook. The copied workflow is [`../n8n/home-valuation-lead.json`](../n8n/home-valuation-lead.json). See [MIGRATION.md](../MIGRATION.md) before changing any public link.

The source repository's root `index.html` only redirected visitors to this folder. That redirect was not copied here. The root of this repository lists every funnel.
