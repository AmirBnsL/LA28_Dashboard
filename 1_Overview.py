import streamlit as st
import pandas as pd
import plotly.express as px
import utils

st.set_page_config(page_title="LA28 Overview", page_icon="🏠", layout="wide")

# Load data
df_athletes, df_medals, df_events, df_nocs = utils.load_data()

if df_athletes is None:
    st.stop()

# Sidebar
selected_countries, selected_sports, selected_medal_types = utils.sidebar_filters(df_athletes, df_events, df_nocs)

# --- Filtering Logic ---

# 1. Filter Athletes
filtered_athletes = df_athletes.copy()
if selected_countries:
    filtered_athletes = filtered_athletes[filtered_athletes['country'].isin(selected_countries)]
if selected_sports:
    # disciplines is a string representation of a list, e.g., "['Wrestling']"
    # We check if any of the selected sports appear in the string
    # A regex join is efficient: "Sport1|Sport2"
    pattern = '|'.join(selected_sports)
    filtered_athletes = filtered_athletes[filtered_athletes['disciplines'].str.contains(pattern, regex=True, na=False)]

# 2. Filter NOCs (Countries)
filtered_nocs = df_nocs.copy()
if selected_countries:
    filtered_nocs = filtered_nocs[filtered_nocs['country'].isin(selected_countries)]

# 3. Filter Events
filtered_events = df_events.copy()
if selected_sports:
    filtered_events = filtered_events[filtered_events['sport'].isin(selected_sports)]

# 4. Filter Medals
filtered_medals = df_medals.copy()
if selected_countries:
    filtered_medals = filtered_medals[filtered_medals['country'].isin(selected_countries)]

# --- KPI Metrics ---

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

# --- Visualizations ---

col_charts_1, col_charts_2 = st.columns(2)

# 1. Global Medal Distribution (Pie/Donut)
with col_charts_1:
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
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("No medals found for the current selection.")
    else:
        st.warning("No data available for Medal Distribution.")

# 2. Top 10 Medal Standings (Horizontal Bar)
with col_charts_2:
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
            
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("No medals found for the current selection.")
    else:
        st.warning("No data available for Medal Standings.")