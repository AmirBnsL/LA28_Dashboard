import streamlit as st
import pandas as pd
import utils
from components.overview_metrics import render_overview_metrics
from components.overview_medal_distribution import render_overview_medal_distribution
from components.overview_top_standings import render_overview_top_standings

st.set_page_config(page_title="LA28 Overview", page_icon="🏠", layout="wide")

# Load data
df_athletes, df_medals, df_events, df_nocs = utils.load_data()

if df_athletes is None:
    st.stop()

# Sidebar
selected_countries, selected_sports, selected_medal_types = utils.sidebar_filters(df_athletes, df_events, df_nocs)

# --- Filtering Logic ---

filtered_athletes, filtered_nocs, filtered_events, filtered_medals = utils.filter_data(
    df_athletes, df_nocs, df_events, df_medals, selected_countries, selected_sports
)

# --- KPI Metrics ---

render_overview_metrics(
    filtered_athletes,
    filtered_nocs,
    filtered_events,
    filtered_medals,
    selected_medal_types
)

# --- Visualizations ---

col_charts_1, col_charts_2 = st.columns(2)

# 1. Global Medal Distribution (Pie/Donut)
with col_charts_1:
    render_overview_medal_distribution(filtered_medals, selected_medal_types)

# 2. Top 10 Medal Standings (Horizontal Bar)
with col_charts_2:
    render_overview_top_standings(filtered_medals, selected_medal_types)
