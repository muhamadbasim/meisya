# WhatsApp repair: reset invalid session and send QR as image

Use this when WhatsApp/Baileys is logged out (`device_removed`, `Logged out. Delete session and restart to re-authenticate`), the gateway has paused WhatsApp after repeated reconnect failures, or the user cannot scan a terminal-rendered QR.

## Observed signatures

- `gateway.log`: `whatsapp paused after 10 consecutive failures (failed to reconnect)`.
- `bridge.log`: `stream errored out`, `conflict type=device_removed`, HTTP `401`, repeated `Logged out. Delete session and restart to re-authenticate`.
- `ss -ltnp | grep :3000` shows no WhatsApp bridge listener.
- Gateway can remain healthy for Telegram while WhatsApp alone is failed/paused.

## Repair workflow

1. Backup current WhatsApp session before destructive changes:
   ```bash
   TS=$(date +%Y%m%d_%H%M%S)
   mkdir -p ~/.hermes/backups
   tar -czf ~/.hermes/backups/whatsapp-session-$TS.tar.gz -C ~/.hermes/whatsapp session
   ```
2. Fix known bridge deps if logs mention missing modules:
   ```bash
   cd ~/.hermes/hermes-agent/scripts/whatsapp-bridge
   npm install link-preview-js --save
   npm install qrcode --save   # only needed for PNG QR generation helper below
   node -e "import('link-preview-js').then(()=>console.log('IMPORT_OK'))"
   ```
3. Move the invalid session out of the active path and remove stale bridge pid:
   ```bash
   TS=$(date +%Y%m%d_%H%M%S)
   mv ~/.hermes/whatsapp/session ~/.hermes/whatsapp/session.reset-$TS
   rm -f ~/.hermes/whatsapp/bridge.pid
   ```
4. Restart gateway and inspect health:
   ```bash
   hermes gateway restart
   hermes gateway status
   ```
   If the restart interrupts the current messaging session, continue from the next turn and inspect logs/status.
5. Run pairing interactively:
   ```bash
   hermes whatsapp
   ```
   If it asks whether to update allowed users, keep the current allowlist unless the user asked to change it.

## Sending the QR as an image

If the user cannot see/scan the terminal QR, stop the interactive pairing process (so two Baileys sockets do not compete), then generate a fresh QR PNG with Baileys + `qrcode`:

```bash
cd ~/.hermes/hermes-agent/scripts/whatsapp-bridge
node --input-type=module - <<'NODE'
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
let done = false;
const timeout = setTimeout(() => {
  if (!done) { console.error('TIMEOUT_WAITING_FOR_QR'); process.exit(2); }
}, 30000);
sock.ev.on('connection.update', async (update) => {
  const { connection, lastDisconnect, qr } = update;
  if (qr && !done) {
    done = true; clearTimeout(timeout);
    const out = '/tmp/hermes-whatsapp-qr.png';
    await QRCode.toFile(out, qr, { type: 'png', width: 1024, margin: 4, errorCorrectionLevel: 'M' });
    console.log(`QR_FILE=${out}`);
    try { sock.end?.(); } catch {}
    process.exit(0);
  }
  if (connection === 'open') { console.log('ALREADY_PAIRED'); process.exit(0); }
  if (connection === 'close') {
    const statusCode = lastDisconnect?.error?.output?.statusCode;
    console.error(`CONNECTION_CLOSED=${statusCode}`);
    if (!done && statusCode !== DisconnectReason.restartRequired) process.exit(3);
  }
});
NODE
```

Deliver the resulting image to the user with `MEDIA:/tmp/hermes-whatsapp-qr.png` and ask them to reply after scanning. Then restart/verify the gateway.

## Pitfalls

- Do not assume `hermes gateway status` showing the service running means WhatsApp is connected; inspect platform-specific health and bridge process/port.
- If the gateway restart kills the current chat session, the next assistant turn should first summarize completed repair steps, then continue verification.
- Avoid sending/answering in WhatsApp groups for this user; group ingest/summary should remain read-only and delivered to DM unless explicitly overridden.
