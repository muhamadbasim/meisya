# OpenAI Codex provider repair pattern for Hermes cron

Session pattern captured from a cron failure repair:

## Symptom

A scheduled news-summary cron job repeatedly failed and delivered failure notices:

```text
RuntimeError: HTTP 503: Layanan AI sedang mengalami kendala sementara. Silakan coba lagi beberapa menit lagi.
```

A separate carousel cron had previous provider quota errors:

```text
RuntimeError: HTTP 429: Kuota model sedang penuh.
```

## Important observations

- `cronjob(action='list')` showed the failing news job using no explicit model/provider at first, so it inherited the default GrowthCircle/custom provider.
- Scheduler logs showed the actual cron run details, not guesses:

```text
conversation turn: session=cron_<job> model=gpt-5.5 provider=custom platform=cron
API call failed ... provider=custom base_url=https://ai.growthcircle.id/v1 model=gpt-5.5
```

- The live chat session had later been switched to OpenAI Codex / `gpt-5.5`; that did not automatically change existing cron jobs unless explicitly updated.
- A previous attempted fix deleted/recreated the job. Avoid this: update in place unless deletion is explicitly required.

## Repair steps that worked

1. Audit jobs and logs:
   - `cronjob(action='list')`
   - read `~/.hermes/cron/jobs.json`
   - inspect `~/.hermes/logs/agent.log` around the failing run
2. Pin agent-driven cron jobs to the working provider/model:
   - provider: `openai-codex`
   - model: `gpt-5.5`
3. Do not modify no-agent script jobs; they do not call an LLM provider.
4. Create a temporary one-shot `deliver='local'` provider test job with prompt: `Reply exactly: OK_OPENAI_CODEX_CRON`.
5. Verify the output file contains the sentinel and logs show:

```text
loaded credential pool for provider openai-codex
provider=openai-codex base_url=https://chatgpt.com/backend-api/codex model=gpt-5.5
completed successfully
```

6. Run the real job only after the local provider test succeeds.
7. Confirm the real job status becomes `ok`, the output file exists, and there are no duplicate/temp jobs remaining.

## OAuth token revoked / invalidated credential variant

A later cron repair had this OpenAI Codex OAuth failure:

```text
RuntimeError: Error code: 401 - {'error': {'message': 'Encountered invalidated oauth token for user, failing request', 'code': 'token_revoked'}, 'status': 401}
```

Useful lessons:

- `hermes auth status openai-codex` may still print `logged in`; do not treat that alone as proof cron can use the credential.
- If the user asks to get the automation running again now, prefer a pragmatic fallback:
  1. Test a known working provider/model with a tiny chat or sentinel prompt, e.g. Gemini if configured.
  2. Update the existing cron job in place with `cronjob(action='update', job_id=..., model={provider: ..., model: ...})`.
  3. Preserve schedule, delivery target, skills, and job ID.
  4. Trigger or wait for the run, then verify `last_status=ok` and inspect the newest output file.
- Manual `hermes cron run <job_id>` / `cronjob(action='run')` can schedule the run for the next tick and recurring jobs may then advance `next_run_at`; verify completion from the job record and `~/.hermes/cron/output/<job_id>/`, not from the trigger command alone.
- Do not print `.env`, OAuth tokens, API keys, or request dumps containing credentials; summarize credentials as `[REDACTED]`.

Example successful final state to report:

```text
provider: gemini
model: gemini-2.5-flash
last_status: ok
next_run_at: <normal schedule preserved>
```

## User-facing repair summary format

Keep it concise:

- Akar masalah: provider/model actually used by cron + exact HTTP error.
- Yang diperbaiki: job IDs, provider/model, schedule/delivery unchanged.
- Verifikasi nyata: sentinel test output + production job status/output path.
- Acknowledge if a previous action was too aggressive (e.g. deleted/recreated a job) and state current final state.