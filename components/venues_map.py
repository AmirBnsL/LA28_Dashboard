"""
Venues Map Component
Displays an interactive 2D map of Olympic venues.
"""
import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os

# Add parent directory to path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.venue_geocoder import add_coordinates_to_venues, get_venue_type_colors


def render_venues_map(df_venues: pd.DataFrame):
    """Render the Olympic Venues Map section."""
    st.header("🗺️ Olympic Venues Map")
    st.markdown("Explore the locations of Olympic venues across Paris and beyond.")

    # Add coordinates dynamically using geocoding
    df_venues_with_coords = add_coordinates_to_venues(df_venues)
    map_data = df_venues_with_coords.dropna(subset=["latitude", "longitude"])

    if not map_data.empty:
        # Get venue type colors
        venue_colors = get_venue_type_colors()
        
        # Create hover text
        map_data = map_data.copy()
        map_data["hover_text"] = map_data.apply(
            lambda row: f"<b>{row['venue']}</b><br>Type: {row['venue_type']}<br>Sports: {row.get('sports', 'N/A')}",
            axis=1
        )
        
        # Create 2D scatter map with Plotly
        fig_venues = px.scatter_mapbox(
            map_data,
            lat="latitude",
            lon="longitude",
            color="venue_type",
            color_discrete_map=venue_colors,
            hover_name="venue",
            hover_data={"venue_type": True, "sports": True, "latitude": False, "longitude": False},
            zoom=9,
            center={"lat": 48.8566, "lon": 2.3522},  # Paris center
            height=600,
            title="Paris 2024 Olympic Venues",
        )
        
        fig_venues.update_layout(
            mapbox_style="carto-positron",
            margin={"r": 0, "t": 40, "l": 0, "b": 0},
            legend_title_text="Venue Type",
        )
        
        fig_venues.update_traces(marker=dict(size=14))
        
        st.plotly_chart(fig_venues, width='stretch')
        
        # Legend
        st.subheader("🎨 Venue Type Legend")
        cols = st.columns(len(venue_colors))
        for i, (venue_type, color) in enumerate(venue_colors.items()):
            with cols[i]:
                st.markdown(f"<span style='color:{color}; font-size:24px;'>●</span> **{venue_type}**", unsafe_allow_html=True)
        
        # Venue details table
        with st.expander("📋 All Venue Details"):
            display_cols = ["venue", "venue_type", "sports"] if "sports" in map_data.columns else ["venue", "venue_type"]
            st.dataframe(
                map_data[display_cols].drop_duplicates(),
                width='stretch',
                hide_index=True,
            )
    else:
        st.warning("⚠️ Could not generate map: Venue coordinates are missing.")
