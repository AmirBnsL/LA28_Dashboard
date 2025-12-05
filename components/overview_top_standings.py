"""
Overview Top Standings Component
Displays a horizontal bar chart of the top 10 medal standings.
"""
import streamlit as st
import plotly.express as px
import pandas as pd


def render_overview_top_standings(filtered_medals: pd.DataFrame, selected_medal_types: list):
    """Render the Top 10 Medal Standings bar chart."""
    st.subheader("Top 10 Medal Standings")
    
    if not filtered_medals.empty:
        # Recalculate 'Total' based on selected medal types for sorting
        filtered_medals['Selected Total'] = 0
        for m_type in selected_medal_types:
            if m_type in filtered_medals.columns:
                filtered_medals['Selected Total'] += filtered_medals[m_type]
        
        # Sort and take top 10
        top_10_medals = filtered_medals.sort_values(by='Selected Total', ascending=False).head(10)
        
        if not top_10_medals.empty and top_10_medals['Selected Total'].sum() > 0:
            fig_bar = px.bar(
                top_10_medals,
                x='Selected Total',
                y='country',
                orientation='h',
                text='Selected Total',
                labels={'Selected Total': 'Total Medals', 'country': ''},
                color='Selected Total',
                color_continuous_scale='Viridis'
            )
            # Professional Styling
            fig_bar.update_layout(
                template="plotly_white",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis={'categoryorder': 'total ascending'},
                xaxis=dict(showgrid=False, showticklabels=False),
                margin=dict(t=20, b=20, l=0, r=0),
                coloraxis_showscale=False
            )
            fig_bar.update_traces(textposition='outside')
            
            st.plotly_chart(fig_bar, width='stretch')
        else:
            st.warning("No medals found for the current selection.")
    else:
        st.warning("No data available for Medal Standings.")
