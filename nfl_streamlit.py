# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 13:21:40 2024
@author: wirickm
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import time

# Streamlit App Title
st.title('NFL Win Probability Dashboard')

# Download and load the data
@st.cache_data
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

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 13:21:40 2024

@author: MichaelJWirickJr
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import time

# Streamlit App Title
st.title('NFL Win Probability Dashboard')

# Download and load the data
@st.cache_data
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

# Run the loop to reload data every 60 seconds
while True:
    # Load the play-by-play data
    play_by_play_data = load_data()

    # Select a game to visualize
    game_id = st.selectbox('Select a Game ID', play_by_play_data['game_id'].unique())

    # Filter relevant columns for win probability
    wp_columns = ['game_id', 'play_id', 'wp', 'def_wp', 'wpa', 'posteam', 'defteam']
    filtered_wp_data = play_by_play_data[wp_columns]

    # Filter the data for the selected game
    game_data = filtered_wp_data[filtered_wp_data['game_id'] == game_id]

    # Sort the game data by play_id to ensure chronological order
    game_data = game_data.sort_values(by='play_id')

    # Get the last play of the game to determine the final win probabilities
    final_wp = game_data['wp'].iloc[-1]
    final_def_wp = game_data['def_wp'].iloc[-1]
    posteam = game_data['posteam'].iloc[-1]
    defteam = game_data['defteam'].iloc[-1]

    # Determine which team is currently favored to win
    if final_wp > final_def_wp:
        favored_team = posteam
        favored_prob = final_wp
    else:
        favored_team = defteam
        favored_prob = final_def_wp

    # Plot the win probability for the possessing team ('wp') and defending team ('def_wp')
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot 'wp' and 'def_wp' over the course of the game with thicker lines
    ax.plot(game_data['play_id'], game_data['wp'], label='Possessing Team Win Probability', color='blue', linewidth=2)
    ax.plot(game_data['play_id'], game_data['def_wp'], label='Defending Team Win Probability', color='red', linestyle='--', linewidth=2)

    # Highlight the start and end win probabilities with thicker markers
    ax.scatter(game_data['play_id'].iloc[0], game_data['wp'].iloc[0], color='blue', label='Start of Game (WP)', zorder=5, s=100)
    ax.scatter(game_data['play_id'].iloc[-1], game_data['wp'].iloc[-1], color='blue', label='End of Game (WP)', zorder=5, s=100)

    ax.scatter(game_data['play_id'].iloc[0], game_data['def_wp'].iloc[0], color='red', label='Start of Game (Def WP)', zorder=5, s=100)
    ax.scatter(game_data['play_id'].iloc[-1], game_data['def_wp'].iloc[-1], color='red', label='End of Game (Def WP)', zorder=5, s=100)

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

    # Add a description below the graph
    st.markdown("""
    ### About this Dashboard
    This interactive dashboard tracks **real-time win probabilities** for NFL games. Select a game from the dropdown menu to view the **possession-based win probabilities** (blue) and **defending team probabilities** (red) over time. The **green bars** indicate **Win Probability Added (WPA)** for each play. The favored team and their win probability are displayed at the top of the chart. This tool helps analyze how each play impacts a team's chances of winning throughout the game.
    """)

    # Sleep for 60 seconds before refreshing the data
    time.sleep(60)
