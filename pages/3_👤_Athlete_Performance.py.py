import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
import requests
from urllib.parse import quote_plus

# Add parent directory to path to import utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils

st.set_page_config(page_title="Athlete Performance", page_icon="👤", layout="wide")

# Load data - use utils for common data, load additional files needed for this page
df_athletes, _, df_events, df_nocs = utils.load_data()

# Load additional data files needed for athlete performance page
@st.cache_data
def load_athlete_page_data():
    try:
        df_coaches = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'coaches.csv'))
    except FileNotFoundError:
        df_coaches = pd.DataFrame()
    
    try:
        df_teams = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'teams.csv'))
    except FileNotFoundError:
        df_teams = pd.DataFrame()
    
    try:
        df_medallists = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'medallists.csv'))
    except FileNotFoundError:
        df_medallists = pd.DataFrame()
    
    return df_coaches, df_teams, df_medallists

df_coaches, df_teams, df_medallists = load_athlete_page_data()




# ============ GOOGLE IMAGE SEARCH FUNCTION ============
@st.cache_data(ttl=3600, show_spinner=False)
def get_athlete_image(athlete_name: str, country: str = "") -> str:
    """
    Fetches the first image result from Google Images for an athlete.
    Uses Google's image search with proper headers to avoid blocks.
    Returns image URL or a fallback avatar URL.
    """
    try:
        # Build search query with athlete name + country + "olympic athlete"
        search_query = f"{athlete_name} {country} olympic athlete"
        encoded_query = quote_plus(search_query)
        
        # Google Images search URL
        url = f"https://www.google.com/search?q={encoded_query}&tbm=isch&safe=active"
        
        # Headers to mimic a real browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            # Parse for image URLs in the response
            # Google embeds image URLs in specific patterns
            import re
            
            # Look for image URLs in the HTML content
            # Pattern to find image URLs from Google's response
            patterns = [
                r'\["(https?://[^"]+\.(?:jpg|jpeg|png|webp))"',  # Direct image links
                r'"ou":"(https?://[^"]+)"',  # Original URL pattern
                r'data-src="(https?://[^"]+)"',  # Data-src pattern
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, response.text, re.IGNORECASE)
                for match in matches:
                    # Filter out Google's own domain and icons
                    if 'gstatic' not in match and 'google' not in match and 'favicon' not in match:
                        # Validate the URL is accessible
                        if match.startswith('http'):
                            return match
        
        # Fallback: return None to use default avatar
        return None
        
    except Exception as e:
        # Return None on any error
        return None


def get_profile_image_url(name: str, gender: str, country: str = "") -> str:
    """
    Get profile image URL - tries Google search first, falls back to avatar.
    """
    # Try to get image from Google
    google_image = get_athlete_image(name, country)
    
    if google_image:
        return google_image
    
    # Fallback to generated avatar with initials
    initials = "+".join([part[0].upper() for part in name.split()[:2]]) if name else "A"
    if gender == 'Male':
        return f"https://ui-avatars.com/api/?name={initials}&size=200&background=3498db&color=fff&bold=true"
    else:
        return f"https://ui-avatars.com/api/?name={initials}&size=200&background=e74c3c&color=fff&bold=true"



# Calculate age from birth_date
def calculate_age(birth_date):
    try:
        if pd.notna(birth_date):
            birth = pd.to_datetime(birth_date)
            age = 2025 - birth.year
            return age
    except:
        pass
    return None

df_athletes['age'] = df_athletes['birth_date'].apply(calculate_age)

