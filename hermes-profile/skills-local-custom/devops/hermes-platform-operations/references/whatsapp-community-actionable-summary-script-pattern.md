# Actionable WhatsApp Summary Script Pattern

Session-derived pattern from repairing a Hermes cron `no_agent` WhatsApp summary script.

## Problem observed

The summary generator could identify broad topics, but the output was too generic and not operational enough. Specific failures:

- Short/noisy messages such as `v`, `Belum`, `Ga perlu`, `ok`, laughter, or emoji-only were included.
- Already-generated summaries were being summarized again, causing recursive low-quality output.
- Questions were mixed into practical points instead of being prioritized.
- Follow-up items were sometimes raw chat quotes or jokes rather than actions.
- Technical topics lacked risk notes and “so what” analysis.

## Durable fix pattern

Add a second layer of semantic post-processing after raw message fetch.

### 1. Noise filter

Implement `is_low_value_chat_noise(text)` and use it both when fetching messages and when building grouped output.

Filter examples:

- `v`, `ok`, `oke`, `siap`, `noted`, `mantap`, `gas`
- `wkwk`, `haha`, `hehe`, emoji-only
- `iya`, `ya`, `ga`, `gak`, `Belum`, `Ga perlu`
- compliments without operational content like `Pak X mah ahlinya`
- generated summaries: messages starting with `Ringkasan Pagi`, `Ringkasan Harian`, `Ringkasan WhatsApp`, or pasted sections such as `3) Pertanyaan-pertanyaan` followed by `4) Langkah`

Keep short text if it is a real question or contains a link/actionable state, e.g. `belum bisa add on storage ya om?`.

### 2. Question priority

Implement `question_priority(question)`:

- `Urgent`: error/gagal/failed, billing/saldo/credit/limit/API key, bot tidak jalan, down, payment, HTTP 4xx/5xx.
- `Medium`: how-to/setup, skill/plugin/tool/workflow, model/provider, VPS/server/storage/RAM/CPU/core/bandwidth, scraping/Playwright/Shopee, endpoint/API, OpenClaw/Hermes/Codex.
- `Opportunity`: non-blocking ideas, content/tutorial/product opportunities.

### 3. Technical risk notes

Implement `technical_risks_for_text(text)` with topic-specific notes:

- Provider/AI: saldo, limit, model, API key/project, tiny test request before bot debugging.
- Bot/WhatsApp: provider vs webhook/bridge vs auth/channel vs runtime logs.
- Scraping marketplace: ToS, anti-bot/CAPTCHA, rate limit, IP block, DOM changes, cache, data quality.
- VPS: CPU/RAM/storage/bandwidth matched to use case, not just price/core count.
- Skill/plugin/tool/workflow: clarify concepts to reduce repeated support questions.

Avoid false positives: do not treat generic promo wording like `Kuota Promo VPS` as AI-provider quota. Require AI/API/model/provider context for provider-risk classification.

### 4. So-what and role-based action

Implement:

- `strategic_importance_for_text(text, topic_label)` — explains why the issue matters.
- `role_based_actions(item, msgs)` — maps actions to Admin/Mentor/Member.

Examples:

- Admin: create checklist for saldo, limit, model, API key, fallback provider.
- Mentor: explain skill vs plugin vs tool vs workflow with examples.
- Member: include screenshot/log/model/provider when reporting errors.

### 5. Output shape

For priority groups, use:

```text
1. <Group> — <n> pesan, <m> anggota aktif
   - Fakta: ...
   - Sinyal percakapan: ...
   - Makna/so what: ...
   - Pertanyaan prioritas: [Urgent|Medium|Opportunity] “...”
   - Risiko/batasan: ...
   - Aksi berikutnya: <Role>: ...
```

Add global sections:

- Executive brief
- Pertanyaan belum terjawab — diprioritaskan
- Risiko / batasan teknis yang perlu dijaga
- Rekomendasi tindakan
- Link penting
- Aktivitas ringan
- Audit kualitas

## Verification

After patching a Python script:

```bash
python3 -m py_compile /path/to/script.py
```

Then run a dry sample through the script’s functions or a recent safe message window. Inspect for:

- no recursive summary content,
- no one-word noise,
- priority labels appear,
- risks are contextually correct,
- follow-ups are actions, not chat quotes.
