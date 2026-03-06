# Operations Runbook

## Commands

### Submit

```bash
python src/playlist_manager.py submit \
  --name "Artist Name" \
  --email "artist@example.com" \
  --track-url "https://open.spotify.com/track/..." \
  --playlist-url "https://open.spotify.com/playlist/..."
```

### Approve

```bash
python src/playlist_manager.py approve --email "artist@example.com"
```

### Cleanup

```bash
python src/playlist_manager.py cleanup
```

## Cron Recommendation

Run cleanup daily:

- `15 2 * * *` local timezone

## Troubleshooting

### `Missing SPOTIFY_CLIENT...`
Set required env vars:
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `SPOTIFY_REFRESH_TOKEN`

### `Only Spotify track URLs are accepted`
Submission included album/artist URL. Ask submitter for `open.spotify.com/track/...`.

### 403 from Spotify API
Check:
- playlist owner account matches OAuth account
- scopes include `playlist-modify-public` or `playlist-modify-private`
- playlist privacy and permission settings
