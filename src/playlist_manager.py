import argparse
import csv
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def state_dir() -> Path:
    root = Path(os.environ.get("PLAYLIST_OPS_STATE_DIR", "state"))
    root.mkdir(parents=True, exist_ok=True)
    return root


SUBMISSIONS = lambda: state_dir() / "spotify_playlist_submissions.csv"
ENTRIES = lambda: state_dir() / "spotify_playlist_entries.json"


def parse_spotify_id(url: str, kind: str) -> str:
    p = urlparse(url)
    parts = [x for x in p.path.split("/") if x]
    if len(parts) >= 2 and parts[0] == kind:
        return parts[1]
    raise ValueError(f"Could not parse {kind} id from URL: {url}")


def ensure_submissions_csv():
    path = SUBMISSIONS()
    if path.exists():
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "submitted_at",
            "name",
            "email",
            "track_url",
            "track_id",
            "playlist_url",
            "playlist_id",
            "status",
            "verified",
            "added_at",
            "remove_after",
            "notes",
        ])


def read_entries() -> list:
    path = ENTRIES()
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []


def write_entries(entries: list):
    ENTRIES().write_text(json.dumps(entries, indent=2), encoding="utf-8")


def next_playlist_insert_position(entries: list, playlist_id: str) -> int:
    pattern = [18, 22, 26, 29]
    active = [e for e in entries if e.get("status") == "active" and e.get("playlist_id") == playlist_id]
    idx = len(active)
    if idx < len(pattern):
        return pattern[idx]
    return pattern[-1] + ((idx - len(pattern) + 1) * 3)


def token_refresh() -> str:
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    refresh_token = os.environ.get("SPOTIFY_REFRESH_TOKEN")

    if not client_id or not client_secret or not refresh_token:
        raise RuntimeError("Missing SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET / SPOTIFY_REFRESH_TOKEN")

    body = (
        f"grant_type=refresh_token&refresh_token={quote(refresh_token)}"
        f"&client_id={quote(client_id)}&client_secret={quote(client_secret)}"
    ).encode("utf-8")

    req = Request("https://accounts.spotify.com/api/token", data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    with urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode("utf-8"))

    token = data.get("access_token")
    if not token:
        raise RuntimeError("Failed to refresh Spotify access token")
    return token


def spotify_add_track(playlist_id: str, track_id: str, position: int):
    token = token_refresh()
    payload = json.dumps({
        "uris": [f"spotify:track:{track_id}"],
        "position": position,
    }).encode("utf-8")

    req = Request(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", data=payload, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")

    with urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def spotify_remove_track(playlist_id: str, track_id: str):
    token = token_refresh()
    payload = json.dumps({"tracks": [{"uri": f"spotify:track:{track_id}"}]}).encode("utf-8")

    req = Request(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", data=payload, method="DELETE")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")

    with urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def submit(name: str, email: str, track_url: str, playlist_url: str):
    if "open.spotify.com/track/" not in track_url:
        raise ValueError("Only Spotify track URLs are accepted")

    ensure_submissions_csv()

    track_id = parse_spotify_id(track_url, "track")
    playlist_id = parse_spotify_id(playlist_url, "playlist")

    with SUBMISSIONS().open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            utc_now_iso(),
            name,
            email,
            track_url,
            track_id,
            playlist_url,
            playlist_id,
            "submitted",
            "pending",
            "",
            "",
            "verification_email_sent",
        ])

    return {"ok": True, "track_id": track_id, "playlist_id": playlist_id}


def approve(email: str):
    ensure_submissions_csv()

    rows = []
    target = None

    with SUBMISSIONS().open("r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)

    for row in reversed(rows):
        if row.get("email", "").strip().lower() == email.strip().lower() and row.get("status") == "submitted":
            target = row
            break

    if not target:
        raise RuntimeError("No submitted row found for this email")

    entries = read_entries()
    insert_position = next_playlist_insert_position(entries, target["playlist_id"])

    spotify_add_track(target["playlist_id"], target["track_id"], insert_position)

    added_at = datetime.now(timezone.utc)
    remove_after = added_at + timedelta(days=30)

    for row in rows:
        if row is target:
            row["status"] = "added"
            row["verified"] = "yes"
            row["added_at"] = added_at.isoformat()
            row["remove_after"] = remove_after.isoformat()
            row["notes"] = f"insert_position={insert_position}"

    with SUBMISSIONS().open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    entries.append({
        "email": target["email"],
        "playlist_id": target["playlist_id"],
        "track_id": target["track_id"],
        "insert_position": insert_position,
        "added_at": added_at.isoformat(),
        "remove_after": remove_after.isoformat(),
        "status": "active",
    })
    write_entries(entries)

    return {
        "ok": True,
        "playlist_id": target["playlist_id"],
        "track_id": target["track_id"],
        "insert_position": insert_position,
        "remove_after": remove_after.isoformat(),
    }


def cleanup():
    entries = read_entries()
    now = datetime.now(timezone.utc)
    removed = 0

    for e in entries:
        if e.get("status") != "active":
            continue

        ra = datetime.fromisoformat(e["remove_after"])
        if ra <= now:
            spotify_remove_track(e["playlist_id"], e["track_id"])
            e["status"] = "removed"
            e["removed_at"] = utc_now_iso()
            removed += 1

    write_entries(entries)
    return {"ok": True, "removed": removed}


def main():
    ap = argparse.ArgumentParser(description="Spotify playlist ops manager")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("submit")
    s.add_argument("--name", required=True)
    s.add_argument("--email", required=True)
    s.add_argument("--track-url", required=True)
    s.add_argument("--playlist-url", required=True)

    a = sub.add_parser("approve")
    a.add_argument("--email", required=True)

    sub.add_parser("cleanup")

    args = ap.parse_args()

    if args.cmd == "submit":
        out = submit(args.name, args.email, args.track_url, args.playlist_url)
    elif args.cmd == "approve":
        out = approve(args.email)
    else:
        out = cleanup()

    print(json.dumps(out))


if __name__ == "__main__":
    main()
