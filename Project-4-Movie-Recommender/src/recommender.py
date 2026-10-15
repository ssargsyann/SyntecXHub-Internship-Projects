"""Content-based movie recommendation utilities."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


REQUIRED_COLUMNS = {
    "movie_id",
    "title",
    "year",
    "genres",
    "keywords",
    "overview",
    "rating",
}


def load_movies(csv_path: str | Path) -> pd.DataFrame:
    """Load and validate the bundled movie catalogue."""
    movies = pd.read_csv(csv_path)
    missing = REQUIRED_COLUMNS.difference(movies.columns)
    if missing:
        missing_text = ", ".join(sorted(missing))
        raise ValueError(f"Movie catalogue is missing required columns: {missing_text}")

    if movies["title"].duplicated().any():
        raise ValueError("Movie catalogue contains duplicate movie titles.")

    return movies.fillna("")


def recommend_movies(movies: pd.DataFrame, selected_title: str, top_n: int = 5) -> pd.DataFrame:
    """Return the closest content-based matches for a selected movie.

    The score compares genre, keywords, and the short plot description with a
    TF-IDF/cosine-similarity model. A small rating tie-breaker keeps results
    useful when several movies have very similar descriptions.
    """
    matches = movies.index[movies["title"] == selected_title].tolist()
    if not matches:
        raise ValueError(f"Movie not found in catalogue: {selected_title}")
    if top_n < 1:
        raise ValueError("top_n must be at least 1")

    content = (
        movies["genres"].astype(str)
        + " "
        + movies["keywords"].astype(str)
        + " "
        + movies["overview"].astype(str)
    )
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    vectors = vectorizer.fit_transform(content)
    selected_position = movies.index.get_loc(matches[0])
    scores = linear_kernel(vectors[selected_position], vectors).ravel()

    ranked = movies.copy()
    ranked["_similarity"] = scores
    ranked = ranked.drop(index=matches[0])
    ranked = ranked.sort_values(
        ["_similarity", "rating"], ascending=[False, False], kind="stable"
    )
    return ranked.head(top_n).drop(columns="_similarity")
