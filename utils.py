import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_data():
    # Get the directory where utils.py is located (project root)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    
    try:
        df_athletes = pd.read_csv(os.path.join(data_dir, 'athletes.csv'))
        df_medals = pd.read_csv(os.path.join(data_dir, 'medals_total.csv'))
        df_events = pd.read_csv(os.path.join(data_dir, 'events.csv'))
        df_nocs = pd.read_csv(os.path.join(data_dir, 'nocs.csv'))
        return df_athletes, df_medals, df_events, df_nocs
    except FileNotFoundError as e:
        st.error(f"Data files not found: {e}. Please ensure CSVs are in the 'data/' folder.")
        return None, None, None, None

def sidebar_filters(df):
    st.sidebar.header("Global Filters")
    if df is not None:
        countries = st.sidebar.multiselect("Country", sorted(df['country'].unique()))
        sports = st.sidebar.multiselect("Sport", sorted(df['disciplines'].unique()))
        return countries, sports, None
    return [], [], None