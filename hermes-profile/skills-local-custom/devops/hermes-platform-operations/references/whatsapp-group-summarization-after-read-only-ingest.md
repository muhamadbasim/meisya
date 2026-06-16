# WhatsApp read-only ingest summarization

Use this when Hermes is configured to collect WhatsApp group messages without replying, and you need to generate a recap later.

## Ingest model

The working pattern is:

- bridge allows selected groups through even in `WHATSAPP_MODE=self-chat`
- bridge annotates the forwarded event with `suppress_auto_reply: true`
- gateway stores the inbound text in the session transcript and returns an empty response
- the group never receives an assistant reply

## What to summarize

Do not assume one session per group.

Instead, aggregate all sessions whose key starts with:

`agent:main:whatsapp:group:<group_jid>:`

That prefix captures the per-sender sessions created by the gateway.

## Summarization shape

A human-friendly recap should look like:

- date-based title
- numbered group sections
- group title resolved via the bridge `/chat/<group_jid>` endpoint if available
- 1–2 narrative paragraphs per group
- optional short bullets only for standout links or highlights
- closing stats line with total messages and most active members

## Practical aggregation steps

1. Load `sessions.json` and collect WhatsApp group sessions by prefix.
2. Read the canonical message store (`state.db`) for `role='user'` rows in those sessions.
3. Group the messages by group JID and speaker.
4. Resolve the group subject via the bridge metadata endpoint.
5. Emit a digest that reads like a community recap, not a debug log.

## Verification signs

When read-only ingest is healthy, you should see:

- gateway log line similar to `Stored read-only group message without reply`
- session entries under `agent:main:whatsapp:group:<group_jid>:<sender>`
- no assistant message sent back to the group
