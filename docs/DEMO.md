# Demo Setup

## Live Form Demo

Squarespace page:
- https://www.blakmarigold.com/playlist-submission

## Expected Submission Fields

- Name
- Email
- Spotify Song URL
- Optional metadata (genre, socials)

## Zapier Routing Pattern

1. Trigger: Squarespace Form Submission
2. Action: Post message to Discord `#website-forms`
3. Action (optional): Send backup email copy
4. Poller consumes new messages and calls submit flow

## Manual Test Walkthrough

1. Submit valid Spotify track URL via form.
2. Confirm row is queued in `state/spotify_playlist_submissions.csv`.
3. Run approval:
   - `python src/playlist_manager.py approve --email "artist@example.com"`
4. Verify insertion position in output.
5. Force cleanup test (with edited date) and run:
   - `python src/playlist_manager.py cleanup`
