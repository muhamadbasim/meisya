# SenangCarousels API Notes

Session-specific reference for `http://43.156.20.232:8000` carousel API behavior observed in June 2026.

## Contract observed

- `GET /openapi.json` returned an OpenAPI 3.1 spec.
- Main endpoints:
  - `POST /api/carousel/generate`
  - `POST /api/carousel/export`
  - `POST /api/carousel/save`
  - `GET /api/carousel/{carousel_id}`
- `CarouselGenerateRequest` fields:
  - `topic` required string
  - `tone` string, default `professional`
  - `num_slides` integer, default `5`
  - `user_openai_key` nullable string
  - `user_gemini_key` nullable string
- No OpenAPI `security` scheme was declared.

## Credential behavior observed

Despite the presence of `user_openai_key`, generation behaved as if Gemini was mandatory:

- `user_openai_key` with an OpenAI-compatible/GrowthCircle key returned:
  - `400 API Key tidak tersedia. Silakan masukkan Gemini API Key Anda (BYOK) atau hubungi administrator.`
- `user_openai_key` with Codex/ChatGPT OAuth access token returned the same Gemini-key-required error.
- `Authorization: Bearer <OAuth token>` returned the same Gemini-key-required error.
- Putting the OAuth token into `user_gemini_key` reached Google validation but failed:
  - `400 API key not valid. Please pass a valid API key.`

Interpretation: for this backend version, GPT/OAuth is not actually supported by the generate path even though an OpenAI-key field exists. A valid Gemini API key is required unless the backend is changed.

## Gemini key/model behavior observed

A user-supplied Gemini API key can be valid while `/api/carousel/generate` still fails. In this session:

- Direct Gemini `ListModels` with the key succeeded and showed supported `generateContent` models including `gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-flash-latest`, and newer preview models.
- SenangCarousels `/api/carousel/generate` with the same key returned:
  - `404 models/gemini-1.5-flash is not found for API version v1beta, or is not supported for generateContent.`
- Extra request fields/query params such as `model=gemini-2.5-flash` and `gemini_model=gemini-2.5-flash` did not override the backend model choice.
- Direct provider generation with `gemini-flash-latest` succeeded after `gemini-2.5-flash` returned temporary high-demand `503` and `gemini-2.0-flash` returned quota `429`.
- The resulting direct-Gemini carousel JSON could be normalized to `CarouselCreate` and saved successfully via `/api/carousel/save`.

Interpretation: distinguish “invalid key” from “valid key, backend pinned to unavailable model.” When the latter happens, validate the key directly, use a current Gemini model to produce schema-conformant JSON if allowed, then POST to `/save` or `/export` as separate steps. Do not print the key; print only presence/length and model/status outcomes.

## Export failure signature observed

A minimal valid `CarouselCreate` payload to `/api/carousel/export` returned HTTP 500 with:

```text
BrowserType.launch: Executable doesn't exist at /ms-playwright/chromium_headless_shell-1223/chrome-headless-shell-linux64/chrome-headless-shell
Looks like Playwright was just updated to 1.60.0.
current: mcr.microsoft.com/playwright/python:v1.44.0-jammy
required: mcr.microsoft.com/playwright/python:v1.60.0-jammy
```

Interpretation: export/rendering was blocked by server-side Playwright/container version mismatch, independent of payload validity.

## Practical debugging recipe

1. Fetch `/openapi.json` and inspect schemas/security before relying on `AGENTS.md` prose.
2. Test `/api/carousel/generate` with sanitized credentials and capture status/error body.
3. Test `/api/carousel/export` with a minimal `CarouselCreate` payload separately.
4. If export fails with the Playwright signature above, the likely fix is server-side: update container image/browser install to match Playwright version, e.g. use the required `mcr.microsoft.com/playwright/python:v1.60.0-jammy` for that version or install the expected browser bundle.
5. If user still needs an artifact immediately, create a clearly labeled local fallback ZIP/PNG and do not present it as API-generated.
