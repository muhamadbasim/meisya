# WhatsApp cron hidden operational output + narrative group summaries

Session-derived pattern for the user's WhatsApp daily group-summary cron.

## User-facing behavior

- Cron operational messages should be hidden/silent. Examples: “group baru terdeteksi”, “ditambahkan ke allowlist”, or “belum ada pesan baru” should not be delivered to WhatsApp DM as user-facing messages.
- In `no_agent=true` cron jobs, empty stdout means silent delivery. Keep discovery/reload notes on stderr/logs only.
- Actual group summaries should still print to stdout so the cron can deliver them.

## Implementation pattern

For a wrapper script like `~/.hermes/scripts/whatsapp_group_discovery_and_summary.py`:

```python
def main():
    changed, _discovered, _allow = update_allowlist()
    out = run_summary()
    if out:
        print(out, end="")
    # No stdout for operational-only changes. In no_agent mode, empty stdout is silent.
```

Avoid printing “added group to allowlist” or “no messages” to stdout. Those are operational, not summary content.

## Preferred summary shape

For each group, use a narrative digest similar to:

```text
*Ringkasan Harian <Nama Group> — <Tanggal>*

Obrolan <Nama Group> pada <Tanggal> ...

<Poin utama dalam paragraf naratif, including who said what, context, risks, and what is still uncertain.>

*Catatan untuk lanjutannya:*
- ...
- ...

*Tambahan relevan dari group lain:*
- ...

Link Penting:
- ...

Pertanyaan Belum Terjawab:
- ...

Statistik: <n> pesan dari <n> anggota aktif; member paling aktif: <names>.
```

Important style notes:

- Prefer paragraphs over rigid numbered debug sections.
- Preserve the existing Statistik line semantics: total messages, active members, and most active members when available.
- Include Link Penting and Pertanyaan Belum Terjawab even when empty, with a clear “tidak ada” line.
- Add “Tambahan relevan dari group lain” only when there is useful cross-group context.
- Use Indonesian, concise but deeper analysis: context, who said what, nuance, implications/risks, and follow-up.
