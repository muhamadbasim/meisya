# Basim Threads carousel visual style notes

Session learning from adapting a Basim carousel to the `@ceritaberkelas` Threads profile.

## When Basim asks for a carousel inspired by a profile

Do not jump straight to a generic "premium" or "best in the world" design. First inspect the reference profile/media and infer concrete visual traits:

- aspect ratio: `@ceritaberkelas` carousels observed as portrait **4:5** (`1080x1350`), not square `1080x1080`.
- mood: calm self-improvement / reflective tips, not SaaS pitch deck or AI-tech poster.
- background: soft pastel, cream, muted color blocks; avoid dark cyber/tech unless explicitly requested.
- hierarchy: large simple text, generous whitespace, minimal supporting illustration.
- composition: one clear thought per slide; text is the product, decoration is secondary.
- illustration: small/simple line or soft shape, usually bottom or side; avoid noisy nodes, glow, dashboards, warning icons, and over-designed metaphors.
- typography: readable, human, quote-like. Avoid all-caps shouting unless the reference uses it.
- slide-to-slide system: allow muted color variation while keeping a consistent type scale, margins, footer, and numbering.

## Pitfall from the session

Basim rejected designs that were technically more polished but contextually wrong:

1. Square cream notebook version: too stiff and cheap.
2. Dark premium AI/tech version: looked like a startup/agency poster, not the reference style.
3. Editorial notebook with aggressive red marks: closer, but still too hard compared with `@ceritaberkelas`.

Important June 15 correction: when Basim says the carousel can be inspired by `@ceritaberkelas`, use it mainly for **format and content mechanics** — parable, short reflective slide copy, one idea per slide, saveable flow. Do **not** silently abandon Basim's usual SenangCarousels visual system. If the normal generator/API path is blocked and only a local fallback is possible, do not auto-schedule; deliver a preview/audit first.

Later correction from the same thread: if Basim says to “balikin lagi seperti semua/semula”, revert visual/content experiments back to the normal SenangCarousels carousel behavior. For testing, label dummy/manual content as dummy; for real examples, source the slide content from current web search and prefer the newest safe article from today.

The better direction is: **Basim's usual polished carousel template + trend-grounded content when requested**, not off-brand local cream/line-art fallback and not generic dummy slide copy unless the task is explicitly only a technical export test.

If Basim asks for `format/isi seperti contoh`, clarify or preserve the existing visual template by default: adapt only the narrative mechanics (parable, short reflective copy, one idea per slide, saveable flow), not the reference account's visual identity. If he says `balikin seperti semula`, remove the reference override from cron/prompt and restore the prior carousel prompt from backup where available.

## Live audit notes — @ceritaberkelas (June 2026)

Visible profile signals:

- Profile promise: `cerita yang membentuk karakter`, `menenun makna dalam setiap narasi`, positioned as self-improvement / character-building storytelling.
- Follower count observed: about `37.1K followers` on Threads at audit time.
- Recent carousel captions are intentionally short, almost label-like: `air`, `12 hobi yang diam-diam bikin kamu makin pintar💡`, `fokus pertumbuhan, bukan untuk mengesankan`, and reflective sentence hooks such as `bisa jadi kesulitan hari ini karena kita yang terlalu sering menolak kemungkinan bahkan saat belum mencoba`.
- Recent visible engagement was modest but save/repost-oriented: examples included roughly 44–50 likes, 1 comment, 6–14 reposts, 2 shares on visible posts. Treat these as live-observed page signals, not a guarantee of performance.

Observed slide mechanics:

- Format is portrait 4:5. Browser thumbnails showed `224x280`; production target should be `1080x1350`.
- Visual system is very minimal: white/cream canvas, large whitespace, black text, tiny brand mark near top right, small line-art human illustration near bottom/right.
- Text is the product. One idea per slide, usually 1–2 short sentences. Example observed cover copy: `kita semua tahu` then `ular tidak punya kaki, tapi bisa memangsa hewan yang berlari lebih cepat.`
- Hook mechanism: starts from a concrete analogy/object/ordinary observation, then converts it into a life/business insight. It feels like a quiet parable rather than a loud marketing deck.
- Caption often does not explain everything; it acts as a soft curiosity label so the carousel must carry the narrative.
- Works because it is saveable, reflective, and low-friction to repost: no dense charts, no heavy proof burden, no corporate tone.

Adaptation for Basim multi-platform carousels:

- Keep the 4:5 portrait, quiet whitespace, black human typography, and small supporting illustration.
- Translate self-improvement parables into owner/AI/business parables: everyday object/analogy → hidden business system → tiny practical shift.
- Keep slide count around 7–10 for Threads/Instagram. Use 5–7 only for very simple topics; avoid 12+ unless the concept needs it.
- Public copy should feel like reflective Indonesian, not startup jargon: `bisnis sering bocor bukan karena owner malas, tapi karena semua keputusan kecil masih nunggu owner`.
- Put only one main claim per slide. No dense bullet lists except one checklist slide near the end.
- Add stronger Basim payoff than the reference: after the parable, include a practical AI/system checklist that a business owner can save.
- Avoid copying wording, logo placement exactly, character drawings, brand name, or literal parables from @ceritaberkelas. Adapt the mechanics only.

## Practical generation checklist

Before generating final carousel images:

1. Re-check the reference profile/media if available.
2. Match the reference's aspect ratio first.
3. Create a small preview/contact sheet before delivering all slides.
4. Keep each slide sparse: one main sentence + one supporting sentence.
5. Use visual accents only to support comprehension, not to show off.
6. For @ceritaberkelas-style carousels, default to quiet parable format: object/analogy → conflict → hidden system → practical takeaway.
7. If Basim says "masih kurang nendang", improve hierarchy and copy punch, but do not automatically add tech/glow/noise.

## Basim positioning translation

For Basim, adapt self-improvement carousel mechanics to business/AI systems:

- "disiplin/konsisten" style → "owner tidak jadi bottleneck".
- "konten ini memang untukmu" style → make business owners feel recognized: "ini bisnis gue".
- AI should appear as a practical helper for repeated work, not as a futuristic brand identity.
