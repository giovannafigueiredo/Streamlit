import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np
   
# List of Font Awesome icons
icons = ["fa-car", "fa-flag-checkered", "fa-trophy"]

# Set the page title and description

st.set_page_config(
    page_title="Formula 1 Dashboard",
    page_icon="🏁",
    layout="wide",
)


st.markdown(
    '<style>div.block-container{padding-top:1rem;</style>', unsafe_allow_html=True)

# Define KPIs
kpi1 = 123
kpi2 = 456
kpi3 = 789

# Create the Streamlit app
st.title("Formula 1 Dashboard")

# Create a portrait layout
st.markdown('<style> .reportview-container { flex-direction: column; } </style>', unsafe_allow_html=True)

# Create cards to display KPIs and plots inside styled boxes
st.markdown("### Key Performance Indicators (KPIs) and Plots")
col1, col2, col3 = st.columns(3)

# Define a CSS style for the boxes with a blue background
box_style = 'border: 5px solid rgb(104 187 195); border-radius: 30px; padding: 20px; background-color: rgb(71 138 175); color: white;font-size: 25px'

# Randomly select an icon for each column
random_icon = random.choice(icons)

with col1:
    st.markdown(f'<div style="{box_style}"><i class="fa {random_icon}"></i> Player Name: {kpi1}</div>', unsafe_allow_html=True)
    # Create a sample plot
    plt.figure(figsize=(4, 4))
    plt.plot(np.arange(10), np.random.rand(10))
    st.pyplot()

# Randomly select another icon for the second column
random_icon = random.choice(icons)

with col2:
    st.markdown(f'<div style="{box_style}"><i class="fa {random_icon}"></i> Car: {kpi2}</div>', unsafe_allow_html=True)
    # Create a different sample plot
    plt.figure(figsize=(4, 4))
    plt.plot(np.arange(10), np.random.rand(10), color='orange')
    st.pyplot()

# Randomly select yet another icon for the third column
random_icon = random.choice(icons)

with col3:
    st.markdown(f'<div style="{box_style}"><i class="fa {random_icon}"></i> Average Speed per Lap: {kpi3}</div>', unsafe_allow_html=True)
    # Create another sample plot
    plt.figure(figsize=(4, 4))
    plt.plot(np.arange(10), np.random.rand(10), color='green')
    st.pyplot()

