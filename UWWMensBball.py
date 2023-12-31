import streamlit as st
from streamlit_modal import Modal
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import random

# import requests
# from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')
from datetime import timedelta


# st.title('UWW Mens Basketball Data')
st.set_page_config(layout="wide")#, title='UWW Mens Basketball Data')


def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)


# def playbyplay():
    
#     ## Get Information
    
#     date = soup.find_all("div", {"class":"large-4 columns game-details-container"})[0].find("dd").text.strip()

#     ## Box Scores

#     box = soup.find_all("table", {"class":"overall-stats"})
#     if 'Wis.-Whitewater' in box[0].find('caption').get_text().split(" ",1)[0]:
#         team_1 = 'UWW'
#         team_2 = 'OPP'
#         opp_name = box[2].find('caption').get_text().split(" ",1)[0]
#         rows = box[0].find_all("tr")
#         header = [th.text.strip() for th in rows[0].find_all("th")]
#         data = [[td.text.strip() for td in row.find_all("td")] for row in rows[1:]]
#         box_1 = pd.DataFrame(data, columns=header)
#         box_1['Team'] = team_1

#         rows = box[2].find_all("tr")
#         header = [th.text.strip() for th in rows[0].find_all("th")]
#         data = [[td.text.strip() for td in row.find_all("td")] for row in rows[1:]]
#         box_2 = pd.DataFrame(data, columns=header)
#         box_2['Team'] = team_2

#         box = pd.concat([box_1,box_2])

#     else:
#         team_1 = 'OPP'
#         team_2 = 'UWW'
#         opp_name = box[0].find('caption').get_text().split(" ",1)[0]
#         rows = box[0].find_all("tr")
#         header = [th.text.strip() for th in rows[0].find_all("th")]
#         data = [[td.text.strip() for td in row.find_all("td")] for row in rows[1:]]
#         box_1 = pd.DataFrame(data, columns=header)
#         box_1['Team'] = team_1

#         rows = box[2].find_all("tr")
#         header = [th.text.strip() for th in rows[0].find_all("th")]
#         data = [[td.text.strip() for td in row.find_all("td")] for row in rows[1:]]
#         box_2 = pd.DataFrame(data, columns=header)
#         box_2['Team'] = team_2

#         box = pd.concat([box_1,box_2])

#     ### Play by Play

#     section = soup.find("section", {"id":"play-by-play"})
#     table = section.findAll("table")

#     ### First Half
#     rows = table[0].find_all("tr")
#     header = [th.text.strip() for th in rows[0].find_all("th")]
#     data = [[td.text.strip() for td in row.find_all("td")] for row in rows[1:]]
#     pbp_1 = pd.DataFrame(data, columns=header)
#     pbp_1['Half'] = 1

#     ### Second Half
#     rows = table[1].find_all("tr")
#     header = [th.text.strip() for th in rows[0].find_all("th")]
#     data = [[td.text.strip() for td in row.find_all("td")] for row in rows[1:]]
#     pbp_2 = pd.DataFrame(data, columns=header)
#     pbp_2['Half'] = 2

#     pbp = pd.concat([pbp_1,pbp_2])
#     pbp = pbp.drop(columns=['Play Team Indicator','Team Indicator','Away Team Score','Home Team Score','Play'])


#     if 'UWW' in team_1:
#         pbp.columns = ['Time Remaining','UWW','OPP','Game Score','Half']

#     if 'UWW' in team_2:
#         pbp.columns = ['Time Remaining','OPP','UWW','Game Score','Half']

#     pbp['UWW_LINEUP'] = ''
#     pbp['OPP_LINEUP'] = ''

#     pbp['Time Remaining'] = pbp['Time Remaining'].replace("--",np.NaN)
#     pbp['Time Remaining'] = pbp['Time Remaining'].ffill()


#     starters = box[box['GS']=='*']

#     for starter in range(5):

#         starter_add = pd.DataFrame({'Time Remaining':'20:00',
#                                  'UWW':'SUB IN '+starters[starters['Team']=='UWW'].iloc[starter]['Player'].split(" ", 1)[1].replace(" ","").upper(), 
#                                  'OPP':'SUB IN '+starters[starters['Team']=='OPP'].iloc[starter]['Player'].split(" ", 1)[1].replace(" ","").upper(),
#                                  'Game Score':'',
#                                  'Half':'1'#,
#                                  # 'UWW_LINEUP':'SUB IN '+starters[starters['Team']=='UWW'].iloc[starter]['Player'].split(" ", 1)[1].replace(" ","").upper(), 
#                                  # 'OPP_LINEUP':'SUB IN '+starters[starters['Team']=='OPP'].iloc[starter]['Player'].split(" ", 1)[1].replace(" ","").upper()


