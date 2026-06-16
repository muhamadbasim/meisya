# Repliz content analytics API notes

Use this when the user asks to analyze published post performance, check Threads views, or run a recurring content-improvement workflow through Repliz.

## Auth

Use Basic Auth:

```http
Authorization: Basic Base64(AccessKey:SecretKey)
Accept: application/json
```

Security: never echo the secret key in user-facing output. If keys were pasted in chat, advise rotation/regeneration after setup.

## Verify account

```http
GET https://api.repliz.com/public/account/{accountId}
```

Useful safe fields to report:
- `name`
- `username`
- `type`
- `isConnected`
- `updatedAt`

Do not print token fields if returned.

## List published content

```http
GET https://api.repliz.com/public/content?accountId={accountId}&type=media
```

Observed response shape:

```json
{
  "docs": [
    {
      "id": "17911078545219651",
      "title": "",
      "description": "post text",
      "type": "text",
      "url": "https://www.threads.com/@username/post/...",
      "createdAt": "2026-06-03T06:15:14.000Z"
    }
  ],
  "nextToken": "..."
}
```

For daily review, fetch at least the 10 newest posts when available. Use `nextToken` only if more history is needed.

## Fetch statistics per content item

```http
GET https://api.repliz.com/public/content/{contentId}/statistic?accountId={accountId}
```

Threads response fields observed/documented:

```json
{
  "like": 0,
  "replies": 0,
  "views": 4,
  "repost": 0,
  "quotes": 0,
  "share": 0
}
```

Other platforms return different field names, so normalize defensively.

## Analysis pattern

For Threads daily analysis:
1. Rank recent posts by `views` first, then replies/likes/shares.
2. Compare hooks and first 2-3 lines, not just total length.
3. Identify concrete patterns:
   - target clarity: app idea, business owner, digital project, manual process
   - emotional recognition: fear, delay, fatigue, uncertainty
   - specificity: concrete operational pain beats abstract motivation
4. Avoid claiming causality from small samples. Say “indikasi awal” or “sementara” when data is thin.
5. Produce replacement/new-post copy rather than claiming to edit already-published Threads unless an edit endpoint is verified.

## Daily output format for this user

Use Indonesian, concise and evidence-aware:

```text
Analisa Threads Harian — <tanggal WIB>

Update angka:
- ...

Yang kelihatan bekerja:
- ...

Yang perlu diperbaiki:
- ...

Posting perbaikan hari ini:
<copy siap posting>

Catatan:
- ...
```

Prefer practical edits: stronger hook, shorter setup, clearer target reader, and a copy draft ready to post.