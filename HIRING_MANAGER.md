# Hiring Manager Notes (Automated-Spotify-Playlist-Operations)

## Role Alignment
Strong fit for backend automation, junior platform, and AI-adjacent ops roles where reliability matters more than flashy UI.

## What This Project Shows
- Practical workflow automation tied to a real music-ops process
- External API/OAuth handling with repeatable state transitions
- Human-in-the-loop approval design instead of unsafe blind automation
- Cleanup lifecycle logic and operational documentation

## Verification Snapshot
- Last verified local test run: 2026-03-18
- Verified on machine: Windows (PowerShell)
- Default test runner: `python -m unittest discover -s tests -q`
- CI expectation: GitHub Actions runs the same `unittest` command for consistency

## Suggested Interview Talking Points
1. Why `unittest` was chosen as the default runner for zero-dependency portability
2. How approval gates and 30-day cleanup reduce operational risk
3. How you would extend this into a webhook/API service with retries and observability
