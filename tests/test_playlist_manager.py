import unittest

from src.playlist_manager import parse_spotify_id, next_playlist_insert_position


class PlaylistManagerTests(unittest.TestCase):
    def test_parse_track(self):
        url = "https://open.spotify.com/track/0qGusnDxYospgRJ9w7UUkz?si=abc"
        self.assertEqual(parse_spotify_id(url, "track"), "0qGusnDxYospgRJ9w7UUkz")

    def test_stagger_positions(self):
        entries = []
        pid = "abc"
        self.assertEqual(next_playlist_insert_position(entries, pid), 18)

        entries = [{"status": "active", "playlist_id": pid}]
        self.assertEqual(next_playlist_insert_position(entries, pid), 22)

        entries = [{"status": "active", "playlist_id": pid} for _ in range(4)]
        self.assertEqual(next_playlist_insert_position(entries, pid), 32)


if __name__ == "__main__":
    unittest.main()
