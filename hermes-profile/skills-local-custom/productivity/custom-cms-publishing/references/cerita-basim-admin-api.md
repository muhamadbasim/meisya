# cerita.basim.id Admin API Notes

Session-derived notes for publishing markdown posts to `cerita.basim.id`. Keep secrets out of this file; the admin token must be referenced only as `[REDACTED]` or read from `CERITA_ADMIN_TOKEN`.

## Secret storage

- Store token in `~/.hermes/.env` as:
  - `CERITA_ADMIN_TOKEN=[REDACTED]`
- Keep env file mode at `600`.
- Never print the token in chat, public posts, payload previews, or logs returned to the user.

## Create published post

Endpoint:

```text
POST https://cerita.basim.id/api/admin/posts
Content-Type: application/json
x-admin-token: $CERITA_ADMIN_TOKEN
```

Known body fields:

```json
{
  "slug": "pembelajaran-hermes-basim",
  "title": "Pembelajaran Hermes × Basim",
  "description": "Short summary",
  "body_md": "# Markdown body...",
  "tags": ["catatan", "hermes", "agent", "whatsapp", "telegram"],
  "status": "published",
  "featured": false,
  "author": "Basim",
  "source": "admin-api"
}
```

Observed create success:

- HTTP `201`
- Response shape includes `success: true`, `post.id`, `post.slug`, and `url`.

## Update existing post

If POST returns:

```json
{"error":"Slug already exists","slug":"pembelajaran-hermes-basim"}
```

with HTTP `409`, update by slug instead of retrying POST:

```text
PATCH https://cerita.basim.id/api/admin/posts/<slug>
Content-Type: application/json
x-admin-token: $CERITA_ADMIN_TOKEN
```

Observed update success:

- HTTP `200`
- Response includes `success: true` and updated `post`.

Notes:

- `PUT /api/admin/posts/<slug>` returned an HTML 404 in this session.
- `PATCH /api/admin/posts/<id>` returned JSON 404 `Post not found`.
- The working update endpoint was `PATCH /api/admin/posts/pembelajaran-hermes-basim`.

## Read/verify admin state

Admin list/read endpoints observed:

```text
GET https://cerita.basim.id/api/admin/posts
GET https://cerita.basim.id/api/admin/posts/<slug>
```

Both require `x-admin-token`. Without the token, API returns `401 {"error":"unauthorized","detail":"no_token"}`.

Verification checklist:

- `id` matches expected post.
- `slug` matches expected slug.
- `status` is `published`.
- `body_md` length increased/changed as expected.
- `body_md` contains a unique phrase from the new version.

## Cloudflare/API access pitfall

If Python `urllib`/default client gets HTTP `403` with `error code: 1010`, retry the admin API with `curl` and a normal browser-like `User-Agent`; this succeeded for create and verify calls. Keep tokens in env and do not print them.

Example header pattern:

```text
-A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125 Safari/537.36'
-H 'x-admin-token: $CERITA_ADMIN_TOKEN'
```

## Public route verification

Observed public route that returned HTTP `200`:

```text
https://cerita.basim.id/cerita/d/<slug>
```

For the Hermes × Basim article:

```text
https://cerita.basim.id/cerita/d/pembelajaran-hermes-basim
```

Pitfall:

- `https://cerita.basim.id/cerita/<slug>` returned `404` even though the admin API response/documentation may mention `/cerita/:slug`.
- Use cache-busting (`?nocache=<timestamp>`) when checking whether a recently patched body is visible publicly.

## Content expansion pattern that worked

When the user asked to make each lesson “1 page”, the effective shape was:

- A stronger intro explaining the system-level framing.
- One section per lesson.
- For each lesson:
  - context/incident,
  - what actually failed or worked,
  - technical lesson,
  - risk/implication,
  - practical rule for future use.
- Keep it narrative and readable, not just bullets.
