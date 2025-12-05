"""
Summary Statistics Component
Displays summary metrics for the filtered data.
"""
import streamlit as st
import pandas as pd


def render_summary_statistics(df_filtered: pd.DataFrame):
    """Render the Summary Statistics section."""
    st.subheader("📈 Summary Statistics")
    
    if df_filtered.empty:
        st.info("No data available for the selected filters")
        return

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Countries Displayed", len(df_filtered))
    with col2:
        st.metric("Total Gold Medals", int(df_filtered['Gold Medal'].sum()))
    with col3:
        st.metric("Total Silver Medals", int(df_filtered['Silver Medal'].sum()))
    with col4:
        st.metric("Total Bronze Medals", int(df_filtered['Bronze Medal'].sum()))
