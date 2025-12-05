"""
Athlete Profile Component
Displays detailed athlete profile, including image, personal info, and coach details.
"""
import streamlit as st
import pandas as pd
import requests
from urllib.parse import quote_plus

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


def render_athlete_profile(df_athletes: pd.DataFrame, df_coaches: pd.DataFrame, df_medallists: pd.DataFrame):
    """Render the Athlete Profile Search section."""
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
                
            if pd.notna(athlete_data.get('age')):
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
