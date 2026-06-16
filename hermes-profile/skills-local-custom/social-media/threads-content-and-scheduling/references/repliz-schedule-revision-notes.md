# Repliz schedule revision notes

Session-derived notes for revising already-created Basim Threads schedules.

## Observed API behavior

- `GET /public/schedule/{scheduleId}` works for retrieving a scheduled item, including `description`, `replies`, `status`, and `scheduleAt`.
- `PUT /public/schedule/{scheduleId}` and `PATCH /public/schedule/{scheduleId}` returned `404 Cannot PUT/PATCH ...` in this session, so do not assume direct schedule editing exists.
- `DELETE /public/schedule/{scheduleId}` returned `204` and removed the schedule.
- Recreate revised content with `POST /public/schedule`, preserving the original `scheduleAt` if the user asked to revise existing scheduled posts.
- Verify with `GET /public/schedule/{newScheduleId}` that the new `description` and `replies` match and that the reply count is correct.

## Safe revision flow

1. Fetch the current schedule with `GET /schedule/{id}`.
2. Build the revised body while preserving `scheduleAt`.
3. If direct `PUT/PATCH` fails or is unsupported, delete the old schedule.
4. Recreate with `POST /schedule` at the same `scheduleAt`.
5. Verify the new schedule and report old→new schedule IDs.

## Basim formatting pitfall

For Basim storytelling threads scheduled through Repliz, do **not** include visible numeric prefixes like `1/`, `2/`, `3/` at the start of each Thread part unless Basim explicitly asks for numbering. He corrected this in-session with “hilangin semua angka didepannya.” Use the thread/reply structure itself to imply order.

If a schedule already contains numeric prefixes, strip only the leading `^\s*\d+\s*/` marker from each `description` and reply before recreating the schedule.
