# Repliz schedule API notes

Captured from Repliz docs during a Threads scheduling session. Keep this concise; check the live docs if behavior changes.

## Create schedule

Endpoint:

```http
POST https://api.repliz.com/public/schedule
```

Auth:

```http
Authorization: Basic Base64(AccessKey:SecretKey)
Content-Type: application/json
Accept: application/json
```

Access tier from docs: Premium+.

## Text post body

```json
{
  "title": "",
  "description": "Main post text",
  "topic": "Product Engineering",
  "type": "text",
  "medias": [],
  "additionalInfo": {
    "isAiGenerated": false,
    "isDraft": false
  },
  "replies": [],
  "accountId": "THREADS_ACCOUNT_ID",
  "scheduleAt": "2026-06-02T04:10:00.000Z"
}
```

## Carousel / album post body

Repliz documentation exposes `type: "album"` for multi-image posts, including Threads. Use this for carousel-style posts. Each image must be reachable by Repliz as a **public URL**; local files from the agent sandbox are not enough until uploaded to public storage/CDN.

```json
{
  "title": "",
  "description": "Caption text",
  "topic": "Business Systems",
  "type": "album",
  "medias": [
    {
      "type": "image",
      "thumbnail": "https://example.com/slide-01.png",
      "url": "https://example.com/slide-01.png",
      "alt": "Slide 1 description"
    },
    {
      "type": "image",
      "thumbnail": "https://example.com/slide-02.png",
      "url": "https://example.com/slide-02.png",
      "alt": "Slide 2 description"
    }
  ],
  "additionalInfo": {
    "isAiGenerated": false,
    "isDraft": false
  },
  "replies": [],
  "accountId": "THREADS_ACCOUNT_ID",
  "scheduleAt": "YYYY-MM-DDTHH:MM:SS.000Z"
}
```

Album scheduling checklist:
- Generate/export carousel slides at platform-safe dimensions. For Instagram albums from arbitrary uploaded/reference photos, safest default is 1080×1080 JPEG/PNG after `-auto-orient`, square padding/cropping, and metadata stripping; raw phone/Telegram JPEGs can pass upload but fail at publish with an invalid/blank aspect-ratio error.
- Upload slides first and verify each `url` is publicly accessible without auth.
- Repliz public OpenAPI currently documents account/schedule/queue-style endpoints, not a first-party media upload endpoint; album `medias[].url` must already be a public URL. If no owned CDN/storage is configured, upload to a temporary public host (session-proven fallback: Uguu via `curl -F 'files[]=@slide.png' https://uguu.se/upload.php`) and verify each URL returns `200` with the expected image content type before scheduling. Prefer owned/stable storage for production posts when available.
- Use `type: "album"`; keep `medias` ordered exactly as the intended carousel order.
- Include concise `alt` text for each slide when available.
- Preserve the normal Basim approval gate before calling `POST /public/schedule`; a direct reply like “post/kirim ke repliz” to an already generated carousel counts as approval for that artifact.
- Verify twice: immediately after create (`status: pending` is only queued), then again after `scheduleAt` passes. If the post failed, fetch `errorMessage`, fix the media/payload, reschedule, and check recent content for the final live URL.

Required fields per docs:
- `title`: string
- `description`: caption/body
- `type`: `text`, `image`, `video`, `reel`, `album`, `link`, or `story`
- `medias`: array, empty for text
- `accountId`: connected target account ID
- `scheduleAt`: ISO 8601 datetime

## Threads / nested replies body

For a Threads thread, put the first post in `description`, then subsequent posts in `replies`.

```json
{
  "title": "",
  "description": "Post 1 text",
  "topic": "Product Engineering",
  "type": "text",
  "medias": [],
  "additionalInfo": {
    "isAiGenerated": false,
    "isDraft": false
  },
  "replies": [
    {
      "title": "",
      "description": "Post 2 text",
      "topic": "Product Engineering",
      "type": "text",
      "medias": []
    },
    {
      "title": "",
      "description": "Post 3 text",
      "topic": "Product Engineering",
      "type": "text",
      "medias": []
    }
  ],
  "accountId": "THREADS_ACCOUNT_ID",
  "scheduleAt": "YYYY-MM-DDTHH:MM:SS.000Z"
}
```

## Response

Docs show `200`, but a real successful create returned HTTP `201`:

```json
{"scheduleId":"..."}
```

Treat `200` or `201` with `scheduleId` as success.

## Timezone reminder

WIB is UTC+7. Convert scheduled time to UTC before sending to Repliz:
- 11:10 WIB → 04:10 UTC

If the requested time has passed in WIB and no date is supplied, schedule the next occurrence.
