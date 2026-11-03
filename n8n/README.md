# n8n workflows

History-free copies from [TXASC/DONNA-M](https://github.com/TXASC/DONNA-M) at commit `b76de809bb0c5e0b5bdf6e3a7eb5e35b4cb33679`.

| File | Workflow id | Webhook path |
|------|-------------|--------------|
| `home-valuation-lead.json` | `donnaHomeValLead1` | `home-valuation` |
| `hna-membership.json` | `donnaHnaMember1` | `hna-membership` |

The only edit in these copies is the webhook **Allowed Origins (CORS)** value. It is now both origins, with the current live origin first and no space after the comma:

`https://txasc.github.io,https://lpjproperties.github.io`

n8n compares the browser `Origin` header to that list after splitting on commas. A space after the comma makes the second origin fail the match.

These files do not change the n8n server. Import them there, then re-attach the SMTP credential on each Email node. The export does not contain that credential. Workflow ids are unchanged so an import updates the existing workflows.

Boo Basket has no workflow file in its source repository, so there is nothing to copy for that funnel. Its live webhook still needs the same second origin. Details are in [MIGRATION.md](../MIGRATION.md).

n8n before 1.109.0 answered every allowed origin with the first origin in the list, so a browser on the second origin rejected the response. On those versions the old TXASC pages keep working because that origin is listed first, and the new pages fall back to email until n8n is upgraded.