# Add continent mapping using country names
def get_continent_from_country_name(country_name):
    """Get continent name from country name - EVERY country gets a continent"""
    
    # Complete mapping for ALL Olympic countries including special cases
    complete_mapping = {
        # Special Olympic codes
        'AIN': 'Europe',  # Individual Neutral Athletes (Russia)
        'EOR': 'Africa',  # Refugee Olympic Team
        
        # Name variations and special territories
        'IR Iran': 'Asia',
        'Hong Kong, China': 'Asia',
        'Chinese Taipei': 'Asia',
        'Great Britain': 'Europe',
        'Korea': 'Asia',
        'DPR Korea': 'Asia',
        'Republic of Korea': 'Asia',
        'Republic of Moldova': 'Europe',
        'Türkiye': 'Europe',
        'T�rkiye': 'Europe',
        'Lao PDR': 'Asia',
        'Virgin Islands, US': 'North America',
        'Virgin Islands, B': 'North America',
        'StVincent&Grenadines': 'North America',
        'St Kitts and Nevis': 'North America',
        'Sao Tome & Principe': 'Africa',
        'Bosnia & Herzegovina': 'Europe',
        'Centr Afric Re': 'Africa',  # Central African Republic
        'C�te d\'Ivoire': 'Africa',
        'Côte d\'Ivoire': 'Africa',
        'UA Emirates': 'Asia',  # United Arab Emirates
        
        # Standard country names
        'Afghanistan': 'Asia', 'Albania': 'Europe', 'Algeria': 'Africa', 'American Samoa': 'Oceania',
        'Andorra': 'Europe', 'Angola': 'Africa', 'Antigua and Barbuda': 'North America',
        'Argentina': 'South America', 'Armenia': 'Asia', 'Aruba': 'North America',
        'Australia': 'Oceania', 'Austria': 'Europe', 'Azerbaijan': 'Asia',
        'Bahamas': 'North America', 'Bahrain': 'Asia', 'Bangladesh': 'Asia', 'Barbados': 'North America',
        'Belgium': 'Europe', 'Belize': 'North America', 'Benin': 'Africa', 'Bermuda': 'North America',
        'Bhutan': 'Asia', 'Bolivia': 'South America', 'Botswana': 'Africa', 'Brazil': 'South America',
        'Brunei Darussalam': 'Asia', 'Bulgaria': 'Europe', 'Burkina Faso': 'Africa', 'Burundi': 'Africa',
        'Cabo Verde': 'Africa', 'Cambodia': 'Asia', 'Cameroon': 'Africa', 'Canada': 'North America',
        'Cayman Islands': 'North America', 'Chad': 'Africa', 'Chile': 'South America', 'China': 'Asia',
        'Colombia': 'South America', 'Comoros': 'Africa', 'Congo': 'Africa', 'Cook Islands': 'Oceania',
        'Costa Rica': 'North America', 'Croatia': 'Europe', 'Cuba': 'North America', 'Cyprus': 'Europe',
        'Czechia': 'Europe', 'DR Congo': 'Africa', 'Denmark': 'Europe', 'Djibouti': 'Africa',
        'Dominica': 'North America', 'Dominican Republic': 'North America', 'Ecuador': 'South America',
        'Egypt': 'Africa', 'El Salvador': 'North America', 'Equatorial Guinea': 'Africa',
        'Eritrea': 'Africa', 'Estonia': 'Europe', 'Eswatini': 'Africa', 'Ethiopia': 'Africa',
        'Fiji': 'Oceania', 'Finland': 'Europe', 'France': 'Europe', 'Gabon': 'Africa',
        'Gambia': 'Africa', 'Georgia': 'Asia', 'Germany': 'Europe', 'Ghana': 'Africa',
        'Greece': 'Europe', 'Grenada': 'North America', 'Guam': 'Oceania', 'Guatemala': 'North America',
        'Guinea': 'Africa', 'Guinea-Bissau': 'Africa', 'Guyana': 'South America', 'Haiti': 'North America',
        'Honduras': 'North America', 'Hungary': 'Europe', 'Iceland': 'Europe', 'India': 'Asia',
        'Indonesia': 'Asia', 'Iraq': 'Asia', 'Ireland': 'Europe', 'Israel': 'Asia', 'Italy': 'Europe',
        'Jamaica': 'North America', 'Japan': 'Asia', 'Jordan': 'Asia', 'Kazakhstan': 'Asia',
        'Kenya': 'Africa', 'Kiribati': 'Oceania', 'Kosovo': 'Europe', 'Kuwait': 'Asia',
        'Kyrgyzstan': 'Asia', 'Latvia': 'Europe', 'Lebanon': 'Asia', 'Lesotho': 'Africa',
        'Liberia': 'Africa', 'Libya': 'Africa', 'Liechtenstein': 'Europe', 'Lithuania': 'Europe',
        'Luxembourg': 'Europe', 'Madagascar': 'Africa', 'Malawi': 'Africa', 'Malaysia': 'Asia',
        'Maldives': 'Asia', 'Mali': 'Africa', 'Malta': 'Europe', 'Marshall Islands': 'Oceania',
        'Mauritania': 'Africa', 'Mauritius': 'Africa', 'Mexico': 'North America', 'Micronesia': 'Oceania',
        'Monaco': 'Europe', 'Mongolia': 'Asia', 'Montenegro': 'Europe', 'Morocco': 'Africa',
        'Mozambique': 'Africa', 'Myanmar': 'Asia', 'Namibia': 'Africa', 'Nauru': 'Oceania',
        'Nepal': 'Asia', 'Netherlands': 'Europe', 'New Zealand': 'Oceania', 'Nicaragua': 'North America',
        'Niger': 'Africa', 'Nigeria': 'Africa', 'North Macedonia': 'Europe', 'Norway': 'Europe',
        'Oman': 'Asia', 'Pakistan': 'Asia', 'Palau': 'Oceania', 'Palestine': 'Asia',
        'Panama': 'North America', 'Papua New Guinea': 'Oceania', 'Paraguay': 'South America',
        'Peru': 'South America', 'Philippines': 'Asia', 'Poland': 'Europe', 'Portugal': 'Europe',
        'Puerto Rico': 'North America', 'Qatar': 'Asia', 'Romania': 'Europe', 'Rwanda': 'Africa',
        'Saint Lucia': 'North America', 'Samoa': 'Oceania', 'San Marino': 'Europe', 'Saudi Arabia': 'Asia',
        'Senegal': 'Africa', 'Serbia': 'Europe', 'Seychelles': 'Africa', 'Sierra Leone': 'Africa',
        'Singapore': 'Asia', 'Slovakia': 'Europe', 'Slovenia': 'Europe', 'Solomon Islands': 'Oceania',
        'Somalia': 'Africa', 'South Africa': 'Africa', 'South Sudan': 'Africa', 'Spain': 'Europe',
        'Sri Lanka': 'Asia', 'Sudan': 'Africa', 'Suriname': 'South America', 'Sweden': 'Europe',
        'Switzerland': 'Europe', 'Syria': 'Asia', 'Tajikistan': 'Asia', 'Tanzania': 'Africa',
        'Thailand': 'Asia', 'Timor-Leste': 'Asia', 'Togo': 'Africa', 'Tonga': 'Oceania',
        'Trinidad and Tobago': 'North America', 'Tunisia': 'Africa', 'Turkmenistan': 'Asia',
        'Tuvalu': 'Oceania', 'Uganda': 'Africa', 'Ukraine': 'Europe', 'United States': 'North America',
        'Uruguay': 'South America', 'Uzbekistan': 'Asia', 'Vanuatu': 'Oceania', 'Venezuela': 'South America',
        'Vietnam': 'Asia', 'Yemen': 'Asia', 'Zambia': 'Africa', 'Zimbabwe': 'Africa',
    }
    
    return complete_mapping.get(country_name, 'Other')

