# IMPORTS ----------------------------------------------------------------------

import pandas as pd
import numpy as np
# import matplotlib
# matplotlib.use("Agg")
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_agg import RendererAgg
# from matplotlib.figure import Figure
import seaborn as sns
# import statsmodels
from itertools import combinations
# from statsmodels.nonparametric.smoothers_lowess import lowess
import streamlit as st
# from st_mui_table import st_mui_table

# SETUP ------------------------------------------------------------------------
st.set_page_config(page_title='UWW Mens Basketball Data',
                   page_icon='https://pbs.twimg.com/profile_images/'\
                             '1265092923588259841/LdwH0Ex1_400x400.jpg',
                   layout="wide")

# st.subheader('')

stats = pd.read_csv("https://github.com/fritschcm272/UWW_MensBBALL/blob/main/warhawks_lineups.csv?raw=true")
# stats = pd.read_csv(r"C:\Users\frits\OneDrive\Documents\UWW MBB\warhawks_lineups.csv")


# scouts = pd.read_csv(r"C:\Users\frits\OneDrive\Documents\UWW MBB\scouts.csv")

# ##### Merge Scouts
# stats['OPP_LINEUP_PLAYER'] = stats["OPP_LINEUP"].str.split(";")
# stats = stats.explode("OPP_LINEUP_PLAYER")
# stats['copy_index'] = stats.index
# stats = pd.merge(stats,scouts, how='left',left_on=['Opponent','OPP_LINEUP_PLAYER'],right_on=['team','name'])
# stats[['shooter','driver']] = stats[['shooter','driver']].fillna(0)
# stats['num_shooters'] = stats.groupby(['copy_index'])['shooter'].cumsum()
# stats = stats.drop_duplicates(subset=['copy_index'], keep='last')
# # st.dataframe(stats)
# #####

stats['Date'] = pd.to_datetime(stats['Date'])
stats['Opponent'] = stats['Opponent'] + ' (' + stats['Date'].astype(str) + ')'



#### FILTERS ####

games_list = stats[['Opponent']]
games_list = list(games_list['Opponent'].drop_duplicates())

players_list = list(stats[(stats['Team']=='UWW')&
                           (stats['Play_Player']!='TEAM')]['Play_Player'].sort_values().drop_duplicates())
# players_list = list(full['UWW_LINEUP'].str.split(';',expand=True).stack().reset_index()[0].drop_duplicates().sort_values())

last3games = st.checkbox('Last 3 Games')

if last3games:
    games = st.multiselect("Choose Games", games_list, games_list[-3:])

else:
    games = st.multiselect("Choose Games", games_list)


games_list_search = '|'.join(games)
games_list_search = games_list_search.replace('(','').replace(')','') 

# games_list_search = '|'.join(games)
# games_list_search = games_list_search.replace(r"\(","")#.replace(r"\)","")

players = st.multiselect(
    "Choose Players On Court", players_list, #["China", "United States of America"]
)


if not games:
    
    stats = stats
    
else:
    
    
    stats = stats[(stats['Opponent'].str.replace('(','').str.replace(')','').str.contains(games_list_search))]
    
if not players:

    stats = stats

else:
    if len(players)==1:
        stats = stats[(stats['UWW_LINEUP'].str.contains(players[0]))]
    if len(players)==2:
        stats = stats[(stats['UWW_LINEUP'].str.contains(players[0])) & (stats['UWW_LINEUP'].str.contains(players[1]))]
    if len(players)==3:
        stats = stats[(stats['UWW_LINEUP'].str.contains(players[0])) & (stats['UWW_LINEUP'].str.contains(players[1]))& (stats['UWW_LINEUP'].str.contains(players[2]))]
    if len(players)==4:
        stats = stats[(stats['UWW_LINEUP'].str.contains(players[0])) & (stats['UWW_LINEUP'].str.contains(players[1]))& (stats['UWW_LINEUP'].str.contains(players[2]))& (stats['UWW_LINEUP'].str.contains(players[3]))]
    if len(players)==5:
        stats = stats[(stats['UWW_LINEUP'].str.contains(players[0])) & (stats['UWW_LINEUP'].str.contains(players[1]))& (stats['UWW_LINEUP'].str.contains(players[2]))& (stats['UWW_LINEUP'].str.contains(players[3]))& (stats['UWW_LINEUP'].str.contains(players[4]))]
    if len(players)>=6:
        st.error("Please only select up to five players.")
        stats = stats
        

        
########################
# three_more_shooters = st.checkbox('3 or More Shooters')

