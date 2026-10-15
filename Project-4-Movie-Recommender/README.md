# 🎬 Movie Match — Movie Recommender System

An interactive Streamlit web app that recommends five similar movies based on genres, keywords, and plot summaries. Select a film, press **Show recommendations**, and discover your next watch.

## Live demo

Open the deployed app: [Movie Match](https://movie-match-ssargsyann-2026.streamlit.app)

## Features

- Content-based recommendation engine using TF-IDF and cosine similarity
- Interactive Streamlit interface with 4,803 bundled movies
- Five recommendations for every selected film
- Real movie posters through the TMDb API
- Safe secret management: API keys are never committed to GitHub
- Automated test workflow with GitHub Actions

## Project structure

```text
Project-4-Movie-Recommender/
├── .github/workflows/ci.yml       # GitHub Actions test workflow
├── .streamlit/
│   ├── config.toml                # Streamlit theme and server settings
│   └── secrets.toml.example       # Safe template for a local API key
├── assets/poster-placeholder.svg  # Fallback image without a TMDb key
├── data/movies.csv                # Bundled movie catalogue
├── src/
│   ├── recommender.py             # Recommendation algorithm
│   └── tmdb.py                    # TMDb poster client
├── tests/test_recommender.py      # Automated tests
├── app.py                         # Application entry point
├── requirements.txt               # Python packages
└── README.md
```

## Run locally in VS Code (Windows)

Open the `Project-4-Movie-Recommender` folder in VS Code. Then open **Terminal → New Terminal** and run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) if the browser does not open automatically. Stop the local server with `Ctrl + C`.

## Configure TMDb posters locally (optional)

The online app already has its TMDb key configured securely in Streamlit Community Cloud. For local poster images, create a new file named `.streamlit/secrets.toml` and add your own **API Key (v3 auth)**:

```toml
TMDB_API_KEY = "your-tmdb-v3-api-key"
```

Do not use the TMDb **API Read Access Token** for this project. Do not commit `secrets.toml` or share its value. The file is ignored by `.gitignore`.

## Run tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## How recommendations work

The app combines each movie's genres, keywords, and plot summary into a text profile. It converts those profiles into TF-IDF vectors and uses cosine similarity to find the five closest matches. The TF-IDF matrix is cached so the 4,803-film catalogue remains responsive after the first load.

## Dataset

The bundled catalogue contains 4,803 entries from the [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata). It is a static dataset snapshot used for this educational project.

## Update the deployed app

This project lives inside the `SyntecXHub-Internship-Projects` repository. After changing code, run these commands from the repository root:

```powershell
git add Project-4-Movie-Recommender
git commit -m "Update Movie Recommender"
git push origin main
```

Streamlit Community Cloud automatically redeploys the app after changes are pushed to `main`.

## Deployment settings

| Setting | Value |
| --- | --- |
| Repository | `ssargsyann/SyntecXHub-Internship-Projects` |
| Branch | `main` |
| Main file | `Project-4-Movie-Recommender/app.py` |
| Hosting | Streamlit Community Cloud |

## Attribution

This product uses the TMDB API but is not endorsed or certified by TMDB.
