# WhatsApp group name resolution

Use this when a WhatsApp group session is stored with only a numeric `chat_name`/`display_name`, but the bridge can resolve a human-readable subject.

## Pattern that worked

The WhatsApp bridge exposes a local HTTP endpoint for chat metadata:

- `GET http://127.0.0.1:3000/chat/<group_jid>`

For group chats, the bridge returns JSON like:

```json
{
  "name": "VibeDev ID",
  "isGroup": true,
  "participants": [...]
}
```

If the endpoint fails, the fallback name is usually the bare JID or numeric display name.

## Recommended recap formatting

When building a digest for a human user:

1. Prefer the resolved bridge name if available.
2. If the bridge only returns a numeric label, prefer `Group <group_jid>` over the raw number.
3. Keep the group title editorial, not technical.
4. Use the resolved name in the headline, but preserve the JID in logs/debug output.

## Verification

- `curl http://127.0.0.1:3000/chat/<group_jid>` returns a `name` field for groups.
- If the bridge is restarted, re-query the endpoint rather than assuming the previous resolution is still valid.
- The bridge name is derived from WhatsApp group metadata (`metadata.subject`), so it is often better than `sessions.json`'s `chat_name` field when that field is numeric.

## Example

- Raw session label: `120363402262217562`
- Resolved bridge name: `VibeDev ID`
- Preferred recap title: `VibeDev ID — Diskusi tentang ...`
