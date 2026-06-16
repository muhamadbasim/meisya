# Telegram DM topics for separate Hermes contexts

Use when a user wants Telegram chats separated by context (e.g. Operations, Social Media, Developer) while still talking to the same Hermes bot.

## Feature shape

Hermes supports Telegram DM topic mode via `/topic`: one bot DM becomes a topic-enabled interface where each topic/lane maps to an independent Hermes session and context.

Expected user flow:

1. In the Hermes Telegram DM, send `/topic`.
2. If Hermes reports Telegram Threads/Topics are disabled, configure the bot in BotFather so direct-message topics/threads are enabled and users can create topics.
3. Send `/topic` again.
4. The root DM becomes a system lobby for commands such as `/topic`, `/status`, `/help`, `/usage`.
5. To create a new context, open **All Messages** at the top of the bot interface and send a starter message. Telegram creates a new topic. Each topic has separate history/context.
6. Use `/new` inside a topic only to reset that topic's session; it does not create another lane.
7. Use `/topic <session-id>` inside a topic to bind/restore an older Telegram session into that topic.

## Server-side state

- The state tables are created lazily by `SessionDB.apply_telegram_topic_migration()` / `enable_telegram_topic_mode()`:
  - `telegram_dm_topic_mode`
  - `telegram_dm_topic_bindings`
- Do not assume these tables exist in a fresh `state.db`.
- Manual enabling can be done with `SessionDB.enable_telegram_topic_mode(chat_id=..., user_id=...)`, but this only flips Hermes state. Telegram/BotFather topic capability must still be enabled, and the gateway should be restarted for clean behavior.
- For delivery targets or cron jobs, Telegram thread/topic routing uses `telegram:<chat_id>:<thread_id>`; omitting the thread loses topic targeting.

## Pitfalls

- Do not promise to create Telegram client folders or group rows exactly like another user's screenshot. Hermes can enable topic/session isolation, but the Telegram client UI and topic creation/renaming are controlled by Telegram and the user.
- Restarting the gateway can interrupt the current conversation; warn/obtain approval before doing it.
- If the user just wants separate contexts, prefer `/topic` in the existing Telegram bot DM over creating many Telegram groups. Groups add authorization, mention, and delivery-target complexity.
- After enabling, verify by sending messages in two different topics and confirming they do not share context.
