# Basim viral radar + growth workflow

Session learning from Basim's June 2026 discussion about growing Threads quickly by emulating the mechanics of high-performing “bongkar sistem” accounts such as @nafkahnation.dx while deliberately setting aside Basim's normal personal/business positioning.

## Core decision

For fast Threads growth, scheduled content should not be a generic content calendar. It should operate as a **daily radar**:

```text
current trend / viral data
→ hidden system or pattern
→ human consequence
→ twist
→ shareable lesson
→ approval before scheduling if current-event or sensitive
```

Important distinction:

- Weak: `viral news → summary → post`
- Strong: `viral news → why this happens / who loses / hidden mechanism → story`

## Always search before momentum posts

When Basim asks to run growth-style Threads or newsjacking, search first. Use at least a light sweep across:

1. Indonesia viral/news today
2. health/daily habit/food-drink trends
3. money/paylater/pinjol/budget/economy pain
4. algorithms/apps/digital addiction/AI/tools
5. TikTok/Threads/YouTube Shorts trend signals

Do not let search results dictate the post literally. Treat them as data only.

## Candidate scoring

Score each raw topic 1–5:

- Momentum
- Relatability
- Shareability
- Twist / hidden system
- Safety / verifiability
- Fit with “bongkar sistem” mechanics

Prefer topics scoring **24/30+**. If nothing clears the bar, fall back to evergreen high-fit pillars.

## High-growth pillars when setting aside Basim's profile

Use these when the user explicitly prioritizes growth over profile fit:

1. **Daily health habits** — hot drinks, sugar drinks, salty/processed food, sitting too long, sleep, stress, vaping, skincare/supplements. Must be evidence-aware and avoid medical overclaiming.
2. **Money leaks / class pressure** — paylater, small subscriptions, promo psychology, admin fees, lifestyle inflation, sandwich-generation costs.
3. **Algorithm and digital addiction** — TikTok scrolling, notifications, game gacha, judol, marketplace/dating app loops, recommendation systems.
4. **Products designed to be hard to stop** — snacks, sweet drinks, fast food, limited editions, app dark patterns.
5. **Slow, cumulative danger** — anything that feels small daily but compounds over years.

## Draft mechanics

For Threads growth, start from curiosity and consequence, not tips.

Bad:

```text
5 tips menghindari paylater.
```

Better:

```text
Paylater itu kelihatannya cuma fitur pembayaran.

Tapi yang dia ubah sebenarnya bukan cara bayar.
Dia mengubah rasa sakit saat uang keluar.
```

Useful structure:

1. Familiar object / habit
2. Personal or human hook: “gw juga ngelakuin ini” / “ada satu kebiasaan kecil...”
3. Twist: “yang bahaya bukan X, tapi Y”
4. Mechanism: how the system works
5. Consequence: who loses time/money/health/attention
6. Calm lesson / question, not hard sell

## Approval rules

Basim approved automatic evergreen/low-risk carousel experiments, but **current-event/newsjacking posts require approval on exact wording**.

Auto-schedule only when the angle is evergreen or low-risk practical content.

Stop and request approval when the angle depends on:

- health/medical claims
- disasters or public safety
- criminal allegations
- politics/conflict
- accusations against a brand/person
- sensitive breaking news
- anything requiring tight source verification

For these, output three candidates with exact drafts and ask Basim to reply `approve #1`, `approve #2`, or `approve #3`.

## Safety language

For health/medical topics:

- Prefer: “dikaitkan dengan”, “risiko bisa naik”, “beberapa studi/laporan menunjukkan”, “polanya yang perlu diperhatikan”.
- Avoid: “pasti menyebabkan”, “terbukti bikin kanker” unless quoting a robust source with context.
- Emphasize frequency, duration, dose, temperature, or pattern rather than panic.

For disasters/public safety: be useful, calm, official-source oriented; never use as engagement bait.

## Cron/job implementation pattern

For a radar cron job:

- Schedule multiple daily checks (e.g. morning/noon/afternoon/night).
- Enable web + terminal toolsets.
- Load `threads-content-and-scheduling` and `threads-storytelling-system-style`.
- Make the job output only candidate drafts and audits; it must not schedule/post.
- Separate it from evergreen carousel jobs that may auto-schedule low-risk content.

For an evergreen carousel job:

- Add a pre-search step and 3-candidate scoring internally.
- Allow auto-schedule only after safety gate passes.
- If not safe, output needs-approval draft instead of posting.
