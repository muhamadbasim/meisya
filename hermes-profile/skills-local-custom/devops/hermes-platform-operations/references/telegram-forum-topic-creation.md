# Telegram forum topic creation from Hermes

Use this when a user asks Hermes to create Telegram topics/forum lanes that look like the Telegram topic list shown in a screenshot.

## Pattern that worked

1. Confirm the target chat from Hermes' messaging directory rather than guessing:
   - `send_message(action='list')` shows available Telegram targets.
   - `~/.hermes/channel_directory.json` may include the raw chat/thread identity, e.g. `-100...:1` for a forum group's General topic. Strip the `:thread_id` suffix to get the parent chat id for `createForumTopic`.
2. Use the Telegram Bot API directly with the configured `TELEGRAM_BOT_TOKEN` from `~/.hermes/.env`:
   - Endpoint: `https://api.telegram.org/bot<TOKEN>/createForumTopic`
   - Parameters: `chat_id`, `name`, optional `icon_color` or `icon_custom_emoji_id`.
3. Create each topic and capture `message_thread_id` from the JSON response.
4. Report only what was actually created, with the thread IDs.

## Example script shape

```python
import os, json, time, urllib.parse, urllib.request, urllib.error

TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = '-1003918977336'  # parent group id, not '<chat>:<thread>'
topics = [
    ('Operations', 0x6FB9F0),
    ('Social Media', 0x6FB9F0),
    ('General', 0xCB86DB),
    ('Developer', 0x6FB9F0),
]
base = f'https://api.telegram.org/bot{TOKEN}/'
for name, color in topics:
    body = urllib.parse.urlencode({
        'chat_id': CHAT_ID,
        'name': name,
        'icon_color': color,
    }).encode()
    req = urllib.request.Request(base + 'createForumTopic', data=body)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            resp = json.load(r)
    except urllib.error.HTTPError as e:
        resp = json.loads(e.read().decode('utf-8', 'replace'))
    print(name, resp)
    time.sleep(0.35)
```

## Pitfalls

- Do not confuse Telegram client folders with forum topics. The Bot API can create topics inside a forum-enabled group/supergroup; it cannot create or rearrange a user's client-side chat folders/sidebar.
- A target shown as `telegram:<chat_id>:<thread_id>` or `-100...:1` is a specific topic. `createForumTopic` needs the parent group chat id (`-100...`) rather than the thread-specific id.
- Telegram restricts built-in `icon_color` to allowed values and may normalize/ignore colors. Treat exact icon appearance as best-effort unless using valid custom emoji IDs.
- If topic creation fails with permissions/forum errors, verify the bot is in the group with admin rights to manage topics and that forum/topics mode is enabled.
- For existing duplicate names, Telegram may return a duplicate-name error; do not claim success unless the API returns `ok: true` or you have separately verified the topic exists.
