# Repliz cross-platform carousel publishing notes

Use this when Basim wants carousel content posted/scheduled through Repliz to Threads, Instagram, TikTok, and YouTube.

## Account IDs observed for Basim

Safe operational IDs used in Repliz scheduling:

- Threads: `6a06e4094492e5f5a8f6d3a4` (`muhamadbasim7`)
- Instagram: `6a278b06c5ff4ce3a320c726` (`muhamadbasim7`)
- TikTok: `6a278d5fc5ff4ce3a320c7a4` (`muhamadbasim`)
- YouTube: `6a278d72c5ff4ce3a320c7a7` (`@muhamadbasim`)

If unsure or if accounts may have changed, verify with `GET /public/account?page=1&limit=100` and report only safe fields: id, name, username, type.

## Platform media shape

### Threads and Instagram

- Use `type: "album"`.
- Use ordered image media with public URLs:
  - `type: "image"`
  - `thumbnail`: same public PNG URL
  - `url`: same public PNG URL
  - `alt`: concise slide description
- If Basim says “Instagram” specifically, schedule only the Instagram account unless he explicitly asks for Threads/cross-platform too.
- Before scheduling Instagram albums from arbitrary event/reference photos, normalize every image to a valid Instagram aspect ratio. Safe default: square `1080x1080` JPEG, auto-oriented, padded/cropped consistently, metadata stripped. Example ImageMagick command: `convert input.jpg -auto-orient -resize 1080x1080 -background white -gravity center -extent 1080x1080 -strip -quality 92 slide-01.jpg`. Verify with `identify -format '%wx%h %[channels] %m' slide-01.jpg` before upload.
- Do **not** treat a Repliz create response plus immediate `status: pending` verification as final publication success. After `scheduleAt` passes, fetch `GET /public/schedule/{scheduleId}` again and confirm `status` is not `error`; if `status: error`, read/report `errorMessage`, fix, and reschedule. Also check recent published content for the final Instagram URL.
- Repliz/Instagram observed failure: arbitrary Telegram-uploaded JPEGs may upload successfully and still fail at publish with `The submitted image with aspect ratio () cannot be published. Please submit an image with a valid aspect ratio.` The durable fix is to regenerate platform-safe 1080×1080 slides and reschedule.
- If Basim asks “mana hasil postnya?” or similar after a scheduled publish time, immediately check schedule status and recent content; do not just repeat the schedule ID.
- If Basim adds a visual exclusion such as “tanpa gambar rocket/roket”, verify the actual exported slides before scheduling, not just the source JSON. Practical check: create a contact sheet from `slide-*.png` (e.g. ImageMagick `montage ... -thumbnail 360x360 -tile 2x ...`) and inspect it with vision; if a single-slide spot check is used, still verify the full set when the exclusion affects all slides.
- Repliz does not expose a first-party media upload in the public schedule docs. Upload local slides first to public storage/CDN; Uguu worked as a temporary fallback but owned storage is better for production.

### TikTok and YouTube

- Convert carousel slides into a vertical MP4 slideshow first.
- Use `type: "video"` with one video media URL. If the API rejects `video` for a specific platform, retry once with `type: "reel"` and report the retry.
- Verify public MP4 URL returns HTTP 200 and video content before scheduling.
- YouTube needs a real title. Do not allow title `unknown`; derive a short title from the carousel angle.

## Timing

For “sekarang” or cron near-future publish:

- Set `scheduleAt` at least 10–15 minutes in the future.
- Convert WIB to UTC before calling Repliz.
- Four platforms can share the same `scheduleAt` if Repliz accepts it; if rejected, stagger by 2–5 minutes.

## Replacing or deleting old Repliz items

When Basim asks to “hapus posting lama dan post yang baru”:

1. First identify whether the old item is still a **schedule/queue item** or already a **published content item**.
2. Pending scheduled items can be removed through the schedule API; a successful delete has been observed as HTTP `204`.
3. Published content is different from schedule records. The public Repliz API endpoint `DELETE /public/content/{contentId}?accountId=...` was observed returning `404 Cannot DELETE`, so do **not** promise that published posts can be deleted through the public API.
4. If the old post is already published, tell Basim plainly: the queue/schedule record can be cleaned up, but the live post likely needs deletion from the native platform or Repliz UI if available.
5. For the replacement post, schedule the new media normally and verify every new schedule ID before reporting success.

## Carousel + separate Threads text thread approvals

When Basim asks to analyze a source, create a carousel, draft a viral thread, and then says an approval phrase such as “GAS POST”, treat the approval as covering both artifacts if both were previewed in the same audit message:

1. Schedule the carousel cross-platform: Threads/Instagram as album, TikTok/YouTube as MP4 slideshow.
2. Also schedule the drafted viral text thread as a separate Threads `type: "text"` post with the first part as `description` and remaining parts in `replies`, unless Basim explicitly says carousel only.
3. Keep the text thread on Threads only by default; do not duplicate long multi-reply text threads to Instagram/TikTok/YouTube unless requested.
4. Schedule the text thread a few minutes after the carousel batch so it does not collide with album posting.
5. Verify the text thread schedule via `GET /public/schedule/{scheduleId}` and report reply count, schedule ID, and WIB time.

## Verification

A successful create returns HTTP 200/201 with `scheduleId`. After creating schedules, verify via `GET /public/schedule/{scheduleId}` when possible and report `status: pending` plus local WIB time. For media posts, verify at least the first/last image URLs and the video URL return HTTP 200 with the expected content type before scheduling.

For analysis after posting:

- `GET /public/content?accountId={accountId}&type=media`
- `GET /public/content/{contentId}/statistic?accountId={accountId}`

Normalize metrics by platform:

- Threads: views, like, replies, repost, quotes, share.
- Instagram: views, reach, like, comment, share, saved, interaction.
- TikTok: views, watched, like, comment, share, favourite, newFollower.
- YouTube: views, like, comment, favourite.

## Early performance lesson from Basim carousel cron

Early same-day stats showed:

- TikTok performed best for MP4 slideshow carousel.
- Instagram was second for album carousel.
- Threads got low views and no engagement from generic educational captions.
- YouTube got almost no traction unless title/metadata is strong; a title of `unknown` is an operational bug.

Working hook pattern: contextual/spontaneous hooks such as “ngeliat tren ai creator makin rame…” beat generic educational openings like “AI bisa bantu bikin konten lebih cepat…”.

Operational pitfall: avoid repeating the same AI-creator angle every hour. Rotate content buckets: AI for business owners, manual customer follow-up, Meta Ads leads leaking, app ideas stuck in the head, teams working from scattered chats, and template-feeling business content.
