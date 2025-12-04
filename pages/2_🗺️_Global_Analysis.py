import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Add parent directory to path to import utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils

st.set_page_config(page_title="Global Analysis", page_icon="🗺️", layout="wide")

# Load data
df_athletes, df_medals, df_events, df_nocs = utils.load_data()

# Create continent mapping dictionary
continent_map = {
    'USA': 'North America', 'CHN': 'Asia', 'JPN': 'Asia', 'AUS': 'Oceania', 'FRA': 'Europe',
    'NED': 'Europe', 'GBR': 'Europe', 'KOR': 'Asia', 'ITA': 'Europe', 'GER': 'Europe',
    'NZL': 'Oceania', 'CAN': 'North America', 'UZB': 'Asia', 'HUN': 'Europe', 'ESP': 'Europe',
    'SWE': 'Europe', 'KEN': 'Africa', 'NOR': 'Europe', 'IRL': 'Europe', 'BRA': 'South America',
    'IRN': 'Asia', 'UKR': 'Europe', 'ROU': 'Europe', 'GEO': 'Asia', 'BEL': 'Europe',
    'BUL': 'Europe', 'SRB': 'Europe', 'CZE': 'Europe', 'DEN': 'Europe', 'AZE': 'Asia',
    'CRO': 'Europe', 'CUB': 'North America', 'BRN': 'Asia', 'SLO': 'Europe', 'TPE': 'Asia',
    'AUT': 'Europe', 'HKG': 'Asia', 'PHI': 'Asia', 'ALG': 'Africa', 'INA': 'Asia',
    'ISR': 'Asia', 'POL': 'Europe', 'KAZ': 'Asia', 'JAM': 'North America', 'RSA': 'Africa',
    'THA': 'Asia', 'ETH': 'Africa', 'SUI': 'Europe', 'ECU': 'South America', 'POR': 'Europe',
    'GRE': 'Europe', 'ARG': 'South America', 'EGY': 'Africa', 'TUN': 'Africa', 'NOR': 'Europe',
    'NGR': 'Africa', 'MEX': 'North America', 'DOM': 'North America', 'IND': 'Asia',
    'PER': 'South America', 'VEN': 'South America', 'COL': 'South America', 'UGA': 'Africa',
    'TUR': 'Europe', 'LTU': 'Europe', 'BAH': 'North America', 'CHI': 'South America',
    'SVK': 'Europe', 'MGL': 'Asia', 'ARM': 'Asia', 'TJK': 'Asia', 'MAR': 'Africa',
    'JOR': 'Asia', 'LAT': 'Europe', 'FIJ': 'Oceania', 'KUW': 'Asia', 'GRN': 'North America',
    'MAS': 'Asia', 'PUR': 'North America', 'EST': 'Europe', 'CIV': 'Africa', 'TTO': 'North America',
    'BOT': 'Africa', 'MDA': 'Europe', 'ALB': 'Europe', 'VIE': 'Asia', 'MKD': 'Europe',
    'SIN': 'Asia', 'GUA': 'North America', 'SAM': 'Oceania', 'PAK': 'Asia', 'LCA': 'North America',
    'ZIM': 'Africa', 'DOM': 'North America', 'PAN': 'North America', 'CRC': 'North America',
    'TKM': 'Asia', 'KSA': 'Asia', 'CYP': 'Europe', 'AIN': 'Europe', 'ZAM': 'Africa',
    'SEN': 'Africa', 'TTO': 'North America', 'NAM': 'Africa', 'LIB': 'Asia', 'PAR': 'South America',
    'URU': 'South America', 'SUD': 'Africa', 'KGZ': 'Asia', 'TAN': 'Africa', 'SRI': 'Asia',
    'ISV': 'North America', 'PNG': 'Oceania', 'MON': 'Europe', 'AFG': 'Asia', 'TON': 'Oceania',
}

# Add continent column to medals dataframe
if df_medals is not None:
    df_medals['Continent'] = df_medals['country_code'].map(continent_map)
    df_medals['Continent'] = df_medals['Continent'].fillna('Other')

