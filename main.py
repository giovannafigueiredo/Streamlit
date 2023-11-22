
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
import matplotlib.image as mpimg
from PIL import Image
import mysql.connector

#df = conn.query("select * from mytable")
warnings.filterwarnings("ignore")
# File uploader
st.set_page_config(page_title="Formula 1",
                  page_icon="🏁", layout="wide")

st.markdown(
    '<style>div.block-container{padding-top:1rem; text-align: center;</style>',  unsafe_allow_html=True)

header = st.container()
dataset = st.container()
features = st.container()
interactive = st.container()

with header:
    st.title('Welcome to the F1 22 dashboard')
    
# Set up sidebar
st.sidebar.title("File Selector Player 1")

# File Selector
folder_path = r"C:\Users\giova\Downloads\PythonProjectStreamlit\Streamlit\Data"
filenames = os.listdir(folder_path)

# select file 1
selected_filename = st.sidebar.selectbox('Select the first file:', filenames, key=1)
filename = os.path.join(folder_path, selected_filename)

# Select file 2
selected_filename2 = st.sidebar.selectbox('Select the second file:', filenames, key=2)
filename2 = os.path.join(folder_path, selected_filename2)

# st.sidebar.write('You selected `%s`' % filename)

# Read data from selected file
df = pd.read_csv(filename, sep='\t')

# Select Lap numbers bigger than lap 0
df = df[df['lapNum'] > 0]

# Convert the speed to km/h
df['velocity_X_kmh'] = df['velocity_X'] * 3.6

# Convert the time to seconds 
df['Time'] = pd.to_datetime(df.lap_time, unit='s').dt.time.astype(str).str[3:-3]

# Get the number of laps (using Max() so it will get the last lap number)
TotalLaps = df['lapNum'].max()

# Get top speed using the velocity in km/h defined previously and rounding it
TopSpeed = df['velocity_X_kmh'].max().round(2)

# Finding out the time spent per lap and then getting the lap that took less time using Min()
time_per_lap = df.groupby(by="lapNum")["Time"].max()
fastest_lap = time_per_lap.min()

# st.dataframe(df, use_container_width=True)

# Column selection
data = {}
for i in range(20):
    col = f'col{i}'
    data[col] = range(10)
df = pd.DataFrame(df)
df = df[:-1]

# Columns and filter selection in the sidebar
columns = st.sidebar.multiselect("Columns:", df.columns)
filter = st.sidebar.radio("Choose by:", ("View specific columns", "View dataset"))

if filter == "View dataset":
    columns = [col for col in df.columns if col not in columns]

# Display the selected columns in the main area
st.write(df[columns])

# Setting up the metric cards with css

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div style="text-align: center; padding: 10px; background-color: white; 
                    box-shadow: 2px 2px 5px gray; border-left: 6px solid #33a6ddd9;
                    border-radius: 7px;">
            <h3 style="color: #1f77b4; font-weight: bold;"> ⏱️Top Speed</h3>
            <p style="font-size: 24px; color: #1f77b4; font-weight: bold;">
                {TopSpeed}
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
            <h3 style="color: #ff7f0e; font-weight: bold;">⏳ Fastest Lap Time</h3>
            <p style="font-size: 24px; color: #ff7f0e; font-weight: bold;">
                {fastest_lap}
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
            <h3 style="color: #2ca02c; font-weight: bold;">🔁 Total Laps</h3>
            <p style="font-size: 24px; color: #2ca02c; font-weight: bold;">
                {TotalLaps}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.text("")
    st.text("")

# Creating and if statement to display the car images accorinf to to the cardID
def display_car_image(df):
    st.subheader('Car')
    if df.iloc[0, 0] == 'Ferrari':
        st.image('img/anything.gif', caption='Ferrari', use_column_width=True)
    elif df.iloc[0, 0] == 'Aston Martin':
        st.image('img/aston_martin.png', caption='Aston Martin', use_column_width=True)
    elif df.iloc[0, 0] == 'Red Bull':
        st.image('img/redbull.png', caption='Red Bull', use_column_width=True)
    else:
        st.write('No image available.')

# Creating tabs to display the player information
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Car Details", "Speed Variation", "Time Per Lap", "Velocity in Km/h", "Brake Percentage", "Throttle Percentage", "RPM"])
css = '''
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:1.15rem; gap: 2px;
    }
</style>
'''

st.markdown(css, unsafe_allow_html=True)

# Display car image in tab1
with tab1:
    display_car_image(df)

# Display content in other tabs
with tab2:
    st.subheader("Speed Variation Per Lap")
    # line plot
    speed_per_lap = px.line(df, x="binIndex", y="velocity_X_kmh", color='lapNum')
    speed_per_lap.update_layout(width=800)
    tab2.write(speed_per_lap)

with tab3:
   
    #Time spent per lap
    st.subheader('Time Spent Per Lap')
    Time_per_lap = df.groupby(by="lapNum")["Time"].max()
    tab3.write(time_per_lap[:-1])
    
    st.subheader('Average Time Per Lap')
    average_time_per_lap = px.line(
    df, x="lap_time", y="binIndex", color='lapNum')
    speed_per_lap.update_layout(width=800)
    tab3.write(average_time_per_lap)

with tab4:
    st.subheader("Velocity in Km/h Per Lap ")
# Plortting the speed per lap player 1
    AvgPerLap = df.groupby(by="lapNum", as_index=False)["velocity_X_kmh"].mean()
    AvgPerLapFig2 = px.bar(AvgPerLap, x="lapNum", y="velocity_X_kmh")
    AvgPerLapFig2.update_xaxes(showline=True, linewidth=1.5, linecolor='black'
                 )
    tab4.write(AvgPerLapFig2)

with tab5:
    st.subheader("Brake Percentage")

    # Create a Plotly line plot for Brake Percentage
    brakeplot = px.line(df, x='lap_distance', y='brake', color='lapNum')
    brakeplot.update_layout(width=800, height=600)
    st.write(brakeplot)

with tab6:
    st.subheader("Throttle Percentage")

    # Selectbox to choose the lap number
    selected_lap_throttle = st.selectbox("Select Lap Number", df['lapNum'].unique(), key=6)

    # Filter DataFrame based on selected lap number
    filtered_df_throttle = df[df['lapNum'] == selected_lap_throttle]

    # Create a Plotly line plot for Throttle Percentage
    throttleplot = px.line(filtered_df_throttle, x='lap_distance', y='throttle', title='Throttle Percentage over the Lap')
    throttleplot.update_layout(width=800, height=600)
    st.write(throttleplot)

with tab7:
    st.subheader("RPM")
    # Create a Plotly line plot
    rpmplot = px.line(df, x='lap_distance', y='rpm')
    st.plotly_chart(rpmplot)


