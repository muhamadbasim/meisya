# Basim social cron repair checklist

Use this when Basim says variants of `cek semua dan perbaikin`, `cek cron job`, `kok berubah`, or asks to repair Threads/Repliz/social automation after provider/model/prompt edits.

## Audit scope

Check every relevant Basim social/news cron, not only the one mentioned most recently:

- Threads viral radar + approval queue
- Threads aggressive evergreen publisher
- Threads daily Repliz analytics + improvement drafts
- Carousel multi-platform Repliz job
- News Digest if it shares the same provider/model failure pattern
- One-shot monitor jobs created to verify later runs
- WhatsApp summary jobs only for status/safety; keep WhatsApp read-only and do not modify unless explicitly requested

## What to verify

For each job, verify and report:

- `provider` / `model`
- schedule and `next_run_at` in WIB
- `last_status`, `last_error`, and latest output file
- loaded `skills`
- enabled toolsets
- prompt consistency: no stale instruction like “use GrowthCircle” when the job is configured for Codex, or vice versa
- whether sensitive credentials are present in visible output (never echo them)

## Common repairs

- If an interval job drifted because an update reset the anchor, convert it to an explicit cron time when the user expects a stable daily time, e.g. analytics daily → `30 7 * * *` for 07:30 WIB.
- If a one-shot monitor was scheduled with the wrong offset (`+08` instead of WIB `+07`), update it to the exact `+07:00` ISO timestamp.
- If a job failed on one provider and the user has chosen another provider, update the model override and remove stale provider wording from the prompt.
- For carousel jobs, attach `basim-carousel-quality-control` and make the prompt explicitly require the approved 1:1 avatar+hologram visual style.
- For evergreen publisher jobs, require anti-repetition evidence: name recent angle/hooks avoided, character count, and real Repliz scheduleId or real error.

## Verification pattern

1. Create a backup of `~/.hermes/cron/jobs.json` before manual edits.
2. Prefer `cronjob(action='update')` for supported changes; only patch `jobs.json` directly for prompt text cleanup that the tool interface cannot target precisely.
3. Run or rerun only jobs where verification matters and the schedule will not create unsafe duplicate public posts.
4. Re-list cron jobs after edits and confirm the live state, not just that the update call returned success.
5. If a rerun takes time, check gateway/agent logs or latest output file until it reaches `ok/error`; do not claim recovery from a queued run alone.

## Reporting style

Basim prefers concise Indonesian status with tables. State:

- what was checked,
- what was changed,
- what is now OK,
- what is still waiting for the next scheduled run,
- any monitor job that will report later.
