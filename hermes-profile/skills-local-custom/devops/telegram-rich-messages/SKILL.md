---
name: telegram-rich-messages
description: "Configure and troubleshoot Telegram Bot API rich messages in Hermes/gateway workflows."
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [telegram, rich-messages, gateway, markdown, bot-api, troubleshooting]
    category: devops
created_by: agent
---

# Telegram Rich Messages

Use this skill when the user wants Telegram bot replies to render as rich/native content (tables, task lists, headings, collapsible details, footnotes, math, inline media), or when a Hermes Telegram reply still appears as plain/legacy Markdown even after `rich_messages: true`.

## Core facts

- Telegram rich rendering uses Bot API rich-message endpoints, not ordinary `sendMessage` + `parse_mode`.
- Final rich messages should be sent via `sendRichMessage` with an `InputRichMessage` payload:

```json
{
  "chat_id": "...",
  "rich_message": {
    "markdown": "## Heading\n\n| A | B |\n|---|---|\n| 1 | 2 |"
  }
}
```

- `InputRichMessage` accepts exactly one of `markdown` or `html`.
- Rich message limits include 32,768 UTF-8 chars, 500 blocks, 16 nesting levels, 50 media attachments, and 20 table columns.
- Useful rich Markdown includes headings, tables, task lists, blockquotes, `<details>`, footnotes, formulas, superscript/subscript via HTML tags, and media blocks.

## Hermes setup workflow

1. Update Hermes first if the local checkout predates Telegram Bot API rich-message support.
2. Enable rich messages in config:

```yaml
telegram:
  extra:
    rich_messages: true
```

3. Restart the gateway from outside the running gateway process:

```bash
hermes gateway restart
```

   From Telegram, `/restart` is usually the appropriate gateway-side command. A tool call from inside the gateway may refuse with “Refusing to restart the gateway from inside the gateway process”; that refusal is expected and not a durable failure.

4. Send a test message containing a heading, short summary, table, task checklist, and `<details>` block.

## Important pitfall: streaming/edit path vs rich final path

If rich syntax still renders as plain text after config + restart, inspect the delivery path:

- Rich final delivery requires `sendRichMessage`.
- Streaming previews and edit-based replies often use `sendMessage`/`editMessageText` with MarkdownV2, which cannot render the full rich feature set.
- In Hermes Telegram code, rich send can be skipped when metadata includes `expect_edits` because the message is expected to be edited/streamed.
- Telegram draft streaming is private-DM oriented; group topics/supergroups may fall back to edit-based streaming.

Practical fixes to try, in order:

1. Enable fresh-final replacement so the completed streamed answer is resent as a fresh final message that can go through `sendRichMessage`:

```yaml
streaming:
  fresh_final_after_seconds: 0.1
```

Then restart the gateway.

2. If group/topic replies still do not render richly, disable Telegram streaming so the response is sent once as a final message instead of being edited:

```yaml
display:
  platforms:
    telegram:
      streaming: false
```

Tradeoff: rich rendering is more consistent, but progressive streaming/typing-style updates in Telegram are reduced or disabled.

## Test prompt

Ask the agent to send:

```text
Summarize this as a Telegram rich table with columns: Task, Owner, Status.
Give me a checklist for the deployment, using completed and incomplete task boxes.
Format this as:
- heading
- short summary
- table
- checklist
- collapsible details section for risks
```

Expected rich Markdown sample:

```md
## Sprint Status

| Item | Owner | Status |
|---|---|---|
| Driver App release | Alex | ✅ Done |
| Portal QA | Sam | In progress |
| Route optimizer | Luke | Blocked |

- [x] Review PR
- [ ] Run staging smoke test
- [ ] Send release note

<details>
<summary>Risks</summary>

- QA may slip if staging data is stale.
- Route optimizer dependency needs confirmation.

</details>
```

## Verification checklist

- [ ] Config has `telegram.extra.rich_messages: true`.
- [ ] Gateway restarted after the config change.
- [ ] Logs or behavior indicate final delivery is not stuck on legacy edit/MarkdownV2 path.
- [ ] A table renders as a native table, not pipe text.
- [ ] Task list boxes render as checkboxes.
- [ ] `<details>` renders as collapsible details on the client being tested.
- [ ] If testing in a group topic, compare with a Telegram DM because group/topic streaming paths may differ.

## Reference

- Telegram blog: `https://telegram.org/blog/watch-apps-and-more`
- Telegram Bot API rich formatting docs: `https://core.telegram.org/bots/api#rich-message-formatting-options`
- Telegram Bot API `sendRichMessage`: `https://core.telegram.org/bots/api#sendrichmessage`
- Telegram Bot API `InputRichMessage`: `https://core.telegram.org/bots/api#inputrichmessage`
