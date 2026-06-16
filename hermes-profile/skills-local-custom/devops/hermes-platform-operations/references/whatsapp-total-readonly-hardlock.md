# WhatsApp total read-only hardlock

Use this when Basim/Tuan says Hermes must never chat/reply on WhatsApp. Treat this as stronger than “no group replies”: **no WhatsApp outbound at all**, including DMs, groups, reactions, cron deliveries, shutdown notifications, and `send_message` tool sends.

## Required policy

- WhatsApp may be used only as an ingest/read source for summaries or audits.
- Deliver summaries/status/audits outside WhatsApp, preferably Telegram DM or another explicitly non-WhatsApp target.
- Do not use `send_message` with `whatsapp` or `whatsapp_cloud` targets.
- Do not rely on “free_response_chats is empty” alone; old sessions, restart notifications, home-channel delivery, or adapter-level sends can still produce outbound messages.

## Audit steps

1. Inspect config:
   - `whatsapp.enabled: false`
   - `whatsapp.reply_enabled: false`
   - `whatsapp.auto_reply_enabled: false`
   - `whatsapp.dm_reply_enabled: false`
   - `whatsapp.group_reply_enabled: false`
   - `whatsapp.free_response_chats: []`
   - optional explicit belt-and-suspenders keys when present: `read_only: true`, `outbound_disabled: true`.
2. Check `.env` for `WHATSAPP_ENABLED=false`; note that `WHATSAPP_HOME_CHANNEL` may still exist but must not be used for delivery.
3. Check cron jobs. Any WhatsApp summary/digest job should deliver to non-WhatsApp, e.g. `telegram`, not `origin` if the origin may resolve to WhatsApp. Historical `origin.platform: whatsapp` metadata can remain in job records; judge the active `deliver` value.
4. Search recent gateway logs for:
   - `platform=whatsapp`
   - `[Whatsapp] Sending response`
   - `Sent shutdown notification ... whatsapp`
   - `whatsapp connected` / `Connecting to whatsapp`
   - `Gateway running with 2 platform(s)` vs `Gateway running with 1 platform(s)`
5. Build an outbound table from log evidence. Treat both normal responses and shutdown notifications as outbound events. Group by target chat ID and mark target type from suffix (`@g.us` = group, `@lid` = DM/home). Gateway send logs usually include char counts but not message bodies.
6. Recover message bodies separately from `~/.hermes/state.db` when possible:
   - `sessions` table gives session `id`, `source`, `user_id`, `started_at`, `ended_at`.
   - `messages` table has assistant `content`, timestamp, and sometimes `platform_message_id`.
   - Match by source=`whatsapp`, time window, and nearby `response ready` log lines. Do not assume every `[Whatsapp] Sending response` has recoverable content in state.db; some short 67-char sends and shutdown notifications may not be stored as assistant messages.
7. Resolve chat/group names conservatively. Check `channel_directory.json` and snapshots, but if the stored `name` is just the numeric group id, report that the human-readable group name is unavailable. Do not infer or invent a group name from old summaries unless labeled as uncertain.
8. Verify gateway restarted and is running without WhatsApp connected if `whatsapp.enabled=false`. A config change is not sufficient while an old gateway runtime is still connected; look for the post-restart `Gateway running with 1 platform(s)` marker and no later WhatsApp send/connect lines.

## Hardlock pattern

When config-only controls are insufficient or the user explicitly demands “read-only only”, add/verify adapter/tool-level outbound guards:

- In `gateway/platforms/whatsapp.py`, at the top of `WhatsAppAdapter.send(...)`, return failure before any bridge POST:
  - log warning: `WhatsApp outbound blocked by read-only hardlock`
  - return `SendResult(success=False, error="WhatsApp outbound disabled/read-only")`
- In `gateway/platforms/whatsapp_cloud.py`, do the same in `WhatsAppCloudAdapter.send(...)` before Graph API calls.
- In `tools/send_message_tool.py`, reject `platform_name in {"whatsapp", "whatsapp_cloud"}` for both send and react/unreact paths.

Run syntax checks after editing:

```bash
python3 -m py_compile \
  ~/.hermes/hermes-agent/gateway/platforms/whatsapp.py \
  ~/.hermes/hermes-agent/gateway/platforms/whatsapp_cloud.py \
  ~/.hermes/hermes-agent/tools/send_message_tool.py
```

Then restart/reload the gateway from outside the gateway process when possible. If inside the gateway, use a delayed `systemd-run --user --on-active=... systemctl --user restart hermes-gateway` or ensure WhatsApp is disabled and wait for the service to come back.

## Reporting discipline

If audit logs show prior outbound WhatsApp after the user's instruction, say so directly. Do not present the system as safe until you have verified the current runtime has no WhatsApp adapter active and no recent post-lock send lines.

Report status in Indonesian for Basim/Tuan, concise but explicit:

- what was unsafe,
- what was changed,
- what was verified,
- remaining caveat if any.
