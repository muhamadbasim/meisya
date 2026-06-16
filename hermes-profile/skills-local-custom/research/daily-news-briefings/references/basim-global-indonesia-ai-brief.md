# Basim — Global, Indonesia, and AI Morning Briefing Notes

Derived from a session where Basim requested a daily 06:00 WIB briefing and then asked for an audit of the same morning's output.

## User expectation

Basim wants an Indonesian-language morning briefing covering:

1. Global news
2. Local/domestic Indonesia news
3. AI news
4. Audit and analysis, not just summary

Tone should be concise, critical, evidence-aware, and useful for strategic/content decisions.

## Specific lesson from audit

A prior briefing was acceptable as a fast radar but failed the contract in one important way: the “Indonesia” material was mostly **impact on Indonesia** from global/AI issues, not **local Indonesia news**. Future briefings should always include a separate `Indonesia Hari Ini` section with domestic items, then add `Dampak untuk Indonesia/Basim` as a separate analysis layer.

## Quality rubric used in audit

- Radar usefulness: can be good even when verification is partial.
- Decision usefulness: lower unless sources are cross-checked and recency is tight.
- AI section often yields the most strategic content angles if it covers infrastructure, security, distribution, pricing, regulation, and adoption.
- Global conflict/military/casualty/market claims require stronger source discipline than normal tech/product news.

## Recommended daily output for Basim

- `Top 5 yang wajib tahu pagi ini`
- `Global`
- `Indonesia Hari Ini`
- `AI & Teknologi`
- `Dampak untuk Indonesia/Basim`
- `Audit kualitas informasi`
- `Ide konten/strategi hari ini` when relevant
- `Yang perlu dipantau hari ini`

## Cron hygiene lesson

When creating or updating recurring briefings, check for existing jobs with similar schedule/scope. In this session there were two 06:00 news jobs, creating a risk of duplicate delivery. Future agents should list cron jobs before adding a new daily briefing when the user implies an existing one might already exist.
