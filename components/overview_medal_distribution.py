"""
Overview Medal Distribution Component
Displays a pie chart of global medal distribution.
"""
import streamlit as st
import plotly.express as px
import pandas as pd


def render_overview_medal_distribution(filtered_medals: pd.DataFrame, selected_medal_types: list):
    """Render the Global Medal Distribution pie chart."""
    st.subheader("Global Medal Distribution")
    
    if not filtered_medals.empty and selected_medal_types:
        # Aggregate medals by type
        medal_counts = {m_type: filtered_medals[m_type].sum() for m_type in selected_medal_types if m_type in filtered_medals.columns}
        df_medal_dist = pd.DataFrame(list(medal_counts.items()), columns=['Medal Type', 'Count'])
        
        if df_medal_dist['Count'].sum() > 0:
            fig_pie = px.pie(
                df_medal_dist, 
                values='Count', 
                names='Medal Type', 
                hole=0.5,
                color='Medal Type',
                color_discrete_map={
                    'Gold Medal': '#FFD700',
                    'Silver Medal': '#C0C0C0',
                    'Bronze Medal': '#CD7F32'
                }
            )
            # Professional Styling
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(
                template="plotly_white",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20)
            )
            st.plotly_chart(fig_pie, width='stretch')
        else:
            st.warning("No medals found for the current selection.")
    else:
        st.warning("No data available for Medal Distribution.")
