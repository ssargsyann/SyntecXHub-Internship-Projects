"""Small, optional client for movie poster images from TMDb."""

from __future__ import annotations

from typing import Optional

import requests


TMDB_MOVIE_URL = "https://api.themoviedb.org/3/movie/{movie_id}"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500{poster_path}"


def fetch_poster_url(movie_id: int, api_key: str | None) -> Optional[str]:
    """Return a TMDb poster URL, or ``None`` when no poster is available.

    The app remains usable without a key: it simply shows its bundled fallback
    image instead of live posters.
    """
    if not api_key:
        return None

    try:
        response = requests.get(
            TMDB_MOVIE_URL.format(movie_id=movie_id),
            params={"api_key": api_key, "language": "en-US"},
            timeout=10,
        )
        response.raise_for_status()
        poster_path = response.json().get("poster_path")
        if poster_path:
            return TMDB_IMAGE_URL.format(poster_path=poster_path)
    except (requests.RequestException, ValueError):
        return None
    return None
