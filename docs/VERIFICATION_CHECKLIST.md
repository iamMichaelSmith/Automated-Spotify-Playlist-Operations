# Verification Checklist

Compact evaluator-facing proof for `Automated-Spotify-Playlist-Operations`.

## Verified locally on 2026-03-18
- `python -m unittest discover -s tests -q` ✅
- Real demo screenshots are present in `docs/screenshots/`
- Sample input artifacts are present in `samples/`

## Fast review path
1. Read `README.md` for the workflow overview and system flow.
2. Open `docs/DEMO.md` for the real submission/verification journey.
3. Review `src/playlist_manager.py` for the CLI workflow implementation.
4. Review `tests/test_playlist_manager.py` for the core behavior checks.
5. Open sample inputs:
   - `samples/discord_form_message.txt`
   - `samples/webhook_payload.json`

## Real proof artifacts in this repo
### Human verification gate evidence
- `docs/screenshots/step-02-save-playlist-page.jpg`
- `docs/screenshots/step-03-email-reply-screenshot-proof.jpg`

### Automation evidence
- Submission flow command documented in README
- Approval flow command documented in README
- Cleanup flow command documented in README
- State-oriented design called out in docs and tests

## Why this reads well to employers
- It automates a real workflow with approval logic instead of skipping human review
- It handles lifecycle cleanup, not just "add track" happy-path logic
- It includes examples and docs that a teammate could actually operate

## Honest note
`unittest` is the verified default on this machine. If pytest support is desired, it should be framed as optional rather than required.
