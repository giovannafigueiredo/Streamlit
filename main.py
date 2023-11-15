
# Importing libraries
from streamlit_extras.metric_cards import style_metric_cards
import base64
from turtle import goto
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pydataset import data
import os
import warnings
import scipy as sp
import plotly.figure_factory as ff
import numpy as np
from millify import millify  # shortens values (10_000 ---> 10k)
import altair as alt
import sqlite3

#df = conn.query("select * from mytable")


warnings.filterwarnings("ignore")


# File uploader
st.set_page_config(page_title="Formula 1",
                  page_icon="🏁", layout="wide")


st.markdown(
    '<style>div.block-container{padding-top:1rem;</style>', unsafe_allow_html=True)


header = st.container()
dataset = st.container()
features = st.container()
interactive = st.container()


with header:
    st.title('Welcome to the F1 22 dashboard!')
    st.text(
        'In this dashboard you can visualize the data generated by you after racing.')

with dataset:
    st.header('F1 Dataset')

# File Selector Player 1


folder_path = r"C:\Users\giova\Downloads\PythonProjectStreamlit\Streamlit\Data"
filenames = os.listdir(folder_path)
# select file 1
selected_filename = st.selectbox('Select the first file:', filenames, key=1)
filename = os.path.join(folder_path, selected_filename)

# Select file 2
selected_filename2 = st.selectbox('Select the second file:', filenames, key=2)
filename2 = os.path.join(folder_path, selected_filename2)

# st.write('You selected `%s`' % filename)

df = pd.read_csv(filename, sep='\t')
df['velocity_X_kmh'] = df['velocity_X'] * 3.6
# st.dataframe(df, use_container_width=True)


# Column selection
data = {}
for i in range(20):
    col = f'col{i}'
    data[col] = range(10)
df = pd.DataFrame(df)
df = df[:-1]

columns = st.multiselect("Columns:", df.columns)
filter = st.radio("Choose by:", ("Columns that I want to check",
                  "Columns that I do not want to check"))

if filter == "Columns that I do not want to check":
    columns = [col for col in df.columns if col not in columns]

df[columns]

# Setting up the metric cards with css

col1, col2, col3 = st.columns(3)


with col1:
    st.markdown(
        f"""
        <div style="text-align: center; padding: 10px; background-color: white; 
                    box-shadow: 2px 2px 5px gray; border-left: 6px solid #33a6ddd9;
                    border-radius: 7px;">
            <h3 style="color: #1f77b4; font-weight: bold;"> ⏱️Speed</h3>
            <p style="font-size: 24px; color: #1f77b4; font-weight: bold;">
                {df.velocity_X_kmh.values[0]}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        f"""
        <div style="text-align: center; padding: 10px; background-color: white; 
                    box-shadow: 2px 2px 5px gray; border-left: 6px solid #dda133d9;
                    border-radius: 7px;">
            <h3 style="color: #ff7f0e; font-weight: bold;">⏳ Time</h3>
            <p style="font-size: 24px; color: #ff7f0e; font-weight: bold;">
                {df.lap_time.values[0]}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        f"""
        <div style="text-align: center; padding: 10px; background-color: white; 
                    box-shadow: 2px 2px 5px gray; border-left: 6px solid #2ed133;
                    border-radius: 7px;">
            <h3 style="color: #2ca02c; font-weight: bold;">🔁 Laps</h3>
            <p style="font-size: 24px; color: #2ca02c; font-weight: bold;">
                {df.binIndex.values[0]}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
# Plortting the speed per lap player 1
st.subheader('Average Speed Per Lap')
# AvgPerLap = df.groupby(by="lapNum")["velocity_X_kmh"].mean()
AvgPerLapFig2 = px.bar(df, x="lapNum", y="velocity_X_kmh")
st.write(AvgPerLapFig2)
# line plot
st.subheader('Speed per Lap')
speed_per_lap = px.line(df, x="binIndex", y="velocity_X_kmh", color='lapNum')
speed_per_lap.update_layout(width=800)
st.write(speed_per_lap)

# line plot
st.subheader('Lap time')
time_per_lap = df.groupby(by="lapNum")["lap_time"].max()
st.write(time_per_lap[:-1])

st.subheader('Fastest Lap')
fastest_lap = time_per_lap[1:-1].min()
st.write(fastest_lap)

average_time_per_lap = px.line(
    df, x="lap_time", y="binIndex", color='lapNum')
speed_per_lap.update_layout(width=800)
st.write(average_time_per_lap)


with features:
    st.header('F1 Dataset')
    # st.markdown('* **First** feature I am adding to this app')
    # st.markdown('* **Second** feature I am adding to this app')

