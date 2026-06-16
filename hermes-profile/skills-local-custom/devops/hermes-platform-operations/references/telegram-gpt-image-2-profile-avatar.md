# gpt-image-2 for Telegram bot avatar work

Use these notes when a user asks for a Telegram bot profile photo generated with OpenAI `gpt-image-2`, especially realistic or semi-robot/cybernetic portraits.

## Provider routes in Hermes

Hermes has two bundled gpt-image-2 image-gen backends:

- `image_gen/openai` — requires `OPENAI_API_KEY`.
- `image_gen/openai-codex` — uses Codex/ChatGPT OAuth; no API key, but requires an interactive device-code login.

The general `image_generate` tool uses the user-configured image backend/model. If it fails, check whether the requested backend is actually configured and authenticated before trying unrelated fallbacks.

## Codex OAuth device-code flow

The documented CLI hint may say `hermes auth codex`, but the current CLI surface uses the auth subcommand shape:

```bash
hermes auth add openai-codex
```

Run it in PTY mode. If the task is happening through a messaging gateway, start it as a tracked background process so the agent can continue the conversation while the CLI waits:

```bash
hermes auth add openai-codex
```

Expected output shape:

```text
To continue, follow these steps:

  1. Open this URL in your browser:
     https://auth.openai.com/codex/device

  2. Enter this code:
     XXXX-XXXX

Waiting for sign-in... (press Ctrl+C to cancel)
```

Send the URL and code to the user, then wait for them to confirm completion. After confirmation, poll/wait the process and verify the image provider is available before generation.

## Prompt pattern: realistic semi-robot assistant

For the user's “semi robot realistis” preference, avoid cartoon, full robot, horror cyborg, or cheap metallic masks. Prompt for a human-first professional avatar with subtle cybernetic elements:

```text
Photorealistic professional portrait of an Indonesian female AI assistant named Meisya, warm confident expression, elegant navy blazer and ivory blouse, subtle cybernetic details integrated near one temple and cheek, faint luminous circuit accents under natural skin, realistic human eyes, clean teal/deep-blue digital studio background, premium soft lighting, head-and-shoulders corporate headshot, suitable for Telegram circular profile crop, not scary, not full robot, no text, no logo, no watermark.
```

Quality gate before upload:

- Face is centered and readable after circular crop.
- Looks professional and realistic, not crude/uncanny if avoidable.
- No text, watermark, extra limbs, severe facial asymmetry, or distorted collar/hands.
- If the user already criticized a prior avatar as low-quality, regenerate rather than defending it.
