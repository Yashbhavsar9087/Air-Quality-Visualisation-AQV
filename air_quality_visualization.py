##############################################################################################################################################################################################################################################################################
########## import libraries as per required ##################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################

import base64
import plotly
import numpy as np
import pandas as pd
import streamlit as st
from plotly import tools
import plotly.offline as py
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
import streamlit.components.v1 as components

import plotly.express as px
from dotenv import load_dotenv
import os

##############################################################################################################################################################################################################################################################################

# Load environment variables from .env file
load_dotenv()

# Fetch the Mapbox token from the environment variable
mapbox_token = os.getenv('MAPBOX_TOKEN')

#################

##############################################################################################################################################################################################################################################################################
########## STREAMLIT START ###################################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################

st.set_page_config(layout="wide")

st.title("**Air Quality Visualisation (AQV)**")
st.write("BY JAY MUNJAPARA | ISHA PATEL | JENIL KANANI | YASH BHAVSAR")
st.image('img/air_quality.jpg')

##############################################################################################################################################################################################################################################################################

st.title("**WHAT AIR QUALITY INDEX VALUE SAY?**")
st.write("Find out what AQI values say about the possible health impacts given to you by air pollution.")

c1, c2, c3 = st.columns((1,5,1))
with c2:
    st.image('img/aqi.png')

##############################################################################################################################################################################################################################################################################
########### AQV for Metropolitian Cities #####################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################

st.title("**Air Quality Visualisation for Metropolitian Cities, India**")
st.write("Air quality index (AQI) along with air pollution, Health Condition and Demographic data near")

########## CITY - DATA #######################################################################################################################################################################################################################################################

city = st.selectbox("City: ", ['MUMBAI', 'KOLKATA', 'CHENNAI', 'DELHI'])

px.set_mapbox_access_token(mapbox_token)

########## READ CSV DATA #####################################################################################################################################################################################################################################################

df = pd.read_csv("datasets/{}_DATA.csv".format(city))

########## Downloading csv file ###############################################################################################################################################################################################################################################

if st.checkbox('Show Data'):
    st.subheader("{}_DATA.csv".format(city))
    st.dataframe(df)
    coded_data = base64.b64encode(df.to_csv(index = False).encode()).decode()
    st.markdown(f'<a href="data:file/csv;base64,{df}" download = "{city}_DATA.csv">Download csv file</a>', unsafe_allow_html = True)

########## 3D GRAPH PLOT #####################################################################################################################################################################################################################################################

X = df[['AQI', 'Population', 'Health', 'Latitude', 'Longitude']]

pca = PCA(n_components=3)
components = pca.fit_transform(X)

total_var = pca.explained_variance_ratio_.sum() * 100

fig_3d = px.scatter_3d(
    df, x='AQI', y='Population', z='Health', color='AQI',
    color_continuous_scale=[[0, 'green'], [0.2, 'yellow'],[0.4, 'red'], [0.6, 'rgb(128,0,128)'], [1.0, 'rgb(191,30,46)']], 
    hover_name='Area', hover_data=['AQI', 'Population', 'Health', 'Area'],
)

fig_3d.update_layout(
    margin=dict(l=25, r=150, t=25, b=25),
    # paper_bgcolor="LightSteelBlue",
)

########## 2D GRAPH PLOT #####################################################################################################################################################################################################################################################

fig_2d = px.scatter_mapbox(
    df, lat="Latitude", lon="Longitude", color="AQI", size="Population",
    color_continuous_scale=[[0, 'green'], [0.2, 'yellow'],[0.4, 'red'], [0.6, 'rgb(128,0,128)'], [1.0, 'rgb(191,30,46)']], 
    size_max=15, zoom=10, hover_name = "Area", hover_data = ['AQI', 'Population', 'Health', 'Area']
)

fig_2d.update_layout(
    margin=dict(l=10, r=200, t=10, b=10),
    # paper_bgcolor="LightSteelBlue",
)

########### PLOTTING GRAPHS ##################################################################################################################################################################################################################################################

c1, c2 = st.columns((1.1,1))

with c1:
    st.subheader('3D Graph')
    st.plotly_chart(fig_3d)

with c2:
    st.subheader('2D Graph')
    st.plotly_chart(fig_2d)

st.success("Graph Plotted, Successfully!!")

##############################################################################################################################################################################################################################################################################
########### METROPOLITIAN AIR POLLUTANTS values ##############################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################

df = pd.read_csv("datasets/METROPOLITIAN_AIR_DATA.csv")

