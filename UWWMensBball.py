import streamlit as st
import pandas as pd
import numpy as np

# st.title('UWW Mens Basketball Data')
st.set_page_config(layout="wide")#, title='UWW Mens Basketball Data')




# @st.cache_data
# def get_UN_data():
#     # AWS_BUCKET_URL = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"
#     # df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
#     df = pd.read_csv("https://panthers-my.sharepoint.com/:x:/g/personal/fritschc_uwm_edu/EWfbnEaYFIpDsBMsbL_K2GkBXtknAvGdnlgYAToLwhapJA?e=e4JwLa")
#     return df.set_index("UWW_LINEUP")

# try:
df = pd.read_csv("https://github.com/fritschcm272/Auger_BBALL/blob/master/warhawks.csv?raw=true")
# df = df.set_index("UWW_LINEUP")

players_list = list(df['UWW_LINEUP'].str.split(';',expand=True).stack().reset_index()[0].drop_duplicates().sort_values())

df['UWW_LINEUP'] = df['UWW_LINEUP'].replace(';','<br>', regex=True)



players = st.multiselect(
    "Choose Players", players_list, #["China", "United States of America"]
)

if not players:
    # st.error("Please select at least one Player.")
    data = df
    st.write("### 5 Man Lineups")
    st.markdown(data.to_html(escape=False), unsafe_allow_html=True)
else:
    if len(players)==1:
        data = df[(df['UWW_LINEUP'].str.contains(players[0]))]# & (df['UWW_LINEUP'].str.contains('BARNSTABLE,MILES'))]
    if len(players)==2:
        data = df[(df['UWW_LINEUP'].str.contains(players[0])) & (df['UWW_LINEUP'].str.contains(players[1]))]
    if len(players)==3:
        data = df[(df['UWW_LINEUP'].str.contains(players[0])) & (df['UWW_LINEUP'].str.contains(players[1]))& (df['UWW_LINEUP'].str.contains(players[2]))]
    if len(players)==4:
        data = df[(df['UWW_LINEUP'].str.contains(players[0])) & (df['UWW_LINEUP'].str.contains(players[1]))& (df['UWW_LINEUP'].str.contains(players[2]))& (df['UWW_LINEUP'].str.contains(players[3]))]
    if len(players)==5:
        data = df[(df['UWW_LINEUP'].str.contains(players[0])) & (df['UWW_LINEUP'].str.contains(players[1]))& (df['UWW_LINEUP'].str.contains(players[2]))& (df['UWW_LINEUP'].str.contains(players[3]))& (df['UWW_LINEUP'].str.contains(players[4]))]
    if len(players)>=6:
        st.error("Please only select up to five players.")
        data = df
    st.write("### 5 Man Lineups")
    st.markdown(data.to_html(escape=False), unsafe_allow_html=True)

#     data = data.T.reset_index()
#     data = pd.melt(data, id_vars=["index"]).rename(
#         columns={"index": "year", "MinutesOnCourt": "UWW REBOUNDING"}
#     )
    
    
    
    
    
    # chart = (
    #     alt.Chart(data)
    #     .mark_area(opacity=0.3)
    #     .encode(
    #         x="year:T",
    #         y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
    #         color="Region:N",
    #     )
    # )
    # st.altair_chart(chart, use_container_width=True)
# except URLError as e:
#     st.error(
#         """
#         **This demo requires internet access.**
#         Connection error: %s
#     """
#         % e.reason
#     )