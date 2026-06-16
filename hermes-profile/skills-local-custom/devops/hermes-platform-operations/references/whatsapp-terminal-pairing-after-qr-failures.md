# WhatsApp terminal pairing after remote QR failures

Use this when WhatsApp/Baileys QR images generated for a remote user repeatedly fail with phone-side `Couldn't link device` / `Try again later`, helper timeouts, or connection close codes such as `408` / `515`.

## Pattern observed

- Remote PNG QR generation worked (`QR_READY=/tmp/hermes-whatsapp-qr-live.png`).
- Phone-side scan failed repeatedly with WhatsApp's `Couldn't link device` dialog.
- Helper refreshed several QRs, then ended with:
  - `CONNECTION_CLOSED=408` or `CONNECTION_CLOSED=515`
  - `TIMEOUT_WAITING_FOR_SCAN`
- The same account later paired successfully when the user ran the terminal pairing flow directly.

## Durable lesson

Remote QR PNG delivery is convenient, but when WhatsApp starts rejecting scans, do not keep generating QR images in a tight loop. It can make rate-limit / stale-QR confusion worse. Pause, clean stale helpers, and prefer direct terminal pairing if the user has shell access.

## Recommended sequence

1. Stop stale pairing helpers so only one process owns the session directory:
   ```bash
   pkill -f 'hermes_pair_qr.mjs|bridge.js --pair-only' 2>/dev/null || true
   ```
2. If the session is known invalid, reset it only after backup has already been made:
   ```bash
   rm -rf ~/.hermes/whatsapp/session
   mkdir -p ~/.hermes/whatsapp/session
   ```
3. If the user can access the terminal, ask them to run the built-in pairing flow there instead of scanning a relayed QR image:
   ```bash
   cd ~/.hermes/hermes-agent
   hermes whatsapp
   ```
4. After the user reports success, verify from the agent side rather than assuming:
   ```bash
   test -f ~/.hermes/whatsapp/session/creds.json && echo paired
   hermes gateway status
   ps -eo pid,etime,cmd | grep '[w]hatsapp-bridge/bridge.js'
   grep -Ei 'whatsapp connected|inbound message: platform=whatsapp|Sending response' ~/.hermes/logs/gateway.log | tail -40
   ```

## Success signature

- `~/.hermes/whatsapp/session/creds.json` exists and is recently modified.
- Gateway status shows the service running.
- A process like this exists:
  ```text
  node .../scripts/whatsapp-bridge/bridge.js --port 3000 --session ~/.hermes/whatsapp/session --mode self-chat
  ```
- `gateway.log` shows:
  - `✓ whatsapp connected`
  - `inbound message: platform=whatsapp ...`
  - `Sending response ... to <lid>`
- Read-only group ingest resumes with `Stored read-only group message without reply` entries.

## Pitfalls

- Do not treat a warning that references another path (for example `~/.hermes/platforms/whatsapp/session/creds.json`) as authoritative if the live bridge is configured with `--session ~/.hermes/whatsapp/session`; verify the actual process args and active session path.
- Do not keep sending old QR images. If a helper emits multiple `QR_READY` lines, the newest file is the only candidate; once the helper exits, consider that QR stale.
- After repeated phone-side failures, waiting 30–60 minutes and clearing old linked devices on the phone may be more productive than immediate retries.
