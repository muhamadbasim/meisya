# Manual JSON → Export fallback for SenangCarousels

Use this when `/api/carousel/generate` fails but `/api/carousel/export` is reachable.

## Durable failure pattern

Observed from SenangCarousels `/api/carousel/generate`:

- API returns HTTP 500, but the wrapped upstream error is Gemini `429` quota exceeded.
- Example indicators:
  - `Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests`
  - `GenerateRequestsPerDayPerProjectPerModel-FreeTier`
  - model such as `gemini-3.5-flash`
- This is not an export/render problem. Do not keep retrying daily quota failures.

## Fallback workflow

1. Search/choose the topic with the agent's normal web tools.
2. Write the complete CarouselCreate JSON yourself. Do **not** call `/api/carousel/generate`.
3. POST the JSON directly to `http://43.156.20.232:8000/api/carousel/export`.
4. Verify:
   - HTTP 200
   - `Content-Type: application/zip`
   - ZIP contains `slide-1.png`, etc.
   - `zipfile.testzip()` returns `None`
5. If publishing to TikTok/YouTube, extract slide PNGs and create a vertical MP4 slideshow with ffmpeg.

## Known-good JSON shape

Required top-level fields:

```json
{
  "title": "ai creator bukan jalan pintas",
  "aspect_ratio": "1:1",
  "theme_colors": "[\"#ffffff\", \"#000000\", \"#000000\"]",
  "title_font": "Playfair Display",
  "body_font": "Plus Jakarta Sans",
  "logo_url": null,
  "handle_name": "@cerita.basim.id",
  "slides": []
}
```

For each slide:

```json
{
  "position": 0,
  "slide_type": "intro",
  "title": "tren **ai**\nmakin ramai",
  "subtitle": null,
  "body": "tapi jangan **asal**",
  "image_url": "http://43.156.20.232:8000/static/illustration.jpg",
  "image_layout": "right",
  "visual_cue": null
}
```

## Style checks

- 6 slides by default.
- Lowercase text.
- Title contains line 1 and line 2 separated by `\n`; body is line 3.
- 1–4 words per line.
- Exactly one `**bold**` word per line.
- Keep Basim style practical and beginner/business-owner friendly.

## MP4 slideshow command pattern

Use this after extracting PNGs:

```bash
ffmpeg -y -f concat -safe 0 -i concat.txt \
  -vf 'scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:white,format=yuv420p' \
  -r 30 -c:v libx264 -pix_fmt yuv420p carousel-slideshow.mp4
```

Where `concat.txt` repeats each slide with a duration, for example:

```text
file '/tmp/slides/slide-1.png'
duration 2.5
file '/tmp/slides/slide-2.png'
duration 2.5
...
file '/tmp/slides/slide-6.png'
```
