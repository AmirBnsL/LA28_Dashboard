"""
Continent Medals Bar Component
Displays a grouped bar chart of medals by continent.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def render_continent_medals_bar(df_filtered: pd.DataFrame):
    """Render the Continent vs. Medals Comparison section."""
    st.subheader("📊 Continent vs. Medals Comparison")
    st.markdown("*Total medals by continent (Gold, Silver, Bronze)*")

    if df_filtered.empty:
        st.info("No data available for the selected filters")
        return

    # Aggregate medals by continent
    continent_medals = df_filtered.groupby('Continent')[['Gold Medal', 'Silver Medal', 'Bronze Medal']].sum().reset_index()
    continent_medals = continent_medals.sort_values('Gold Medal', ascending=False)

    fig_continent = go.Figure()
    fig_continent.add_trace(go.Bar(
        name='Gold',
        x=continent_medals['Continent'],
        y=continent_medals['Gold Medal'],
        marker_color='#FFD700'
    ))
    fig_continent.add_trace(go.Bar(
        name='Silver',
        x=continent_medals['Continent'],
        y=continent_medals['Silver Medal'],
        marker_color='#C0C0C0'
    ))
    fig_continent.add_trace(go.Bar(
        name='Bronze',
        x=continent_medals['Continent'],
        y=continent_medals['Bronze Medal'],
        marker_color='#CD7F32'
    ))

    fig_continent.update_layout(
        barmode='group',
        title='Medal Distribution by Continent',
        xaxis_title='Continent',
        yaxis_title='Number of Medals',
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig_continent, width='stretch')
