# Telegram bot profile photo upload recipe

Session-tested pattern for changing a Telegram bot profile picture from Hermes.

## Preconditions

- A valid `TELEGRAM_BOT_TOKEN` is available in the active Hermes environment/config.
- Final avatar is a static JPG/PNG, square, and suitable for circular crop.
- Do not print or log the token value.

## Verification endpoints

```text
GET https://api.telegram.org/bot<TOKEN>/getMe
GET https://api.telegram.org/bot<TOKEN>/getUserProfilePhotos?user_id=<bot_id>&limit=1
```

`getMe` gives the bot `id` and `username`. `getUserProfilePhotos` confirms Telegram has accepted and exposed the updated profile photo. A verified result includes `total_count >= 1` and usually photo sizes like `160x160`, `320x320`, and `640x640`.

## Upload endpoint

```text
POST https://api.telegram.org/bot<TOKEN>/setMyProfilePhoto
Content-Type: multipart/form-data
```

Multipart fields:

- text field `photo`: `{"type":"static","photo":"attach://photo"}`
- file field `photo`: image bytes, e.g. `image/jpeg`

Python stdlib sketch:

```python
import os, urllib.request
from pathlib import Path

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
path = Path("/tmp/avatar.jpg")
boundary = "----HermesBoundary"
parts = []

def field(name, value):
    parts.append(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode()
    )

def filepart(name, filename, data, ctype):
    parts.append(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"; filename=\"{filename}\"\r\n"
        f"Content-Type: {ctype}\r\n\r\n".encode()
        + data + b"\r\n"
    )

field("photo", '{"type":"static","photo":"attach://photo"}')
filepart("photo", path.name, path.read_bytes(), "image/jpeg")
body = b"".join(parts) + f"--{boundary}--\r\n".encode()
req = urllib.request.Request(
    f"https://api.telegram.org/bot{TOKEN}/setMyProfilePhoto",
    data=body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
)
with urllib.request.urlopen(req, timeout=60) as r:
    print(r.status, r.read().decode())
```

## User-facing follow-up

If API verification succeeds but the user cannot see the new avatar, the likely cause is Telegram client cache. Ask them to reopen the profile, restart Telegram, clear cache, or check another device. Avoid implying the upload failed unless Bot API verification failed.
