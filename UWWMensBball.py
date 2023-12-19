import streamlit as st
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
full = pd.read_csv("https://github.com/fritschcm272/UWW_MensBBALL/blob/8b14858e205007e231252c2dd86bb8ca3ef20fa3/warhawks.csv?raw=true")
full = full.sort_values(['UWW_LINEUP','Date'])
full['Date'] = pd.to_datetime(full['Date'])
full = full.sort_values('Date')
full['Opponent'] = full['Opponent'] + ' (' + full['Date'].astype(str) + ')'

games_list = full[['Opponent']]
games_list = list(games_list['Opponent'].drop_duplicates())

players_list = list(full['UWW_LINEUP'].str.split(';',expand=True).stack().reset_index()[0].drop_duplicates().sort_values())

games = st.multiselect(
    "Choose Games", games_list, #["China", "United States of America"]
)

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
    
if not players:

    df = df

else:
    if len(players)==1:
        df = df[(df['UWW_LINEUP'].str.contains(players[0]))]
    if len(players)==2:
        df = df[(df['UWW_LINEUP'].str.contains(players[0])) & (df['UWW_LINEUP'].str.contains(players[1]))]
    if len(players)==3:
        df = df[(df['UWW_LINEUP'].str.contains(players[0])) & (df['UWW_LINEUP'].str.contains(players[1]))& (df['UWW_LINEUP'].str.contains(players[2]))]
    if len(players)==4:
        df = df[(df['UWW_LINEUP'].str.contains(players[0])) & (df['UWW_LINEUP'].str.contains(players[1]))& (df['UWW_LINEUP'].str.contains(players[2]))& (df['UWW_LINEUP'].str.contains(players[3]))]
    if len(players)==5:
        df = df[(df['UWW_LINEUP'].str.contains(players[0])) & (df['UWW_LINEUP'].str.contains(players[1]))& (df['UWW_LINEUP'].str.contains(players[2]))& (df['UWW_LINEUP'].str.contains(players[3]))& (df['UWW_LINEUP'].str.contains(players[4]))]
    if len(players)>=6:
        st.error("Please only select up to five players.")
    #     data = df
    # st.write("### 5 Man Lineups")
    # st.markdown(data.style.hide(axis="index").to_html(escape=False), unsafe_allow_html=True)

        
       
df['UWW_PLUS_MINUS_CUMSUM'] = df.groupby('UWW_LINEUP')['UWW_PLUS_MINUS'].cumsum()
min_pm = df['UWW_PLUS_MINUS_CUMSUM'].min()
max_pm = df['UWW_PLUS_MINUS_CUMSUM'].max()
df['UWW_LINEUP'] = df['UWW_LINEUP'].replace(';',' ; ', regex=True)
# df['UWW_LINEUP_PICS'] = df['UWW_LINEUP'].replace('*BARKER,JAMEER*', 'https://uwwsports.com/images/2023/11/9/Jameer_Barker.jpg?width=40', regex=True)
# replace("BARKER,JAMEER",'https://uwwsports.com/images/2023/11/9/Jameer_Barker.jpg?width=40')
df['Opponent'] = df['Opponent'] + ' (' + df['Date'].astype(str) + ')'
df = df.drop(columns=['Date'])
df = df.groupby(['UWW_LINEUP'], as_index=False).agg({'Opponent': 'count',
                                                     'MinutesOnCourt': 'sum',
                                                     'UWW_PLUS_MINUS': 'sum',
                                                     'UWW_PLUS_MINUS_CUMSUM':lambda x: list(x),
                                                     'UWW_ASST_TURN': 'sum',
                                                     'UWW_REBOUNDING': 'sum'})
df = df.sort_values(['UWW_PLUS_MINUS','MinutesOnCourt'],ascending=[False,False])

st.dataframe(
    df,
    column_config={
        "Opponent":"Games",
        "MinutesOnCourt": "Minutes",
        "UWW_PLUS_MINUS": "Current Points +/-",
        "UWW_PLUS_MINUS_CUMSUM": st.column_config.LineChartColumn(
            "Trending +/-", 
            # y_min= 0,#min_pm, 
            # y_max= max_pm
        ),
        "UWW_ASST_TUN": "Assist/Turnover",
        "UWW_REBOUNDING": "Rebounding +/-"
    },
    hide_index=True
)
