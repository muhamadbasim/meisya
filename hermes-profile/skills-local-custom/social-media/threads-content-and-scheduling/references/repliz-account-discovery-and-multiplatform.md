# Repliz account discovery and multi-platform carousel notes

Session-derived operational notes for Basim's Repliz workflow.

## Discover connected accounts

Use Repliz public account listing with Basic Auth:

```http
GET https://api.repliz.com/public/account?page=1&limit=100
Authorization: Basic Base64(REPLIZ_ACCESS_KEY:REPLIZ_SECRET_KEY)
Accept: application/json
```

The endpoint returns `docs[]` with at least:
- `id`
- `name`
- `type` (`threads`, `instagram`, `tiktok`, `youtube`, etc.)
- `username`

Do not echo secrets. It is safe to report account names/usernames/IDs after verifying they are Repliz account IDs, not credentials.

## Basim verified Repliz account IDs

Observed connected accounts for Basim:
- Threads: `6a06e4094492e5f5a8f6d3a4` — `muhamadbasim7`
- Instagram: `6a278b06c5ff4ce3a320c726` — `muhamadbasim7`
- TikTok: `6a278d5fc5ff4ce3a320c7a4` — `muhamadbasim`
- YouTube: `6a278d72c5ff4ce3a320c7a7` — `@muhamadbasim`

Before reusing in a far-future session, refresh the account list because connected Repliz accounts can change.

## Multi-platform carousel strategy

For a SenangCarousels PNG carousel:
- Threads + Instagram: schedule as `type: "album"` with ordered public PNG URLs.
- TikTok + YouTube: create a platform-safe vertical MP4 slideshow from the PNG slides, then schedule as video/reel media.
- If Repliz rejects `type: "video"` for TikTok/YouTube, retry once with `type: "reel"` and report exactly which type succeeded.

## Cron safety

When a user says to pause while debugging the generate/API path:
1. Pause the cron job first.
2. Verify the job state is paused/disabled.
3. Then investigate generate/export with a minimal probe.
4. Do not claim root cause if the probe was blocked by approval or did not run.
