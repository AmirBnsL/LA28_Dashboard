"""
Top Countries Medals Component
Displays a bar chart of the top 20 countries by medal count.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def render_top_countries_medals(df_filtered: pd.DataFrame):
    """Render the Top 20 Countries vs. Medals section."""
    st.subheader("🏆 Top 20 Countries vs. Medals")
    st.markdown("*Leading nations in the medal race*")

    if df_filtered.empty:
        st.info("No data available for the selected filters")
        return

    # Get top 20 countries by total medals
    top20 = df_filtered.nlargest(20, 'Filtered_Total')

    fig_top20 = go.Figure()
    fig_top20.add_trace(go.Bar(
        name='Gold',
        y=top20['country'],
        x=top20['Gold Medal'],
        orientation='h',
        marker_color='#FFD700'
    ))
    fig_top20.add_trace(go.Bar(
        name='Silver',
        y=top20['country'],
        x=top20['Silver Medal'],
        orientation='h',
        marker_color='#C0C0C0'
    ))
    fig_top20.add_trace(go.Bar(
        name='Bronze',
        y=top20['country'],
        x=top20['Bronze Medal'],
        orientation='h',
        marker_color='#CD7F32'
    ))

    fig_top20.update_layout(
        barmode='group',
        title='Top 20 Countries by Medal Count',
        xaxis_title='Number of Medals',
        yaxis_title='Country',
        height=700,
        hovermode='y unified',
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig_top20, use_container_width=True)
