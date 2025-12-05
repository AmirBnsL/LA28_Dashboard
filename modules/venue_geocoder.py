"""
Venue geocoding module using geopy for dynamic coordinate lookup.
Uses parallel processing and caching for efficiency.
"""
import pandas as pd
import streamlit as st
from geopy.geocoders import Nominatim
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
import hashlib


# Venue type categories for legend
VENUE_TYPES = {
    "Stadium": ["Stadium", "Stade", "Arena"],
    "Aquatic": ["Aquatics", "Nautical", "Marina", "Swimming"],
    "Indoor": ["Arena", "Palais", "Centre", "Velodrome"],
    "Outdoor": ["Hill", "Beach", "Golf", "Park"],
    "Historic": ["Château", "Invalides", "Trocadéro", "Pont", "Hôtel de Ville"],
}

VENUE_TYPE_COLORS = {
    "Stadium": "#e74c3c",      # Red
    "Aquatic": "#3498db",      # Blue
    "Indoor": "#9b59b6",       # Purple
    "Outdoor": "#2ecc71",      # Green
    "Historic": "#f39c12",     # Orange
    "Other": "#95a5a6",        # Gray
}

# RGB colors for PyDeck (0-255 scale)
VENUE_TYPE_COLORS_RGB = {
    "Stadium": [231, 76, 60, 200],      # Red
    "Aquatic": [52, 152, 219, 200],     # Blue
    "Indoor": [155, 89, 182, 200],      # Purple
    "Outdoor": [46, 204, 113, 200],     # Green
    "Historic": [243, 156, 18, 200],    # Orange
    "Other": [149, 165, 166, 200],      # Gray
}


def get_venue_type(venue_name: str) -> str:
    """Categorize venue by type for legend."""
    for venue_type, keywords in VENUE_TYPES.items():
        for keyword in keywords:
            if keyword.lower() in venue_name.lower():
                return venue_type
    return "Other"


# Fallback coordinates for venues that may be hard to geocode
FALLBACK_COORDS = {
    "Teahupo'o, Tahiti": (-17.8471, -149.2667),
    "Champ de Mars Arena": (48.8556, 2.2986),
    "Eiffel Tower Stadium": (48.8584, 2.2945),
    "La Concorde": (48.8656, 2.3212),
    "South Paris Arena": (48.8325, 2.2870),
    "North Paris Arena": (48.9018, 2.3700),
    "Aquatics Centre": (48.9329, 2.3705),
    "Bercy Arena": (48.8386, 2.3785),
    "Bordeaux Stadium": (44.8976, -0.5660),
    "Château de Versailles": (48.8049, 2.1204),
    "Chateauroux Shooting Centre": (46.8190, 1.7010),
    "Elancourt Hill": (48.7885, 1.9683),
    "Geoffroy-Guichard Stadium": (45.4608, 4.3901),
    "Grand Palais": (48.8661, 2.3125),
    "Hôtel de Ville": (48.8566, 2.3522),
    "Invalides": (48.8554, 2.3123),
    "La Beaujoire Stadium": (47.2556, -1.5254),
    "Le Bourget Sport Climbing Venue": (48.9540, 2.4300),
    "Golf National": (48.7547, 2.0754),
    "Lyon Stadium": (45.7653, 4.9820),
    "Marseille Marina": (43.2766, 5.3697),
    "Marseille Stadium": (43.2699, 5.3959),
    "Nice Stadium": (43.7051, 7.1926),
    "Parc des Princes": (48.8414, 2.2530),
    "Paris La Defense Arena": (48.8958, 2.2297),
    "Pierre Mauroy Stadium": (50.6119, 3.1305),
    "Pont Alexandre III": (48.8639, 2.3135),
    "Porte de La Chapelle Arena": (48.9013, 2.3590),
    "Stade Roland-Garros": (48.8471, 2.2492),
    "Saint-Quentin-en-Yvelines BMX Stadium": (48.7880, 2.0200),
    "Saint-Quentin-en-Yvelines Velodrome": (48.7881, 2.0345),
    "Stade de France": (48.9244, 2.3601),
    "Trocadéro": (48.8624, 2.2875),
    "Vaires-sur-Marne Nautical Stadium": (48.8647, 2.6438),
    "Yves-du-Manoir Stadium": (48.9294, 2.2481),
}


