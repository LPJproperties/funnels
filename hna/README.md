# HNA 2027 membership

History-free copy from [TXASC/DONNA-M](https://github.com/TXASC/DONNA-M) at commit `b76de809bb0c5e0b5bdf6e3a7eb5e35b4cb33679`.

The page that is live today, and the URL encoded in the print QR code, is still:

https://txasc.github.io/DONNA-M/hna/

| File | What it is |
|------|------------|
| `index.html` | Membership form. The Highlands logo is embedded in the page. Google Fonts load from `fonts.googleapis.com`. |
| `assets/hna-qr.png` and `.svg` | Print QR codes. Left unchanged. |

The form posts to the existing n8n webhook. The copied workflow is [`../n8n/hna-membership.json`](../n8n/hna-membership.json). See [MIGRATION.md](../MIGRATION.md) before changing any public link.
