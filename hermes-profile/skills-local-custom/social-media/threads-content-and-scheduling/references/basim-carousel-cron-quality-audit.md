# Basim carousel cron quality audit

Use this when maintaining or recovering Basim's scheduled carousel-to-Repliz workflow, especially after cron/model/provider updates.

## Durable lesson

Do not replace the detailed production carousel prompt with a short instruction such as “run existing config.” Cron jobs do not reliably preserve prior qualitative behavior from implication. If updating only the provider/model, preserve the detailed content/audit prompt or explicitly re-add the quality gates below.

## Baseline quality from the good 15 June run

The preferred carousel run output included:

- current trend/signal scan before choosing the angle;
- 48-hour Repliz performance notes by platform;
- 3 candidate angle scores with dimensions like momentum, relatability, shareability/saveability, twist, safety, and Basim fit;
- one low-risk evergreen angle selected from the scores;
- collision check against nearby scheduled posts (±45 minutes);
- media validation: slide count, `1080x1350`, ZIP `testzip=None`, public image URLs HTTP 200, MP4 public URL HTTP 200;
- per-platform Repliz schedule IDs and local WIB times;
- clear note if a local fallback artifact was used instead of the SenangCarousels API.

A later regressed run only said the angle was “ai agent butuh sistem dulu,” made 6 slides, and skipped most scoring/audit detail. Treat that as a prompt regression to fix.

## Required production workflow

1. Search current signals on the run day: AI/tools/creator, UMKM/business, workflow manual, Meta Ads/leads, customer follow-up, security/digital behavior, and safe economy/business trends.
2. If the signal is disaster, protest, policy conflict, or another sensitive current event, do **not** auto-schedule it as newsjacking. Convert to an evergreen systems lesson only if safe, otherwise output draft + approval request.
3. Pull/inspect recent Repliz performance when feasible. Current lesson: TikTok tends to work best for MP4 slideshow carousel, Instagram is moderate, Threads needs a concrete/human hook, YouTube needs a real title and should never be `unknown`.
4. Score at least 3 angle candidates. Pick the highest-scoring low-risk evergreen candidate.
5. Avoid repeating the same bucket from the last 48 hours. Rotate among: AI for owner, manual customer follow-up, Meta Ads leads leaking, app ideas stuck, scattered team chats, AI output kaku karena minim konteks, SOP/decision bottlenecks.
6. Keep public caption short, natural, soft-curiosity, 1–2 lines, and **no hashtags**.
7. Keep visual template aligned with Basim/SenangCarousels by default. Reference accounts like @ceritaberkelas inform content mechanics only: parable, one idea per slide, reflective copy, saveable flow. They should not replace Basim's established visual style unless Basim explicitly approves.
8. Validate media before scheduling. If the SenangCarousels API is unavailable or blocked, local fallback is allowed only if it preserves 1080x1350 and the usual Basim look; label it as fallback in the report.
9. Schedule Threads/Instagram as `album`, TikTok/YouTube as MP4 `video`, and report each schedule ID separately. Do not claim all-platform success if one platform fails.

## Report format

```text
Laporan carousel otomatis — <tanggal WIB>

Tren/sinyal yang dicek:
- ...

Performa Repliz 48 jam terakhir:
- ...

Skor kandidat:
1. ... Skor ...
2. ... Skor ...
3. ... Skor ...

Angle terpilih:
- ...

Audit konten:
- Kenapa aman/low-risk
- Kenapa cocok untuk carousel/saveable
- Kenapa tidak mengulang angle 48 jam terakhir

Status:
- Auto-scheduled / butuh approval jika sensitif
- Collision check: ...

Validasi media:
- jumlah slide dan dimensi
- ZIP valid
- public URLs
- MP4

Schedule Repliz:
- Threads — <WIB> scheduleId: ...
- Instagram — <WIB> scheduleId: ...
- TikTok — <WIB> scheduleId: ...
- YouTube — <WIB> scheduleId: ...

Local artifact:
MEDIA:<zip path>
```