# if three_more_shooters:
#     stats = stats[stats['num_shooters']>=3]
#########################   
    
    

# stats = stats[stats.index <=34 ]
# st.dataframe(stats)

#### ADDITIONAL STATS #######

stats['Rebounds'] = stats['REBOUND OFF'] + stats['REBOUND DEF'] + stats['REBOUND DEADB']

#### INITIAL GROUPING ####

stats_possessions = stats.groupby(['Date','Opponent','Half','Time Remaining','UWW_LINEUP','Team','OPP_LINEUP']).agg({
                                                     'MinutesOnCourt': 'sum',
                                                     'Possession': 'sum',
                                                     'PTS_SCORED': 'sum',
                                                     'Rebounds': 'sum',
                                                     'ASSIST': 'sum'
                                                     }).rename(columns=
     {'MinutesOnCourt':'Minutes',
      'Possession':'Off_Possessions',
      'PTS_SCORED':'Points',
      'ASSIST':'Assists'}).sort_values(['Date','Opponent','Half','Time Remaining'],ascending=[True,True,True,False]).reset_index()



stats_possessions['Off_Possessions_OPP'] = np.where(stats_possessions['Team']=='OPP',stats_possessions['Off_Possessions'],0)
stats_possessions['Off_Possessions'] = np.where(stats_possessions['Team']=='OPP',0, stats_possessions['Off_Possessions'])

stats_possessions['Points_OPP'] = np.where(stats_possessions['Team']=='OPP',stats_possessions['Points'],0)
stats_possessions['Points'] = np.where(stats_possessions['Team']=='OPP',0, stats_possessions['Points'])

stats_possessions['Rebounds_OPP'] = np.where(stats_possessions['Team']=='OPP',stats_possessions['Rebounds'],0)
stats_possessions['Rebounds'] = np.where(stats_possessions['Team']=='OPP',0, stats_possessions['Rebounds'])

stats_possessions['Assists_OPP'] = np.where(stats_possessions['Team']=='OPP',stats_possessions['Assists'],0)
stats_possessions['Assists'] = np.where(stats_possessions['Team']=='OPP',0, stats_possessions['Assists'])

stats_possessions = stats_possessions.groupby(['Date','Opponent','Half','Time Remaining','UWW_LINEUP','OPP_LINEUP']).sum().sort_values(['Date','Opponent','Half','Time Remaining'],ascending=[True,True,True,False]).reset_index()

stats_possessions['Points_Total'] = stats_possessions.groupby(['Opponent'])['Points'].cumsum()
stats_possessions['Points_Total_OPP'] = stats_possessions.groupby(['Opponent'])['Points_OPP'].cumsum()
stats_possessions['Score_Difference'] = stats_possessions['Points_Total'] - stats_possessions['Points_Total_OPP']
stats_possessions['Score_Difference_plus10'] = np.where(stats_possessions['Score_Difference']>=10,'Yes','No')
stats_possessions['Score_Difference_plus1_9'] = np.where((stats_possessions['Score_Difference']>=1)&(stats_possessions['Score_Difference']<=9),'Yes','No')
stats_possessions['Score_Difference_even'] = np.where(stats_possessions['Score_Difference']==0,'Yes','No')
stats_possessions['Score_Difference_minus1_9'] = np.where((stats_possessions['Score_Difference']<=-1)&(stats_possessions['Score_Difference']>=-9),'Yes','No')
stats_possessions['Score_Difference_minus10'] = np.where(stats_possessions['Score_Difference']<=-10,'Yes','No')

score_difference = st.selectbox('Select Score Difference', ['All','Up 10 or more','Up between 1 and 9','Tied','Down between 1 and 9','Down 10 or more'], 0)

if score_difference == 'Up 10 or more':
    stats_possessions = stats_possessions[stats_possessions['Score_Difference_plus10']=='Yes']

if score_difference == 'Up between 1 and 9':
    stats_possessions = stats_possessions[stats_possessions['Score_Difference_plus1_9']=='Yes']

if score_difference == 'Tied':
    stats_possessions = stats_possessions[stats_possessions['Score_Difference_even']=='Yes']

if score_difference == 'Down between 1 and 9':
    stats_possessions = stats_possessions[stats_possessions['Score_Difference_minus1_9']=='Yes']

if score_difference == 'Down 10 or more':
    stats_possessions = stats_possessions[stats_possessions['Score_Difference_minus10']=='Yes']

    
# st.dataframe(stats_possessions)

