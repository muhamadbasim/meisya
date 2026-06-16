# News digest manual rerun verification pattern

Session pattern: user asked to continue the Automation Blueprints news digest after a gateway restart and provider switch to OpenAI Codex.

## Durable lesson

`cronjob(action='run')` / `hermes cron run <id>` can return success while only moving `next_run_at` to an immediate/manual trigger time. Delivery is not proven until the scheduler actually runs the job and `agent.log` shows completion + delivery.

## Verification sequence that worked

1. `cronjob(action='list')` to identify the production job and verify:
   - provider/model pinned to `openai-codex` / target model
   - delivery target has the correct Telegram thread/topic
   - job is enabled
2. Trigger the job.
3. Wait longer than one scheduler tick, then inspect `~/.hermes/logs/agent.log` rather than only `gateway.log`.
4. Look for this chain:
   - `Running job '<name>' (ID: <id>)`
   - cron session line with `platform=cron`, expected provider/model
   - `Job '<name>' completed successfully`
   - `Job '<id>': delivered to <telegram target> via live adapter`
5. Re-list jobs to confirm `last_status: ok` and `next_run_at` has returned to the normal schedule.

## Pitfalls observed

- Gateway logs may only show cron ticker activity and inbound user messages; cron execution details are in `agent.log`.
- `next_run_at` can temporarily look stale/past-due right after a manual trigger; do not call the job successful until logs and `last_status` confirm it.
- If the job is a news briefing with web extraction trouble, the cron can still succeed using terminal/web fallbacks; do not treat an intermediate tool warning as the final job status.
