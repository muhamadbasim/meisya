# WhatsApp digest editorial heuristics: false questions, topics, follow-ups

Session-derived update from auditing and patching `whatsapp_all_groups_summary.py` after a digest was compact but still editorially noisy.

## Failure patterns observed

- Promo/job/event broadcasts can contain `?` or words like `apakah`, but are not actionable unanswered questions. Example pattern: “Apakah Anda menikmati akhir pekan... kami menyediakan kesempatan...” with work/link captions.
- Weak/rhetorical chat fragments such as `loh`, `jujur aja`, `wkwk`, `mantap`, `siap`, or short jokes can outrank better messages if scoring rewards length or `?` too much.
- Topic labels can be hijacked by broad trigger words (`kelas`, `zoom`, `payment`) even when the actual discussion is LLM workflow, endpoint/API, VPS/server, or coding setup.
- Light-group topics can fall back to raw keywords (`bikin, bener, ikuuuttt`, `review, padahal, pilihan`, `enggak, jujur, masalah`) that look robotic.
- Follow-ups become repetitive when every group with links gets the same “cek konteks, keamanan, manfaat” line.

## Durable fixes to apply in formatter audits

1. **Question detection**
   - Treat promo/lowongan/event/social/broadcast patterns as non-questions unless there is strong help context.
   - Strong help context examples: `error`, `gagal`, `solusi`, `kenapa`, `gimana`, `server`, `vps`, `install`, `deploy`, `payment`, `endpoint`, `twilio`, `message bird`, `api`.
   - Do not let weak words (`apakah`, `cara`, `gimana`) mark a question without `?` unless accompanied by explicit help patterns like `izin tanya`, `mau tanya`, `butuh bantuan`, `mohon bantu`, `solusinya apa`, or `cara atasinya`.
   - Penalize/ignore rhetorical joking fragments containing `loh`, `jujur aja`, `wkwk`, `haha`, etc. unless they include clear technical/payment/server context.

2. **Snippet scoring**
   - Boost actionable terms: `berhasil`, `solved`, `workaround`, `solusi`, `cara atasinya`, `kenapa`, `gagal`, `error`, `down`, `deploy`, `vps`, `server`, `payment`, `bayar`, `kartu`.
   - Penalize weak acknowledgements/jokes: `wkwk`, `haha`, `hehe`, `loh`, `jujur aja`, `mantap`, `siap`, `ikut`, `ikuuuttt`, emoji laughter.
   - Penalize short non-question text; prefer messages that carry problem/solution/context.

3. **Topic labeling**
   - Add human labels for common technical clusters:
     - `workflow AI, model, dan konteks teknis`
     - `VPS/server dan troubleshooting infrastruktur`
     - `workflow coding AI dan setup tools`
     - `review, feedback, dan pilihan tools`
     - `konfirmasi progres dan pengecekan`
     - `WhatsApp, koneksi bot, dan setup channel`
   - Let high-signal clusters override broad schedule/payment triggers. Example: LLM/context/endpoint/API should not be reduced to `jadwal kelas / sesi Zoom` just because the group also mentioned a class.
   - For light groups, if selected keywords are generic/short/filler, fallback to a human label or `obrolan ringan` instead of printing raw keyword triples.

4. **Contextual follow-ups**
   - VPS/server/down: ask for provider, resource, service status, logs, and time of incident.
   - Payment: separate reports by method/bank and label them as member experiences, not a universal recommendation.
   - Project/demo: capture link, how to try, feedback, and blockers.
   - Event/lowongan/artikel: store context/deadline; do not inflate into a technical issue.
   - Links: use generic “cek konteks/keamanan” only as fallback, not as the first follow-up for every linked group.

## Verification fixture checklist

Use synthetic data, not live WhatsApp, unless advancing `last_message_id` is acceptable. Include:

- Promo/job broadcast with `Apakah...` and links — must not appear in `Pertanyaan belum terjawab`.
- VPS down questions — topic should be VPS/server infra and follow-up should ask for resource/service/log/time.
- LLM workflow + endpoint/Twilio/MessageBird question — topic should be workflow/AI/context and endpoint question should remain.
- Weak chat fragments (`loh`, `jujur aja`, `mantap`, `ikuuuttt`) — should not be top signal or raw topic.
- Raw topic keyword cases — should map to human labels or `obrolan ringan`.

Always run `python3 -m py_compile` on the formatter after patching and a synthetic fixture that asserts the above checks pass.
