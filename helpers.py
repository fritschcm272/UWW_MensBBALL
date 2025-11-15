import numpy as np
import pandas as pd
import glob
import os
import helpers
import re
from typing import Dict, List

agg_dict = {
        'DURATION_SECONDS': 'sum',
        'AWAY_POINTS': 'sum',
        'HOME_POINTS': 'sum',
        'IS_END_OF_POSSESSION': 'sum',
        'GAME_ID': 'nunique' 
    }



AWAY_TEAM_NAME = "Wis.-Whitewater"
HOME_TEAM_NAME = "Ripon"

# Define the columns to keep for the focused analysis 
kept_cols = ['LINEUP', 'POSSESSIONS', 'Points For', 'Points Against', 'Plus/Minus', 'Offensive Rating', 'Defensive Rating', 'Net Rating']

def load_data_from_game_data():
    # --- 1. Data Loading and Aggregation ---


    # Assuming your CSV folder is named 'csv_data' and is in the same directory as the script.
    folder_name = 'Game_Data' 
    excluded_file_name = "Scouting.csv"
    
    # Get the current working directory (where the script is located)
    current_dir = os.getcwd() 
    # Create the full path to the folder
    path = os.path.join(current_dir, folder_name)
    
    # Use glob to find all files ending with .csv in the specified path
    all_files = glob.glob(os.path.join(path, "*.csv"))
    
    # 2. Filter the list to exclude the specified file name
    all_files = [
        file 
        for file in all_files 
        if os.path.basename(file) != excluded_file_name
    ]
    
    # --- Loading and Concatenating Data ---
    
    # Create a list to hold the individual DataFrames
    df_list = []
    
    print(f"--- Loading CSVs from: {path} ---")
    
    # Loop through the list of file paths
    for filename in all_files:
        # Read the file into a pandas DataFrame
        try:
            df = pd.read_csv(filename, index_col=None, header=0)
            df_list.append(df)
            print(f"Loaded: {os.path.basename(filename)}")
        except Exception as e:
            print(f"Error loading {os.path.basename(filename)}: {e}")
    
    # Concatenate all DataFrames in the list into one single DataFrame
    if df_list:
        combined_df = pd.concat(df_list, axis=0, ignore_index=True)
        combined_df = combined_df[~combined_df['Game'].isnull()]
    
        # 📌 NEW: Create a unique game identifier if GAME_ID doesn't exist.
        # Assuming 'AWAY_TEAM_NAME' and 'HOME_TEAM_NAME' columns might define the game.
        # If your CSVs have a proper 'GAME_ID' column, use that instead.
        if 'GAME_ID' not in combined_df.columns:
            # Create a simple unique identifier based on the file name/path
            # NOTE: If your raw data already has a unique 'Game ID', use that column!
            combined_df['GAME_ID'] = combined_df['AwayTeam'] + ' vs ' + combined_df['HomeTeam']
        
        # 📌 NEW: Get all unique game IDs for the filter
        ALL_GAME_IDS = sorted(combined_df['GAME_ID'].unique().tolist())
        
        print("\n--- Combined DataFrame Info ---")
        print(combined_df.info())
        print("\n--- First 5 rows of Combined Data ---")
        print(combined_df.head())
    else:
        print("\nNo CSV files found or loaded.")

    return combined_df



def time_to_seconds(time_str):
    """Converts MM:SS time string to total seconds."""
    if pd.isna(time_str) or not isinstance(time_str, str):
        return 0
    try:
        m, s = map(int, time_str.split(':'))
        return m * 60 + s
    except ValueError:
        return 0

def lineup_html_formatter(lineup_list):
    """Converts the list of players into an HTML string with <br> breaks."""
    if isinstance(lineup_list, list):
        return '<br>'.join(lineup_list)
    return str(lineup_list)

def seconds_to_time(seconds):
    """Converts total seconds back to MM:SS format."""
    seconds = int(round(seconds))
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


# Function to render the DataFrame with custom HTML line breaks
def display_formatted_lineups(df, title):
    print(f"\n{title}")
    # Use Styler to apply the custom HTML formatter only to the 'LINEUP' column
    styled_df = df[kept_cols].style.format({
        'LINEUP': lineup_html_formatter
    })
    display(styled_df)


