# Provider account usage checks

Use this recipe when the user asks to check Hermes provider usage, quota, account limits, or OpenAI-Codex/Gemini/Anthropic/OpenRouter consumption from a gateway chat.

## OpenAI-Codex OAuth usage

1. Load `hermes-agent` for canonical CLI/provider context if not already loaded.
2. Confirm active provider/model without exposing secrets:
   - `hermes status`
   - `hermes auth list openai-codex`
3. For session-level token usage, run Insights with the relevant platform/time window:
   - `hermes insights --days 1 --source telegram`
   - Adjust `--days` / `--source` to the user's scope.
4. For account-limit state, use the built-in account usage helper instead of inventing API calls:

```bash
cd ~/.hermes/hermes-agent && python - <<'PY'
from agent.account_usage import fetch_account_usage, render_account_usage_lines
snap = fetch_account_usage('openai-codex')
print('snapshot:', bool(snap))
if snap:
    for line in render_account_usage_lines(snap, markdown=False):
        print(line)
PY
```

5. If the rendered helper only shows plan/provider but no percent windows, the OpenAI-Codex usage API likely returned no `rate_limit` object for that account. To verify safely, fetch and summarize only non-secret fields from `https://chatgpt.com/backend-api/wham/usage` via Hermes' `agent.account_usage._resolve_codex_usage_url` and `hermes_cli.auth.resolve_codex_runtime_credentials`; do **not** paste OAuth tokens/access tokens.
6. Report separately:
   - **Account status**: logged in, plan, spend-control / overage status, whether credits exist.
   - **Session usage**: Insights token totals and model breakdown.
   - **Limitation**: whether the provider API did or did not expose rate-limit percentages.

## Reporting pattern for Basim/Tuan

Keep the report concise in Indonesian with Markdown tables. Include exact command-derived facts and a timestamp from `date`, but avoid account IDs, user IDs, emails, OAuth tokens, and raw credential JSON unless the user explicitly asks and redaction policy permits it.

Example fields:

| Item | Status |
|---|---:|
| Provider aktif | OpenAI Codex |
| Model aktif | gpt-5.5 |
| Login OAuth | aktif / logged in |
| Plan terdeteksi | Self Serve Business Usage Based |
| Rate limit API | tidak menampilkan persentase usage |
| Spend control | belum kena limit |
| Overage limit | belum tercapai |

Then add a second small table for `hermes insights` totals (sessions, messages, tool calls, input/output/total tokens, and model breakdown).