#                                    },index =[0])

#         pbp = pd.concat([starter_add, pbp]).reset_index(drop = True)


#     ### UWW
#     uww_players = list(box[((box['Team']=='UWW')&(~box['Player'].str.contains('TEAM|Totals')))]['Player'].str.split(" ", 1, expand=True)[1].str.replace(" ","").str.upper())
#     pbp = pd.concat([pbp,pd.DataFrame(columns=uww_players)])

#     for player in uww_players:
#         sub_index = pbp[((pbp['UWW'].str.contains('SUB'))&(pbp['UWW'].str.contains(player)))].index
#         sub_index = [sub_index[i:i + 2] for i in range(0, len(sub_index), 2)]
#         for x in sub_index:
#             try :
#                 pbp.iloc[x[0]:x[1], pbp.columns.get_loc(player)] = player
#             except IndexError:
#                 pbp.iloc[x[0]:len(pbp), pbp.columns.get_loc(player)] = player

#     pbp['UWW_LINEUP'] = pbp.assign(combined = pbp[uww_players].stack().sort_values().groupby(level=0).agg(list))['combined']
#     pbp['UWW_LINEUP'] = pbp['UWW_LINEUP'].fillna('Empty')
#     pbp['UWW_LINEUP'] = [';'.join(map(str, l)) for l in pbp['UWW_LINEUP']]

#     pbp = pbp[['Time Remaining','UWW','OPP','Game Score','Half','UWW_LINEUP']]




#     ### OPP
#     opp_players = list(box[((box['Team']=='OPP')&(~box['Player'].str.contains('TEAM|Totals')))]['Player'].str.split(" ", 1, expand=True)[1].str.replace(" ","").str.upper())
#     pbp = pd.concat([pbp,pd.DataFrame(columns=opp_players)])

#     for player in opp_players:
#         sub_index = pbp[((pbp['OPP'].str.contains('SUB'))&(pbp['OPP'].str.contains(player)))].index
#         sub_index = [sub_index[i:i + 2] for i in range(0, len(sub_index), 2)]
#         for x in sub_index:
#             try :
#                 pbp.iloc[x[0]:x[1], pbp.columns.get_loc(player)] = player
#             except IndexError:
#                 pbp.iloc[x[0]:len(pbp), pbp.columns.get_loc(player)] = player

#     pbp['OPP_LINEUP'] = pbp.assign(combined = pbp[opp_players].stack().sort_values().groupby(level=0).agg(list))['combined']
#     pbp['OPP_LINEUP'] = pbp['OPP_LINEUP'].fillna('Empty')
#     pbp['OPP_LINEUP'] = [';'.join(map(str, l)) for l in pbp['OPP_LINEUP']]


#     pbp = pbp[['Time Remaining','UWW','OPP','Game Score','Half','UWW_LINEUP','OPP_LINEUP']]


#     pbp = pbp[~((pbp['UWW'].str.contains('SUB IN'))|(pbp['UWW'].str.contains('SUB OUT')))].reset_index(drop=True)
#     pbp = pbp[~((pbp['OPP'].str.contains('SUB IN'))|(pbp['OPP'].str.contains('SUB OUT')))].reset_index(drop=True)


#     pbp['Date'] = date
#     pbp['Opponent'] = opp_name


