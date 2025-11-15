import pandas as pd
import glob
import os
import numpy as np
import helpers
import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib.backends.backend_pdf import PdfPages




# --- Configuration ---
# Assuming your CSV folder is named 'csv_data' and is in the same directory as the script.
folder_name = 'Game_Data' 
# Get the current working directory (where the script is located)
current_dir = os.getcwd() 
# Create the full path to the folder
path = os.path.join(current_dir, folder_name)

# Use glob to find all files ending with .csv in the specified path
all_files = glob.glob(os.path.join(path, "*.csv"))

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
    
    print("\n--- Combined DataFrame Info ---")
    print(combined_df.info())
    print("\n--- First 5 rows of Combined Data ---")
    print(combined_df.head())
else:
    print("\nNo CSV files found or loaded.")


# --- 1. Data Loading and Aggregation ---

# # Specify the path to the directory containing your CSV files
# csv_directory_path = 'Game_Data\\'

# # Use glob to find all files ending with .csv in the specified directory
# csv_files = glob.glob(os.path.join(csv_directory_path, "*.csv"))



# # Construct the relative path to the CSV file
# csv_files = os.path.join(script_dir, 'Game_Data', '*.csv')
# print(csv_files)

# Initialize an empty list to store the DataFrames
list_of_dfs = []

# Loop through files to read them into the list
for file_path in csv_files:
    try:
        df = pd.read_csv(file_path)
        list_of_dfs.append(df)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        
# Combine all DataFrames
if list_of_dfs:
    combined_df = pd.concat(list_of_dfs, ignore_index=True)
else:
    combined_df = pd.DataFrame()

# Define ALL potential columns for grouping based on your provided scouted roles
ALL_GROUPING_COLS = [
    "Driver/Shooter", 
    "Post Scorer", 
    "Playmaker", 
    "Mid-Range Specialist", 
    "Spot-Up Shooter", 
    "Rebounder", 
    "Not Scouted"
] 

# Loop through the grouping columns and convert their values to strings
if not combined_df.empty:
    for col in ALL_GROUPING_COLS:
        if col in combined_df.columns:
            # Convert values to strings
            combined_df[col] = combined_df[col].astype(str)


agg_dict = {
        'DURATION_SECONDS': 'sum',
        'AWAY_POINTS': 'sum',
        'HOME_POINTS': 'sum',
        'IS_END_OF_POSSESSION': 'sum'
    }

AWAY_TEAM_NAME = "Wis.-Whitewater"
HOME_TEAM_NAME = "Ripon"

# Filter out 'LINEUP' if it exists here, as it is always included
ALL_GROUPING_COLS = [col for col in ALL_GROUPING_COLS if col != 'LINEUP'] 

# --- 2. Streamlit Configuration and Dynamic Grouping ---

st.set_page_config(page_title="Lineup Dashboard", layout="wide")

st.title("📈 Lineup Analysis Dashboard")
st.caption("Consistent sections, interactive filters, CSV/PNG downloads, and a polished PDF report.")




# Define all columns that should be kept in the final results dataframe
RATING_COLS = ['POSSESSIONS', 'Points For', 'Points Against',
               'Plus/Minus', 'Offensive Rating', 'Defensive Rating', 'Net Rating']

# --- CORE DATA CALCULATION ---
if combined_df.empty:
    st.error("🚨 Error: No data available. Please ensure CSV files exist in the 'Game_Data\\' directory.")
    away_final_results_top = pd.DataFrame()
    away_final_results_explorer = pd.DataFrame()
else:
    # 1. Calculate Results for TOP 3 and PDF (LINEUP ONLY)
    group_dict_top = ['LINEUP']
    kept_cols_top = ['LINEUP'] + RATING_COLS
    away_final_results_top = helpers.calculate_lineup_ratings(combined_df, AWAY_TEAM_NAME, HOME_TEAM_NAME, group_dict_top, agg_dict)



# --- 3. Streamlit Helper Functions & Data Preparation ---

# Function to reorder columns with 'LINEUP' and grouping context first
def reorder_lineup_first(df, group_cols):
    if 'LINEUP' in df.columns:
        # Create new list with 'LINEUP' and other group cols first, followed by rating cols
        cols = [col for col in group_cols if col in df.columns] + [col for col in df.columns if col not in group_cols]
        return df[cols]
    return df

