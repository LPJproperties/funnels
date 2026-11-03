import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const qrPagePath = path.join(root, 'home-valuation', 'qr.html');
const vendorPath = path.join(root, 'home-valuation', 'assets', 'vendor', 'qrcode-1.4.4.min.js');
const expectedHash = '0e1769a0feb8c5c87f16bcfc0a2050135d9e9f9e4d5fe46194f19183a2969b9b';
const pageUrl = 'https://txasc.github.io/DONNA-M/home-valuation/';

test('QR page uses the checked-in browser build', () => {
  const html = fs.readFileSync(qrPagePath, 'utf8');
  assert.match(html, /<script src="assets\/vendor\/qrcode-1\.4\.4\.min\.js"><\/script>/);
  assert.doesNotMatch(html, /cdn\.jsdelivr\.net|qrcode@1\.5\.3/);
});

test('checked-in QR browser build has the recorded hash', () => {
  const digest = crypto.createHash('sha256').update(fs.readFileSync(vendorPath)).digest('hex');
  assert.equal(digest, expectedHash);
});

test('QR page keeps the old public URL and rendering options', () => {
  const html = fs.readFileSync(qrPagePath, 'utf8');
  assert.match(html, new RegExp(pageUrl.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
  assert.match(html, /QRCode\.toCanvas\(canvas, urlInput\.value \|\| " ", \{ width: 320, margin: 2 \}/);
});

test('vendor draws the expected module matrix for the page URL', async () => {
  let rendered;
  const context = {
    clearRect: () => {},
    createImageData: (width, height) => ({
      data: new Uint8ClampedArray(width * height * 4),
      width,
      height,
    }),
    putImageData: (image) => { rendered = image; },
  };
  const canvas = { style: {}, getContext: () => context };
  const sandbox = { console, setTimeout, clearTimeout, Uint8Array, Uint8ClampedArray };
  vm.runInNewContext(fs.readFileSync(vendorPath, 'utf8'), sandbox, { filename: vendorPath });
  await new Promise((resolve, reject) => {
    sandbox.QRCode.toCanvas(canvas, pageUrl, { width: 320, margin: 2 }, (error) => error ? reject(error) : resolve());
  });
  assert.equal(canvas.width, 320);
  assert.equal(canvas.height, 320);
  assert.equal(rendered.width, 320);
  assert.equal(rendered.height, 320);
  const digest = crypto.createHash('sha256').update(rendered.data).digest('hex');
  assert.equal(digest, '686299906158244201a95f11c1eb21111d8fecf65102fff3719770c825c4d76d');
});
