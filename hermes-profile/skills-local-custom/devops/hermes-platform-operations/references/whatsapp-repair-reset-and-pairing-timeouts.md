# WhatsApp repair: reset, re-pair, and QR/linking timeouts

Use when WhatsApp stopped replying and logs show `device_removed`, `Logged out`, bridge exits, or repeated reconnect failures.

## Diagnostic signature from a real repair session

- `gateway.log`: `whatsapp paused after 10 consecutive failures (failed to reconnect)`.
- `bridge.log`: `conflict type=device_removed`, HTTP/stream `401`, then `Logged out. Delete session and restart to re-authenticate.`
- No `whatsapp-bridge/bridge.js` process and port 3000 empty.
- Gateway status may say WhatsApp enabled but not paired, sometimes checking a profile-aware session path such as `~/.hermes/platforms/whatsapp/session/creds.json` while the CLI pairing helper uses `~/.hermes/whatsapp/session`; verify the live code/config path before assuming pairing succeeded.

## Repair sequence

1. Backup existing session before deleting anything:
   ```bash
   TS=$(date +%Y%m%d_%H%M%S)
   mkdir -p ~/.hermes/backups
   tar -czf ~/.hermes/backups/whatsapp-session-$TS.tar.gz -C ~/.hermes/whatsapp session
   ```
2. Fix bridge dependencies if logs show missing modules:
   ```bash
   cd ~/.hermes/hermes-agent/scripts/whatsapp-bridge
   npm install link-preview-js --save
   node -e "import('link-preview-js').then(()=>console.log('IMPORT_OK'))"
   ```
   If you need to render QR as a PNG from a custom helper, install `qrcode` too:
   ```bash
   npm install qrcode --save
   ```
3. Move the invalid session out of the way instead of deleting it outright:
   ```bash
   TS=$(date +%Y%m%d_%H%M%S)
   mv ~/.hermes/whatsapp/session ~/.hermes/whatsapp/session.reset-$TS
   rm -f ~/.hermes/whatsapp/bridge.pid
   ```
4. Restart or resume the gateway. A restart can interrupt the current gateway turn; warn the user first and expect the conversation to resume after restart.
5. Run `hermes whatsapp` in a PTY for normal QR pairing. If driving it programmatically, answer the allowlist prompt (`n` when keeping the existing number), then leave the process running until scan completes.
6. After scan succeeds, verify `creds.json` exists at the session path the gateway actually checks, restart gateway, and send a test WhatsApp DM/self-chat message.

## QR / phone-side pitfalls

- A QR sent as a static screenshot can expire quickly. If the phone shows `Couldn't link device — Try again later`, treat the QR as stale or WhatsApp-side rate limiting; generate a fresh QR from a clean session.
- Repeated failed scans may trigger WhatsApp linking rate limits. Ask the user to wait 10–15 minutes, remove old linked devices named like `Hermes Agent` / `Chrome` / `Linux`, force-close WhatsApp, disable VPN/proxy, and retry.
- A helper that creates a PNG QR and exits after QR generation is useful for sharing the QR, but it cannot complete pairing unless a live Baileys connection remains open until WhatsApp sends the `open` event and credentials are saved. Prefer a long-running helper or `hermes whatsapp` PTY for actual pairing.
- Connection close `408` during pairing plus no `PAIRED_OK` usually means no successful scan/handshake occurred before timeout; do not declare WhatsApp fixed until credentials are saved and gateway receives an inbound WhatsApp message.

## When to stop

If several clean-session QR attempts fail with the phone dialog `Couldn't link device`, stop looping. The durable fix is already applied server-side; the blocker is WhatsApp/linking state on the phone. Tell the user to wait and retry later rather than repeatedly burning fresh QR attempts.