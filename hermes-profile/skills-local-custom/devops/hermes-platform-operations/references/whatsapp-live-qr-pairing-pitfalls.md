# WhatsApp live QR pairing pitfalls

Use this when repairing a logged-out WhatsApp/Baileys session for a remote user who needs the QR delivered as an image in chat.

## Key lesson: QR image must stay backed by a live pairing process

Do **not** generate a QR PNG and immediately exit the Baileys process. The phone may show `Couldn't link device` / `Try again later` because the QR payload is no longer backed by an active websocket handshake.

Preferred pattern:

1. Stop stale pairing helpers so there is only one process using the session directory:
   ```bash
   pkill -f 'hermes_pair_qr.mjs|bridge.js --pair-only' 2>/dev/null || true
   ```
2. Clear the partial active session directory only after an old session has already been backed up/moved:
   ```bash
   rm -rf ~/.hermes/whatsapp/session
   mkdir -p ~/.hermes/whatsapp/session
   ```
3. Start a live helper in the bridge directory and keep it running until the user scans:
   ```bash
   cd ~/.hermes/hermes-agent/scripts/whatsapp-bridge
   node hermes_pair_qr.mjs
   ```
4. Deliver the latest `/tmp/hermes-whatsapp-qr-live.png` quickly. If the helper emits multiple `QR_READY` events, the file is overwritten; the latest mtime is the current QR.
5. Wait for `PAIRED_OK`. Only then restart the gateway and verify WhatsApp status.

## Node module resolution pitfall

If the helper is placed under `/tmp`, Node ESM may not resolve bridge-local packages such as `@whiskeysockets/baileys` even when the command is run with `cwd` in the bridge directory. Put the `.mjs` helper inside `scripts/whatsapp-bridge/` or use imports resolvable from that directory.

## Output/logging pitfall

A background helper can create `/tmp/hermes-whatsapp-qr-live.png` even when no stdout is visible yet through the process log. Check for the file directly and send it if it exists:

```bash
ls -lh /tmp/hermes-whatsapp-qr-live.png
stat -c 'mtime=%y size=%s' /tmp/hermes-whatsapp-qr-live.png
```

## Error interpretation

- `CONNECTION_CLOSED=408` followed by `TIMEOUT_WAITING_FOR_SCAN`: the scan did not complete before timeout, or WhatsApp did not accept the QR in time.
- `CONNECTION_CLOSED=515` with timeout: transient WhatsApp/Baileys restart/handshake failure; stop stale helpers, clear partial session, wait briefly, and generate a fresh live QR.
- Phone dialog `Couldn't link device / Try again later`: commonly stale QR, concurrent helpers, too many failed attempts/rate limiting, or linked-device list issues on the phone. Ask the user to remove old `Hermes Agent`/`Chrome`/unknown linked devices, force-close WhatsApp, and retry with a fresh QR after a short wait.

## Verification after successful scan

After `PAIRED_OK`:

```bash
test -f ~/.hermes/whatsapp/session/creds.json && echo paired
hermes gateway restart
hermes gateway status
ps -eo pid,cmd | grep '[w]hatsapp-bridge/bridge.js'
```

Then have the user send a WhatsApp self-chat test message and check gateway/bridge logs for inbound WhatsApp activity.