# WhatsApp repair + QR pairing notes

Use this when WhatsApp/Baileys is logged out (`device_removed`, `Logged out`, bridge paused) and the user needs a fresh QR, especially over a messaging platform where terminal QR is hard to scan.

## Observed failure pattern

- Gateway running, but WhatsApp platform reports not paired or paused.
- Bridge log contains `conflict type=device_removed`, `stream errored out`, `Logged out. Delete session and restart to re-authenticate.`
- Gateway log may show repeated reconnect failures followed by `whatsapp paused after 10 consecutive failures`.
- Phone scan can fail with WhatsApp dialog: `Couldn't link device` / `Try again later`.
- Pairing helper may emit several refreshed QRs then exit with `CONNECTION_CLOSED=408` and `TIMEOUT_WAITING_FOR_SCAN` if no scan succeeds in time.

## Safe repair sequence

1. Backup old session before destructive cleanup:
   ```bash
   TS=$(date +%Y%m%d_%H%M%S)
   mkdir -p ~/.hermes/backups
   tar -czf ~/.hermes/backups/whatsapp-session-$TS.tar.gz -C ~/.hermes/whatsapp session
   ```
2. Move or remove the invalid active session and stale PID:
   ```bash
   TS=$(date +%Y%m%d_%H%M%S)
   mv ~/.hermes/whatsapp/session ~/.hermes/whatsapp/session.reset-$TS 2>/dev/null || true
   rm -f ~/.hermes/whatsapp/bridge.pid
   ```
3. Ensure bridge dependencies are healthy. `link-preview-js` prevents link-preview import errors; `qrcode` is useful when generating PNG QR images for remote scan:
   ```bash
   cd ~/.hermes/hermes-agent/scripts/whatsapp-bridge
   npm install link-preview-js qrcode --save
   node -e "import('link-preview-js').then(()=>console.log('link-preview OK'))"
   node -e "import('qrcode').then(()=>console.log('qrcode OK'))"
   ```
4. Start pairing. Prefer the built-in interactive path when the operator can see the terminal:
   ```bash
   hermes whatsapp
   ```
   If a Telegram/remote user cannot see the terminal QR, generate a PNG with a temporary helper that uses Baileys + `qrcode` and deliver the image to the current chat.
5. After the user scans successfully, verify `~/.hermes/whatsapp/session/creds.json` exists, restart the gateway, and check `hermes gateway status` plus a WhatsApp test message.

## QR pitfalls

- QR codes expire quickly. Do not send an old QR after the pairing process has timed out or emitted a newer QR.
- If the phone says `Couldn't link device` / `Try again later`, stop stale pairing helpers, clear the partial session directory, wait a few minutes if repeated attempts were made, then generate a fresh QR.
- If a helper emits multiple `QR_READY` lines, the last generated file is the current QR; earlier images are stale.
- Avoid running multiple pairing processes against the same session directory. Concurrent helpers can race and make WhatsApp reject linking.
- If remote-delivered QR PNGs repeatedly fail with phone-side `Couldn't link device` or helper closes such as `408` / `515`, stop the loop instead of generating more QRs. Have the user clear stale linked devices, wait for WhatsApp's rate limit to cool down, and prefer running the built-in `hermes whatsapp` pairing flow in a real terminal when possible. A terminal-visible pairing can succeed even after remote QR attempts fail, because the operator scans the freshest QR directly and avoids Telegram/image-delivery latency.

## Remote PNG helper pattern

Run from the bridge directory (or place the `.mjs` helper inside it so Node resolves local packages):

```js
import { default as makeWASocket, useMultiFileAuthState, DisconnectReason } from '@whiskeysockets/baileys';
import pino from 'pino';
import QRCode from 'qrcode';
import fs from 'fs';

const sessionDir = `${process.env.HOME}/.hermes/whatsapp/session`;
fs.mkdirSync(sessionDir, { recursive: true });
const { state, saveCreds } = await useMultiFileAuthState(sessionDir);
const sock = makeWASocket({
  auth: state,
  logger: pino({ level: 'silent' }),
  printQRInTerminal: false,
  browser: ['Hermes Agent', 'Chrome', '120.0'],
  syncFullHistory: false,
});
sock.ev.on('creds.update', saveCreds);

const out = '/tmp/hermes-whatsapp-qr-live.png';
const timeout = setTimeout(() => process.exit(2), 180000);
sock.ev.on('connection.update', async ({ connection, lastDisconnect, qr }) => {
  if (qr) {
    await QRCode.toFile(out, qr, { type: 'png', width: 1024, margin: 4, errorCorrectionLevel: 'M' });
    console.log('QR_READY=' + out);
  }
  if (connection === 'open') {
    clearTimeout(timeout);
    console.log('PAIRED_OK');
    setTimeout(() => process.exit(0), 1500);
  }
  if (connection === 'close') {
    const statusCode = lastDisconnect?.error?.output?.statusCode;
    console.error('CONNECTION_CLOSED=' + statusCode);
    if (statusCode === DisconnectReason.loggedOut) process.exit(3);
  }
});
```

Deliver `MEDIA:/tmp/hermes-whatsapp-qr-live.png`, wait for `PAIRED_OK`, then restart gateway.
