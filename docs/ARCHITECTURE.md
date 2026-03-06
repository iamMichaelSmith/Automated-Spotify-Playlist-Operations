# Architecture

## Components

- **Squarespace Form**: Frontdoor for playlist submissions
- **Zapier**: Routes submission events
- **Discord Channel (`#website-forms`)**: Structured event log for form messages
- **Playlist Manager (`src/playlist_manager.py`)**:
  - submit queueing
  - approval execution
  - timed cleanup
- **Spotify Web API**:
  - add track to playlist
  - remove track after 30-day window
- **State Storage**:
  - `state/spotify_playlist_submissions.csv`
  - `state/spotify_playlist_entries.json`

## Control Flow

1. New submission arrives from form/router.
2. Submission is validated (must be `open.spotify.com/track/...`).
3. Verification email is sent (outside this script in production route).
4. On approval, track is added in staggered position.
5. Daily cleanup removes tracks whose retention period expired.

## Positioning Strategy

The system inserts tracks at staggered positions to maintain natural listening flow:

- 18, 22, 26, 29, then +3 increments

## Failure Handling

- Invalid links are rejected early.
- Missing env credentials fail fast.
- Cleanup is idempotent for non-expired entries.

## Security

- OAuth credentials must be loaded from env/secret manager.
- No secrets committed to source control.