def calculate_lineup_ratings(combined_df, team_name, opponent_name, group_dict, agg_dict):
    """
    Performs line-up aggregation and advanced rating calculations for a single team.
    (Replaces AWAY/HOME Lineup Aggregation duplication)
    """
    team_prefix = 'AWAY' if team_name == AWAY_TEAM_NAME else 'HOME'
    opp_prefix = 'HOME' if team_name == AWAY_TEAM_NAME else 'AWAY'
    
    roster_col = f'{team_prefix}_ROSTER_ON_COURT'
    points_for_col = f'{team_prefix}_POINTS'
    points_against_col = f'{opp_prefix}_POINTS'

    # --- THE FIX: Standardize the lineup string BEFORE grouping ---
    # Convert the comma-separated string of players into a list, sort the list,
    # and rejoin it as a new, standardized string key (e.g., "A,B,C,D,E").
    def standardize_lineup(lineup_str):
        if pd.isna(lineup_str) or not isinstance(lineup_str, str):
            return ""
        # Split, sort the player names alphabetically, and rejoin with a comma
        # This ensures 'A,B' and 'B,A' are both grouped as 'A,B'
        return ','.join(sorted(lineup_str.split(',')))

    # Apply the standardization to the roster column
    combined_df['LINEUP'] = combined_df[roster_col].apply(standardize_lineup)
    # -----------------------------------------------------------------

    # group_dict = ['STANDARDIZED_LINEUP']
    # 1. Aggregate Line-ups
    # Group by the new standardized column
    aggregated_data = combined_df.groupby(group_dict).agg(agg_dict).reset_index()
    
    # Split the standardized string back into a list for the final 'LINEUP' column
    # The list is already sorted alphabetically because of the standardization step above
    aggregated_data['LINEUP_LIST'] = aggregated_data['LINEUP'].str.split(',')
    
    # Filter for 5-man lineups
    aggregated_data['player_length'] = aggregated_data['LINEUP_LIST'].apply(len)
    aggregated_data = aggregated_data[aggregated_data['player_length'] == 5].sort_values(by='DURATION_SECONDS', ascending=False)
    aggregated_data = aggregated_data.rename(columns={'IS_END_OF_POSSESSION': 'POSSESSIONS'})
    aggregated_data['POSSESSIONS'] = pd.to_numeric(aggregated_data['POSSESSIONS'])
    
    # 2. Ratings calculations (rest of code is unchanged)
    aggregated_data['Points For Per 40 Mins'] = (aggregated_data[points_for_col] / aggregated_data['DURATION_SECONDS']) * 2400
    aggregated_data['Points Against Per 40 Mins'] = (aggregated_data[points_against_col] / aggregated_data['DURATION_SECONDS']) * 2400
    aggregated_data['Offensive Rating'] = np.where(aggregated_data['POSSESSIONS'] > 0,
    (aggregated_data[points_for_col] / aggregated_data['POSSESSIONS']) * 100,
    0.0
    )
    aggregated_data['Defensive Rating'] = np.where(
        aggregated_data['POSSESSIONS'] > 0,
        (aggregated_data[points_against_col] / aggregated_data['POSSESSIONS']) * 100,
        0.0
    )
    aggregated_data['Net Rating'] = aggregated_data['Offensive Rating'] - aggregated_data['Defensive Rating']


    # 3. ROUNDING & NAN/INF HANDLING
    rounding_cols = ['Points For Per 40 Mins', 'Points Against Per 40 Mins',
                     'Offensive Rating', 'Defensive Rating', 'Net Rating',
                     points_for_col, points_against_col]
                         
    aggregated_data[rounding_cols] = aggregated_data[rounding_cols].fillna(0).replace([np.inf, -np.inf], 0)
    # Note: I changed the rounding to use `.round(1)` for ratings, as rounding to 0 might lose too much precision, 
    # but I left your original `.round(0).astype(int)` for points/time stats.
    int_cols = [points_for_col, points_against_col, 'POSSESSIONS']
    aggregated_data[int_cols] = aggregated_data[int_cols].round(0).astype(int)
    
    float_cols = ['Points For Per 40 Mins', 'Points Against Per 40 Mins',
                  'Offensive Rating', 'Defensive Rating', 'Net Rating']
    aggregated_data[float_cols] = aggregated_data[float_cols].round(1)


    # 4. Final Formatting
    aggregated_data['AGGREGATED_TIME_MM:SS'] = aggregated_data['DURATION_SECONDS'].apply(seconds_to_time)
    final_results = aggregated_data.drop(columns=['DURATION_SECONDS', 'player_length', 'LINEUP']).rename(columns={
        'LINEUP_LIST': 'LINEUP', points_for_col: 'Points For', points_against_col: 'Points Against'
    })
    final_results['Plus/Minus'] = final_results['Points For'] - final_results['Points Against']

    # Rename the aggregated 'GAME_ID' to 'Games'
    final_results = final_results.rename(columns={'GAME_ID': 'Games'})
    
    final_results = final_results[group_dict+['AGGREGATED_TIME_MM:SS', 'POSSESSIONS', 'Points For', 'Points Against', 
                                   'Plus/Minus', 'Offensive Rating', 'Defensive Rating', 'Net Rating', 'Games',
                                   'Points For Per 40 Mins', 'Points Against Per 40 Mins']]

    return final_results
