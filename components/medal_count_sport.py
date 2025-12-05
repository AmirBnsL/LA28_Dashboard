"""
Medal Count by Sport Component
Displays a treemap of medal distribution across sports and events.
"""
import streamlit as st
import plotly.express as px
import pandas as pd


def render_medal_count_by_sport(
    df_medals: pd.DataFrame,
    selected_medals: list,
    selected_countries: list,
    selected_sports: list
):
    """Render the Medal Count by Sport section with treemap visualization."""
    st.header("🥇 Medal Count by Sport")

    medals_filtered = df_medals.copy()

    if selected_medals:
        medals_filtered = medals_filtered[medals_filtered["medal_type"].isin(selected_medals)]

    if selected_countries:
        medals_filtered = medals_filtered[medals_filtered["country"].isin(selected_countries)]

    if selected_sports:
        medals_filtered = medals_filtered[medals_filtered["discipline"].isin(selected_sports)]

    if medals_filtered.empty:
        st.warning("⚠️ No medal data available for the current filters.")
        st.caption("**Tip:** Try clearing the **Sport** filter to view total medal counts.")
    else:
        medals_counts = (
            medals_filtered
            .groupby(["discipline", "event"])
            .size()
            .reset_index(name="count")
        )

        fig_treemap = px.treemap(
            medals_counts,
            path=[px.Constant("Medals"), "discipline", "event"],
            values="count",
            color="count",
            color_continuous_scale="Viridis",
            title="Distribution of Medals across Sports and Events",
        )
        fig_treemap.update_traces(root_color="lightgrey")
        st.plotly_chart(fig_treemap, width='stretch')