def _geocode_single(venue_name: str, city: str = "Paris, France") -> tuple:
    """
    Geocode a single venue (internal function for parallel processing).
    
    Returns:
        Tuple of (venue_name, latitude, longitude)
    """
    # Check fallback first
    for key, coords in FALLBACK_COORDS.items():
        if key.lower() in venue_name.lower():
            return (venue_name, coords[0], coords[1])
    
    try:
        # Create a new geocoder instance for thread safety
        geolocator = Nominatim(user_agent=f"la28_dashboard_{hashlib.md5(venue_name.encode()).hexdigest()[:8]}")
        
        search_queries = [
            f"{venue_name}, {city}",
            f"{venue_name}, Paris",
            venue_name,
        ]
        
        for query in search_queries:
            try:
                location = geolocator.geocode(query, timeout=10)
                if location:
                    return (venue_name, location.latitude, location.longitude)
            except Exception:
                continue
        
        return (venue_name, None, None)
    
    except Exception:
        return (venue_name, None, None)


@st.cache_data(ttl=86400, show_spinner=False)  # Cache for 24 hours
def geocode_venues_parallel(venue_names: list, max_workers: int = 5) -> dict:
    """
    Geocode multiple venues in parallel using ThreadPoolExecutor.
    
    Args:
        venue_names: List of venue names to geocode
        max_workers: Maximum number of parallel workers (default: 5)
    
    Returns:
        Dictionary mapping venue names to (lat, lon) tuples
    """
    coords = {}
    venues_to_geocode = []
    
    # First, check fallback for all venues
    for venue in venue_names:
        found = False
        for key, fallback_coords in FALLBACK_COORDS.items():
            if key.lower() in venue.lower():
                coords[venue] = fallback_coords
                found = True
                break
        if not found:
            venues_to_geocode.append(venue)
    
    # Geocode remaining venues in parallel
    if venues_to_geocode:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(_geocode_single, venue): venue for venue in venues_to_geocode}
            
            for future in as_completed(futures):
                venue_name, lat, lon = future.result()
                coords[venue_name] = (lat, lon)
    
    return coords


def add_coordinates_to_venues(df_venues: pd.DataFrame) -> pd.DataFrame:
    """
    Add latitude, longitude, and venue_type columns to venues dataframe.
    Uses parallel geocoding for efficiency.
    
    Args:
        df_venues: DataFrame with venue information
    
    Returns:
        DataFrame with added latitude, longitude, and venue_type columns
    """
    if "latitude" in df_venues.columns and "longitude" in df_venues.columns:
        if df_venues["latitude"].notna().any():
            df = df_venues.copy()
            # Add venue_type if missing
            if "venue_type" not in df.columns:
                df["venue_type"] = df["venue"].apply(get_venue_type)
            # Add color_rgb if missing
            if "color_rgb" not in df.columns:
                df["color_rgb"] = df["venue_type"].apply(lambda x: VENUE_TYPE_COLORS_RGB.get(x, VENUE_TYPE_COLORS_RGB["Other"]))
            return df
    
    df = df_venues.copy()
    
    # Get unique venues
    unique_venues = df["venue"].dropna().unique().tolist()
    
    # Show spinner while geocoding
    with st.spinner(f"📍 Geocoding {len(unique_venues)} venues in parallel..."):
        coords_cache = geocode_venues_parallel(unique_venues)
    
    # Apply coordinates
    df["latitude"] = df["venue"].map(lambda x: coords_cache.get(x, (None, None))[0] if x else None)
    df["longitude"] = df["venue"].map(lambda x: coords_cache.get(x, (None, None))[1] if x else None)
    
    # Add venue type for legend
    df["venue_type"] = df["venue"].apply(lambda x: get_venue_type(x) if x else "Other")
    
    # Add RGB colors for PyDeck
    df["color_rgb"] = df["venue_type"].apply(lambda x: VENUE_TYPE_COLORS_RGB.get(x, VENUE_TYPE_COLORS_RGB["Other"]))
    
    return df


def get_venue_type_colors() -> dict:
    """Return the color mapping for venue types."""
    return VENUE_TYPE_COLORS


def get_venue_type_colors_rgb() -> dict:
    """Return the RGB color mapping for PyDeck."""
    return VENUE_TYPE_COLORS_RGB
