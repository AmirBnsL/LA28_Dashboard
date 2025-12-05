"""
Top Athletes Component
Displays bar chart of top athletes by medal count.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def render_top_athletes(df_medallists: pd.DataFrame, selected_countries: list, gender_filter: list, selected_sports: list):
    """Render the Top Athletes by Medal Count section."""
    st.subheader("🏆 Top Athletes by Medal Count")

    # Apply filters to medallists
    df_medallists_filtered = df_medallists.copy()

    # Filter by country if selected
    if selected_countries:
        df_medallists_filtered = df_medallists_filtered[df_medallists_filtered['country'].isin(selected_countries)]

    # Filter by gender if selected
    if gender_filter:
        df_medallists_filtered = df_medallists_filtered[df_medallists_filtered['gender'].isin(gender_filter)]

    # Filter by sport if selected
    if selected_sports:
        df_medallists_filtered = df_medallists_filtered[df_medallists_filtered['discipline'].str.contains('|'.join(selected_sports), na=False, case=False)]

    if df_medallists_filtered.empty:
        st.info("No medallists found for the selected filters.")
        return

    # Count medals per athlete
    medal_counts = df_medallists_filtered.groupby('name').agg({
        'medal_type': 'count',
        'country': 'first',
        'discipline': 'first'
    }).reset_index()
    medal_counts.columns = ['name', 'total_medals', 'country', 'discipline']

    # Get medal breakdown
    medal_breakdown = df_medallists_filtered.groupby(['name', 'medal_type']).size().reset_index(name='count')
    medal_pivot = medal_breakdown.pivot(index='name', columns='medal_type', values='count').fillna(0)

    # Merge with total medals
    medal_counts = medal_counts.merge(medal_pivot, left_on='name', right_index=True, how='left')
    medal_counts = medal_counts.fillna(0)

    # Ensure medal columns exist
    for medal_type in ['Gold Medal', 'Silver Medal', 'Bronze Medal']:
        if medal_type not in medal_counts.columns:
            medal_counts[medal_type] = 0

    # Convert to int to avoid any issues
    medal_counts['Gold Medal'] = medal_counts['Gold Medal'].astype(int)
    medal_counts['Silver Medal'] = medal_counts['Silver Medal'].astype(int)
    medal_counts['Bronze Medal'] = medal_counts['Bronze Medal'].astype(int)

    # Sort by Gold first (descending), then Silver (descending), then Bronze (descending)
    medal_counts = medal_counts.sort_values(
        by=['Gold Medal', 'Silver Medal', 'Bronze Medal'], 
        ascending=[False, False, False]
    ).head(10)

    # Create bar chart
    fig_medals = go.Figure()

    if 'Gold Medal' in medal_counts.columns:
        fig_medals.add_trace(go.Bar(
            name='Gold',
            y=medal_counts['name'],
            x=medal_counts['Gold Medal'],
            orientation='h',
            marker_color='#FFD700'
        ))

    if 'Silver Medal' in medal_counts.columns:
        fig_medals.add_trace(go.Bar(
            name='Silver',
            y=medal_counts['name'],
            x=medal_counts['Silver Medal'],
            orientation='h',
            marker_color='#C0C0C0'
        ))

    if 'Bronze Medal' in medal_counts.columns:
        fig_medals.add_trace(go.Bar(
            name='Bronze',
            y=medal_counts['name'],
            x=medal_counts['Bronze Medal'],
            orientation='h',
            marker_color='#CD7F32'
        ))

    fig_medals.update_layout(
        barmode='stack',
        title='Top 10 Athletes by Total Medal Count',
        xaxis_title='Number of Medals',
        yaxis_title='Athlete',
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )

    st.plotly_chart(fig_medals, width='stretch')
