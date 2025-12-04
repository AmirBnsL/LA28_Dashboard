import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
from datetime import datetime

# Add parent directory to path to import utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils

st.set_page_config(page_title="Athlete Performance", page_icon="👤", layout="wide")

# Load data
@st.cache_data
def load_athlete_data():
    # Get the directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir, 'data')
    
    df_athletes = pd.read_csv(os.path.join(data_dir, 'athletes.csv'))
    df_coaches = pd.read_csv(os.path.join(data_dir, 'coaches.csv'))
    df_teams = pd.read_csv(os.path.join(data_dir, 'teams.csv'))
    df_medallists = pd.read_csv(os.path.join(data_dir, 'medallists.csv'))
    df_nocs = pd.read_csv(os.path.join(data_dir, 'nocs.csv'))
    return df_athletes, df_coaches, df_teams, df_medallists, df_nocs

df_athletes, df_coaches, df_teams, df_medallists, df_nocs = load_athlete_data()

# Calculate age from birth_date
def calculate_age(birth_date):
    try:
        if pd.notna(birth_date):
            birth = pd.to_datetime(birth_date)
            age = 2024 - birth.year
            return age
    except:
        pass
    return None

df_athletes['age'] = df_athletes['birth_date'].apply(calculate_age)

# Add continent mapping
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
    'GRE': 'Europe', 'ARG': 'South America', 'EGY': 'Africa', 'TUN': 'Africa',
    'NGR': 'Africa', 'MEX': 'North America', 'DOM': 'North America', 'IND': 'Asia',
    'PER': 'South America', 'VEN': 'South America', 'COL': 'South America', 'UGA': 'Africa',
    'TUR': 'Europe', 'LTU': 'Europe', 'BAH': 'North America', 'CHI': 'South America',
    'SVK': 'Europe', 'MGL': 'Asia', 'ARM': 'Asia', 'TJK': 'Asia', 'MAR': 'Africa',
    'JOR': 'Asia', 'LAT': 'Europe', 'FIJ': 'Oceania', 'KUW': 'Asia', 'GRN': 'North America',
    'MAS': 'Asia', 'PUR': 'North America', 'EST': 'Europe', 'CIV': 'Africa', 'TTO': 'North America',
    'BOT': 'Africa', 'MDA': 'Europe', 'ALB': 'Europe', 'VIE': 'Asia', 'MKD': 'Europe',
    'SIN': 'Asia', 'GUA': 'North America', 'SAM': 'Oceania', 'PAK': 'Asia', 'LCA': 'North America',
    'ZIM': 'Africa', 'PAN': 'North America', 'CRC': 'North America',
    'TKM': 'Asia', 'KSA': 'Asia', 'CYP': 'Europe', 'AIN': 'Europe', 'ZAM': 'Africa',
    'SEN': 'Africa', 'NAM': 'Africa', 'LIB': 'Asia', 'PAR': 'South America',
    'URU': 'South America', 'SUD': 'Africa', 'KGZ': 'Asia', 'TAN': 'Africa', 'SRI': 'Asia',
    'ISV': 'North America', 'PNG': 'Oceania', 'MON': 'Europe', 'AFG': 'Asia', 'TON': 'Oceania',
}

df_athletes['Continent'] = df_athletes['country_code'].map(continent_map).fillna('Other')

# Sidebar filters
st.sidebar.header("🎯 Global Filters")
all_countries = sorted(df_athletes['country'].dropna().unique())
selected_countries = st.sidebar.multiselect("Select Countries", all_countries)

all_sports = sorted([sport.strip("[]'\" ") for sublist in df_athletes['disciplines'].dropna().unique() 
                     for sport in str(sublist).split(',') if sport.strip("[]'\" ")])
all_sports = sorted(list(set(all_sports)))
selected_sports = st.sidebar.multiselect("Select Sports", all_sports)

st.sidebar.subheader("Gender")
show_male = st.sidebar.checkbox("Male", value=True)
show_female = st.sidebar.checkbox("Female", value=True)

# Filter data
df_filtered = df_athletes.copy()
if selected_countries:
    df_filtered = df_filtered[df_filtered['country'].isin(selected_countries)]

if selected_sports:
    df_filtered = df_filtered[df_filtered['disciplines'].str.contains('|'.join(selected_sports), na=False)]

gender_filter = []
if show_male:
    gender_filter.append('Male')
if show_female:
    gender_filter.append('Female')
if gender_filter:
    df_filtered = df_filtered[df_filtered['gender'].isin(gender_filter)]

