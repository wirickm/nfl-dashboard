import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import time

# Streamlit App Title
st.title('NFL Win Probability Dashboard')

# Download and load the data
#@st.cache_data
def load_data():
    github_api_url = 'https://api.github.com/repos/nflverse/nflverse-data/releases/latest'
    response = requests.get(github_api_url)
    data = response.json()

    for asset in data['assets']:
        if 'play_by_play_2024' in asset['name']:
            download_url = asset['browser_download_url']
            break

    response = requests.get(download_url)
    filename = asset['name']
    with open(filename, 'wb') as f:
        f.write(response.content)

    if filename.endswith('.csv'):
        return pd.read_csv(filename, low_memory=False)
    elif filename.endswith('.parquet'):
        return pd.read_parquet(filename)

# Load the play-by-play data
play_by_play_data = load_data()

# Select a game to visualize
game_id = st.selectbox('Select a Game ID', play_by_play_data['game_id'].unique())
selected_week = st.selectbox('Select a Week', play_by_play_data['week'].unique())

# Filter relevant columns for win probability
wp_columns = ['game_id', 'play_id', 'home_team', 'away_team','home_wp', 'away_wp', 'wpa', 'posteam', 'defteam', 'vegas_wp', 'vegas_home_wp', 'vegas_wpa']
filtered_wp_data = play_by_play_data[wp_columns]

# Filter the data for the selected game
game_data = filtered_wp_data[filtered_wp_data['game_id'] == game_id]

# Sort the game data by play_id to ensure chronological order
game_data = game_data.sort_values(by='play_id')

# Get the last play of the game to determine the final win probabilities
final_home_wp = game_data['home_wp'].iloc[-1]
final_away_wp = game_data['away_wp'].iloc[-1]
home_team = game_data['home_team'].iloc[-1]
away_team = game_data['away_team'].iloc[-1]

# Determine which team is currently favored to win
if final_home_wp > final_away_wp:
    favored_team = home_team
    favored_prob = final_home_wp
else:
    favored_team = away_team
    favored_prob = final_away_wp

# Plot the win probability for the home and away teams
fig, ax = plt.subplots(figsize=(12, 6))

# Plot 'home_wp' and 'away_wp' over the course of the game with thicker lines
ax.plot(game_data['play_id'], game_data['home_wp'], label='Home Team Win Probability', color='blue', linewidth=2)
ax.plot(game_data['play_id'], game_data['away_wp'], label='Away Team Win Probability', color='red', linestyle='--', linewidth=2)

# Highlight the start and end win probabilities with thicker markers
ax.scatter(game_data['play_id'].iloc[0], game_data['home_wp'].iloc[0], color='blue', label='Start of Game (Home WP)', zorder=5, s=100)
ax.scatter(game_data['play_id'].iloc[-1], game_data['home_wp'].iloc[-1], color='blue', label='End of Game (Home WP)', zorder=5, s=100)

ax.scatter(game_data['play_id'].iloc[0], game_data['away_wp'].iloc[0], color='red', label='Start of Game (Away WP)', zorder=5, s=100)
ax.scatter(game_data['play_id'].iloc[-1], game_data['away_wp'].iloc[-1], color='red', label='End of Game (Away WP)', zorder=5, s=100)

# Overlay the 'wpa' (win probability added) with larger, more visible bars
ax.bar(game_data['play_id'], game_data['wpa'], label='Win Probability Added (WPA)', alpha=0.6, color='green', width=15)

# Customize the plot
ax.set_title(f'Win Probability and WPA Over Time for Game {game_id}', fontsize=14)
ax.set_xlabel('Play ID', fontsize=12)
ax.set_ylabel('Win Probability / WPA', fontsize=12)

# Annotate the currently favored team and their win probability at the top left
ax.annotate(
    f'Favored Team: {favored_team}\nWin Probability: {favored_prob:.2%}', 
    xy=(0.02, 0.90), xycoords='axes fraction', fontsize=12,
    bbox=dict(facecolor='white', alpha=0.6, edgecolor='black')
)

# Move the legend to the bottom left
ax.legend(loc='lower left', fontsize=10)