#     pbp['UWW_GOOD LAYUP'] = np.where(pbp['UWW'].str.contains('GOOD LAYUP'),1,0)
#     pbp['UWW_MISS LAYUP'] = np.where(pbp['UWW'].str.contains('MISS LAYUP'),1,0)
#     pbp['UWW_GOOD DUNK'] = np.where(pbp['UWW'].str.contains('GOOD DUNK'),1,0)
#     pbp['UWW_MISS DUNK'] = np.where(pbp['UWW'].str.contains('MISS DUNK'),1,0)
#     pbp['UWW_GOOD JUMPER'] = np.where(pbp['UWW'].str.contains('GOOD JUMPER'),1,0)
#     pbp['UWW_MISS JUMPER'] = np.where(pbp['UWW'].str.contains('MISS JUMPER'),1,0)
#     pbp['UWW_GOOD 3PTR'] = np.where(pbp['UWW'].str.contains('GOOD 3PTR'),1,0)
#     pbp['UWW_MISS 3PTR'] = np.where(pbp['UWW'].str.contains('MISS 3PTR'),1,0)
#     pbp['UWW_GOOD FT'] = np.where(pbp['UWW'].str.contains('GOOD FT'),1,0)
#     pbp['UWW_MAKE FT'] = np.where(pbp['UWW'].str.contains('MAKE FT'),1,0)
#     pbp['UWW_ASSIST'] = np.where(pbp['UWW'].str.contains('ASSIST'),1,0)
#     pbp['UWW_REBOUND OFF'] = np.where(pbp['UWW'].str.contains('REBOUND OFF'),1,0)
#     pbp['UWW_REBOUND DEF'] = np.where(pbp['UWW'].str.contains('REBOUND DEF'),1,0)
#     pbp['UWW_REBOUND DEADB'] = np.where(pbp['UWW'].str.contains('REBOUND DEADB'),1,0)
#     pbp['UWW_FOUL'] = np.where(pbp['UWW'].str.contains('FOUL'),1,0)
#     pbp['UWW_BLOCK'] = np.where(pbp['UWW'].str.contains('BLOCK'),1,0)
#     pbp['UWW_TURNOVER'] = np.where(pbp['UWW'].str.contains('TURNOVER'),1,0)
#     pbp['UWW_PTS_SCORED'] = ((pbp['UWW_GOOD LAYUP']*2)+
#                               (pbp['UWW_GOOD DUNK']*2)+
#                               (pbp['UWW_GOOD JUMPER']*2)+
#                               (pbp['UWW_GOOD 3PTR']*3)+
#                               (pbp['UWW_GOOD FT']*1))


#     pbp['OPP_GOOD LAYUP'] = np.where(pbp['OPP'].str.contains('GOOD LAYUP'),1,0)
#     pbp['OPP_MISS LAYUP'] = np.where(pbp['OPP'].str.contains('MISS LAYUP'),1,0)
#     pbp['OPP_GOOD DUNK'] = np.where(pbp['OPP'].str.contains('GOOD DUNK'),1,0)
#     pbp['OPP_MISS DUNK'] = np.where(pbp['OPP'].str.contains('MISS DUNK'),1,0)
#     pbp['OPP_GOOD JUMPER'] = np.where(pbp['OPP'].str.contains('GOOD JUMPER'),1,0)
#     pbp['OPP_MISS JUMPER'] = np.where(pbp['OPP'].str.contains('MISS JUMPER'),1,0)
#     pbp['OPP_GOOD 3PTR'] = np.where(pbp['OPP'].str.contains('GOOD 3PTR'),1,0)
#     pbp['OPP_MISS 3PTR'] = np.where(pbp['OPP'].str.contains('MISS 3PTR'),1,0)
#     pbp['OPP_GOOD FT'] = np.where(pbp['OPP'].str.contains('GOOD FT'),1,0)
#     pbp['OPP_MAKE FT'] = np.where(pbp['OPP'].str.contains('MAKE FT'),1,0)
#     pbp['OPP_ASSIST'] = np.where(pbp['OPP'].str.contains('ASSIST'),1,0)
#     pbp['OPP_REBOUND OFF'] = np.where(pbp['OPP'].str.contains('REBOUND OFF'),1,0)
#     pbp['OPP_REBOUND DEF'] = np.where(pbp['OPP'].str.contains('REBOUND DEF'),1,0)
#     pbp['OPP_REBOUND DEADB'] = np.where(pbp['OPP'].str.contains('REBOUND DEADB'),1,0)
#     pbp['OPP_FOUL'] = np.where(pbp['OPP'].str.contains('FOUL'),1,0)
#     pbp['OPP_BLOCK'] = np.where(pbp['OPP'].str.contains('BLOCK'),1,0)
#     pbp['OPP_TURNOVER'] = np.where(pbp['OPP'].str.contains('TURNOVER'),1,0)
#     pbp['OPP_PTS_SCORED'] = ((pbp['OPP_GOOD LAYUP']*2)+
#                               (pbp['OPP_GOOD DUNK']*2)+
#                              (pbp['OPP_GOOD JUMPER']*2)+
#                              (pbp['OPP_GOOD 3PTR']*3)+
#                              (pbp['OPP_GOOD FT']*1))
    
#     pbp = pbp.groupby(['Date','Opponent','Time Remaining','Half','UWW_LINEUP','OPP_LINEUP']).sum().reset_index().sort_values(['Date','Opponent','Half','Time Remaining'],ascending=[True,True,True,False])


#     pbp['UWW_PLUS_MINUS'] = pbp['UWW_PTS_SCORED'] - pbp['OPP_PTS_SCORED']
#     pbp['OPP_PLUS_MINUS'] = pbp['OPP_PTS_SCORED'] - pbp['UWW_PTS_SCORED']
    
