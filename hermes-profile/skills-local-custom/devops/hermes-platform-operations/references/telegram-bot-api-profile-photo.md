# Telegram bot profile photo notes

Captured from a successful Telegram bot avatar update workflow.

## OAuth / image generation path

- Hermes bundled plugin `image_gen/openai-codex` can generate `gpt-image-2` images via ChatGPT/Codex OAuth.
- If unavailable, run `hermes auth add openai-codex` and complete the device-code authorization flow.
- Validate availability programmatically by instantiating `OpenAICodexImageGenProvider().is_available()` if needed.

## Bot API request shape

Static bot profile photo updates use multipart form-data:

```python
photo_json = '{"type":"static","photo":"attach://photo"}'
# field: photo = photo_json
# file part: name="photo"; filename="avatar.png"; Content-Type: image/png
POST https://api.telegram.org/bot<TOKEN>/setMyProfilePhoto
```

Expected success:

```json
{"ok": true, "result": true}
```

Verification:

```text
GET https://api.telegram.org/bot<TOKEN>/getUserProfilePhotos?user_id=<bot_id>&limit=1
```

Telegram normally returns generated sizes such as 160x160, 320x320, and 640x640 for the active profile photo.

## Presentation pattern

When generating options for the user, send each candidate as `MEDIA:/absolute/path.png` with concise labels:

- Opsi A — natural/professional, subtle cybernetic
- Opsi B — most futuristic / strongest semi-robot cue
- Opsi C — most official/formal

Ask the user to pick before installing.