# stats_totals['Minutes'] = stats_totals['Minutes'] + stats_totals['Opp_Minutes']
# stats_totals['Points'] = stats_totals['Points']
# stats_totals['Points_PP'] = stats_totals['Points']/stats_totals['Off_Possessions']
# stats_totals['Opp_Points'] = stats_totals['Points'].shift(1)
# stats_totals['Plus_Minus_PP'] = (stats_totals['Points'] - stats_totals['Opp_Points']) / stats_totals['Off_Possessions']
# stats_totals['Rebounds'] = stats_totals['Rebounds']
# stats_totals['Opp_Rebounds'] = stats_totals['Rebounds'].shift(1)
# stats_totals['Rebounds_Plus_Minus_PP'] = (stats_totals['Rebounds'] - stats_totals['Opp_Rebounds']) /stats_totals['Off_Possessions']




# stats_totals = stats_totals[stats_totals['Team']=='UWW']



#### CHOOSE LINEUP LEVEL ####
num_players = st.selectbox('Select Number of Players', [1,2,3,4,5], 4)
# # if num_players == 1:
# #     comb_div = 5
# # if num_players == 2:
# #     comb_div = 10
# # if num_players == 3:
# #     comb_div = 10 
# # if num_players == 4:
# #     comb_div = 5
# # if num_players == 5:
# #     comb_div = 1

stats_possessions['Players'] = stats_possessions.UWW_LINEUP.str.split(';').apply(lambda r: list(combinations(r, num_players)))
stats_possessions = stats_possessions.explode('Players')


stats_games = stats_possessions.groupby(['Opponent','Players']).sum().reset_index()
stats_games['Games'] = 1
# st.dataframe(stats_games)




stats_totals = stats_games.groupby(['Players']).sum().reset_index()

###
stats_totals = stats_totals[stats_totals['Off_Possessions']>0]
stats_totals = stats_totals[stats_totals['Off_Possessions_OPP']>0]
###

stats_totals['Plus_Minus'] = stats_totals['Points'] - stats_totals['Points_OPP']
stats_totals['Off_Eff'] = (100 * ((stats_totals['Points']) / (stats_totals['Off_Possessions']))).fillna(0)
stats_totals['Def_Eff'] = (100 * ((stats_totals['Points_OPP']) / (stats_totals['Off_Possessions_OPP']))).fillna(0)



stats_totals['Reb_Plus_Minus'] = (stats_totals['Rebounds'] - stats_totals['Rebounds_OPP'])

stats_totals = stats_totals[['Players','Games','Minutes','Off_Possessions','Plus_Minus','Off_Eff','Def_Eff','Reb_Plus_Minus']]
# stats_totals = stats_totals.drop(columns=['Points','Assists',
#                                           'Rebounds','Rebounds_OPP',
#                                           'Off_Possessions_OPP','Points_OPP','Assists_OPP',
#                                           'Points_Total','Points_Total_OPP','Score_Difference',
#                                           'Half'])

stats_totals = stats_totals.sort_values(['Minutes'],ascending=[False])

cm = sns.light_palette('#462e88', as_cmap=True)

stats_totals_style = stats_totals.style.background_gradient(cmap=cm).set_precision(0)

st.write(stats_totals.dtypes)
st.dataframe(stats_totals_style,hide_index=True) #,height=700
# st.dataframe(stats_totals)


# st_mui_table(stats_totals,key="table2")


# import pandas as pd
# import streamlit as st
# from st_aggrid import JsCode, AgGrid, GridOptionsBuilder

# df=pd.DataFrame([{"orgHierarchy": 'A', "jobTitle": "CEO", "employmentType": "Permanent" },
#     { "orgHierarchy": 'A/B', "jobTitle": "VP", "employmentType": "Permanent" }])
# st.write(df)
# gb = GridOptionsBuilder.from_dataframe(df)
# gridOptions = gb.build()


# gridOptions["columnDefs"]= [
#     { "field": 'jobTitle' },
#     { "field": 'employmentType' },
# ]
# gridOptions["defaultColDef"]={
#       "flex": 1,
#     },
# gridOptions["autoGroupColumnDef"]= {
#     "headerName": 'Organisation Hierarchy',
#     "minWidth": 300,
#     "cellRendererParams": {
#       "suppressCount": True,
#     },
#   },
# gridOptions["treeData"]=True
# gridOptions["animateRows"]=True
# gridOptions["groupDefaultExpanded"]= -1
# gridOptions["getDataPath"]=JsCode(""" function(data){
#     return data.orgHierarchy.split("/");
#   }""").js_code

