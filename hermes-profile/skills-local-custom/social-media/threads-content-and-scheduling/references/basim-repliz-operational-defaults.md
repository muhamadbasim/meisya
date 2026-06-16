# Basim Repliz operational defaults

Use these defaults when scheduling Basim Threads content through Repliz.

## Destination language

- If Basim says **“kirim ke repliz”**, **“post jadwalkan ke repliz”**, or gives explicit schedule intent, call Repliz `POST /public/schedule` after audit/approval.
- Do **not** interpret a bare “kirim” in an already-approved Repliz scheduling flow as “send to the Telegram update topic”. The internal Telegram topic is only for review/update delivery when explicitly requested.
- If the destination is genuinely ambiguous, state the current action clearly before executing: “Saya jadwalkan ke Repliz, bukan kirim ke topic internal.”

## Batch posts with repeated second-thread CTA

When the user provides numbered posts and says to add the same **utas kedua** to every post:

- Create one Repliz schedule per numbered post.
- Put the numbered post body in top-level `description`.
- Put the CTA in `replies[0].description`.
- Keep `title` and `topic` as empty strings to avoid leaking internal labels to Threads.
- Use `type: "text"`, `medias: []`, and `additionalInfo.isAiGenerated: false`.

## Default timing when not specified

If the user approved scheduling but did not give exact times:

- Start at the next near-future 15-minute slot, at least ~10 minutes ahead in WIB.
- Space posts every 90 minutes by default.
- Convert WIB to UTC for Repliz `scheduleAt`.
- Report every scheduled local WIB time and `scheduleId`.

## Approving numbered candidates from radar cron output

When Basim replies with a short approval such as `approve #1`, `approve #2`, or `approve #3` after a radar/approval-queue cron message:

1. Treat it as explicit approval for that exact numbered candidate from the most recent relevant radar output, not as a request to draft again.
2. Retrieve the latest matching cron output for the radar job (or the currently visible approval message if it is in context), extract the approved candidate's exact draft body, recommended slot, status/risk, and character counts.
3. Preserve the approved wording exactly except for removing internal labels/metadata and visible numbering prefixes if present. For Threads thread scheduling, put the first part in top-level `description` and the remaining parts in `replies[]`.
4. If the candidate includes a recommended WIB slot and it is still safely in the future, use that slot. If it has passed or collides with another known scheduled item, use the next safe near-future slot and report the adjustment.
5. Re-check all parts are under 500 characters before calling Repliz.
6. Keep `title` and `topic` empty unless Basim explicitly asks otherwise, to avoid leaking internal labels into Threads.
7. Verify the created schedule via `GET /public/schedule/{scheduleId}` and report local WIB time, platform/account, schedule ID, and pending/success status.

## Verification

Before scheduling, count characters for each main post and reply. Prefer main posts under 500 characters. Treat HTTP 200 or 201 with a `scheduleId` as success. Never print the Repliz secret key in the response.