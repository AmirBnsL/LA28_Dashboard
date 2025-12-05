"""
Data loading functions for the LA28 Dashboard.
"""
import pandas as pd
import streamlit as st
import os


def get_data_path(filename: str) -> str:
    """
    Get the absolute path to a data file.
    Works whether called from main app or pages folder.
    """
    # Try relative to current file first
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_path = os.path.join(parent_dir, "data", filename)
    
    if os.path.exists(data_path):
        return data_path
    
    # Fallback: try relative path
    if os.path.exists(f"data/{filename}"):
        return f"data/{filename}"
    
    if os.path.exists(f"../data/{filename}"):
        return f"../data/{filename}"
    
    raise FileNotFoundError(f"Could not find {filename} in data folder")


@st.cache_data
def load_schedule_data() -> pd.DataFrame:
    """Load and preprocess schedule data."""
    df = pd.read_csv(get_data_path("schedules.csv"))
    df["start_date"] = pd.to_datetime(df["start_date"])
    df["end_date"] = pd.to_datetime(df["end_date"])
    return df


@st.cache_data
def load_medals_data() -> pd.DataFrame:
    """Load medals data."""
    return pd.read_csv(get_data_path("medals.csv"))


@st.cache_data
def load_venues_data() -> pd.DataFrame:
    """Load venues data."""
    return pd.read_csv(get_data_path("venues.csv"))


@st.cache_data
def load_athletes_data() -> pd.DataFrame:
    """Load athletes data."""
    return pd.read_csv(get_data_path("athletes.csv"))


@st.cache_data
def load_medals_total_data() -> pd.DataFrame:
    """Load medals total data."""
    return pd.read_csv(get_data_path("medals_total.csv"))


@st.cache_data
def load_events_data() -> pd.DataFrame:
    """Load events data."""
    return pd.read_csv(get_data_path("events.csv"))


@st.cache_data
def load_nocs_data() -> pd.DataFrame:
    """Load NOCs data."""
    return pd.read_csv(get_data_path("nocs.csv"))
