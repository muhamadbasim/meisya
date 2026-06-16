# WhatsApp read-only group collection

Use this reference when Hermes must ingest WhatsApp group traffic for later summarization/search without ever replying into the group.

## Working pattern

Observed working implementation in Hermes:

1. Keep `WHATSAPP_MODE=self-chat` so ordinary non-self traffic is still blocked.
2. Reuse `WHATSAPP_GROUP_ALLOWED_USERS` / `whatsapp.group_allow_from` as the source of truth for which groups may pass through.
3. In `scripts/whatsapp-bridge/bridge.js`:
   - parse `WHATSAPP_GROUP_ALLOWED_USERS`
   - if a message is non-self in self-chat mode, still allow it when `isGroup && READ_ONLY_GROUPS.has(chatId)`
   - skip DM allowlist checks for group events
   - annotate forwarded events with `suppress_auto_reply: true`
4. In `gateway/run.py`:
   - before normal agent dispatch, detect `event.raw_message["suppress_auto_reply"]`
   - create/load the session for the group source
   - append a `role=user` transcript row with the inbound text/message_id
   - return `""` so the adapter sends nothing back
5. In `gateway/run.py::_is_user_authorized`:
   - include `Platform.WHATSAPP: "WHATSAPP_GROUP_ALLOWED_USERS"` in the group-chat allowlist env map so allowlisted groups are authorized even if the sender is not DM-paired/allowlisted
6. In `gateway/platforms/whatsapp.py`:
   - when config.extra is empty, populate `_allow_from` from `WHATSAPP_ALLOWED_USERS`
   - populate `_group_allow_from` from `WHATSAPP_GROUP_ALLOWED_USERS`

## Why this pattern

- Bridge-level forwarding is required because Python group policy checks cannot run if the Node bridge already dropped the event.
- Gateway-level transcript-only interception is safer than letting the message reach the normal agent path and trying to suppress replies later.
- Reusing existing allowlist settings avoids growing a second set of knobs (`WHATSAPP_READ_ONLY_GROUPS`, etc.) that drift out of sync.

## Config example

```yaml
whatsapp:
  group_policy: allowlist
  group_allow_from:
    - 120363402262217562@g.us
  free_response_chats:
    - 120363402262217562@g.us
```

## Validation checklist

- `tests/gateway/test_whatsapp_group_gating.py`
- `tests/gateway/test_whatsapp_connect.py`
- verify bridge log no longer shows `self_chat_mode_rejects_non_self` for the allowlisted group
- verify transcript receives user rows for the group
- verify no assistant reply is sent back to the group

## Operational note

Changing `config.yaml` or `.env` is not enough by itself. The running gateway + Node bridge must restart cleanly before the new group behavior is live.
