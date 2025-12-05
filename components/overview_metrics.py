"""
Overview Metrics Component
Displays high-level KPIs for the dashboard.
"""
import streamlit as st
import pandas as pd


def render_overview_metrics(
    filtered_athletes: pd.DataFrame,
    filtered_nocs: pd.DataFrame,
    filtered_events: pd.DataFrame,
    filtered_medals: pd.DataFrame,
    selected_medal_types: list
):
    """Render the Overview Metrics section."""
    st.title("🏅 Paris 2024 Olympic Games Overview")
    st.caption("A high-level summary of the Paris 2024 Olympic Games.")
    st.divider()

    # Calculate Metrics
    total_athletes = len(filtered_athletes)
    total_countries = len(filtered_nocs)
    total_sports = len(filtered_events['sport'].unique())
    number_of_events = len(filtered_events)

    # Calculate Total Medals based on selected types
    total_medals_awarded = 0
    if not filtered_medals.empty:
        for medal_type in selected_medal_types:
            if medal_type in filtered_medals.columns:
                total_medals_awarded += filtered_medals[medal_type].sum()

    # Display KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Athletes", f"{total_athletes:,}")
    col2.metric("Total Countries", total_countries)
    col3.metric("Total Sports", total_sports)
    col4.metric("Total Medals", total_medals_awarded)
    col5.metric("Number of Events", number_of_events)

    st.divider()