# Main content
st.title("👤 Athlete Performance Analysis")
st.markdown("### Explore athlete profiles, demographics, and achievements")

# Task 1: Athlete Detailed Profile Card
st.subheader("🔍 Athlete Profile Search")

# Create searchable athlete list
athlete_names = sorted(df_athletes['name'].dropna().unique())
selected_athlete = st.selectbox(
    "Search and select an athlete by name:",
    options=[''] + athlete_names,
    help="Start typing to search for an athlete"
)

if selected_athlete:
    athlete_data = df_athletes[df_athletes['name'] == selected_athlete].iloc[0]
    
    # Create profile card
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 2])
    
    with col1:
        st.markdown("### 📸 Profile")
        # Placeholder for image (dataset doesn't have image URLs)
        st.image("https://via.placeholder.com/200x250/3498db/ffffff?text=Athlete", 
                caption=f"{athlete_data['name']}")
    
    with col2:
        st.markdown("### 📋 Personal Information")
        st.markdown(f"**Full Name:** {athlete_data['name']}")
        
        # Add flag emoji (simplified)
        country_code = athlete_data['country_code']
        st.markdown(f"**Country/NOC:** {athlete_data['country']} ({country_code})")
        
        if pd.notna(athlete_data.get('height')) and athlete_data.get('height') > 0:
            st.markdown(f"**Height:** {athlete_data['height']} cm")
        else:
            st.markdown(f"**Height:** N/A")
            
        if pd.notna(athlete_data.get('weight')) and athlete_data.get('weight') > 0:
            st.markdown(f"**Weight:** {athlete_data['weight']} kg")
        else:
            st.markdown(f"**Weight:** N/A")
            
        if pd.notna(athlete_data['age']):
            st.markdown(f"**Age:** {int(athlete_data['age'])} years")
        
        if pd.notna(athlete_data['birth_date']):
            st.markdown(f"**Birth Date:** {athlete_data['birth_date']}")
        
        if pd.notna(athlete_data['birth_place']):
            st.markdown(f"**Birth Place:** {athlete_data['birth_place']}")
    
    with col3:
        st.markdown("### 🏅 Athletic Information")
        
        # Sports & Disciplines
        if pd.notna(athlete_data['disciplines']):
            st.markdown(f"**Sport(s):** {athlete_data['disciplines']}")
        
        if pd.notna(athlete_data['events']):
            st.markdown(f"**Event(s):** {athlete_data['events']}")
        
        # Coach information
        if pd.notna(athlete_data['coach']):
            st.markdown(f"**Coach(es):** {athlete_data['coach']}")
        else:
            st.markdown(f"**Coach(es):** N/A")
        
        # Check for medals
        athlete_medals = df_medallists[df_medallists['name'] == selected_athlete]
        if not athlete_medals.empty:
            medal_counts = athlete_medals['medal_type'].value_counts()
            st.markdown("**🏆 Medals Won:**")
            if 'Gold Medal' in medal_counts:
                st.markdown(f"  - 🥇 Gold: {medal_counts['Gold Medal']}")
            if 'Silver Medal' in medal_counts:
                st.markdown(f"  - 🥈 Silver: {medal_counts['Silver Medal']}")
            if 'Bronze Medal' in medal_counts:
                st.markdown(f"  - 🥉 Bronze: {medal_counts['Bronze Medal']}")

st.markdown("---")

# Task 2: Athlete Age Distribution
st.subheader("📊 Athlete Age Distribution")

age_data = df_filtered[df_filtered['age'].notna()].copy()

col1, col2 = st.columns(2)

with col1:
    # Box plot by gender
    if not age_data.empty:
        fig_box = px.box(
            age_data,
            x='gender',
            y='age',
            color='gender',
            title='Age Distribution by Gender',
            labels={'age': 'Age (years)', 'gender': 'Gender'},
            color_discrete_map={'Male': '#3498db', 'Female': '#e74c3c'}
        )
        fig_box.update_layout(height=400)
        st.plotly_chart(fig_box, use_container_width=True)

with col2:
    # Violin plot by sport (top 10 sports)
    if not age_data.empty:
        # Get top 10 sports by athlete count
        top_sports = age_data['disciplines'].value_counts().head(10).index.tolist()
        age_sports = age_data[age_data['disciplines'].isin(top_sports)]
        
        fig_violin = px.violin(
            age_sports,
            y='disciplines',
            x='age',
            color='gender',
            title='Age Distribution by Top 10 Sports',
            labels={'age': 'Age (years)', 'disciplines': 'Sport'},
            orientation='h',
            box=True
        )
        fig_violin.update_layout(height=400)
        st.plotly_chart(fig_violin, use_container_width=True)

