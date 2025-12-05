"""
Athlete Performance Page - LA28 Dashboard
Explore athlete profiles, demographics, and achievements.
"""
import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.data_loader import (
    load_athletes_data,
    load_coaches_data,
    load_teams_data,
    load_medallists_data
)
from modules.helpers import get_continent

# Import components
from components.athlete_profile import render_athlete_profile
from components.age_distribution import render_age_distribution
from components.gender_distribution import render_gender_distribution
from components.top_athletes import render_top_athletes
from components.athlete_summary import render_athlete_summary

# -------------------------------------------------------
# Page Config
# -------------------------------------------------------

st.set_page_config(
    page_title="Athlete Performance",
    page_icon="👤",
    layout="wide"
)

st.title("👤 Athlete Performance Analysis")
st.markdown("### Explore athlete profiles, demographics, and achievements")

# -------------------------------------------------------
# Data Loading
# -------------------------------------------------------

try:
    df_athletes = load_athletes_data()
    df_coaches = load_coaches_data()
    df_teams = load_teams_data()
    df_medallists = load_medallists_data()
except FileNotFoundError as e:
    st.error(f"❌ {e}")
    st.stop()

# -------------------------------------------------------
# Data Preprocessing
# -------------------------------------------------------

# Calculate age from birth_date
def calculate_age(birth_date):
    try:
        if pd.notna(birth_date):
            birth = pd.to_datetime(birth_date)
            age = 2025 - birth.year
            return age
    except:
        pass
    return None

df_athletes['age'] = df_athletes['birth_date'].apply(calculate_age)

# Add continent mapping using helper function
df_athletes['Continent'] = df_athletes['country'].apply(get_continent)

# -------------------------------------------------------
# Sidebar Filters
# -------------------------------------------------------

st.sidebar.header("🎯 Global Filters")

all_countries = sorted(df_athletes['country'].dropna().unique())
selected_countries = st.sidebar.multiselect("Select Countries", all_countries)

# Extract all unique sports from disciplines column
all_sports = sorted([sport.strip("[]'\" ") for sublist in df_athletes['disciplines'].dropna().unique() 
                     for sport in str(sublist).split(',') if sport.strip("[]'\" ")])
all_sports = sorted(list(set(all_sports)))
selected_sports = st.sidebar.multiselect("Select Sports", all_sports)

st.sidebar.subheader("Gender")
show_male = st.sidebar.checkbox("Male", value=True)
show_female = st.sidebar.checkbox("Female", value=True)

# -------------------------------------------------------
# Data Filtering
# -------------------------------------------------------

df_filtered = df_athletes.copy()

if selected_countries:
    df_filtered = df_filtered[df_filtered['country'].isin(selected_countries)]

if selected_sports:
    df_filtered = df_filtered[df_filtered['disciplines'].str.contains('|'.join(selected_sports), na=False)]

gender_filter = []
if show_male:
    gender_filter.append('Male')
if show_female:
    gender_filter.append('Female')
if gender_filter:
    df_filtered = df_filtered[df_filtered['gender'].isin(gender_filter)]

# -------------------------------------------------------
# Render Components
# -------------------------------------------------------

# Task 1: Athlete Detailed Profile Card
render_athlete_profile(df_athletes, df_coaches, df_medallists)
st.divider()

# Task 2: Athlete Age Distribution
render_age_distribution(df_filtered)
st.divider()

# Task 3: Gender Distribution by Continent and Country
render_gender_distribution(df_filtered)
st.divider()

# Task 4: Top Athletes by Medals
render_top_athletes(df_medallists, selected_countries, gender_filter, selected_sports)
st.divider()

# Summary Statistics
render_athlete_summary(df_filtered)