#     pbp['UWW_ASST_TURN'] = pbp['UWW_ASSIST'] - pbp['UWW_TURNOVER']
#     pbp['OPP_ASST_TURN'] = pbp['OPP_ASSIST'] - pbp['OPP_TURNOVER']
    
#     pbp['UWW_REBOUNDING'] = pbp['UWW_REBOUND OFF'] + pbp['UWW_REBOUND DEF'] + pbp['UWW_REBOUND DEADB'] - pbp['OPP_REBOUND OFF'] - pbp['OPP_REBOUND DEF'] - pbp['OPP_REBOUND DEADB']
#     pbp['OPP_REBOUNDING'] = pbp['OPP_REBOUND OFF'] + pbp['OPP_REBOUND DEF'] + pbp['OPP_REBOUND DEADB'] - pbp['UWW_REBOUND OFF'] - pbp['UWW_REBOUND DEF'] - pbp['UWW_REBOUND DEADB']

#     pbp['UWW_PTS_TOTAL'] = pbp['UWW_PTS_SCORED'].cumsum()
#     pbp['OPP_PTS_TOTAL'] = pbp['OPP_PTS_SCORED'].cumsum()
    
    
#     def seconder(x):
#         mins, secs = map(float, x.split(':'))
#         td = timedelta(minutes=mins, seconds=secs)
#         return td.total_seconds()

#     pbp['Seconds'] = pbp['Time Remaining'].apply(seconder)

#     pbp['MinutesOnCourt'] = np.where((pbp['Date']==pbp['Date'].shift(1))&
#                                           (pbp['Opponent']==pbp['Opponent'].shift(1))&
#                                           (pbp['Half']==pbp['Half'].shift(1)),
#                                           pbp['Seconds'].shift(1) - pbp['Seconds'],
#                                           1200 - pbp['Seconds'])
    
#     pbp['MinutesOnCourt'] = round(pbp['MinutesOnCourt'] / 60,2)
    
    
    
    
    
#     return(pbp)




# games_full = pd.DataFrame()
# pbp_full = pd.DataFrame()

# years = [
#          #'2021-22',
#          # '2022-23'
#         '2023-24'
#         ]

# for year in years:
#     print('YEAR: ', year)
#     url = 'https://uwwsports.com/sports/mens-basketball/schedule/'+year+'?grid=true'

#     headers = {
#         "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/77.0.3865.90 Safari/537.36'}

#     page = requests.get(url, headers=headers)

#     soup = BeautifulSoup(page.content, 'html.parser')

#     table = soup.find("table")
#     rows = table.find_all("tr")
#     # lines = table.find_all("li")
#     header = [th.text.strip() for th in rows[0].find_all("th")]
#     data = [[td.text.strip() for td in row.find_all("td")] for row in rows[1:]]
#     games = pd.DataFrame(data, columns=header)
#     #####Need to fix this so it includes other games
#     games = games[games['Links'].str.contains('Box Score')]
#     #####
#     games['Year'] = year

#     links = soup.findAll(lambda tag:tag.name=="a" and "box score" in tag.text.lower())
#     hrefs = [link.get('href') for link in links]
#     games['box_link'] = hrefs

#     games_full = games_full.append(games)


# for index, row in games_full.iterrows():
#     print(row['box_link'])
    
#     url = 'https://uwwsports.com/'+row['box_link']

#     headers = {
#         "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/77.0.3865.90 Safari/537.36'}

#     page = requests.get(url, headers=headers)

#     soup = BeautifulSoup(page.content, 'html.parser')
    
#     pbp = playbyplay()
    
#     pbp_full = pbp_full.append(pbp)


# df = pbp_full


stats = pd.read_csv("https://github.com/fritschcm272/UWW_MensBBALL/blob/main/warhawks_stats.csv?raw=true")
stats['Date'] = pd.to_datetime(stats['Date'])
stats['Opponent'] = stats['Opponent'] + ' (' + stats['Date'].astype(str) + ')'


full = pd.read_csv("https://github.com/fritschcm272/UWW_MensBBALL/blob/main/warhawks_lineups.csv?raw=true")
full = full.sort_values(['UWW_LINEUP','Date'])
full['Date'] = pd.to_datetime(full['Date'])
full = full.sort_values('Date')
full['Opponent'] = full['Opponent'] + ' (' + full['Date'].astype(str) + ')'

games_list = full[['Opponent']]
games_list = list(games_list['Opponent'].drop_duplicates())

players_list = list(full['UWW_LINEUP'].str.split(';',expand=True).stack().reset_index()[0].drop_duplicates().sort_values())