# r = AgGrid(
#     df,
#     gridOptions=gridOptions,
#     height=500,
#     allow_unsafe_jscode=True,
#     enable_enterprise_modules=True,
#     filter=True,
#     update_mode=GridUpdateMode.SELECTION_CHANGED,
#     theme="material",
#     tree_data=True
# )





# # import streamlit as st
# # from streamlit_modal import Modal
# # import streamlit.components.v1 as components
# # import pandas as pd
# # import numpy as np
# # import random

# # # import requests
# # # from bs4 import BeautifulSoup
# # import warnings
# # warnings.filterwarnings('ignore')
# # from datetime import timedelta


# # # st.title('UWW Mens Basketball Data')
# # st.set_page_config(layout="wide")#, title='UWW Mens Basketball Data')


# # def dataframe_with_selections(df):
# #     df_with_selections = df.copy()
# #     df_with_selections.insert(0, "Select", False)

# #     # Get dataframe row-selections from user with st.data_editor
# #     edited_df = st.data_editor(
# #         df_with_selections,
# #         hide_index=True,
# #         column_config={"Select": st.column_config.CheckboxColumn(required=True)},
# #         disabled=df.columns, 
# #     )

# #     # Filter the dataframe using the temporary column, then drop the column
# #     selected_rows = edited_df[edited_df.Select]
# #     return selected_rows.drop('Select', axis=1)



# # stats = pd.read_csv("https://github.com/fritschcm272/UWW_MensBBALL/blob/main/warhawks_stats.csv?raw=true")
# # stats['Date'] = pd.to_datetime(stats['Date'])
# # stats['Opponent'] = stats['Opponent'] + ' (' + stats['Date'].astype(str) + ')'


# # full = pd.read_csv("warhawks_lineups.csv")
# # # full = pd.read_csv("https://github.com/fritschcm272/UWW_MensBBALL/blob/main/warhawks_lineups.csv?raw=true")
# # full = full.sort_values(['UWW_LINEUP','Date'])
# # full['Date'] = pd.to_datetime(full['Date'])
# # full = full.sort_values('Date')
# # full['Opponent'] = full['Opponent'] + ' (' + full['Date'].astype(str) + ')'

# # games_list = full[['Opponent']]
# # games_list = list(games_list['Opponent'].drop_duplicates())

# # players_list = list(full['UWW_LINEUP'].str.split(';',expand=True).stack().reset_index()[0].drop_duplicates().sort_values())



# # last3games = st.checkbox('Last 3 Games')

# # if last3games:
# #     games = st.multiselect("Choose Games", games_list, games_list[-3:])

# # else:
# #     games = st.multiselect("Choose Games", games_list)


# # games_list_search = '|'.join(games)
# # games_list_search = games_list_search.replace('(','').replace(')','') 

# # players = st.multiselect(
# #     "Choose Players", players_list, #["China", "United States of America"]
# # )

# # num_players = st.selectbox("Number of Players to Analyze", [1, 2, 3, 4, 5], 0)


# # if not games:
    
# #     df = full
    
# # else:
    
# #     games_list_search = '|'.join(games)
# #     games_list_search = games_list_search.replace(r"\(","")#.replace(r"\)","")
# #     df = full[(full['Opponent'].str.replace('(','').str.replace(')','').str.contains(games_list_search))]
# #     stats = stats[(stats['Opponent'].str.replace('(','').str.replace(')','').str.contains(games_list_search))]
    
# # if not players:

# #     df_l = df

# # else:
# #     if len(players)==1:
# #         df_l = df[(df['UWW_LINEUP'].str.contains(players[0]))]
# #     if len(players)==2:
# #         df_l = df[(df['UWW_LINEUP'].str.contains(players[0])) & (df['UWW_LINEUP'].str.contains(players[1]))]
# #     if len(players)==3:
# #         df_l = df[(df['UWW_LINEUP'].str.contains(players[0])) & (df['UWW_LINEUP'].str.contains(players[1]))& (df['UWW_LINEUP'].str.contains(players[2]))]
# #     if len(players)==4:
# #         df_l = df[(df['UWW_LINEUP'].str.contains(players[0])) & (df['UWW_LINEUP'].str.contains(players[1]))& (df['UWW_LINEUP'].str.contains(players[2]))& (df['UWW_LINEUP'].str.contains(players[3]))]
# #     if len(players)==5:
# #         df_l = df[(df['UWW_LINEUP'].str.contains(players[0])) & (df['UWW_LINEUP'].str.contains(players[1]))& (df['UWW_LINEUP'].str.contains(players[2]))& (df['UWW_LINEUP'].str.contains(players[3]))& (df['UWW_LINEUP'].str.contains(players[4]))]
# #     if len(players)>=6:
# #         st.error("Please only select up to five players.")
# #         df_l = df
# #     # st.write("### 5 Man Lineups")
# #     # st.markdown(data.style.hide(axis="index").to_html(escape=False), unsafe_allow_html=True)
    
