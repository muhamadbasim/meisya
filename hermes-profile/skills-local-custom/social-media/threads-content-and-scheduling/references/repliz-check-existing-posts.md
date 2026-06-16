# Repliz check-existing-posts workflow

Use this when Basim asks whether a previously drafted/sent social post is already in Repliz, scheduled, or published (e.g. “cek di Repliz”).

## Goal

Determine whether the artifact exists in Repliz as:
- a pending/scheduled queue item,
- a successful/past schedule record,
- or published content on Instagram/Threads.

Do not assume absence from recent published posts means absence from Repliz; check schedules and content separately.

## API probes

Use Basic Auth with `REPLIZ_ACCESS_KEY:REPLIZ_SECRET_KEY`; never print credentials.

1. Refresh connected accounts:

```http
GET https://api.repliz.com/public/account?page=1&limit=100
```

Prefer current account IDs from this response over stale remembered IDs.

2. Search schedules with pagination:

```http
GET https://api.repliz.com/public/schedule?page=1&limit=100
GET https://api.repliz.com/public/schedule?page=2&limit=100
...
```

Continue until an empty page or error. Filter locally by keyword(s) from the target draft/event and inspect `description`, `title`, `status`, `scheduleAt`, `type`, and `accountId`.

Observed statuses can include `success`; therefore this endpoint may include historical records, not only pending schedules. Also separately collect any `pending`, `queued`, or `scheduled` records if the user specifically asks whether something is queued.

3. Search published content for each relevant platform account:

```http
GET https://api.repliz.com/public/content?accountId=<accountId>&type=media
```

For Basim, usually check Instagram and Threads when the request mentions Instagram/Repliz unless the user narrows the platform. Search recent docs for event-specific terms and inspect `description`, `type`, `url`, and `createdAt`.

## Keyword strategy

Build a regex/list from the draft/event’s distinctive terms, not generic words. For event checks, include venue, sponsor, event title, product name, and obvious variants. Example for Codex meetup:

- `codex`
- `openai`
- `foundry`
- `meetup`
- `hellolive`
- `coding agent`

## User-facing report

Keep it concise and evidence-aware:

- Say which Repliz accounts/platforms were checked and whether they are connected.
- State whether matches were found in schedules and published content.
- If no match, say “belum terlihat di Repliz / belum scheduled / belum published” rather than “pasti tidak ada” when API coverage is limited to accessible accounts.
- If local images are involved and the user wants Instagram carousel scheduling, remind that Repliz album media needs public image URLs, not sandbox/local Telegram file paths.

## Pitfalls

- Do not call `POST /public/schedule` just because the user says “cek di Repliz”; checking is read-only.
- Do not treat Repliz schedule IDs and content IDs interchangeably.
- Do not leak API keys from env files or command output.
- Do not only check Threads if the current request is Instagram-related; Basim often has both Instagram and Threads connected under the same username.