last3games = st.checkbox('Last 3 Games')

if last3games:
    games = st.multiselect("Choose Games", games_list, games_list[-3:])

else:
    games = st.multiselect("Choose Games", games_list)


games_list_search = '|'.join(games)
games_list_search = games_list_search.replace('(','').replace(')','') 

players = st.multiselect(
    "Choose Players", players_list, #["China", "United States of America"]
)


if not games:
    
    df = full
    
else:
    
    games_list_search = '|'.join(games)
    games_list_search = games_list_search.replace(r"\(","")#.replace(r"\)","")
    df = full[(full['Opponent'].str.replace('(','').str.replace(')','').str.contains(games_list_search))]
    stats = stats[(stats['Opponent'].str.replace('(','').str.replace(')','').str.contains(games_list_search))]
    
if not players:

    df_l = df

else:
    if len(players)==1:
        df_l = df[(df['UWW_LINEUP'].str.contains(players[0]))]
    if len(players)==2:
        df_l = df[(df['UWW_LINEUP'].str.contains(players[0])) & (df['UWW_LINEUP'].str.contains(players[1]))]
    if len(players)==3:
        df_l = df[(df['UWW_LINEUP'].str.contains(players[0])) & (df['UWW_LINEUP'].str.contains(players[1]))& (df['UWW_LINEUP'].str.contains(players[2]))]
    if len(players)==4:
        df_l = df[(df['UWW_LINEUP'].str.contains(players[0])) & (df['UWW_LINEUP'].str.contains(players[1]))& (df['UWW_LINEUP'].str.contains(players[2]))& (df['UWW_LINEUP'].str.contains(players[3]))]
    if len(players)==5:
        df_l = df[(df['UWW_LINEUP'].str.contains(players[0])) & (df['UWW_LINEUP'].str.contains(players[1]))& (df['UWW_LINEUP'].str.contains(players[2]))& (df['UWW_LINEUP'].str.contains(players[3]))& (df['UWW_LINEUP'].str.contains(players[4]))]
    if len(players)>=6:
        st.error("Please only select up to five players.")
        df_l = df
    # st.write("### 5 Man Lineups")
    # st.markdown(data.style.hide(axis="index").to_html(escape=False), unsafe_allow_html=True)
    
########################################
st.header('Players', divider='gray')
df_p = df
df_p = df_p.explode('UWW_LINEUP')
df_p['UWW_LINEUP']=df_p['UWW_LINEUP'].str.split(';').fillna(df_p['UWW_LINEUP'])
df_p=df_p.explode('UWW_LINEUP',ignore_index=True)

###
players_list_search = '|'.join(players)
df_p = df_p[(df_p['UWW_LINEUP'].str.contains(players_list_search))]
###

df_p = df_p.groupby(['UWW_LINEUP','Opponent'], as_index=False).agg({
                                                     # 'Opponent': 'nunique',
                                                     'MinutesOnCourt': 'sum',
                                                     'UWW_PLUS_MINUS': 'sum',
                                                     # 'UWW_PLUS_MINUS_CUMSUM':lambda x: list(x),
                                                     'UWW_ASST_TURN': 'sum',
                                                     'UWW_REBOUNDING': 'sum'})

df_p['UWW_PLUS_MINUS_CUMSUM'] = df_p.groupby('UWW_LINEUP')['UWW_PLUS_MINUS'].cumsum()

df_p = df_p.groupby(['UWW_LINEUP'], as_index=False).agg({
                                                     'Opponent': 'nunique',
                                                     'MinutesOnCourt': 'sum',
                                                     'UWW_PLUS_MINUS': 'sum',
                                                     'UWW_PLUS_MINUS_CUMSUM':lambda x: list(x),
                                                     'UWW_ASST_TURN': 'sum',
                                                     'UWW_REBOUNDING': 'sum'})

df_p = df_p.sort_values(['UWW_PLUS_MINUS','MinutesOnCourt'],ascending=[False,False])


stats = stats.groupby(['Play_Player'])[['Points','Field_Goals_Made',
                                                                                 'Field_Goals_Missed','3P_Field_Goals_Made','3P_Field_Goals_Missed',
                                                                                 'FT_Made','FT_Missed','Rebound_Off','Rebound_Def',
                                                                                 'Rebound_Total', 'Assists', 'Turnovers']].sum().reset_index()

# format(,".1%")
stats['fgpercent'] = (stats['Field_Goals_Made'] / (stats['Field_Goals_Made'] + stats['Field_Goals_Missed']))*100
stats['threeptpercent'] = (stats['3P_Field_Goals_Made'] / (stats['3P_Field_Goals_Made'] + stats['3P_Field_Goals_Missed']))*100
stats['ftpercent'] = (stats['FT_Made'] / (stats['FT_Made'] + stats['FT_Missed']))*100

