"""
Global Analysis Page - LA28 Dashboard
Explore Olympic medals from a geographical and continental perspective.
"""
import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.data_loader import load_medals_total_data, load_athletes_data, load_medals_data
from modules.helpers import get_continent

# Import components
from components.global_medal_distribution import render_global_medal_distribution
from components.medal_hierarchy import render_medal_hierarchy
from components.continent_medals_bar import render_continent_medals_bar
from components.top_countries_medals import render_top_countries_medals
from components.summary_statistics import render_summary_statistics

# -------------------------------------------------------
# Page Config
# -------------------------------------------------------

st.set_page_config(
    page_title="Global Analysis",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Global Medal Analysis")
st.markdown("### Explore Olympic medals from a geographical and continental perspective")

# -------------------------------------------------------
# Data Loading
# -------------------------------------------------------

try:
    df_medals_total = load_medals_total_data()
    df_athletes = load_athletes_data()
    df_medals = load_medals_data()
except FileNotFoundError as e:
    st.error(f"❌ {e}")
    st.stop()

# Add continent column to medals dataframe
df_medals_total['Continent'] = df_medals_total['country'].apply(get_continent)
df_medals['continent'] = df_medals['country'].apply(get_continent)

# -------------------------------------------------------
# Sidebar Filters
# -------------------------------------------------------

st.sidebar.header("🎯 Global Filters")

# Country filter
all_countries = sorted(df_medals_total['country'].unique())
selected_countries = st.sidebar.multiselect("Select Countries", all_countries)

# Continent filter for detail view
all_continents = sorted(df_medals_total['Continent'].unique())
selected_continent = st.sidebar.selectbox("Select Continent for Detail View", all_continents)

# Medal type filter
st.sidebar.subheader("Medal Type")
show_gold = st.sidebar.checkbox("Gold", value=True)
show_silver = st.sidebar.checkbox("Silver", value=True)
show_bronze = st.sidebar.checkbox("Bronze", value=True)

# -------------------------------------------------------
# Data Filtering
# -------------------------------------------------------

df_filtered = df_medals_total.copy()

if selected_countries:
    df_filtered = df_filtered[df_filtered['country'].isin(selected_countries)]

# Calculate Filtered Total based on selected medal types
medal_columns = []
if show_gold:
    medal_columns.append('Gold Medal')
if show_silver:
    medal_columns.append('Silver Medal')
if show_bronze:
    medal_columns.append('Bronze Medal')

if medal_columns:
    df_filtered['Filtered_Total'] = df_filtered[medal_columns].sum(axis=1)
else:
    df_filtered['Filtered_Total'] = 0

# -------------------------------------------------------
# Render Components
# -------------------------------------------------------

# Global Medal Distribution (Map + Continent Detail)
render_global_medal_distribution(df_medals, medal_columns, selected_continent)
st.divider()

# Medal Hierarchy
render_medal_hierarchy(df_filtered, show_gold, show_silver, show_bronze)
st.divider()

# Continent vs. Medals Bar Chart
render_continent_medals_bar(df_filtered)
st.divider()

# Top 20 Countries vs. Medals
render_top_countries_medals(df_filtered)
st.divider()

# Summary Statistics
render_summary_statistics(df_filtered)
