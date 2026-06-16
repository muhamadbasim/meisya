# Cron response cleanup for WhatsApp scheduled summaries

Session-derived lesson: the user noticed that delivered cronjob summaries still showed raw operational framing:

- `Cronjob Response: <name>`
- `(job_id: <id>)`
- separator lines
- `To stop or manage this job...`

For WhatsApp daily summaries, that is too noisy and should be hidden from the user-facing message.

## Fix pattern

In Hermes cron delivery wrapping, prefer a clean header:

```text
Ringkasan Terjadwal — <job name>

<content>
```

Explicitly remove or assert absence of:

```text
job_id
To stop or manage this job
Cronjob Response
-------------
```

## Test pattern

For scheduler wrapper changes, update or add tests around `_deliver_result`:

```python
sent_content = send_mock.call_args.kwargs.get("content") or send_mock.call_args[0][-1]
assert "Ringkasan Terjadwal — daily-report" in sent_content
assert "job_id" not in sent_content
assert "To stop or manage this job" not in sent_content
assert "Cronjob Response" not in sent_content
assert "-------------" not in sent_content
```

## Wording review notes

The user asked to review the summary sentences after hiding cron operational text. Prefer concise Indonesian wording:

- “Topik utamanya berkisar pada …” rather than longer “Arah utamanya berkisar…” paragraphs.
- “Ada <n> pesan dari <n> anggota aktif; ringkasan ini menangkap arah percakapan baru, bukan keputusan final.”
- “Link ini perlu dicek konteks dan relevansinya sebelum dijadikan dasar tindakan.”
- “Belum ada pertanyaan eksplisit dari pesan baru; pantau jika ada lanjutan.”

Avoid markdown-heavy headings in WhatsApp if legibility is the goal. Plain headings like `Catatan untuk lanjutannya:` are safer than bold/asterisk-heavy variants.
