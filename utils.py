import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    try:
        df_athletes = pd.read_csv('data/athletes.csv')
        df_medals = pd.read_csv('data/medals_total.csv')
        df_events = pd.read_csv('data/events.csv')
        df_nocs = pd.read_csv('data/nocs.csv')
        return df_athletes, df_medals, df_events, df_nocs
    except FileNotFoundError:
        st.error("Data files not found. Please upload CSVs to the 'data/' folder.")
        return None, None, None, None

def sidebar_filters(df_athletes, df_events, df_nocs):
    st.sidebar.header("Global Filters")
    
    # Country Filter
    # Get list of countries from NOCs or Athletes. NOCs is cleaner.
    if df_nocs is not None:
        all_countries = sorted(df_nocs['country'].unique())
        selected_countries = st.sidebar.multiselect("Select Country (NOC)", all_countries)
    else:
        selected_countries = []
    
    # Sport Filter
    # Get list of sports from Events
    if df_events is not None:
        all_sports = sorted(df_events['sport'].unique())
        selected_sports = st.sidebar.multiselect("Select Sport", all_sports)
    else:
        selected_sports = []
    
    # Medal Type Filter
    st.sidebar.subheader("Medal Type")
    col1, col2, col3 = st.sidebar.columns(3)
    gold = col1.checkbox("Gold", value=True)
    silver = col2.checkbox("Silver", value=True)
    bronze = col3.checkbox("Bronze", value=True)
    
    medal_types = []
    if gold: medal_types.append("Gold Medal")
    if silver: medal_types.append("Silver Medal")
    if bronze: medal_types.append("Bronze Medal")
    
    return selected_countries, selected_sports, medal_types 