# 🎬 Movie Match

A small, polished **Streamlit** movie recommender that is ready to open in VS Code and upload to GitHub. Select a movie and receive five recommendations based on genre, keywords, and plot summary.

The project works immediately with the included catalogue. Adding your own free TMDb API key is optional, but enables real poster images.

## Features

- Content-based recommendations using TF-IDF and cosine similarity
- Responsive Streamlit interface
- Bundled catalogue of popular films, so no model `.pkl` files are required
- Optional TMDb poster integration with safe secret handling
- Tests and GitHub Actions workflow included
- No API key is committed to the repository

## Project structure

```text
movie-recommender/
├── .github/workflows/ci.yml       # GitHub test automation
├── .streamlit/
│   ├── config.toml                # App appearance settings
│   └── secrets.toml.example       # Safe secret template
├── assets/poster-placeholder.svg  # Image used without a TMDb key
├── data/movies.csv                # Built-in movie catalogue
├── src/
│   ├── recommender.py             # Recommendation algorithm
│   └── tmdb.py                    # Optional poster client
├── tests/test_recommender.py      # Automated tests
├── app.py                         # Application entry point
├── requirements.txt               # Python dependencies
└── README.md
```

## Run locally in VS Code (Windows)

1. Open the `movie-recommender` folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install the packages:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Start the website:

   ```powershell
   streamlit run app.py
   ```

6. Your browser should open automatically. If it does not, open **http://localhost:8501**.

To stop the site, return to the VS Code terminal and press `Ctrl + C`.

## Enable real TMDb posters (optional)

1. Create a free account at [TMDb](https://www.themoviedb.org/).
2. Create a **v3 API key** from the API section of the account settings.
3. In VS Code, copy `.streamlit/secrets.toml.example` and rename the copied file to `secrets.toml`.
4. Replace `paste-your-tmdb-v3-api-key-here` with your key.
5. Restart `streamlit run app.py`.

`secrets.toml` is already ignored by Git, so your key will not be uploaded.

## Test the project

```powershell
pytest -q
```

## Upload to GitHub

Create an empty repository on GitHub, then run these commands in the VS Code terminal from the project folder. Replace the URL with your repository URL.

```powershell
git init
git add .
git commit -m "Initial Movie Match app"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/movie-recommender.git
git push -u origin main
```

## Publish online with Streamlit Community Cloud (optional)

1. Push the project to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
3. Click **Create app**, choose this repository, branch `main`, and file `app.py`.
4. In **Advanced settings → Secrets**, add:

   ```toml
   TMDB_API_KEY = "your-real-key"
   ```

5. Click **Deploy**. Streamlit will provide a public web address.

## Notes

The original code used `st.beta_columns`, which is no longer available. This project uses the current `st.columns` API instead.
