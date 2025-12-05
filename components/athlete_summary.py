"""
Athlete Summary Statistics Component
Displays summary metrics for the filtered athlete data.
"""
import streamlit as st
import pandas as pd


def render_athlete_summary(df_filtered: pd.DataFrame):
    """Render the Summary Statistics section."""
    st.subheader("📈 Summary Statistics")
    
    if df_filtered.empty:
        st.info("No data available for the selected filters")
        return

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Athletes", len(df_filtered))
    with col2:
        st.metric("Countries Represented", df_filtered['country'].nunique())
    with col3:
        st.metric("Sports Covered", df_filtered['disciplines'].nunique())
    with col4:
        avg_age = df_filtered['age'].mean()
        if pd.notna(avg_age):
            st.metric("Average Age", f"{avg_age:.1f} years")
        else:
            st.metric("Average Age", "N/A")
