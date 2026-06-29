# nfl-dashboard
NFL Win Probability Dashboard
This interactive dashboard tracks real-time win probabilities for NFL games. Select a game from the dropdown menu to see the possession-based win probabilities (blue) and defending team probabilities (red) throughout the game. The green bars below show Win Probability Added (WPA) by each play. The favored team and their win probability are displayed at the top. This tool offers insights into how in-game events impact each team's chances of winning.

## Setup and Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the dashboard:

```bash
streamlit run nfl_streamlit.py
```

> **Note:** The season is hardcoded to 2024. Play-by-play data is downloaded automatically from the [nflverse](https://github.com/nflverse/nflverse-data) releases on first run.