# Task 3: Gender Distribution by Continent and Country
st.subheader("⚖️ Gender Distribution Analysis")

continent_country_selector = st.radio(
    "View by:",
    ["World", "Continent", "Country"],
    horizontal=True
)

if continent_country_selector == "World":
    gender_dist = df_filtered['gender'].value_counts()
    
    col1, col2 = st.columns(2)
    with col1:
        fig_pie = px.pie(
            values=gender_dist.values,
            names=gender_dist.index,
            title='Global Gender Distribution',
            color=gender_dist.index,
            color_discrete_map={'Male': '#3498db', 'Female': '#e74c3c'}
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        fig_bar = px.bar(
            x=gender_dist.index,
            y=gender_dist.values,
            title='Global Gender Count',
            labels={'x': 'Gender', 'y': 'Number of Athletes'},
            color=gender_dist.index,
            color_discrete_map={'Male': '#3498db', 'Female': '#e74c3c'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

elif continent_country_selector == "Continent":
    selected_continent = st.selectbox(
        "Select Continent:",
        sorted(df_filtered['Continent'].unique())
    )
    
    continent_data = df_filtered[df_filtered['Continent'] == selected_continent]
    gender_dist = continent_data['gender'].value_counts()
    
    col1, col2 = st.columns(2)
    with col1:
        fig_pie = px.pie(
            values=gender_dist.values,
            names=gender_dist.index,
            title=f'Gender Distribution in {selected_continent}',
            color=gender_dist.index,
            color_discrete_map={'Male': '#3498db', 'Female': '#e74c3c'}
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Country breakdown
        country_gender = continent_data.groupby(['country', 'gender']).size().reset_index(name='count')
        fig_bar = px.bar(
            country_gender,
            x='country',
            y='count',
            color='gender',
            title=f'Gender Distribution by Country in {selected_continent}',
            barmode='group',
            color_discrete_map={'Male': '#3498db', 'Female': '#e74c3c'}
        )
        fig_bar.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_bar, use_container_width=True)

else:  # Country
    selected_country_gender = st.selectbox(
        "Select Country:",
        sorted(df_filtered['country'].unique())
    )
    
    country_data = df_filtered[df_filtered['country'] == selected_country_gender]
    gender_dist = country_data['gender'].value_counts()
    
    col1, col2 = st.columns(2)
    with col1:
        fig_pie = px.pie(
            values=gender_dist.values,
            names=gender_dist.index,
            title=f'Gender Distribution in {selected_country_gender}',
            color=gender_dist.index,
            color_discrete_map={'Male': '#3498db', 'Female': '#e74c3c'}
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Sport breakdown
        sport_gender = country_data.groupby(['disciplines', 'gender']).size().reset_index(name='count')
        fig_bar = px.bar(
            sport_gender.head(20),
            x='disciplines',
            y='count',
            color='gender',
            title=f'Gender Distribution by Sport in {selected_country_gender}',
            barmode='group',
            color_discrete_map={'Male': '#3498db', 'Female': '#e74c3c'}
        )
        fig_bar.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_bar, use_container_width=True)

# Task 4: Top Athletes by Medals
st.subheader("🏆 Top Athletes by Medal Count")

# Count medals per athlete
medal_counts = df_medallists.groupby('name').agg({
    'medal_type': 'count',
    'country': 'first',
    'discipline': 'first'
}).reset_index()
medal_counts.columns = ['name', 'total_medals', 'country', 'discipline']

# Get medal breakdown
medal_breakdown = df_medallists.groupby(['name', 'medal_type']).size().reset_index(name='count')
medal_pivot = medal_breakdown.pivot(index='name', columns='medal_type', values='count').fillna(0)

# Merge with total medals
medal_counts = medal_counts.merge(medal_pivot, left_on='name', right_index=True, how='left')
medal_counts = medal_counts.fillna(0)

# Sort by total medals
medal_counts = medal_counts.sort_values('total_medals', ascending=False).head(10)

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

st.plotly_chart(fig_medals, use_container_width=True)

# Summary Statistics
st.markdown("---")
st.subheader("📈 Summary Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Athletes", len(df_filtered))
with col2:
    st.metric("Countries Represented", df_filtered['country'].nunique())
with col3:
    st.metric("Sports Covered", df_filtered['disciplines'].nunique())
with col4:
    avg_age = df_filtered['age'].mean()
    if pd.notna(avg_age):
        st.metric("Average Age", f"{avg_age:.1f} years")
    else:
        st.metric("Average Age", "N/A")