# Remove the gridlines
ax.grid(False)

# Display the plot in Streamlit
st.pyplot(fig)

# Now, for the Vegas win probability plot
fig2, ax2 = plt.subplots(figsize=(12, 6))

# Plot 'vegas_wp' and 'vegas_home_wp' over the course of the game with thicker lines
ax2.plot(game_data['play_id'], game_data['vegas_home_wp'], label='Vegas Home Team Win Probability', color='blue', linewidth=2)
ax2.plot(game_data['play_id'], game_data['vegas_wp'], label='Vegas Away Team Win Probability', color='red', linestyle='--', linewidth=2)

# Highlight the start and end win probabilities with thicker markers
ax2.scatter(game_data['play_id'].iloc[0], game_data['vegas_home_wp'].iloc[0], color='blue', label='Start of Game (Vegas Home WP)', zorder=5, s=100)
ax2.scatter(game_data['play_id'].iloc[-1], game_data['vegas_home_wp'].iloc[-1], color='blue', label='End of Game (Vegas Home WP)', zorder=5, s=100)

ax2.scatter(game_data['play_id'].iloc[0], game_data['vegas_wp'].iloc[0], color='red', label='Start of Game (Vegas Away WP)', zorder=5, s=100)
ax2.scatter(game_data['play_id'].iloc[-1], game_data['vegas_wp'].iloc[-1], color='red', label='End of Game (Vegas Away WP)', zorder=5, s=100)

# Overlay the 'vegas_wpa' (Vegas win probability added) with larger, more visible bars
ax2.bar(game_data['play_id'], game_data['vegas_wpa'], label='Vegas Win Probability Added (Vegas WPA)', alpha=0.6, color='purple', width=15)

# Customize the plot
ax2.set_title(f'Vegas Win Probability and WPA Over Time for Game {game_id}', fontsize=14)
ax2.set_xlabel('Play ID', fontsize=12)
ax2.set_ylabel('Vegas Win Probability / WPA', fontsize=12)

# Move the legend to the bottom left
ax2.legend(loc='lower left', fontsize=10)

# Remove the gridlines
ax2.grid(False)

# Display the second plot in Streamlit
#st.pyplot(fig2)

st.markdown("""
### About this Dashboard
This interactive dashboard tracks **real-time win probabilities** for NFL games. Select a game from the dropdown menu to view the **possession-based win probabilities** (blue) and **defending team probabilities** (red) over time. The **green bars** indicate **Win Probability Added (WPA)** for each play. The favored team and their win probability are displayed at the top of the chart. This tool helps analyze how each play impacts a team's chances of winning throughout the game.

#### What is Win Probability (WP)?
**Win Probability (WP)** estimates the chance that a team will win the game at any given moment. It considers:
- Current score
- Time remaining
- Down and distance
- Field position (yard line)
- Which team has possession of the ball

WP is calculated based on historical NFL data, using patterns from past games to predict the outcome. The model updates in real-time, showing fans how the likelihood of each team winning changes as the game progresses.

#### Simplified Formula for WP:
The formula for WP typically looks like:
```
WP = f(score differential, time remaining, down, distance, yard line, possession)
```

#### What is Win Probability Added (WPA)?
**Win Probability Added (WPA)** measures how much each play changes a team's chances of winning. It shows the difference in win probability before and after a play.

#### Simplified Formula for WPA:
```
WPA = WP(after) - WP(before)
```

WPA highlights the most important plays in the game by showing how much impact a single play had on the team's chances of winning.

#### What is XGBoost?
**XGBoost (Extreme Gradient Boosting)** is a machine learning algorithm often used for predicting outcomes. It works by creating decision trees that build on each other to improve accuracy. In sports analytics, XGBoost is valuable for improving predictions, such as win probabilities, by learning from game features.

#### Simplified Formula for XGBoost:
XGBoost aims to minimize an objective function, which typically looks like:
```
Objective = Loss Function + (sum of Regularization Terms)
```

The **Loss Function** measures prediction errors, while **Regularization** helps prevent overfitting by keeping the model simple.
""")
#
