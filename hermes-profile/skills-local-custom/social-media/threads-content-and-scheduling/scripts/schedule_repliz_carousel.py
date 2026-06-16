#!/usr/bin/env python3
"""Schedule an exported carousel to Basim's Repliz accounts.

Inputs:
- PNG slides directory containing slide-*.png
- optional MP4 slideshow for TikTok/YouTube
- caption text

Environment:
- REPLIZ_ACCESS_KEY
- REPLIZ_SECRET_KEY

Behavior:
- Uploads local media to Uguu public URLs
- Verifies public URLs by HEAD
- Schedules Threads/Instagram as album posts
- Schedules TikTok/YouTube as video posts when --video is provided
- Verifies every created Repliz schedule with GET /public/schedule/{id}
- Prints a JSON summary; never prints credentials
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import pathlib
import subprocess
import sys
import urllib.error
import urllib.request

DEFAULT_ACCOUNTS = {
    "threads": "6a06e4094492e5f5a8f6d3a4",
    "instagram": "6a278b06c5ff4ce3a320c726",
    "tiktok": "6a278d5fc5ff4ce3a320c7a4",
    "youtube": "6a278d72c5ff4ce3a320c7a7",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--slides-dir", required=True, help="Directory containing slide-*.png")
    p.add_argument("--video", help="MP4 slideshow for TikTok/YouTube")
    p.add_argument("--caption", required=True, help="Post caption/body")
    p.add_argument("--title", default="", help="Video title; album title stays empty")
    p.add_argument("--start-utc", help="ISO UTC schedule time. Default: now + 8 minutes")
    p.add_argument("--platforms", default="threads,instagram,tiktok,youtube")
    p.add_argument("--stagger-minutes", type=int, default=1)
    return p.parse_args()


def upload_uguu(path: pathlib.Path) -> str:
    cp = subprocess.run(
        ["curl", "-sS", "-F", f"files[]=@{path}", "https://uguu.se/upload.php"],
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    if cp.returncode != 0:
        raise RuntimeError(f"Uguu upload failed for {path.name}: {cp.stderr.strip()}")
    # Uguu may pretty-print JSON over multiple lines. Parse the whole stdout, not line-by-line.
    data = json.loads(cp.stdout)
    if not data.get("success") or not data.get("files"):
        raise RuntimeError(f"Uguu upload returned no file for {path.name}: {cp.stdout[:500]}")
    return data["files"][0]["url"]


def verify_url(url: str) -> dict:
    req = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(req, timeout=30) as r:
        return {
            "status": r.status,
            "content_type": r.headers.get("Content-Type"),
            "content_length": r.headers.get("Content-Length"),
        }


def repliz_headers() -> dict:
    access = os.environ["REPLIZ_ACCESS_KEY"]
    secret = os.environ["REPLIZ_SECRET_KEY"]
    token = base64.b64encode(f"{access}:{secret}".encode()).decode()
    return {
        "Authorization": "Basic " + token,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def request_json(method: str, url: str, headers: dict, payload: dict | None = None) -> tuple[int, str]:
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read().decode(errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")


def main() -> int:
    args = parse_args()
    slides_dir = pathlib.Path(args.slides_dir)
    slides = sorted(slides_dir.glob("slide-*.png"))
    if not slides:
        raise SystemExit(f"No slide-*.png found in {slides_dir}")
    video = pathlib.Path(args.video) if args.video else None
    platforms = [p.strip() for p in args.platforms.split(",") if p.strip()]

    media_urls = {p.name: upload_uguu(p) for p in slides}
    if video:
        media_urls[video.name] = upload_uguu(video)

    verifications = {name: verify_url(url) for name, url in media_urls.items()}

    if args.start_utc:
        base = dt.datetime.fromisoformat(args.start_utc.replace("Z", "+00:00"))
    else:
        base = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=8)).replace(second=0, microsecond=0)

    headers = repliz_headers()
    slide_urls = [media_urls[p.name] for p in slides]
    results = []

    for idx, platform in enumerate(platforms):
        schedule_at = (base + dt.timedelta(minutes=idx * args.stagger_minutes)).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        if platform in {"threads", "instagram"}:
            payload = {
                "title": "",
                "description": args.caption,
                "topic": "",
                "type": "album",
                "medias": [
                    {"type": "image", "thumbnail": u, "url": u, "alt": f"Carousel slide {n}"}
                    for n, u in enumerate(slide_urls, 1)
                ],
                "additionalInfo": {"isAiGenerated": False, "isDraft": False},
                "replies": [],
                "accountId": DEFAULT_ACCOUNTS[platform],
                "scheduleAt": schedule_at,
            }
        else:
            if not video:
                results.append({"platform": platform, "error": "video required"})
                continue
            payload = {
                "title": args.title,
                "description": args.caption,
                "topic": "",
                "type": "video",
                "medias": [
                    {"type": "video", "thumbnail": slide_urls[0], "url": media_urls[video.name], "alt": args.title or "Carousel slideshow"}
                ],
                "additionalInfo": {"isAiGenerated": False, "isDraft": False},
                "replies": [],
                "accountId": DEFAULT_ACCOUNTS[platform],
                "scheduleAt": schedule_at,
            }

        status, body = request_json("POST", "https://api.repliz.com/public/schedule", headers, payload)
        schedule_id = None
        try:
            schedule_id = json.loads(body).get("scheduleId")
        except Exception:
            pass
        verify_status = None
        verify_summary = None
        if schedule_id:
            verify_status, verify_body = request_json("GET", f"https://api.repliz.com/public/schedule/{schedule_id}", headers)
            try:
                obj = json.loads(verify_body)
                verify_summary = {
                    "type": obj.get("type"),
                    "media_count": len(obj.get("medias") or []),
                    "scheduleAt": obj.get("scheduleAt"),
                    "accountId": obj.get("accountId"),
                }
            except Exception:
                verify_summary = verify_body[:300]
        results.append({
            "platform": platform,
            "createStatus": status,
            "scheduleId": schedule_id,
            "scheduleAtUTC": schedule_at,
            "verifyStatus": verify_status,
            "verify": verify_summary,
        })

    print(json.dumps({"media": media_urls, "mediaVerification": verifications, "results": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
