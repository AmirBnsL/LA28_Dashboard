"""
Medal Hierarchy Component
Displays Sunburst and Treemap visualizations for medal hierarchy.
"""
import streamlit as st
import plotly.express as px
import pandas as pd


def render_medal_hierarchy(df_filtered: pd.DataFrame, show_gold: bool, show_silver: bool, show_bronze: bool):
    """Render the Medal Hierarchy section with Sunburst and Treemap."""
    st.subheader("🌐 Medal Hierarchy by Continent")
    st.markdown("*Drill down from Continent → Country → Medal Type*")

    if df_filtered.empty:
        st.info("No data available for the selected filters")
        return

    # Prepare data for sunburst/treemap
    hierarchy_data = []
    for _, row in df_filtered.iterrows():
        if show_gold and row['Gold Medal'] > 0:
            hierarchy_data.append({
                'Continent': row['Continent'],
                'Country': row['country'],
                'Medal_Type': 'Gold',
                'Count': row['Gold Medal']
            })
        if show_silver and row['Silver Medal'] > 0:
            hierarchy_data.append({
                'Continent': row['Continent'],
                'Country': row['country'],
                'Medal_Type': 'Silver',
                'Count': row['Silver Medal']
            })
        if show_bronze and row['Bronze Medal'] > 0:
            hierarchy_data.append({
                'Continent': row['Continent'],
                'Country': row['country'],
                'Medal_Type': 'Bronze',
                'Count': row['Bronze Medal']
            })

    df_hierarchy = pd.DataFrame(hierarchy_data)

    col1, col2 = st.columns(2)

    with col1:
        if not df_hierarchy.empty:
            fig_sunburst = px.sunburst(
                df_hierarchy,
                path=['Continent', 'Country', 'Medal_Type'],
                values='Count',
                color='Medal_Type',
                color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'},
                title='Sunburst: Continent → Country → Medal Type'
            )
            fig_sunburst.update_layout(height=500)
            st.plotly_chart(fig_sunburst, use_container_width=True)
        else:
            st.info("No data available for the selected filters")

    with col2:
        if not df_hierarchy.empty:
            fig_treemap = px.treemap(
                df_hierarchy,
                path=['Continent', 'Country', 'Medal_Type'],
                values='Count',
                color='Medal_Type',
                color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'},
                title='Treemap: Continent → Country → Medal Type'
            )
            fig_treemap.update_layout(height=500)
            st.plotly_chart(fig_treemap, use_container_width=True)
        else:
            st.info("No data available for the selected filters")