df_athletes['Continent'] = df_athletes['country'].apply(get_continent_from_country_name)

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
    
    # Find coach for this athlete
    athlete_coach_name = None
    coach_data = None
    if pd.notna(athlete_data['coach']):
        # Extract first coach name from the coach field
        coach_text = str(athlete_data['coach']).replace('<br>', ',').replace('<BR>', ',')
        # Get first coach mentioned
        if '(' in coach_text:
            athlete_coach_name = coach_text.split('(')[0].strip().strip(',').strip()
        else:
            athlete_coach_name = coach_text.split(',')[0].strip()
    
    # Try to find coach in coaches dataframe
    if athlete_coach_name:
        coach_match = df_coaches[df_coaches['name'].str.contains(athlete_coach_name.split()[0], case=False, na=False)]
        if not coach_match.empty:
            coach_data = coach_match.iloc[0]
    
    # Athlete profile (3 columns)
    col1, col2, col3 = st.columns([1, 2, 2])
    
    with col1:
        st.markdown("### 📸 Profile")
        # Fetch athlete image from Google search
        with st.spinner("Loading image..."):
            image_url = get_profile_image_url(
                athlete_data['name'], 
                athlete_data['gender'],
                athlete_data['country'] if pd.notna(athlete_data['country']) else ""
            )
        
        try:
            st.image(image_url, caption=f"{athlete_data['name']}", width=200)
        except Exception:
            # If image fails to load, use fallback
            fallback_url = f"https://ui-avatars.com/api/?name={athlete_data['name'].replace(' ', '+')}&size=200&background=667eea&color=fff&bold=true"
            st.image(fallback_url, caption=f"{athlete_data['name']}", width=200)
    
    with col2:
        st.markdown("### 📋 Personal Information")
        st.markdown(f"**Full Name:** {athlete_data['name']}")
        
        # Add flag emoji (simplified)
        country_code = athlete_data['country_code']
        st.markdown(f"**Country/NOC:** {athlete_data['country']} ({country_code})")
        
        if pd.notna(athlete_data.get('height')) and athlete_data.get('height') > 0:
            st.markdown(f"**Height:** {athlete_data['height']} cm")
        else:
            st.markdown(f"**Height:** Unknown")
            
        if pd.notna(athlete_data.get('weight')) and athlete_data.get('weight') > 0:
            st.markdown(f"**Weight:** {athlete_data['weight']} kg")
        else:
            st.markdown(f"**Weight:** Unknown")
            
        if pd.notna(athlete_data['age']):
            st.markdown(f"**Age:** {int(athlete_data['age'])} years")
        else:
            st.markdown(f"**Age:** Unknown")
        
        if pd.notna(athlete_data['birth_date']):
            st.markdown(f"**Birth Date:** {athlete_data['birth_date']}")
        else:
            st.markdown(f"**Birth Date:** Unknown")
        
        if pd.notna(athlete_data['birth_place']):
            st.markdown(f"**Birth Place:** {athlete_data['birth_place']}")
        else:
            st.markdown(f"**Birth Place:** Unknown")
    
    with col3:
        st.markdown("### 🏅 Athletic Information")
        
        # Sports & Disciplines (clean display - remove brackets and quotes)
        if pd.notna(athlete_data['disciplines']):
            disciplines_clean = str(athlete_data['disciplines']).strip("[]'\"").replace("'", "").replace('"', '')
            st.markdown(f"**Sport(s):** {disciplines_clean}")
        else:
            st.markdown(f"**Sport(s):** Unknown")
        
        if pd.notna(athlete_data['events']):
            events_clean = str(athlete_data['events']).strip("[]'\"").replace("'", "").replace('"', '')
            st.markdown(f"**Event(s):** {events_clean}")
        else:
            st.markdown(f"**Event(s):** Unknown")
        
        # Coach information (clean display - remove HTML tags)
        if pd.notna(athlete_data['coach']):
            coach_clean = str(athlete_data['coach']).replace('<br>', ', ').replace('<BR>', ', ')
            st.markdown(f"**Coach(es):** {coach_clean}")
        else:
            st.markdown(f"**Coach(es):** Unknown")
        
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
    
    # Coach mini card BELOW athlete profile (if found)
    if coach_data is not None:
        st.markdown("---")
        st.subheader("👨‍🏫 Coach Information")
        
        coach_col1, coach_col2, coach_col3 = st.columns([1, 2, 2])
        
        with coach_col1:
            # Coach image - also fetched from Google
            with st.spinner("Loading coach image..."):
                coach_image_url = get_profile_image_url(
                    coach_data['name'],
                    coach_data['gender'],
                    coach_data['country'] if pd.notna(coach_data['country']) else ""
                )
            
            try:
                st.image(coach_image_url, caption="Coach", width=200)
            except Exception:
                fallback_url = f"https://ui-avatars.com/api/?name=Coach&size=200&background=2ecc71&color=fff&bold=true"
                st.image(fallback_url, caption="Coach", width=200)
        
        with coach_col2:
            st.markdown("### 📋 Coach Profile")
            st.markdown(f"**Full Name:** {coach_data['name']}")
            st.markdown(f"**Country:** {coach_data['country']}")
            st.markdown(f"**Gender:** {coach_data['gender']}")
            
            if pd.notna(coach_data.get('birth_date')):
                st.markdown(f"**Birth Date:** {coach_data['birth_date']}")
            else:
                st.markdown(f"**Birth Date:** Unknown")
        
        with coach_col3:
            st.markdown("### 🏅 Coaching Details")
            
            if pd.notna(coach_data.get('disciplines')):
                coach_disciplines = str(coach_data['disciplines']).strip("[]'\"").replace("'", "").replace('"', '')
                st.markdown(f"**Sport(s):** {coach_disciplines}")
            else:
                st.markdown(f"**Sport(s):** Unknown")
            
            if pd.notna(coach_data.get('category')):
                category_map = {'C': 'Coach', 'HC': 'Head Coach', 'AC': 'Assistant Coach'}
                category = category_map.get(coach_data['category'], coach_data['category'])
                st.markdown(f"**Role:** {category}")
            else:
                st.markdown(f"**Role:** Coach")
            
            if pd.notna(coach_data.get('events')):
                events_clean = str(coach_data['events']).strip("[]'\"").replace("'", "").replace('"', '')
                st.markdown(f"**Event(s):** {events_clean}")

