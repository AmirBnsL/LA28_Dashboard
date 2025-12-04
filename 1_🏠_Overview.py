import streamlit as st
import pandas as pd
import plotly.express as px
import utils

st.set_page_config(page_title="LA28 Overview", page_icon="🏠", layout="wide")

# Load data
df_athletes, df_medals, df_events, df_nocs = utils.load_data()

# Sidebar
selected_countries, selected_sports, medal_flags = utils.sidebar_filters(df_athletes)

st.title("🏅 Paris 2024 Olympic Games Overview")
st.info("Welcome to the LA28 Volunteer Selection Dashboard.")