# # ########################################
# # st.header('Players', divider='gray')
# # df_p = df
# # df_p = df_p.explode('UWW_LINEUP')
# # df_p['UWW_LINEUP']=df_p['UWW_LINEUP'].str.split(';').fillna(df_p['UWW_LINEUP'])
# # df_p=df_p.explode('UWW_LINEUP',ignore_index=True)

# # ###
# # players_list_search = '|'.join(players)
# # df_p = df_p[(df_p['UWW_LINEUP'].str.contains(players_list_search))]
# # ###

# # df_p = df_p.groupby(['UWW_LINEUP','Opponent'], as_index=False).agg({
# #                                                      # 'Opponent': 'nunique',
# #                                                      'MinutesOnCourt': 'sum',
# #                                                      'UWW_PLUS_MINUS': 'sum',
# #                                                      # 'UWW_PLUS_MINUS_CUMSUM':lambda x: list(x),
# #                                                      'UWW_ASST_TURN': 'sum',
# #                                                      'UWW_REBOUNDING': 'sum'
# # })

# # df_p['UWW_PLUS_MINUS_CUMSUM'] = df_p.groupby('UWW_LINEUP')['UWW_PLUS_MINUS'].cumsum()

# # df_p = df_p.groupby(['UWW_LINEUP'], as_index=False).agg({
# #                                                      'Opponent': 'nunique',
# #                                                      'MinutesOnCourt': 'sum',
# #                                                      'UWW_PLUS_MINUS': 'sum',
# #                                                      'UWW_PLUS_MINUS_CUMSUM':lambda x: list(x),
# #                                                      'UWW_ASST_TURN': 'sum',
# #                                                      'UWW_REBOUNDING': 'sum'})

# # df_p = df_p.sort_values(['UWW_PLUS_MINUS','MinutesOnCourt'],ascending=[False,False])


# # stats = stats.groupby(['Play_Player'])[['Points','Field_Goals_Made',
# #                                                                                  'Field_Goals_Missed','3P_Field_Goals_Made','3P_Field_Goals_Missed',
# #                                                                                  'FT_Made','FT_Missed','Rebound_Off','Rebound_Def',
# #                                                                                  'Rebound_Total', 'Assists', 'Turnovers']].sum().reset_index()

# # # format(,".1%")
# # stats['fgpercent'] = (stats['Field_Goals_Made'] / (stats['Field_Goals_Made'] + stats['Field_Goals_Missed']))*100
# # stats['threeptpercent'] = (stats['3P_Field_Goals_Made'] / (stats['3P_Field_Goals_Made'] + stats['3P_Field_Goals_Missed']))*100
# # stats['ftpercent'] = (stats['FT_Made'] / (stats['FT_Made'] + stats['FT_Missed']))*100

# # # Merge in player stats table

# # df_p = pd.merge(df_p,stats, how='left', left_on='UWW_LINEUP', right_on='Play_Player')
                
                  
                

# # # df_p.insert(0, "Select", False)

# # # df_p['Photo'] = "https://uwwsports.com/images/2023/11/9/Jameer_Barker.jpg?width=40"


# # # col1, col2 = st.columns([3, 1])

# # # with col1:

    
# # st.dataframe(
# #     df_p[[
# #           'UWW_LINEUP',
# #           'Opponent',
# #           'MinutesOnCourt',
# #           'UWW_PLUS_MINUS',
# #           'UWW_PLUS_MINUS_CUMSUM',
# #           'UWW_ASST_TURN',
# #           'UWW_REBOUNDING',
# #           'Points',
# #           'fgpercent',
# #           'threeptpercent',
# #           'ftpercent'
# #          ]],
# #     column_config={
# #         # "Select": st.column_config.CheckboxColumn(required=True),
# #         "UWW_LINEUP":"Player",
# # #         "Photo": {st.write(321)},
# # #         # "": st.column_config.ImageColumn("Photo", help="The user's avatar"),
# # #         # "Photo":{"Player","Games"},

