import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    # Placeholder for data loading logic
    # Ensure you place your CSVs in the 'data/' folder
    try:
        df_athletes = pd.read_csv('data/athletes.csv')
        df_medals = pd.read_csv('data/medals_total.csv')
        df_events = pd.read_csv('data/events.csv')
        df_nocs = pd.read_csv('data/nocs.csv')
        return df_athletes, df_medals, df_events, df_nocs
    except FileNotFoundError:
        st.error("Data files not found. Please upload CSVs to the 'data/' folder.")
        return None, None, None, None

def sidebar_filters(df):
    st.sidebar.header("Global Filters")
    if df is not None:
        countries = st.sidebar.multiselect("Country", sorted(df['country'].unique()))
        sports = st.sidebar.multiselect("Sport", sorted(df['disciplines'].unique()))
        return countries, sports, None
    return [], [], None