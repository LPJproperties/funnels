# Shared code

Nothing was moved here. Each funnel still contains its own pages and assets, so a folder can be opened on its own.

These are the duplicates worth a later, deliberate extraction. Pulling them out now would change markup, validation, or failure behavior, or it would make a funnel depend on a sibling folder.

## Byte-identical assets

Left in place so each funnel stays self-contained.

| File | Copies | SHA-256 |
|------|--------|---------|
| `kw-logo-white.png` | `home-valuation/assets/`, `boo-basket/assets/` | `be6882de42b96e528eb61a0f168ec686b5f483ca5533424eb3dbe206e0245677` |
| `mallory-headshot.webp` | `home-valuation/assets/`, `boo-basket/assets/` | `0a69a5bee8d38f1dfb44ce4c58bfc2c9eb250c6136362850d4744cec74a8547a` |

HNA does not use these files. Its logo is a base64 PNG inside `hna/index.html`.

## Same idea, different behavior

- Every form has a honeypot field named `website`. The fields around it, and the rules that accept a submission, are different on each page. Boo Basket's rules live in `boo-basket/src/entry-core.mjs`. Home Valuation and HNA validate inline in their pages.
- Home Valuation and HNA `POST` JSON to n8n and, if that fails, open a pre-filled email. Boo Basket posts through `deliverEntry` and, on failure, reveals a mailto link. The payloads are not the same shape.
- Home Valuation and Boo Basket both show the KW logo and Mallory's headshot, with different HTML and CSS. There is no shared stylesheet.
- No analytics snippet appears on any of the three pages.