st.write("")
st.write("")
st.write("")

st.title("**What are AIR POLLUTANTS values of METROPOLITIAN CITIES**")
st.write("Find out what AIR POLLUTANTS say about the possible health impacts, present in air pollution.")

fig_air = go.Figure()

fig_air.add_trace(go.Bar(
    x=df["Area"],
    y=df["AQI"],
    name='AQI',
    marker={'color': '#1DB261'}
))
fig_air.add_trace(go.Bar(
    x=df["Area"],
    y=df["PM2.5"],
    name='PM 2.5',
    marker={'color': '#FFC20F'}
))
fig_air.add_trace(go.Bar(
    x=df["Area"],
    y=df["PM10"],
    name='PM 10',
    marker={'color': '#0080C7'}
))
fig_air.add_trace(go.Bar(
    x=df["Area"],
    y=df["O3"],
    name='O3',
    marker={'color': '#285CA5'}
))
fig_air.add_trace(go.Bar(
    x=df["Area"],
    y=df["NO2"],
    name='NO2',
    marker={'color': '#57409A'}
))
fig_air.add_trace(go.Bar(
    x=df["Area"],
    y=df["SO2"],
    name='SO2',
    marker={'color': '#A52677'}
))
fig_air.add_trace(go.Bar(
    x=df["Area"],
    y=df["CO"],
    name='CO',
    marker={'color': '#F36523'}
))

fig_air.update_layout(
    autosize=False,
    barmode='group', #xaxis_tickangle=-45,
    # title= "'PM 2.5' and 'PM 10' values of cities in {}".format(states),
    width = 820,
    height = 700,
    bargap = 0.25, # gap between bars of adjacent location coordinates.
    bargroupgap = 0 # gap between bars of the same location coordinate.
)
fig_air.update_yaxes(automargin=True)

##############################################################################################################################################################################################################################################################################
########### METROPOLITIAN DEMOGRAPHIC values #################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################

fig_demo = go.Figure()

fig_demo.add_trace(go.Bar(
    x=df["Area"],
    y=df["Health"],
    name='Health',
    marker={'color': '#FFC20F'}
))
fig_demo.add_trace(go.Bar(
    x=df["Area"],
    y=df["Population"],
    name='Population',
    marker={'color': '#005050'}
))

fig_demo.update_layout(
    autosize=False,
    barmode='group', #xaxis_tickangle=-45,
    # title= "'PM 2.5' and 'PM 10' values of cities in {}".format(states),
    width = 450,
    height = 700,
    bargap = 0.25, # gap between bars of adjacent location coordinates.
    bargroupgap = 0 # gap between bars of the same location coordinate.
)
fig_demo.update_yaxes(automargin=True)

##############################################################################################################################################################################################################################################################################

c1, c2 = st.columns((1.5,1))

with c1:
    st.plotly_chart(fig_air)
with c2:
    st.plotly_chart(fig_demo)

st.write("")
st.write("")
st.write("")

##############################################################################################################################################################################################################################################################################

##############################################################################################################################################################################################################################################################################
########### AQV for Most Air Polluted States #################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################

st.title("**Air Quality Visualisation for Most Air Polluted States in India**")
st.write("Air quality index (AQI) along with air pollution, Health Condition and Demographic data near")

########## CITY - DATA #######################################################################################################################################################################################################################################################


states = st.selectbox("States: ", ['ANDHRA PRADESH', 'BIHAR', 'GUJARAT', 'KARNATAKA', 'MADHYA PRADESH', 'MAHARASHTRA', 'RAJASTHAN', 'TAMIL NADU', 'UTTAR PRADESH', 'WEST BENGAL'])

px.set_mapbox_access_token(mapbox_token)

########## READ CSV DATA #####################################################################################################################################################################################################################################################

df = pd.read_csv("datasets/{}_DATA.csv".format(states))

########## Downloading csv file ###############################################################################################################################################################################################################################################

if st.checkbox('Show Data:'):
    st.subheader("{}_DATA.csv".format(states))
    st.dataframe(df)
    coded_data = base64.b64encode(df.to_csv(index = False).encode()).decode()
    st.markdown(f'<a href="data:file/csv;base64,{df}" download = "{states}_DATA.csv">Download csv file</a>', unsafe_allow_html = True)

########## 3D GRAPH PLOT #####################################################################################################################################################################################################################################################

X = df[['AQI', 'Population', 'Health', 'Latitude', 'Longitude']]

pca = PCA(n_components=3)
components = pca.fit_transform(X)

