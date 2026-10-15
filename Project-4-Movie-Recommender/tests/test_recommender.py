from pathlib import Path

import pytest

from src.recommender import load_movies, recommend_movies


DATA_PATH = Path(__file__).parents[1] / "data" / "movies.csv"


def test_catalogue_loads_and_has_expected_columns():
    movies = load_movies(DATA_PATH)

    assert len(movies) >= 20
    assert {"movie_id", "title", "genres"}.issubset(movies.columns)


def test_recommendations_exclude_the_selected_movie():
    movies = load_movies(DATA_PATH)
    recommendations = recommend_movies(movies, "Inception", top_n=5)

    assert len(recommendations) == 5
    assert "Inception" not in recommendations["title"].tolist()


def test_unknown_movie_has_a_clear_error():
    movies = load_movies(DATA_PATH)

    with pytest.raises(ValueError, match="Movie not found"):
        recommend_movies(movies, "A Movie That Does Not Exist")