# # #         # "Photo": st.image('https://uwwsports.com/images/2023/11/9/Jameer_Barker.jpg?width=40'),
# #         "Opponent":"Games",
# #         "MinutesOnCourt": "Minutes",
# #         "UWW_PLUS_MINUS": "Current Points +/-",
# #         "UWW_PLUS_MINUS_CUMSUM": st.column_config.LineChartColumn(
# #             "Trending +/-", 
# #             # y_min= 0,#min_pm, 
# #             # y_max= max_pm
# #         ),
# #         "UWW_ASST_TURN": "Assist/Turnover",
# #         "UWW_REBOUNDING": "Rebounding +/-",
# #         "Points": "Points Scored",
# #         "fgpercent": st.column_config.NumberColumn('FG %', format='%.1f %%'),
# #         "threeptpercent": st.column_config.NumberColumn('3PT FG %', format='%.1f %%'),
# #         "ftpercent": st.column_config.NumberColumn('FT %', format='%.1f %%')
        
# #     },
# #     hide_index=True
# # )


# # if len(players) == 1:
# #     stats = stats[stats['Play_Player']==players[0]].reset_index()


    



# #     modal = Modal(
# #         "Player Details", 
# #         key="demo-modal",

# #         # Optional
# #         padding=20,    # default value
# #         max_width=744  # default value
# #     )

# #     open_modal = st.button("Player Details")
# #     if open_modal:
# #         modal.open()

# #     if modal.is_open():
# #         with modal.container():

# #     #         st.write("Text goes here")

# #     #         html_string = '''
# #     #         <h1>HTML string in RED</h1>

# #     #         <script language="javascript">
# #     #           document.querySelector("h1").style.color = "red";
# #     #         </script>
# #     #         '''
# #     #         components.html(html_string)

# #     #         st.write("Some fancy text")
# #     #         value = st.checkbox("Check me")
# #     #         st.write(f"Checkbox checked: {value}")




# #             # st.header('Player Details', divider='gray')

# #             col1, col2 = st.columns(2)

# #             col1.image('https://uwwsports.com/images/2023/11/9/Miles_Barnstable.jpg?width=80&quality=90')
# #             col2.text('Miles Barnstable')


# #             col1, col2, col3 = st.columns(3)
# #             col1.metric("Points", stats['Points'][0])# df_l_tot_pm)
# #             col2.metric("FG %", stats['fgpercent'][0])
# #             col3.metric("3PT %", stats['threeptpercent'][0])# df_l_tot_reb)

# #             st.dataframe(stats)


# # ########################################
# # st.header('5 Man Lineups', divider='gray')
# # if not games:
# #     st.caption("Games: All")
# # else:
# #     st.caption("Games: "+','.join(games))
# # if not players:
# #     st.caption("Players: All")
# # else:
# #     st.caption("Players: "+'|'.join(players))





# # df_l['UWW_PLUS_MINUS_CUMSUM'] = df_l.groupby('UWW_LINEUP')['UWW_PLUS_MINUS'].cumsum()
# # min_pm = df_l['UWW_PLUS_MINUS_CUMSUM'].min()
# # max_pm = df_l['UWW_PLUS_MINUS_CUMSUM'].max()
# # df_l['UWW_LINEUP'] = df_l['UWW_LINEUP'].replace(';',' ; ', regex=True)
# # # df['UWW_LINEUP_PICS'] = df['UWW_LINEUP'].replace('*BARKER,JAMEER*', 'https://uwwsports.com/images/2023/11/9/Jameer_Barker.jpg?width=40', regex=True)
# # # replace("BARKER,JAMEER",'https://uwwsports.com/images/2023/11/9/Jameer_Barker.jpg?width=40')
# # df_l['Opponent'] = df_l['Opponent'] + ' (' + df_l['Date'].astype(str) + ')'
# # df_l = df_l.drop(columns=['Date'])
# # df_l = df_l.groupby(['UWW_LINEUP'], as_index=False).agg({'Opponent': 'count',
# #                                                      'MinutesOnCourt': 'sum',
# #                                                      'UWW_PLUS_MINUS': 'sum',
# #                                                      'UWW_PLUS_MINUS_CUMSUM':lambda x: list(x),
# #                                                      'UWW_ASST_TURN': 'sum',
# #                                                      'UWW_REBOUNDING': 'sum',
# #                                                      'UWW_FG_MADE': 'sum',
# #                                                      'UWW_FG_MISS': 'sum',
# #                                                      'UWW_GOOD 3PTR': 'sum',
# #                                                      'UWW_MISS 3PTR': 'sum',
# #                                                      'UWW_GOOD FT':'sum',
# #                                                      'UWW_MISS FT':'sum'})




