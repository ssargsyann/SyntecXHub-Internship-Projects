from pathlib import Path

import pytest

from src.recommender import build_feature_matrix, build_feature_texts, load_movies, recommend_movies


DATA_PATH = Path(__file__).parents[1] / "data" / "movies.csv"


def test_catalogue_loads_and_has_expected_columns():
    movies = load_movies(DATA_PATH)

    assert len(movies) >= 4_800
    assert {"movie_id", "title", "genres", "selection_label"}.issubset(movies.columns)
    assert movies["selection_label"].is_unique


def test_recommendations_exclude_the_selected_movie():
    movies = load_movies(DATA_PATH)
    inception_index = movies.index[movies["title"] == "Inception"][0]
    feature_matrix = build_feature_matrix(build_feature_texts(movies))
    recommendations = recommend_movies(
        movies, inception_index, top_n=5, feature_matrix=feature_matrix
    )

    assert len(recommendations) == 5
    assert "Inception" not in recommendations["title"].tolist()


def test_unknown_movie_has_a_clear_error():
    movies = load_movies(DATA_PATH)

    with pytest.raises(ValueError, match="Movie not found"):
        recommend_movies(movies, "A Movie That Does Not Exist")
