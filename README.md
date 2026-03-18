# Automated Spotify Playlist Operations

Production-style automation pipeline for managing inbound playlist submissions and lifecycle rotation.

## Hiring manager snapshot

This repo reads well as an automation / ops portfolio piece because it shows:

- real creator-economy workflow thinking instead of toy CRUD work
- Python scripting tied to business rules, approvals, and lifecycle cleanup
- practical state management for submissions and active playlist entries
- useful handoff docs for a non-author operator or teammate

## Proof artifacts

- Demo walkthrough: `docs/DEMO.md`
- Verification checklist: `docs/VERIFICATION_CHECKLIST.md`
- Architecture notes: `docs/ARCHITECTURE.md`
- Operations notes: `docs/OPERATIONS.md`
- Screenshots: `docs/screenshots/`
- Sample inputs: `samples/`

## Local verification status

Validated in this workspace:

- `python -m unittest discover -s tests -q` ✅
- `python -m pytest -q` ⚠️ not available by default on this machine, so the repo currently verifies via built-in `unittest`

If you want this to read cleaner to employers, explicitly documenting `unittest` as the default test runner is stronger than implying pytest is required.

## What this project does

This system automates the end-to-end process for playlist submissions:

1. Ingests submissions from **Squarespace forms** (via Zapier) and/or **Discord form feed**
2. Sends a verification email to the submitter
3. Requires a screenshot confirmation step before approval
4. Adds approved songs to a target Spotify playlist using a staggered insertion pattern
5. Auto-removes songs after 30 days
6. Maintains submission and active-entry logs for ops visibility

## Why this is useful

For music ops teams and studios, playlist workflows are usually manual and error-prone. This project shows a practical automation system with:

- API auth + token refresh management (Spotify OAuth)
- Human-in-the-loop verification gates
- Idempotent submission processing patterns
- Scheduled lifecycle cleanup jobs
- Recruiter-friendly operational documentation

---

## System Flow

```text
Squarespace Form
   -> Zapier
      -> Discord #website-forms (and/or email)
         -> Poller + Parser
            -> Verification Email
               -> Screenshot Reply Verification
                  -> Spotify Add Track (staggered position)
                     -> 30-Day Cleanup Cron -> Spotify Remove Track
```

## Demo Source (Squarespace)

Example public submission page used in this workflow:
- https://www.blakmarigold.com/playlist-submission

Verification UX evidence screenshots are documented in:
- `docs/DEMO.md`

## End-to-End Test Flow (Step + Proof)

1. Submit a song through the Squarespace page above.
2. Submission is routed by Zapier into Discord `#website-forms` and enters the automation queue.
3. System sends verification email asking submitter to **save the playlist** and reply with screenshot proof.
4. Submitter replies with screenshot evidence.
5. System approves and adds the track using staggered insertion logic.
6. System schedules auto-removal at +30 days.

Proof artifacts:
- Playlist save page screenshot: `docs/screenshots/step-02-save-playlist-page.jpg`
- Email reply screenshot proof: `docs/screenshots/step-03-email-reply-screenshot-proof.jpg`

## Quality checks

```bash
python -m unittest discover -s tests -q
```

Optional:
- use `pytest` only if you prefer it locally and already have it installed
- CI is intentionally pinned to the built-in `unittest` command above

## Repository Structure

```text
.
├─ docs/
│  ├─ ARCHITECTURE.md
│  ├─ DEMO.md
│  └─ OPERATIONS.md
├─ samples/
│  ├─ discord_form_message.txt
│  └─ webhook_payload.json
├─ src/
│  └─ playlist_manager.py
├─ tests/
│  └─ test_playlist_manager.py
├─ .env.example
├─ .gitignore
└─ README.md
```

---

## Quick Start

### 1) Clone and enter repo

```bash
git clone https://github.com/iamMichaelSmith/Automated-Spotify-Playlist-Operations.git
cd Automated-Spotify-Playlist-Operations
```

### 2) Configure environment

Copy `.env.example` into your local environment system (or `.env` if you use a loader):

- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `SPOTIFY_REFRESH_TOKEN`
- `PLAYLIST_ID`

### 3) Submit a test lead

```bash
python src/playlist_manager.py submit \
  --name "Test Artist" \
  --email "artist@example.com" \
  --track-url "https://open.spotify.com/track/0qGusnDxYospgRJ9w7UUkz" \
  --playlist-url "https://open.spotify.com/playlist/0HlSskyngVugWJd10JbgKW"
```

### 4) Approve and add

```bash
python src/playlist_manager.py approve --email "artist@example.com"
```

### 5) Run cleanup job

```bash
python src/playlist_manager.py cleanup
```

---

## Insertion Strategy

Approved songs are intentionally staggered to keep playlist flow natural:

- 1st add: position 18
- 2nd add: position 22
- 3rd add: position 26
- 4th add: position 29
- then +3 for each next add (32, 35, 38...)

This avoids clumping and keeps a mix between existing catalog and new submissions.

---

## Security Notes

- Never commit live OAuth secrets or refresh tokens.
- Use local env vars or secure secret manager.
- If a secret is exposed, rotate immediately.

---

## Roadmap

- Direct Zapier webhook endpoint service for submissions
- Attachment-aware screenshot verification parser
- Retry queue + dead-letter handling
- Multi-playlist routing by genre
- Ops dashboard for SLA + conversion metrics

---

## Recruiter Snapshot

This repo demonstrates practical backend automation for creator economy operations:

- Python automation scripting
- OAuth/API lifecycle handling
- Workflow orchestration (Squarespace/Zapier/Discord/Gmail/Spotify)
- Production-oriented state and cleanup jobs
- Clear docs for onboarding and handoff