# Merge in player stats table

df_p = pd.merge(df_p,stats, how='left', left_on='UWW_LINEUP', right_on='Play_Player')
                
                  
                

# df_p.insert(0, "Select", False)

# df_p['Photo'] = "https://uwwsports.com/images/2023/11/9/Jameer_Barker.jpg?width=40"


# col1, col2 = st.columns([3, 1])

# with col1:

    
st.dataframe(
    df_p[[
          'UWW_LINEUP',
          'Opponent',
          'MinutesOnCourt',
          'UWW_PLUS_MINUS',
          'UWW_PLUS_MINUS_CUMSUM',
          'UWW_ASST_TURN',
          'UWW_REBOUNDING',
          'Points',
          'fgpercent',
          'threeptpercent',
          'ftpercent'
         ]],
    column_config={
        # "Select": st.column_config.CheckboxColumn(required=True),
        "UWW_LINEUP":"Player",
#         "Photo": {st.write(321)},
#         # "": st.column_config.ImageColumn("Photo", help="The user's avatar"),
#         # "Photo":{"Player","Games"},

#         # "Photo": st.image('https://uwwsports.com/images/2023/11/9/Jameer_Barker.jpg?width=40'),
        "Opponent":"Games",
        "MinutesOnCourt": "Minutes",
        "UWW_PLUS_MINUS": "Current Points +/-",
        "UWW_PLUS_MINUS_CUMSUM": st.column_config.LineChartColumn(
            "Trending +/-", 
            # y_min= 0,#min_pm, 
            # y_max= max_pm
        ),
        "UWW_ASST_TURN": "Assist/Turnover",
        "UWW_REBOUNDING": "Rebounding +/-",
        "Points": "Points Scored",
        "fgpercent": st.column_config.NumberColumn('FG %', format='%.1f %%'),
        "threeptpercent": st.column_config.NumberColumn('3PT FG %', format='%.1f %%'),
        "ftpercent": st.column_config.NumberColumn('FT %', format='%.1f %%')
        
    },
    hide_index=True
)


if len(players) == 1:
    stats = stats[stats['Play_Player']==players[0]].reset_index()


    



    modal = Modal(
        "Player Details", 
        key="demo-modal",

        # Optional
        padding=20,    # default value
        max_width=744  # default value
    )

    open_modal = st.button("Player Details")
    if open_modal:
        modal.open()

    if modal.is_open():
        with modal.container():

    #         st.write("Text goes here")

    #         html_string = '''
    #         <h1>HTML string in RED</h1>

    #         <script language="javascript">
    #           document.querySelector("h1").style.color = "red";
    #         </script>
    #         '''
    #         components.html(html_string)

    #         st.write("Some fancy text")
    #         value = st.checkbox("Check me")
    #         st.write(f"Checkbox checked: {value}")




            # st.header('Player Details', divider='gray')

            col1, col2 = st.columns(2)

            col1.image('https://uwwsports.com/images/2023/11/9/Miles_Barnstable.jpg?width=80&quality=90')
            col2.text('Miles Barnstable')


            col1, col2, col3 = st.columns(3)
            col1.metric("Points", stats['Points'][0])# df_l_tot_pm)
            col2.metric("FG %", stats['fgpercent'][0])
            col3.metric("3PT %", stats['threeptpercent'][0])# df_l_tot_reb)

            st.dataframe(stats)


########################################
st.header('5 Man Lineups', divider='gray')
if not games:
    st.caption("Games: All")
else:
    st.caption("Games: "+','.join(games))
if not players:
    st.caption("Players: All")
else:
    st.caption("Players: "+'|'.join(players))