def prepare_dataframe(df, cols, group_dict_used):
    if df.empty:
        return pd.DataFrame(columns=cols)
        
    df = df[[c for c in cols if c in df.columns]].copy()
    
    # Apply the column reorder function here
    return reorder_lineup_first(df, group_dict_used)

# --- Sort helpers (Top 3 functions) ---
def top3_by_possessions(df):
    return df.sort_values(by='POSSESSIONS', ascending=False).head(3)

def top3_by_plus_minus(df):
    return df.sort_values(by=['Plus/Minus', 'POSSESSIONS'], ascending=[False, False]).head(3)

def top3_by_net_rating(df):
    return df.sort_values(by=['Net Rating', 'POSSESSIONS'], ascending=[False, False]).head(3)

# --- PDF report generator (omitted for brevity, assume original function is here) ---
# NOTE: The implementation of generate_pdf_report remains unchanged
def generate_pdf_report(team_name, top_pos_df, top_pm_df, top_nr_df):
    buf = BytesIO()
    with PdfPages(buf) as pdf:
        
        # Title page
        fig_title = plt.figure(figsize=(8.5, 11))
        plt.text(0.5, 0.55, f"{team_name} Lineup Analysis Report",
                  ha="center", va="center", fontsize=24, weight="bold")
        plt.text(0.5, 0.45, "Top 3 by Possessions, Plus/Minus, Net Rating",
                  ha="center", va="center", fontsize=14)
        plt.axis("off")
        pdf.savefig(fig_title)
        plt.close(fig_title)
        
        # Function to add a single table section (using original logic)
        def add_table_section(title, df):
             if df.empty: return

             df_pdf = df.copy()
             if 'LINEUP' in df_pdf.columns and not df_pdf.empty and isinstance(df_pdf['LINEUP'].iloc[0], list):
                 df_pdf['LINEUP'] = df_pdf['LINEUP'].apply(lambda x: "\n".join(x))
             
             # Filter columns for the PDF table display 
             if "Possessions" in title:
                 display_cols = ['LINEUP', 'POSSESSIONS']
             elif "Plus/Minus" in title:
                 display_cols = ['LINEUP', 'POSSESSIONS', 'Points For', 'Points Against', 'Plus/Minus']
             elif "Net Rating" in title:
                 display_cols = ['LINEUP', 'POSSESSIONS', 'Offensive Rating', 'Defensive Rating', 'Net Rating']
                 
             df_pdf = df_pdf[[col for col in display_cols if col in df_pdf.columns]]

             fig_tbl = plt.figure(figsize=(8.5, 1.5 + len(df_pdf) * 0.3)) # Dynamic height
             plt.axis("off")
             tbl = plt.table(
                 cellText=df_pdf.values,
                 colLabels=df_pdf.columns.tolist(),
                 loc="center",
                 cellLoc="center"
             )
             tbl.auto_set_font_size(False)
             tbl.set_fontsize(10)
             tbl.scale(1, 1.2)
             plt.title(title, fontsize=14, y=0.9)
             pdf.savefig(fig_tbl, bbox_inches='tight')
             plt.close(fig_tbl)

        # Add tables to the PDF
        add_table_section("Top 3 Lineups by Possessions (Table)", top_pos_df)
        add_table_section("Top 3 Lineups by Plus/Minus (Table)", top_pm_df)
        add_table_section("Top 3 Lineups by Net Rating (Table)", top_nr_df)

    buf.seek(0)
    return buf.getvalue()

# --- 4. STREAMLIT APP DISPLAY ---

# Prepare base dataframe for TOP 3 (LINEUP ONLY)
df_base_top = prepare_dataframe(away_final_results_top, kept_cols_top, group_dict_top)

