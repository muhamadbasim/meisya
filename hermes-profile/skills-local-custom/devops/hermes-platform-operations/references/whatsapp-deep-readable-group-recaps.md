# Deep, readable WhatsApp group recaps

Session-derived pattern for summarizing read-only WhatsApp group traffic for this user.

## User-facing format

Use this structure when recapping a specific WhatsApp group:

```text
Ringkasan group wa
Group: <resolved group name>

Periode yang terbaca: <time window>
Catatan: Saya hanya membaca log/read-only. Tidak ada balasan yang dikirim ke grup.

1. <Narrative topic title>
<1-3 short paragraphs explaining context, who raised it, what changed, and why it matters.>

Analisa saya:
<Implications, risk, assumptions, or decision signal in plain Indonesian.>

...

Link Penting
<URLs with short labels>

Pertanyaan Belum Terjawab
<Open questions / unresolved threads>

Follow Up
<Concrete next actions>

Statistik
Total pesan terbaca: <n>. Anggota aktif: <n>. Paling aktif: <ids/names when available>.
```

The user explicitly asked for summaries that are deeper, better worded, easier to read, and easier to understand. Avoid a raw list of messages. Group related messages into story arcs and explain technical terms briefly.

## Read-only safety rule

For this user, never send any response or summary into a WhatsApp group unless they explicitly override. Deliver group summaries/status only to the DM/origin chat.

## Data extraction pattern when state.db lacks group source keys

Sometimes read-only group messages are stored in `state.db` as `source='whatsapp'` with `user_id=<sender_lid>`, while group membership is only visible in `gateway.log` lines such as:

```text
[Gateway] Stored read-only group message without reply: platform=whatsapp chat=<group_jid> user=<sender_lid>
```

In that case:

1. Resolve the group name via the WhatsApp bridge metadata endpoint, e.g. `GET http://127.0.0.1:<port>/chat/<group_jid>`.
2. Parse `gateway.log` for `chat=<group_jid> user=<sender_lid>` events in the target period.
3. For each event timestamp + sender LID, match to `state.db.messages` joined through `sessions` on `source='whatsapp'`, `user_id=<sender_lid>`, `role='user'`, and timestamp within a small window (±2–3 seconds worked in this session).
4. Deduplicate by message id.
5. Build topic clusters from the matched messages; do not assume one session per group.

This pattern recovered the `AKALA | General` group by matching `120363426067377515@g.us` gateway events to per-sender WhatsApp sessions.

## Recap analysis cues

For each cluster, capture:

- What the discussion was about, not just the message text.
- Who drove the topic, using names when available; if only LIDs are available, use LIDs sparingly in statistics and narrative.
- Technical concepts and product details, explained plainly.
- Links and what they were used for.
- Nuance: joking, speculative, serious support request, product launch/update, unresolved blocker.
- Risk or implication: e.g. scope creep, security implications of remote access, pricing/market-fit concerns, privacy questions for new products.

## Example topic labels from the AKALA recap

- Termul roadmap: chat UI, play button, command library, Product Hunt.
- PR hygiene: small PRs, stale branches, branch access, avoiding merge conflicts.
- Remote web/mobile/tunneling: React Native, Tauri Mobile, Cloudflared, security concerns.
- Model usage: Qwen vs Claude/Gemini, token limits, vision limitations.
- Product launch: LokaClip / AI Clipper and feedback/privacy questions.
- Market strategy: Skool/LMS/community fit for Indonesia and WhatsApp-first behaviour.
- MCP/ACP ecosystem: events, registry, agent CLI integration.