# # df_l['fgpercent'] = (df_l['UWW_FG_MADE'] / (df_l['UWW_FG_MADE'] + df_l['UWW_FG_MISS']))*100
# # df_l['threeptpercent'] = (df_l['UWW_GOOD 3PTR'] / (df_l['UWW_GOOD 3PTR'] + df_l['UWW_MISS 3PTR']))*100
# # df_l['ftpercent'] = (df_l['UWW_GOOD FT'] / (df_l['UWW_GOOD FT'] + df_l['UWW_MISS FT']))*100

# # df_l = df_l.drop(columns=['UWW_FG_MADE',
# #                                                      'UWW_FG_MISS',
# #                                                      'UWW_GOOD 3PTR',
# #                                                      'UWW_MISS 3PTR',
# #                                                      'UWW_GOOD FT',
# #                                                      'UWW_MISS FT'])

# # df_l = df_l.sort_values(['UWW_PLUS_MINUS','MinutesOnCourt'],ascending=[False,False])



# # df_l_tot_moc = round(df_l['MinutesOnCourt'].sum(),2)
# # df_l_tot_pm = df_l['UWW_PLUS_MINUS'].sum()
# # df_l_tot_at = df_l['UWW_ASST_TURN'].sum()                      
# # df_l_tot_reb = df_l['UWW_REBOUNDING'].sum()




# # col1, col2, col3, col4 = st.columns(4)
# # col1.metric("Minutes", df_l_tot_moc) #col1.metric("Minutes", "70 °F", "1.2 °F")
# # col2.metric("Points +/-", df_l_tot_pm)
# # col3.metric("A/T Ratio", df_l_tot_at)
# # col4.metric("Reb +/-", df_l_tot_reb)


# # st.dataframe(
# #     df_l,
# #     column_config={
# #         "UWW_LINEUP":"Lineup",
# #         "Opponent":"Games",
# #         "MinutesOnCourt": "Minutes",
# #         "UWW_PLUS_MINUS": "Current Points +/-",
# #         "UWW_PLUS_MINUS_CUMSUM": st.column_config.LineChartColumn(
# #             "Trending +/-", 
# #             # y_min= 0,#min_pm, 
# #             # y_max= max_pm
# #         ),
# #         "UWW_ASST_TURN": "Assist/Turnover",
# #         "UWW_REBOUNDING": "Rebounding +/-",
# #         # "Points": "Points Scored",
# #         "fgpercent": st.column_config.NumberColumn('FG %', format='%.1f %%'),
# #         "threeptpercent": st.column_config.NumberColumn('3PT FG %', format='%.1f %%'),
# #         "ftpercent": st.column_config.NumberColumn('FT %', format='%.1f %%')
        
# #     },
# #     hide_index=True
# # )






# # ########################################
# # st.header('Player Comparison', divider='gray')
# # if len(players)==2:
# #     df_comp_1 = df[(df['UWW_LINEUP'].str.contains(players[0])) & (~df['UWW_LINEUP'].str.contains(players[1]))]
# #     df_comp_2 = df[(df['UWW_LINEUP'].str.contains(players[1])) & (~df['UWW_LINEUP'].str.contains(players[0]))]
    
# #     if not games:
# #         st.caption("Games: All")
# #     else:
# #         st.caption("Games: "+','.join(games))
# #     if not players:
# #         st.caption("Players: All")
# #     else:
# #         st.caption("Players: "+'|'.join(players))
        
# #     df_comp_1['UWW_PLUS_MINUS_CUMSUM'] = df_comp_1.groupby('UWW_LINEUP')['UWW_PLUS_MINUS'].cumsum()
# #     min_pm = df_comp_1['UWW_PLUS_MINUS_CUMSUM'].min()
# #     max_pm = df_comp_1['UWW_PLUS_MINUS_CUMSUM'].max()
# #     df_comp_1['UWW_LINEUP'] = df_comp_1['UWW_LINEUP'].replace(';',' ; ', regex=True)
# #     df_comp_1['Opponent'] = df_comp_1['Opponent'] + ' (' + df_comp_1['Date'].astype(str) + ')'
# #     df_comp_1 = df_comp_1.drop(columns=['Date'])
# #     df_comp_1 = df_comp_1.groupby(['UWW_LINEUP'], as_index=False).agg({'Opponent': 'count',
# #                                                          'MinutesOnCourt': 'sum',
# #                                                          'UWW_PLUS_MINUS': 'sum',
# #                                                          'UWW_PLUS_MINUS_CUMSUM':lambda x: list(x),
# #                                                          'UWW_ASST_TURN': 'sum',
# #                                                          'UWW_REBOUNDING': 'sum'})
# #     df_comp_1 = df_comp_1.sort_values(['UWW_PLUS_MINUS','MinutesOnCourt'],ascending=[False,False])