df_l['UWW_PLUS_MINUS_CUMSUM'] = df_l.groupby('UWW_LINEUP')['UWW_PLUS_MINUS'].cumsum()
min_pm = df_l['UWW_PLUS_MINUS_CUMSUM'].min()
max_pm = df_l['UWW_PLUS_MINUS_CUMSUM'].max()
df_l['UWW_LINEUP'] = df_l['UWW_LINEUP'].replace(';',' ; ', regex=True)
# df['UWW_LINEUP_PICS'] = df['UWW_LINEUP'].replace('*BARKER,JAMEER*', 'https://uwwsports.com/images/2023/11/9/Jameer_Barker.jpg?width=40', regex=True)
# replace("BARKER,JAMEER",'https://uwwsports.com/images/2023/11/9/Jameer_Barker.jpg?width=40')
df_l['Opponent'] = df_l['Opponent'] + ' (' + df_l['Date'].astype(str) + ')'
df_l = df_l.drop(columns=['Date'])
df_l = df_l.groupby(['UWW_LINEUP'], as_index=False).agg({'Opponent': 'count',
                                                     'MinutesOnCourt': 'sum',
                                                     'UWW_PLUS_MINUS': 'sum',
                                                     'UWW_PLUS_MINUS_CUMSUM':lambda x: list(x),
                                                     'UWW_ASST_TURN': 'sum',
                                                     'UWW_REBOUNDING': 'sum',
                                                     'UWW_FG_MADE': 'sum',
                                                     'UWW_FG_MISS': 'sum',
                                                     'UWW_GOOD 3PTR': 'sum',
                                                     'UWW_MISS 3PTR': 'sum',
                                                     'UWW_GOOD FT':'sum',
                                                     'UWW_MISS FT':'sum'})




df_l['fgpercent'] = (df_l['UWW_FG_MADE'] / (df_l['UWW_FG_MADE'] + df_l['UWW_FG_MISS']))*100
df_l['threeptpercent'] = (df_l['UWW_GOOD 3PTR'] / (df_l['UWW_GOOD 3PTR'] + df_l['UWW_MISS 3PTR']))*100
df_l['ftpercent'] = (df_l['UWW_GOOD FT'] / (df_l['UWW_GOOD FT'] + df_l['UWW_MISS FT']))*100

df_l = df_l.drop(columns=['UWW_FG_MADE',
                                                     'UWW_FG_MISS',
                                                     'UWW_GOOD 3PTR',
                                                     'UWW_MISS 3PTR',
                                                     'UWW_GOOD FT',
                                                     'UWW_MISS FT'])

df_l = df_l.sort_values(['UWW_PLUS_MINUS','MinutesOnCourt'],ascending=[False,False])



df_l_tot_moc = round(df_l['MinutesOnCourt'].sum(),2)
df_l_tot_pm = df_l['UWW_PLUS_MINUS'].sum()
df_l_tot_at = df_l['UWW_ASST_TURN'].sum()                      
df_l_tot_reb = df_l['UWW_REBOUNDING'].sum()




col1, col2, col3, col4 = st.columns(4)
col1.metric("Minutes", df_l_tot_moc) #col1.metric("Minutes", "70 °F", "1.2 °F")
col2.metric("Points +/-", df_l_tot_pm)
col3.metric("A/T Ratio", df_l_tot_at)
col4.metric("Reb +/-", df_l_tot_reb)


st.dataframe(
    df_l,
    column_config={
        "UWW_LINEUP":"Lineup",
        "Opponent":"Games",
        "MinutesOnCourt": "Minutes",
        "UWW_PLUS_MINUS": "Current Points +/-",
        "UWW_PLUS_MINUS_CUMSUM": st.column_config.LineChartColumn(
            "Trending +/-", 
            # y_min= 0,#min_pm, 
            # y_max= max_pm
        ),
        "UWW_ASST_TURN": "Assist/Turnover",
        "UWW_REBOUNDING": "Rebounding +/-",
        # "Points": "Points Scored",
        "fgpercent": st.column_config.NumberColumn('FG %', format='%.1f %%'),
        "threeptpercent": st.column_config.NumberColumn('3PT FG %', format='%.1f %%'),
        "ftpercent": st.column_config.NumberColumn('FT %', format='%.1f %%')
        
    },
    hide_index=True
)






