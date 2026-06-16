# WhatsApp summary audit + compact digest format

Session-derived guidance from auditing a daily WhatsApp summary that became too long/noisy.

## Failure pattern observed

- Per-group full templates for every active group can balloon badly (example: 31 group blocks, ~66k chars, 771 messages).
- Low-volume groups (1–3 messages) should not receive the full template; they create most of the perceived noise.
- Raw WhatsApp group identifiers such as `628...-...` are not user-facing names and should be hidden or replaced with a safe fallback.
- Keyword-only topics can produce unreadable labels (`wkwk`, `pris`, `misi`, `doesn`, etc.).
- Promo/link captions can be misclassified as unanswered questions if question detection is too loose.
- Cross-group notes become spam when generated from weak overlap or merely because links exist.

## Better output architecture

Prefer one compact daily digest over many full per-group blocks:

```text
Ringkasan Harian WhatsApp — <tanggal>

Total: <n> pesan baru dari <m> grup. Ringkasan ini memprioritaskan grup aktif, isu teknis, pertanyaan, dan link penting; grup ringan digabung agar tidak terlalu panjang.

Prioritas utama:
1. <Group> — <count> pesan, <active> anggota aktif. Topik: <human label>. Sinyal: <speaker>: “<excerpt>”. Pertanyaan terbuka: “<question>”.

Isu yang perlu dipantau:
- <Group>: <topic>. <specific follow-up>

Link penting:
- <label> (<Group>): <url>

Aktivitas ringan:
- <Group>: <count> pesan; <topic>.

Catatan: klaim, promosi, dan link eksternal belum diverifikasi otomatis; gunakan sebagai sinyal awal, bukan keputusan final.
```

## Recommended heuristics

- Cap full/prioritized groups (e.g. 8–12 max) and global links (e.g. 5–8 max).
- Prioritize by score: message count + valid unanswered questions + important links + risk terms (error/gagal/payment/deploy/vps/otp/security/etc.).
- Treat groups below the threshold as `Aktivitas ringan` unless they contain a clear issue/question/link worth surfacing.
- Hide raw group IDs. Fetch the display name from the bridge where possible; otherwise use `Group WhatsApp tidak bernama`.
- Detect real questions only when there is `?` or an explicit help/question pattern (`izin tanya`, `mau tanya`, `gimana solusi`, `ada yang tahu`, etc.).
- Do not classify promo/broadcast captions as questions unless they clearly ask something.
- Filter noisy topic tokens: laughter, greetings, generic chat words, partial English fragments, and other filler.
- Use broad human labels when keyword extraction is weak: `obrolan ringan`, `perkenalan dan sapaan`, `event dan jadwal`, `lowongan kerja`, `promosi/jualan akun atau akses AI`, `troubleshooting error`.
- Only include cross-group notes for strong semantic overlap, not weak keyword overlap or presence of any link.

## Verification checklist

Before finishing a formatter change:

1. Import/syntax-check the script.
2. Run a synthetic fixture that includes:
   - raw group ID name;
   - promo/link share with no real question;
   - a real troubleshooting question;
   - a low-volume group;
   - a job/lowongan or event link;
   - media placeholders such as `[video received]` plus a real explanatory follow-up;
   - social chatter such as wedding congratulations that contains `?` but is not actionable.
3. Assert raw IDs are absent, promo/social/Zoom invites are not treated as open questions, media placeholders are not selected as the main signal, human topic labels appear, and output length is compact.
4. If running the live no-agent script directly, remember it may advance `last_message_id`; prefer synthetic fixtures unless live state advancement is acceptable.

## Session-proven formatter fixes

When auditing a noisy WhatsApp digest, prefer patching the existing formatter rather than changing cron jobs when the cron already calls a shared script. Useful durable fixes:

- Add a `message_importance` score and rank snippets by usefulness, not chronology. Boost real questions, errors, links, schedule/Zoom, deploy/server/VPS/payment, GitHub/repo/demo, and media/tooling terms. Penalize media-only placeholders, mentions/user IDs, emoji-only messages, and short laughter/candaan.
- Add a `has_meaningful_text` filter before selecting snippets. Exclude `[video received]`, `[image received]`, mention-only text, numeric IDs, and operational noise.
- Tighten `looks_like_question`: a bare `?` is not enough. Treat promo captions, link-only shares, scheduled Zoom invitations, and wedding/social greetings as non-actionable unless they include explicit help/question terms. Keep true technical questions such as `cara`, `gimana`, `kenapa`, `install`, `server`, `model`, `payment`, `client login/connect`, `mp4`, or `kualitas`.
- Add domain-specific topic labels for repeated misclassifications, e.g. `kompresi video dan tooling media`, `ucapan wedding dan obrolan sosial`, `domain, TLD, dan promo hosting`, and `jadwal kelas / sesi Zoom`.
- Add a short executive section such as `Yang penting hari ini` before `Prioritas utama`; rename generic `Isu yang perlu dipantau` to `Catatan untuk lanjutannya`; include a bounded `Pertanyaan belum terjawab` section.
- Keep compact caps explicit in code, e.g. priority groups around 8, global links around 6, and light groups around 8, unless the user asks for exhaustive logs.
