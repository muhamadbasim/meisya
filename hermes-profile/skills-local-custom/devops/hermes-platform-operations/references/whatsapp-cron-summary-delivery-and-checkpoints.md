# WhatsApp cron summary delivery and checkpoint debugging

Session-derived pattern for debugging “I ran the cron job, why didn’t all WhatsApp group summaries appear here?”

## What happened

A WhatsApp group-summary cron job was configured as `no_agent=true` with `script=whatsapp_group_discovery_and_summary.py`. The script delegated to `whatsapp_all_groups_summary.py`, which only printed output when it found user messages with `id > ~/.hermes/cron/state/whatsapp_all_groups_last_message_id.txt`.

Manual cron execution succeeded (`last_status=ok`, no delivery error), but the user expected all group summaries to appear in the current WhatsApp DM. Investigation showed:

- The morning job origin was WhatsApp DM and delivered to `origin`.
- A separate noon job had `origin.platform=telegram`, so its output could go to Telegram rather than the WhatsApp DM.
- The summarizer uses an incremental checkpoint (`whatsapp_all_groups_last_message_id.txt`), not a “replay all groups” mode.
- After a successful run advanced the checkpoint, re-running found `groups_with_new_messages=0`, so a later manual run had no summary to print.
- Cron output files under `~/.hermes/cron/output/<job_id>/...md` are authoritative evidence of what the job produced even if the user does not notice the delivered message.

## Debug checklist

1. List cron jobs and compare each job’s `origin`, `deliver`, `last_status`, `last_delivery_error`, `script`, and `no_agent`.
2. Read `~/.hermes/cron/jobs.json` if the tool list does not expose origin details.
3. Inspect the latest output under `~/.hermes/cron/output/<job_id>/`.
4. Inspect `~/.hermes/cron/state/whatsapp_all_groups_last_message_id.txt`.
5. Compare the checkpoint with `state.db` group-message rows:
   - Load WhatsApp group session IDs from `~/.hermes/sessions/sessions.json` where keys start with `agent:main:whatsapp:group:`.
   - Query `state.db.messages` for `role='user'`, those session IDs, and `id > last_id`.
   - If count is zero, the summary script is behaving as designed: no new messages since the last checkpoint.
6. If the user wants “show all current summaries here,” do not just re-run the incremental cron. Either reset/adjust the checkpoint intentionally, add a separate replay mode, or send the saved output file/content from the previous run.
7. If multiple platform origins exist, update the wrong cron job’s delivery target/origin or recreate it from the desired DM. Do not assume `deliver=origin` means the current chat; it means the origin captured when that specific job was created.

## User-facing explanation pattern

Keep the response short and concrete:

- State whether the cron actually ran.
- Say whether output existed and where it was saved.
- Explain incremental checkpoint behavior in one sentence.
- Mention any platform-origin mismatch explicitly, e.g. “the noon job’s origin is Telegram, not this WhatsApp DM.”
- Offer the precise fix: align delivery to WhatsApp DM and/or add a non-checkpoint replay mode.
