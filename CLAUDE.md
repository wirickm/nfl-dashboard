# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run nfl_streamlit.py
```

There are no tests or linting configured. Streamlit defaults to `localhost:8501`.

## Architecture

This is a single-file Streamlit app (`nfl_streamlit.py`) with a flat, procedural structure:

1. **Data loading** (`load_data()`): Hits the GitHub API for the latest `nflverse/nflverse-data` release, downloads the `play_by_play_2024` CSV/Parquet asset, and returns a DataFrame. Caching (`@st.cache_data`) is currently commented out.

2. **UI filtering**: Two `st.selectbox` widgets let the user pick a week then a game (game IDs are formatted as "Home vs Away").

3. **Visualization**: Two matplotlib figures are built — one for possession-based WP (`home_wp`/`away_wp`/`wpa`) and one for Vegas WP (`vegas_home_wp`/`vegas_wp`/`vegas_wpa`). Only the first figure is rendered via `st.pyplot()`; the second `st.pyplot(fig2)` call is commented out.

## Key Data Details

- Source: [NFLverse](https://github.com/nflverse/nflverse-data) play-by-play data (~180 columns), filtered down to 12 WP-related columns.
- The Vegas WP chart exists in the code but is disabled — enable by uncommenting `st.pyplot(fig2)` near line 136.
- `index.html` is a standalone exploratory page (not integrated with the Streamlit app) that fetches the NFLverse GitHub release JSON directly.