total_var = pca.explained_variance_ratio_.sum() * 100

fig_3d = px.scatter_3d(
    df, x='AQI', y='Population', z='Health',
    color='AQI',color_continuous_scale=[[0, 'green'], [0.2, 'yellow'],[0.4, 'red'], [0.6, 'rgb(128,0,128)'], [1.0, 'rgb(191,30,46)']], 
    hover_name='Area', hover_data=['AQI', 'Population', 'Health', 'Area'],
)

fig_3d.update_layout(
    margin=dict(l=25, r=150, t=25, b=25),
)

########## 2D GRAPH PLOT #####################################################################################################################################################################################################################################################

fig_2d = px.scatter_mapbox(
    df, lat="Latitude", lon="Longitude", color="AQI", size="Population",
    color_continuous_scale=[[0, 'green'], [0.2, 'yellow'],[0.4, 'red'], [0.6, 'rgb(128,0,128)'], [1.0, 'rgb(191,30,46)']], 
    size_max=15, zoom=5, hover_name = "Area", hover_data = ["Health"]
)

fig_2d.update_layout(
    margin=dict(l=10, r=200, t=10, b=10),
)

########### PLOTTING GRAPHS ##################################################################################################################################################################################################################################################

c1, c2 = st.columns((1.1,1))

with c1:
    st.subheader('3D Graph')
    st.plotly_chart(fig_3d)

with c2:
    st.subheader('2D Graph')
    st.plotly_chart(fig_2d)

st.success("Graph Plotted, Successfully!!")

##############################################################################################################################################################################################################################################################################
########### 'AQV', 'PM 2.5'  and 'PM 10' values OF STATES ####################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################

st.write("")
st.title("**What are 'AQV', 'PM 2.5' and 'PM 10' values of cities in {}**".format(states))
st.write("Find out what 'AQV', 'PM 2.5' and 'PM 10' say about the possible health impacts, present in air pollution.")

fig = go.Figure()

fig.add_trace(go.Bar(
    x=df["Area"],
    y=df["PM2.5"],
    name='PM 2.5',
    marker={'color': '#F7941D'}
))
fig.add_trace(go.Bar(
    x=df["Area"],
    y=df["PM10"],
    name='PM 10',
    marker={'color': '#FEF200'}
))
fig.add_trace(go.Bar(
    x=df["Area"],
    y=df["AQI"],
    name='AQI',
    marker={'color': '#1DB261'}
))

fig.update_layout(
    autosize=False,
    barmode='group', xaxis_tickangle=-45,
    # title= "'PM 2.5' and 'PM 10' values of cities in {}".format(states),
    width = 1300,
    height = 700,
    bargap = 0.25, # gap between bars of adjacent location coordinates.
    bargroupgap = 0 # gap between bars of the same location coordinate.
)
fig.update_yaxes(automargin=True)

st.plotly_chart(fig)

##############################################################################################################################################################################################################################################################################
########## AIR POLLUTANTS ####################################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################

st.title("**WHAT DOES AIR POLLUTANTS SAY?**")
st.write("Find out what 'air pollutants' say about the possible health impacts given to you by air pollution.")
st.image('img/air_pollutants.jpg')

##############################################################################################################################################################################################################################################################################
########## Air Quality and Pollution Measurement #############################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################

st.write("")

c1, c2, c3 = st.columns((1,5,1))
with c2:
    st.title("**About the Air Quality and Pollution Measurement**")
    st.write("")
    st.write("")
    st.write("")

c1, c2 = st.columns((0.9,1.3))

with c1:
    st.image('img/aqi_chart.png')
with c2:
    st.image('img/aqi_guide.png')

st.write("")

col1, col2, col3 = st.columns([1,10,1])

with col1:
    st.write("")

with col2:
    st.write("To know more about Air Quality and Pollution, check " + str('[Air Pollution [wikipedia]](https://en.wikipedia.org/wiki/Air_pollution)') + " or "  + str('[the guide to Air Quality and Your Health [airnow].](https://www.airnow.gov/aqi/aqi-basics/)'))
    st.write("For very useful health tips to Cope with Air Pollution and Stay Safe, check " + str('[www.aqi.in/blog/aqi-india-tips-cope-air-pollution-stay-safe/ [AQI India]](https://www.aqi.in/blog/aqi-india-tips-cope-air-pollution-stay-safe/)') + " blog.")

with col3:
    st.write("")

##############################################################################################################################################################################################################################################################################

##############################################################################################################################################################################################################################################################################
########## STREAMLIT END #####################################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################