# #     df_comp_1_tot_moc = round(df_comp_1['MinutesOnCourt'].sum(),2)
# #     df_comp_1_tot_pm = df_comp_1['UWW_PLUS_MINUS'].sum()
# #     df_comp_1_tot_at = df_comp_1['UWW_ASST_TURN'].sum()                      
# #     df_comp_1_tot_reb = df_comp_1['UWW_REBOUNDING'].sum()


# #     col1, col2, col3, col4, col5 = st.columns(5)
# #     col1.caption(players[0] + " without " + players[1])
# #     col2.metric("Minutes", df_comp_1_tot_moc) #col1.metric("Minutes", "70 °F", "1.2 °F")
# #     col3.metric("Points +/-", df_comp_1_tot_pm)
# #     col4.metric("A/T Ratio", df_comp_1_tot_at)
# #     col5.metric("Reb +/-", df_comp_1_tot_reb)
    
    
# #     df_comp_2['UWW_PLUS_MINUS_CUMSUM'] = df_comp_2.groupby('UWW_LINEUP')['UWW_PLUS_MINUS'].cumsum()
# #     min_pm = df_comp_2['UWW_PLUS_MINUS_CUMSUM'].min()
# #     max_pm = df_comp_2['UWW_PLUS_MINUS_CUMSUM'].max()
# #     df_comp_2['UWW_LINEUP'] = df_comp_2['UWW_LINEUP'].replace(';',' ; ', regex=True)
# #     df_comp_2['Opponent'] = df_comp_2['Opponent'] + ' (' + df_comp_2['Date'].astype(str) + ')'
# #     df_comp_2 = df_comp_2.drop(columns=['Date'])
# #     df_comp_2 = df_comp_2.groupby(['UWW_LINEUP'], as_index=False).agg({'Opponent': 'count',
# #                                                          'MinutesOnCourt': 'sum',
# #                                                          'UWW_PLUS_MINUS': 'sum',
# #                                                          'UWW_PLUS_MINUS_CUMSUM':lambda x: list(x),
# #                                                          'UWW_ASST_TURN': 'sum',
# #                                                          'UWW_REBOUNDING': 'sum'})
# #     df_comp_2 = df_comp_2.sort_values(['UWW_PLUS_MINUS','MinutesOnCourt'],ascending=[False,False])

# #     df_comp_2_tot_moc = round(df_comp_2['MinutesOnCourt'].sum(),2)
# #     df_comp_2_tot_pm = df_comp_2['UWW_PLUS_MINUS'].sum()
# #     df_comp_2_tot_at = df_comp_2['UWW_ASST_TURN'].sum()                      
# #     df_comp_2_tot_reb = df_comp_2['UWW_REBOUNDING'].sum()


# #     col1, col2, col3, col4, col5 = st.columns(5)
# #     col1.caption(players[1] + " without " + players[0])
# #     col2.metric("Minutes", df_comp_2_tot_moc) #col1.metric("Minutes", "70 °F", "1.2 °F")
# #     col3.metric("Points +/-", df_comp_2_tot_pm)
# #     col4.metric("A/T Ratio", df_comp_2_tot_at)
# #     col5.metric("Reb +/-", df_comp_2_tot_reb)

# # #     st.dataframe(
# # #         df_comp_1,
# # #         column_config={
# # #             "Opponent":"Games",
# # #             "MinutesOnCourt": "Minutes",
# # #             "UWW_PLUS_MINUS": "Current Points +/-",
# # #             "UWW_PLUS_MINUS_CUMSUM": st.column_config.LineChartColumn(
# # #                 "Trending +/-", 
# # #                 # y_min= 0,#min_pm, 
# # #                 # y_max= max_pm
# # #             ),
# # #             "UWW_ASST_TURN": "Assist/Turnover",
# # #             "UWW_REBOUNDING": "Rebounding +/-"
# # #         },
# # #         hide_index=True
# # #     )

# # else:
# #     st.subheader('_Available when 2 players are selected_')



