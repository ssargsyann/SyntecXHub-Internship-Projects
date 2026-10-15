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

    movies = movies.fillna("")
    if "selection_label" not in movies.columns:
        movies["selection_label"] = movies["title"] + " (" + movies["year"].astype(str) + ")"
    return movies


def build_feature_texts(movies: pd.DataFrame) -> tuple[str, ...]:
    """Combine the fields used to compare movies into one text per movie."""
    content = (
        movies["genres"].astype(str)
        + " "
        + movies["keywords"].astype(str)
        + " "
        + movies["overview"].astype(str)
    )
    return tuple(content)


def build_feature_matrix(feature_texts: tuple[str, ...]):
    """Create the sparse TF-IDF matrix once and reuse it for selections."""
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    return vectorizer.fit_transform(feature_texts)


def recommend_movies(
    movies: pd.DataFrame,
    selected_index: int | str,
    top_n: int = 5,
    feature_matrix=None,
) -> pd.DataFrame:
    """Return the closest content-based matches for the selected movie.

    A selection index keeps films with the same title unambiguous. Passing a
    title string remains supported for simple scripts and tests.
    """
    if isinstance(selected_index, str):
        matches = movies.index[movies["title"] == selected_index].tolist()
        if not matches:
            raise ValueError(f"Movie not found in catalogue: {selected_index}")
        selected_index = matches[0]
    elif selected_index not in movies.index:
        raise ValueError(f"Movie index not found in catalogue: {selected_index}")
    if top_n < 1:
        raise ValueError("top_n must be at least 1")

    if feature_matrix is None:
        feature_matrix = build_feature_matrix(build_feature_texts(movies))
    selected_position = movies.index.get_loc(selected_index)
    scores = linear_kernel(feature_matrix[selected_position], feature_matrix).ravel()

    ranked = movies.copy()
    ranked["_similarity"] = scores
    ranked = ranked.drop(index=selected_index)
    ranked = ranked.sort_values(
        ["_similarity", "rating"], ascending=[False, False], kind="stable"
    )
    return ranked.head(top_n).drop(columns="_similarity")