st.markdown("---")

# Task 2: Athlete Age Distribution
st.subheader("📊 Athlete Age Distribution")

age_data = df_filtered[df_filtered['age'].notna()].copy()

# Clean disciplines for display (remove brackets and quotes)
age_data['disciplines_clean'] = age_data['disciplines'].apply(
    lambda x: str(x).strip("[]'\"}").replace("'", "").replace('"', '') if pd.notna(x) else 'Unknown'
)

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
        st.plotly_chart(fig_box, width='stretch')

with col2:
    # Violin plot by sport (top 10 sports)
    if not age_data.empty:
        # Get top 10 sports by athlete count (using cleaned disciplines)
        top_sports = age_data['disciplines_clean'].value_counts().head(10).index.tolist()
        age_sports = age_data[age_data['disciplines_clean'].isin(top_sports)]
        
        fig_violin = px.violin(
            age_sports,
            y='disciplines_clean',
            x='age',
            color='gender',
            title='Age Distribution by Top 10 Sports',
            labels={'age': 'Age (years)', 'disciplines_clean': 'Sport'},
            orientation='h',
            box=True
        )
        fig_violin.update_layout(height=400)
        st.plotly_chart(fig_violin, width='stretch')

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
        st.plotly_chart(fig_pie, width='stretch')
    
    with col2:
        fig_bar = px.bar(
            x=gender_dist.index,
            y=gender_dist.values,
            title='Global Gender Count',
            labels={'x': 'Gender', 'y': 'Number of Athletes'},
            color=gender_dist.index,
            color_discrete_map={'Male': '#3498db', 'Female': '#e74c3c'}
        )
        st.plotly_chart(fig_bar, width='stretch')

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
        st.plotly_chart(fig_pie, width='stretch')
    
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
        st.plotly_chart(fig_bar, width='stretch')

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
        st.plotly_chart(fig_pie, width='stretch')
    
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
        st.plotly_chart(fig_bar, width='stretch')

# Task 4: Top Athletes by Medals
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