if not df_base_top.empty:
    # Get Top 3 DataFrames (derived from LINEUP ONLY results)
    top_possessions_list = top3_by_possessions(df_base_top)
    top_plus_minus_list = top3_by_plus_minus(df_base_top)
    top_net_rating_list = top3_by_net_rating(df_base_top)

    # --- Prepare Top 3 DataFrames for Streamlit Display ---
    def prepare_top3_display_df(df_list):
        df_display = df_list.copy()
        if 'LINEUP' in df_display.columns and not df_display.empty and isinstance(df_display['LINEUP'].iloc[0], list):
            df_display['LINEUP'] = df_display['LINEUP'].apply(lambda x: ", ".join(x))
        return df_display

    top_possessions_full = prepare_top3_display_df(top_possessions_list)
    top_plus_minus_full = prepare_top3_display_df(top_plus_minus_list)
    top_net_rating_full = prepare_top3_display_df(top_net_rating_list)
    
    # Top 3 display uses LINEUP column only, since it was calculated with LINEUP only
    POS_COLS = ['LINEUP', 'POSSESSIONS']
    top_possessions = top_possessions_full[[col for col in POS_COLS if col in top_possessions_full.columns]]

    PM_COLS = ['LINEUP', 'POSSESSIONS', 'Points For', 'Points Against', 'Plus/Minus']
    top_plus_minus = top_plus_minus_full[[col for col in PM_COLS if col in top_plus_minus_full.columns]]
    
    NR_COLS = ['LINEUP', 'POSSESSIONS', 'Offensive Rating', 'Defensive Rating', 'Net Rating']
    top_net_rating = top_net_rating_full[[col for col in NR_COLS if col in top_net_rating_full.columns]]
    
    # --- Section 1: Top 3 Lineups in Single Column (st.dataframe) ---
    st.markdown("---")
    st.header("🏆 Top 3 Lineup Analysis")
    
    st.subheader(f"Possessions")
    st.dataframe(top_possessions.style.format({'POSSESSIONS': '{:,}'}), 
                  use_container_width=True, hide_index=True)
    
    st.subheader("Plus/Minus")
    st.dataframe(top_plus_minus.style.format({'POSSESSIONS': '{:,}'}), 
                  use_container_width=True, hide_index=True)
            
    st.subheader("Net Rating")
    st.dataframe(top_net_rating.style.format({'Offensive Rating': '{:.1f}', 
                                            'Defensive Rating': '{:.1f}', 
                                            'Net Rating': '{:.1f}',
                                            'POSSESSIONS': '{:,}'}),
                  use_container_width=True, hide_index=True)

    st.markdown("---")

    # --- Section 2: Full dataset explorer with Player and Numeric Filtering ---
    st.subheader("🔍 Explore full lineup data")

    # # Start with the explorer DataFrame
    # df = away_final_results_explorer.copy() 


    
    # Multiselect for additional grouping columns
    selected_context_cols = st.multiselect(
        "Group By Number of Opponent's Player Type on Court:",
        options=ALL_GROUPING_COLS,
        default=[]
    )

    # Dynamically set group_dict for the EXPLORER TABLE
    group_dict_explorer = ['LINEUP'] + selected_context_cols

    # 2. Calculate Results for EXPLORER TABLE (LINEUP + Context)
    kept_cols_explorer = group_dict_explorer + RATING_COLS
    away_final_results_explorer = helpers.calculate_lineup_ratings(combined_df, AWAY_TEAM_NAME, HOME_TEAM_NAME, group_dict_explorer, agg_dict)
    df = away_final_results_explorer.copy()
    
    # 1. Context Column Filters 
    if selected_context_cols and not df.empty:
        # st.markdown("##### Filter by Grouping Column Values")
        
        # Use a container to manage filter layout
        filter_container = st.container()
        filter_cols = filter_container.columns(min(len(selected_context_cols), 3)) # Max 3 filters per row
        
        # Apply filters to the EXPLORER DataFrame
        for i, col in enumerate(selected_context_cols):
            if col in df.columns:
                unique_values = sorted(df[col].unique().tolist())
                
                selected_values = filter_cols[i % 3].multiselect(
                    f"Filter **{col}**:", 
                    options=unique_values,
                    default=unique_values, 
                    key=f"filter_{col}"
                )
                
                # Apply the filter to the DataFrame immediately
                if selected_values and selected_values != unique_values:
                    df = df[df[col].isin(selected_values)]
    elif selected_context_cols and df.empty:
        st.warning("No data found for the selected grouping options.")

    # 2. Player Filters (Only apply if grouping is LINEUP ONLY, which is signaled by no context columns)
    
    # Check if we are in the LINEUP ONLY aggregation case for player filtering purposes
    is_lineup_only_aggregation = not selected_context_cols
    
    if 'LINEUP' in df.columns and is_lineup_only_aggregation:
        # Determine if LINEUP is a list (unconverted)
        is_lineup_list = not df.empty and isinstance(df['LINEUP'].iloc[0], list)

        if is_lineup_list: 
            all_players = sorted(list(set(player for lineup in df_base_top['LINEUP'] for player in lineup))) 
            
            st.markdown("##### Filter by Player Inclusion/Exclusion")
            col_inc, col_exc = st.columns(2)

            with col_inc:
                include_players = st.multiselect(
                    "Lineups MUST **Include**:", 
                    options=all_players,
                    key="include_filter"
                )
            with col_exc:
                exclude_players = st.multiselect(
                    "Lineups MUST **Exclude**:", 
                    options=all_players,
                    key="exclude_filter"
                )
                
            # Apply the inclusion/exclusion filters
            if include_players:
                df = df[df['LINEUP'].apply(lambda lineup: all(player in lineup for player in include_players))]

            if exclude_players:
                df = df[df['LINEUP'].apply(lambda lineup: not any(player in lineup for player in exclude_players))]
        
    # Final step for the explorer table: Convert LINEUP to string and reorder
    if 'LINEUP' in df.columns:
        if not df.empty and isinstance(df['LINEUP'].iloc[0], list):
            df['LINEUP'] = df['LINEUP'].apply(lambda x: ", ".join(x))
            
    df = reorder_lineup_first(df, group_dict_explorer)

    # 3. Numeric Filters (Use the filtered DF for range determination)
    if not df.empty:
        df_temp = df.copy() 
        pos_min_df, pos_max_df = int(df_temp['POSSESSIONS'].min()), int(df_temp['POSSESSIONS'].max())
        pm_min_df, pm_max_df = int(df_temp['Plus/Minus'].min()), int(df_temp['Plus/Minus'].max())
        nr_min_df, nr_max_df = float(df_temp['Net Rating'].min()), float(df_temp['Net Rating'].max())
        
        # Base ranges remain constant across all filters, based on the explorer data
        pos_min_base, pos_max_base = int(away_final_results_explorer['POSSESSIONS'].min()), int(away_final_results_explorer['POSSESSIONS'].max())
        pm_min_base, pm_max_base = int(away_final_results_explorer['Plus/Minus'].min()), int(away_final_results_explorer['Plus/Minus'].max())
        nr_min_base, nr_max_base = float(away_final_results_explorer['Net Rating'].min()), float(away_final_results_explorer['Net Rating'].max())

        st.markdown("##### Filter by Metric Range")
        col_pos_slider, col_pm_slider, col_nr_slider = st.columns(3)

        with col_pos_slider:
            min_possessions, max_possessions = st.slider(
                "Possessions range:",
                pos_min_base, pos_max_base, (pos_min_df, pos_max_df), key="pos_slider"
            )
            df = df[(df['POSSESSIONS'] >= min_possessions) & (df['POSSESSIONS'] <= max_possessions)]
        
        with col_pm_slider:
            min_plus_minus, max_plus_minus = st.slider(
                "Plus/Minus range:",
                pm_min_base, pm_max_base, (pm_min_df, pm_max_df), key="pm_slider"
            )
            df = df[(df['Plus/Minus'] >= min_plus_minus) & (df['Plus/Minus'] <= max_plus_minus)]

        with col_nr_slider:
            min_net_rating, max_net_rating = st.slider(
                "Net Rating range:",
                float(nr_min_base), float(nr_max_base), (float(nr_min_df), float(nr_max_df)), 
                step=0.1, 
                key="nr_slider"
            )
            df = df[(df['Net Rating'] >= min_net_rating) & (df['Net Rating'] <= max_net_rating)]

        # Apply formatting to the main table for better readability
        st.dataframe(df.style.format({
            'Offensive Rating': '{:.1f}', 
            'Defensive Rating': '{:.1f}', 
            'Net Rating': '{:.1f}',
            'POSSESSIONS': '{:,}'
        }), use_container_width=True, hide_index=True)

        # Download CSV
        csv_bytes = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download filtered data as CSV",
            data=csv_bytes,
            file_name=f"{AWAY_TEAM_NAME}_lineup_analysis.csv",
            mime="text/csv"
        )
    else:
        st.warning("No lineups match the current filter settings.")
        
    # Download full PDF report (uses the LINEUP ONLY results)
    pdf_bytes = generate_pdf_report(AWAY_TEAM_NAME, top_possessions_list, top_plus_minus_list, top_net_rating_list)
    st.download_button(
        label="📄 Download full report as PDF",
        data=pdf_bytes,
        file_name=f"{AWAY_TEAM_NAME}_lineup_report.pdf",
        mime="application/pdf"
    )
