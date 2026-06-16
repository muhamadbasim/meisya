# WhatsApp self-chat / allowlist silent-reply case

A user reported sending a message to their own WhatsApp chat but receiving no Hermes reply.

Observed signals:

- Gateway was running and WhatsApp was connected.
- `~/.hermes/logs/gateway.log` contained:

```text
Unauthorized user: 146312456589400@lid (Muhamad Basim) on whatsapp
```

- `~/.hermes/.env` contained:

```bash
WHATSAPP_MODE=self-chat
WHATSAPP_ALLOWED_USERS=087778219420
```

- WhatsApp session mapping files showed the real aliases:

```text
lid-mapping-6287778219420.json -> "146312456589400"
lid-mapping-146312456589400_reverse.json -> "6287778219420"
```

- `~/.hermes/whatsapp/bridge.log` contained many bridge-level ignores:

```json
{"event":"ignored","reason":"self_chat_mode_rejects_non_self","chatId":"6287778219420@s.whatsapp.net","senderId":"6287778219420@s.whatsapp.net"}
```

Interpretation:

1. The allowlist used local Indonesian phone format (`087...`), but Hermes/Baileys saw international format (`628...`) and LID (`146...@lid`).
2. The bridge was in `self-chat` mode, which only processes messages that Baileys marks as the account's own valid self-chat. Messages that look like ordinary inbound/direct chats are intentionally rejected before they reach the gateway.

Recommended fixes:

For a true personal self-chat setup:

```bash
WHATSAPP_MODE=self-chat
WHATSAPP_ALLOWED_USERS=6287778219420,146312456589400
hermes gateway restart
```

For a separate WhatsApp bot number:

```bash
WHATSAPP_MODE=bot
WHATSAPP_ALLOWED_USERS=6287778219420,146312456589400
hermes gateway restart
```

Verification after config changes:

```bash
hermes gateway status
ps -eo pid,cmd | grep '[w]hatsapp-bridge/bridge.js'
tail -80 ~/.hermes/whatsapp/bridge.log | grep -E 'mode:|Allowed users|✅|146312456589400|agent_echo|ignored' | tail -50
```

Do not rely only on `.env` contents: a restart can be delayed by active gateway sessions. If the service is draining, wait until the bridge process args and latest bridge startup line show the intended `--mode` / `(mode: ...)` before testing again.

Troubleshooting lesson:

- Always inspect both `gateway.log` and `~/.hermes/whatsapp/bridge.log`.
- Gateway auth and bridge mode/allowlist are separate rejection layers.
- Include LID aliases when the bridge sees `@lid` IDs and phone↔LID mapping files exist under `~/.hermes/whatsapp/session/`.
- In a personal self-chat with the same WhatsApp account, final working config may be `WHATSAPP_MODE=self-chat` plus both phone and LID numeric aliases in `WHATSAPP_ALLOWED_USERS`.