########################################
st.header('Player Comparison', divider='gray')
if len(players)==2:
    df_comp_1 = df[(df['UWW_LINEUP'].str.contains(players[0])) & (~df['UWW_LINEUP'].str.contains(players[1]))]
    df_comp_2 = df[(df['UWW_LINEUP'].str.contains(players[1])) & (~df['UWW_LINEUP'].str.contains(players[0]))]
    
    if not games:
        st.caption("Games: All")
    else:
        st.caption("Games: "+','.join(games))
    if not players:
        st.caption("Players: All")
    else:
        st.caption("Players: "+'|'.join(players))
        
    df_comp_1['UWW_PLUS_MINUS_CUMSUM'] = df_comp_1.groupby('UWW_LINEUP')['UWW_PLUS_MINUS'].cumsum()
    min_pm = df_comp_1['UWW_PLUS_MINUS_CUMSUM'].min()
    max_pm = df_comp_1['UWW_PLUS_MINUS_CUMSUM'].max()
    df_comp_1['UWW_LINEUP'] = df_comp_1['UWW_LINEUP'].replace(';',' ; ', regex=True)
    df_comp_1['Opponent'] = df_comp_1['Opponent'] + ' (' + df_comp_1['Date'].astype(str) + ')'
    df_comp_1 = df_comp_1.drop(columns=['Date'])
    df_comp_1 = df_comp_1.groupby(['UWW_LINEUP'], as_index=False).agg({'Opponent': 'count',
                                                         'MinutesOnCourt': 'sum',
                                                         'UWW_PLUS_MINUS': 'sum',
                                                         'UWW_PLUS_MINUS_CUMSUM':lambda x: list(x),
                                                         'UWW_ASST_TURN': 'sum',
                                                         'UWW_REBOUNDING': 'sum'})
    df_comp_1 = df_comp_1.sort_values(['UWW_PLUS_MINUS','MinutesOnCourt'],ascending=[False,False])

    df_comp_1_tot_moc = round(df_comp_1['MinutesOnCourt'].sum(),2)
    df_comp_1_tot_pm = df_comp_1['UWW_PLUS_MINUS'].sum()
    df_comp_1_tot_at = df_comp_1['UWW_ASST_TURN'].sum()                      
    df_comp_1_tot_reb = df_comp_1['UWW_REBOUNDING'].sum()


    col1, col2, col3, col4, col5 = st.columns(5)
    col1.caption(players[0] + " without " + players[1])
    col2.metric("Minutes", df_comp_1_tot_moc) #col1.metric("Minutes", "70 °F", "1.2 °F")
    col3.metric("Points +/-", df_comp_1_tot_pm)
    col4.metric("A/T Ratio", df_comp_1_tot_at)
    col5.metric("Reb +/-", df_comp_1_tot_reb)
    
    
    df_comp_2['UWW_PLUS_MINUS_CUMSUM'] = df_comp_2.groupby('UWW_LINEUP')['UWW_PLUS_MINUS'].cumsum()
    min_pm = df_comp_2['UWW_PLUS_MINUS_CUMSUM'].min()
    max_pm = df_comp_2['UWW_PLUS_MINUS_CUMSUM'].max()
    df_comp_2['UWW_LINEUP'] = df_comp_2['UWW_LINEUP'].replace(';',' ; ', regex=True)
    df_comp_2['Opponent'] = df_comp_2['Opponent'] + ' (' + df_comp_2['Date'].astype(str) + ')'
    df_comp_2 = df_comp_2.drop(columns=['Date'])
    df_comp_2 = df_comp_2.groupby(['UWW_LINEUP'], as_index=False).agg({'Opponent': 'count',
                                                         'MinutesOnCourt': 'sum',
                                                         'UWW_PLUS_MINUS': 'sum',
                                                         'UWW_PLUS_MINUS_CUMSUM':lambda x: list(x),
                                                         'UWW_ASST_TURN': 'sum',
                                                         'UWW_REBOUNDING': 'sum'})
    df_comp_2 = df_comp_2.sort_values(['UWW_PLUS_MINUS','MinutesOnCourt'],ascending=[False,False])

    df_comp_2_tot_moc = round(df_comp_2['MinutesOnCourt'].sum(),2)
    df_comp_2_tot_pm = df_comp_2['UWW_PLUS_MINUS'].sum()
    df_comp_2_tot_at = df_comp_2['UWW_ASST_TURN'].sum()                      
    df_comp_2_tot_reb = df_comp_2['UWW_REBOUNDING'].sum()


    col1, col2, col3, col4, col5 = st.columns(5)
    col1.caption(players[1] + " without " + players[0])
    col2.metric("Minutes", df_comp_2_tot_moc) #col1.metric("Minutes", "70 °F", "1.2 °F")
    col3.metric("Points +/-", df_comp_2_tot_pm)
    col4.metric("A/T Ratio", df_comp_2_tot_at)
    col5.metric("Reb +/-", df_comp_2_tot_reb)

#     st.dataframe(
#         df_comp_1,
#         column_config={
#             "Opponent":"Games",
#             "MinutesOnCourt": "Minutes",
#             "UWW_PLUS_MINUS": "Current Points +/-",
#             "UWW_PLUS_MINUS_CUMSUM": st.column_config.LineChartColumn(
#                 "Trending +/-", 
#                 # y_min= 0,#min_pm, 
#                 # y_max= max_pm
#             ),
#             "UWW_ASST_TURN": "Assist/Turnover",
#             "UWW_REBOUNDING": "Rebounding +/-"
#         },
#         hide_index=True
#     )

else:
    st.subheader('_Available when 2 players are selected_')



