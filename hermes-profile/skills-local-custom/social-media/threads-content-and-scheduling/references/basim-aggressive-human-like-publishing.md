# Basim aggressive human-like Threads publishing

Use this note when Basim asks to “posting brutal”, “growth kenceng”, or increase posting volume without looking like spam/bot behavior.

## Core principle

Do **not** help with bypassing bot detection or evading platform enforcement. Reframe the request into a compliant operating model:

> aggressive human-like publishing = more experiments, faster trend response, better hook rotation, and manual engagement — not spam, evasion, mass-follow, mass-like, or mass-comment automation.

## Recommended operating model

For fast Threads growth while keeping account quality:

- Threads evergreen/low-risk text posts: **6/day** as an initial aggressive mode.
- Viral/current-event radar: **4/day**; research + score + draft only; approval required before scheduling.
- Manual engagement brief: **2/day**; output suggested replies/quotes for Basim to adapt manually, never auto-reply.
- Carousel/multi-platform batch: keep conservative, typically **1/day**, because Instagram/carousels need saveability and visual quality more than volume.
- Daily maintenance audit: check 48h performance and whether aggressive mode is hurting median reach or creating repetitive output.

Example WIB cadence used successfully as a safe aggressive baseline:

- 07:10 radar viral + approval queue
- 08:00 evergreen Threads post
- 09:30 manual engagement brief
- 10:00 evergreen Threads post
- 12:10 radar viral + approval queue
- 12:15 carousel/multi-platform batch
- 13:00 evergreen Threads post
- 16:00 evergreen Threads post
- 17:10 radar viral + approval queue
- 18:30 manual engagement brief
- 19:00 evergreen Threads post
- 21:10 radar viral + approval queue
- 22:00 evergreen Threads post
- 22:45 maintenance audit

## Evergreen publisher guardrails

Only auto-schedule evergreen/low-risk content. Each run should produce **one** Threads text post, not a batch.

Requirements:

1. Use official/legit scheduling such as Repliz; do not automate login, scraping, mass follow/like/comment, or detection evasion.
2. Schedule one post at least 10–25 minutes ahead; avoid bursts.
3. Keep post body around **180–480 characters**; count characters before scheduling.
4. Rotate pillars so the account does not sound repetitive:
   - money leaks: paylater, subscription, promo, small recurring costs;
   - digital habits/algorithms: doomscrolling, notifications, apps designed to keep attention;
   - products designed to be habit-forming: snacks, sweet drinks, marketplaces, without naming brands negatively;
   - low-risk daily habits: patterns/frequency, not hard medical claims;
   - owner-as-manual-system / small business bottlenecks;
   - humane beginner AI.
5. Use growth mechanics: ordinary thing → twist/reversal → hidden system/mechanism → consequence → shareable line or soft question.
6. Rotate hook patterns; do not reuse the same opener repeatedly:
   - “Gw kira A, ternyata B.”
   - “Yang bahaya bukan X, tapi polanya.”
   - “Ini kelihatannya kecil karena efeknya nggak langsung.”
   - “Lo kira ini kebetulan, padahal sistemnya didesain begitu.”
   - “Ada satu kebiasaan kecil yang sering lolos dari hitungan.”
7. Do not include internal labels, scores, audit notes, or title metadata in the published body.

## Current-event/newsjacking gate

Current events, health/medical claims, public safety, criminal cases, politics, disasters, brand accusations, and any potentially sensitive or high-risk claim must **not** be auto-scheduled from a standing cron job.

For those topics:

1. Search and verify trend context.
2. Score candidate topics for momentum, relatability, shareability, twist, safety, and fit.
3. Draft 3 candidates with exact wording.
4. Provide a risk audit and source context.
5. Ask Basim to approve a numbered candidate before any Repliz scheduling.

## Manual engagement brief pattern

A manual engagement job may search trends and output copy-ready ideas, but it must not post/reply automatically. Suggested mix per brief:

- 3 empathetic replies,
- 3 insight/twist replies,
- 2 questions that invite conversation,
- 2 quote-post angles.

Always remind Basim: adapt to the original post, do not send all at once, and choose only the most relevant 5–10.

## Trial-and-audit mode

If Basim says to run the current setup “apa adanya dulu selama 3 hari” and then “audit keras”:

1. Do not keep tweaking the live publishing/radar prompts during the trial unless there is an operational failure or explicit new approval.
2. Create or schedule a self-contained follow-up audit reminder/job for ~3 days later, because the requested value is the delayed critique, not more immediate explanation.
3. The audit should be blunt and evidence-based: compare Repliz/platform metrics before vs during the trial, identify repeated content angles/hooks, separate creative weakness from scheduler/API failures, and give keep/cut/change recommendations.
4. Report to Basim only the actionable result: winners, losers, suspected causes, and next operating mode. Avoid verbose cron internals unless he asks.

## Maintenance throttle

Daily performance audit should evaluate whether aggressive mode remains healthy.

Watch for:

- median Threads views dropping sharply,
- many consecutive 0-reply posts,
- hooks becoming repetitive,
- content feeling broadcast-only,
- duplicate or near-duplicate posts,
- Repliz failures or malformed schedules.

Rule of thumb:

- If median views drop **>40% for 2 days in a row**, recommend reducing aggressive evergreen volume by 30–50%.
- If there is an obvious operational fault such as duplicate posting or repeated scheduler failure, pause the faulty job and report.
- If performance is merely weak but not dangerous, recommend changes; do not pause automatically.

## Reporting format after changing cron/jobs

When implementing this mode, report:

- created/updated job names and IDs,
- exact WIB schedules,
- which jobs auto-schedule vs approval-only,
- safety gates,
- audit/throttle rules,
- verification that the gateway/scheduler is active if checked.