# Sidebar filters
st.sidebar.header("🎯 Global Filters")
if df_athletes is not None and df_medals is not None:
    # Country filter
    all_countries = sorted(df_medals['country'].unique())
    selected_countries = st.sidebar.multiselect("Select Countries", all_countries)
    
    # Sport filter (from athletes data)
    all_sports = sorted([sport.strip("[]'") for sublist in df_athletes['disciplines'].dropna().unique() for sport in str(sublist).split(',')])
    all_sports = sorted(list(set(all_sports)))
    selected_sports = st.sidebar.multiselect("Select Sports", all_sports)
    
    # Medal type filter
    st.sidebar.subheader("Medal Type")
    show_gold = st.sidebar.checkbox("Gold", value=True)
    show_silver = st.sidebar.checkbox("Silver", value=True)
    show_bronze = st.sidebar.checkbox("Bronze", value=True)

# Filter data based on selections
df_filtered = df_medals.copy()
if selected_countries:
    df_filtered = df_filtered[df_filtered['country'].isin(selected_countries)]

# Apply medal type filters
medal_columns = []
if show_gold:
    medal_columns.append('Gold Medal')
if show_silver:
    medal_columns.append('Silver Medal')
if show_bronze:
    medal_columns.append('Bronze Medal')

if medal_columns:
    df_filtered['Filtered_Total'] = df_filtered[medal_columns].sum(axis=1)
else:
    df_filtered['Filtered_Total'] = 0

# Main content
st.title("🗺️ Global Medal Analysis")
st.markdown("### Explore Olympic medals from a geographical and continental perspective")

# Task 1: World Medal Map (Choropleth)
st.subheader("🌍 World Medal Map")
st.markdown("*Countries are color-coded by total medal count*")

fig_map = px.choropleth(
    df_filtered,
    locations='country_code',
    color='Filtered_Total',
    hover_name='country',
    hover_data={
        'country_code': False,
        'Gold Medal': True,
        'Silver Medal': True,
        'Bronze Medal': True,
        'Filtered_Total': True
    },
    color_continuous_scale='YlOrRd',
    labels={'Filtered_Total': 'Total Medals'},
    title='Global Medal Distribution by Country'
)
fig_map.update_layout(
    height=500,
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='natural earth'
    )
)
st.plotly_chart(fig_map, use_container_width=True)

# Task 2: Medal Hierarchy by Continent (Sunburst)
st.subheader("🌐 Medal Hierarchy by Continent")
st.markdown("*Drill down from Continent → Country → Medal Type*")

# Prepare data for sunburst
sunburst_data = []
for _, row in df_filtered.iterrows():
    if show_gold and row['Gold Medal'] > 0:
        sunburst_data.append({
            'Continent': row['Continent'],
            'Country': row['country'],
            'Medal_Type': 'Gold',
            'Count': row['Gold Medal']
        })
    if show_silver and row['Silver Medal'] > 0:
        sunburst_data.append({
            'Continent': row['Continent'],
            'Country': row['country'],
            'Medal_Type': 'Silver',
            'Count': row['Silver Medal']
        })
    if show_bronze and row['Bronze Medal'] > 0:
        sunburst_data.append({
            'Continent': row['Continent'],
            'Country': row['country'],
            'Medal_Type': 'Bronze',
            'Count': row['Bronze Medal']
        })

df_sunburst = pd.DataFrame(sunburst_data)

col1, col2 = st.columns(2)

with col1:
    if not df_sunburst.empty:
        fig_sunburst = px.sunburst(
            df_sunburst,
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
    if not df_sunburst.empty:
        fig_treemap = px.treemap(
            df_sunburst,
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

# Task 3: Continent vs. Medals Bar Chart
st.subheader("📊 Continent vs. Medals Comparison")
st.markdown("*Total medals by continent (Gold, Silver, Bronze)*")

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
st.plotly_chart(fig_continent, use_container_width=True)

# Task 4: Top 20 Countries vs. Medals
st.subheader("🏆 Top 20 Countries vs. Medals")
st.markdown("*Leading nations in the medal race*")

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

# Summary statistics
st.subheader("📈 Summary Statistics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Countries Displayed", len(df_filtered))
with col2:
    st.metric("Total Gold Medals", int(df_filtered['Gold Medal'].sum()))
with col3:
    st.metric("Total Silver Medals", int(df_filtered['Silver Medal'].sum()))
with col4:
    st.metric("Total Bronze Medals", int(df_filtered['Bronze Medal'].sum()))