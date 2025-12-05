"""
Sports & Events Analysis Page - LA28 Dashboard
Explore the schedule, medal distribution by sport, and venue locations.
"""
import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.helpers import get_continent
from modules.data_loader import load_schedule_data, load_medals_data, load_venues_data

# Import components
from components.event_schedule import render_event_schedule
from components.medal_count_sport import render_medal_count_by_sport
from components.venues_map import render_venues_map
from components.global_medal_distribution import render_global_medal_distribution
from components.head_to_head import render_head_to_head
from components.who_won_the_day import render_who_won_the_day
from components.watch_highlights import render_watch_highlights


# -------------------------------------------------------
# Page Config
# -------------------------------------------------------

st.set_page_config(
    page_title="Sports & Events Analysis",
    page_icon="🏟️",
    layout="wide"
)

st.title("🏟️ Sports, Events & Venues")
st.markdown("Explore the schedule, medal distribution by sport, and venue locations of the Paris 2024 Games.")

# -------------------------------------------------------
# Data Loading
# -------------------------------------------------------

try:
    df_schedule = load_schedule_data()
    df_medals = load_medals_data()
    df_venues = load_venues_data()
except FileNotFoundError as e:
    st.error(f"❌ {e}")
    st.stop()

# Add continent to medals
df_medals["continent"] = df_medals["country"].apply(get_continent)
df_medals.sort_values(by=["country"], inplace=True)

# -------------------------------------------------------
# Sidebar Filters
# -------------------------------------------------------

st.sidebar.header("Global Filters")

all_countries_names = sorted(df_medals["country"].dropna().unique().astype(str))
selected_countries = st.sidebar.multiselect("Select Country", all_countries_names)

all_sports = sorted(df_schedule["discipline"].unique().astype(str))
selected_sports = st.sidebar.multiselect("Select Sport", all_sports)

if selected_sports:
    available_venues = df_schedule[df_schedule["discipline"].isin(selected_sports)]["venue"].dropna().unique()
else:
    available_venues = df_schedule["venue"].dropna().unique()

all_venues = sorted(available_venues.astype(str))
selected_venues = st.sidebar.multiselect("Select Venue", all_venues)

medal_types = ["Gold Medal", "Silver Medal", "Bronze Medal"]
selected_medals = st.sidebar.multiselect("Select Medal Type", medal_types, default=medal_types)

all_continents = sorted(df_medals["continent"].dropna().unique().tolist())
selected_continent = st.sidebar.selectbox(
    "Filter by Continent",
    all_continents,
    index=all_continents.index("Europe") if "Europe" in all_continents else 0,
)

# -------------------------------------------------------
# Render Components
# -------------------------------------------------------

# Event Schedule
render_event_schedule(df_schedule, selected_sports, selected_venues)
st.divider()

# Medal Count by Sport
render_medal_count_by_sport(df_medals, selected_medals, selected_countries, selected_sports)
st.divider()

# Venues Map
render_venues_map(df_venues)
st.divider()

# Global Medal Distribution
render_global_medal_distribution(df_medals, selected_medals, selected_continent)
st.divider()

# Head-to-Head Comparison
render_head_to_head(df_medals)
st.divider()

# Who Won the Day
render_who_won_the_day(df_medals, df_schedule)
st.divider()

# Watch Highlights
render_watch_highlights(df_schedule, df_medals)