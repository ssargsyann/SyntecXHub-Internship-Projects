"""Streamlit entry point for the Movie Recommender."""

from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

from src.recommender import load_movies, recommend_movies
from src.tmdb import fetch_poster_url


ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "movies.csv"
PLACEHOLDER_POSTER = ROOT / "assets" / "poster-placeholder.svg"


st.set_page_config(
    page_title="Movie Match | Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_data(show_spinner=False)
def get_movies():
    return load_movies(DATA_PATH)


@st.cache_data(ttl=60 * 60 * 24, show_spinner=False)
def get_poster(movie_id: int, api_key: str | None) -> str | None:
    return fetch_poster_url(movie_id, api_key)


def get_tmdb_api_key() -> str | None:
    """Read a key from local Streamlit secrets or an environment variable."""
    environment_key = os.getenv("TMDB_API_KEY")
    if environment_key:
        return environment_key
    try:
        return st.secrets.get("TMDB_API_KEY")
    except (FileNotFoundError, AttributeError):
        return None


def movie_label(row) -> str:
    return f"{row['title']} ({row['year']})"


st.markdown(
    """
    <style>
      .hero { padding: 1.2rem 0 0.7rem; }
      .hero h1 { margin-bottom: 0.15rem; }
      .movie-meta { color: #b9c2d0; font-size: 0.9rem; min-height: 2.7rem; }
      [data-testid="stImage"] img { border-radius: 12px; box-shadow: 0 12px 28px rgba(0,0,0,.30); }
    </style>
    """,
    unsafe_allow_html=True,
)

movies = get_movies()
api_key = get_tmdb_api_key()

st.markdown(
    """
    <div class="hero">
      <h1>🎬 Movie Match</h1>
      <p>Pick a film and discover five movies with a similar story, mood, or genre.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.subheader("About this app")
    st.write("Recommendations are calculated from genres, keywords, and plot summaries.")
    if api_key:
        st.success("TMDb posters are enabled.")
    else:
        st.info("Add a TMDb API key to show live movie posters.")

selected_index = st.selectbox(
    "Type or select a movie",
    options=movies.index.tolist(),
    format_func=lambda index: movie_label(movies.loc[index]),
)
selected_movie = movies.loc[selected_index]

info_left, info_right = st.columns([1, 3])
with info_left:
    st.metric("Rating", f"{selected_movie['rating']} / 10")
with info_right:
    st.caption(f"{selected_movie['year']} · {selected_movie['genres']}")
    st.write(selected_movie["overview"])

if st.button("Show recommendations", type="primary", use_container_width=True):
    with st.spinner("Finding your next movie night pick…"):
        recommendations = recommend_movies(movies, selected_movie["title"], top_n=5)

    st.subheader("You may also like")
    columns = st.columns(5)
    for column, (_, movie) in zip(columns, recommendations.iterrows()):
        with column:
            poster_url = get_poster(int(movie["movie_id"]), api_key)
            st.image(poster_url or str(PLACEHOLDER_POSTER), use_container_width=True)
            st.markdown(f"**{movie['title']}**")
            st.markdown(
                f"<div class='movie-meta'>{movie['year']} · {movie['genres']}<br>⭐ {movie['rating']}/10</div>",
                unsafe_allow_html=True,
            )

st.divider()
st.caption(
    "Built with Streamlit. Movie metadata comes from the included demo catalogue; "
    "poster images are provided by TMDb when you configure your own API key."
)
