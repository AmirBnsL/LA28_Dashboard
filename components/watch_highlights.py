"""
Watch Highlights Component
YouTube search integration for Olympic highlights.
"""
import streamlit as st
import pandas as pd
import urllib.parse


def generate_youtube_search_url(sport: str, event: str = None, country: str = None) -> str:
    """Generate a YouTube search URL for Olympic highlights."""
    query_parts = ["Paris 2024 Olympics", sport]
    if event:
        query_parts.append(event)
    if country:
        query_parts.append(country)
    query_parts.append("highlights")
    
    query = " ".join(query_parts)
    encoded_query = urllib.parse.quote(query)
    return f"https://www.youtube.com/results?search_query={encoded_query}"


def render_watch_highlights(df_schedule: pd.DataFrame, df_medals: pd.DataFrame):
    """Render the Watch Highlights section with YouTube search integration."""
    st.header("📺 Watch Highlights")
    st.markdown("Search for Paris 2024 Olympic highlights on YouTube!")

    col_yt1, col_yt2, col_yt3 = st.columns(3)

    with col_yt1:
        # Get unique sports from schedule
        all_sports_yt = sorted(df_schedule["discipline"].dropna().unique().tolist())
        selected_sport_yt = st.selectbox(
            "🏅 Select Sport",
            options=all_sports_yt,
            key="youtube_sport"
        )

    with col_yt2:
        # Get events for selected sport
        sport_events = df_schedule[df_schedule["discipline"] == selected_sport_yt]["event"].dropna().unique().tolist()
        selected_event_yt = st.selectbox(
            "🎯 Select Event (Optional)",
            options=["All Events"] + sorted(sport_events),
            key="youtube_event"
        )

    with col_yt3:
        # Get countries that won medals in this sport
        sport_medal_countries = df_medals[df_medals["discipline"] == selected_sport_yt]["country"].dropna().unique().tolist()
        selected_country_yt = st.selectbox(
            "🌍 Select Country (Optional)",
            options=["Any Country"] + sorted(sport_medal_countries) if sport_medal_countries else ["Any Country"],
            key="youtube_country"
        )

    # Generate YouTube search URL
    event_for_search = None if selected_event_yt == "All Events" else selected_event_yt
    country_for_search = None if selected_country_yt == "Any Country" else selected_country_yt

    youtube_url = generate_youtube_search_url(
        sport=selected_sport_yt,
        event=event_for_search,
        country=country_for_search
    )

    # Display search preview
    search_terms = f"Paris 2024 Olympics {selected_sport_yt}"
    if event_for_search:
        search_terms += f" {event_for_search}"
    if country_for_search:
        search_terms += f" {country_for_search}"
    search_terms += " highlights"

    st.markdown(f"**🔍 Search Query:** `{search_terms}`")

    # YouTube button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        st.link_button(
            "🎬 Watch on YouTube",
            url=youtube_url,
            type="primary",
            width='stretch'
        )

    # Quick links for popular events
    st.subheader("⚡ Quick Links - Popular Events")
    quick_links = [
        ("⚽ Football Final", "Football", "Final"),
        ("🏀 Basketball Final", "Basketball", "Final"),
        ("🏊 Swimming 100m", "Swimming", "100m Freestyle"),
        ("🏃 Athletics 100m", "Athletics", "100m"),
        ("🤸 Gymnastics", "Artistic Gymnastics", None),
        ("🎾 Tennis Final", "Tennis", "Final"),
    ]

    cols = st.columns(6)
    for i, (label, sport, event) in enumerate(quick_links):
        with cols[i]:
            url = generate_youtube_search_url(sport, event)
            st.link_button(label, url, width='stretch')
