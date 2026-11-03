# Boo-tiful Home Basket

History-free copy from [BeardedVentures/boo-tiful-home-basket](https://github.com/BeardedVentures/boo-tiful-home-basket) at commit `7c08612c131b9e2cf0091e2c064b93a323cadd70`.

The page that is live today is still:

https://beardedventures.github.io/boo-tiful-home-basket/

This is a static site. There is no package manifest and no build step. The browser loads `styles.css`, `config.js`, and the ES module `src/app.mjs` (which imports `src/entry-core.mjs`). Serve the folder over HTTP so the module script loads. Opening `index.html` as a `file://` URL will not run the module.

On `localhost` or `127.0.0.1`, adding `?preview=1` mocks the submission and does not send the entry. Any other host posts to the webhook in `config.js`.

The source repository does not contain an n8n workflow export for this form. The page still posts to the existing webhook path `boo-tiful-home-basket`. See [MIGRATION.md](../MIGRATION.md) for the CORS edit that has to be made on the server.

No QR image is in the source. Nothing was generated here.
