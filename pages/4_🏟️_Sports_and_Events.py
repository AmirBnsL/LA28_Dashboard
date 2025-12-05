import streamlit as st
import pandas as pd
import plotly.express as px
from functools import lru_cache
import pycountry
from pycountry_convert import (
    country_alpha2_to_continent_code,
    convert_continent_code_to_continent_name
)

# -------------------------------------------------------
# Helpers
# -------------------------------------------------------

@lru_cache(maxsize=None)
def get_continent(country):
    if pd.isna(country) or country is None:
        return "Unknown"
    try:
        country_obj = pycountry.countries.lookup(country.strip())
        country_alpha2 = country_obj.alpha_2
        continent_code = country_alpha2_to_continent_code(country_alpha2)
        continent_name = convert_continent_code_to_continent_name(continent_code)
        return continent_name
    except Exception:
        return "Other/Special"


venue_coords = {
    "Aquatics Centre": [48.9329, 2.3705],
    "Bercy Arena": [48.8386, 2.3785],
    "Bordeaux Stadium": [44.8976, -0.5660],
    "Champ de Mars Arena": [48.8556, 2.2986],  
    "Château de Versailles": [48.8049, 2.1204],
    "Chateauroux Shooting Centre": [46.8190, 1.7010],
    "Eiffel Tower Stadium": [48.8584, 2.2945],
    "Elancourt Hill": [48.7885, 1.9683],
    "Geoffroy-Guichard Stadium": [45.4608, 4.3901],
    "Grand Palais": [48.8661, 2.3125],
    "Hôtel de Ville": [48.8566, 2.3522],
    "Invalides": [48.8554, 2.3123],
    "La Beaujoire Stadium": [47.2556, -1.5254],
    "La Concorde": [48.8656, 2.3212],
    "Le Bourget Sport Climbing Venue": [48.9540, 2.4300],
    "Golf National": [48.7547, 2.0754],
    "Lyon Stadium": [45.7653, 4.9820],
    "Marseille Marina": [43.2766, 5.3697],
    "Marseille Stadium": [43.2699, 5.3959],
    "Nice Stadium": [43.7051, 7.1926],
    "North Paris Arena": [48.9018, 2.3700],
    "Parc des Princes": [48.8414, 2.2530],
    "Paris La Defense Arena": [48.8958, 2.2297],
    "Pierre Mauroy Stadium": [50.6119, 3.1305],
    "Pont Alexandre III": [48.8639, 2.3135],
    "Porte de La Chapelle Arena": [48.9013, 2.3590],
    "Stade Roland-Garros": [48.8471, 2.2492],
    "Saint-Quentin-en-Yvelines BMX Stadium": [48.7880, 2.0200],
    "Saint-Quentin-en-Yvelines Velodrome": [48.7881, 2.0345],
    "South Paris Arena": [48.8325, 2.2870],
    "Stade de France": [48.9244, 2.3601],
    "Teahupo'o, Tahiti": [-17.8471, -149.2667],
    "Trocadéro": [48.8624, 2.2875],
    "Vaires-sur-Marne Nautical Stadium": [48.8647, 2.6438],
    "Yves-du-Manoir Stadium": [48.9294, 2.2481],
}


def add_coords(row):
    for k, v in venue_coords.items():
        if k in str(row["venue"]):
            return pd.Series([v[0], v[1]])
    return pd.Series([None, None])

# -------------------------------------------------------
# Streamlit config
# -------------------------------------------------------

st.set_page_config(
    page_title="Sports & Events Analysis",
    page_icon="🏟️",
    layout="wide"
)

st.title("🏟️ Sports, Events & Venues")
st.markdown("Explore the schedule, medal distribution by sport, and venue locations of the Paris 2024 Games.")

# -------------------------------------------------------
# Data loading
# -------------------------------------------------------

@st.cache_data
def load_data():
    schedule_df = pd.read_csv("../data/schedules.csv")
    medals_df = pd.read_csv("../data/medals.csv")
    venues_df = pd.read_csv("../data/venues.csv")

    schedule_df["start_date"] = pd.to_datetime(schedule_df["start_date"])
    schedule_df["end_date"] = pd.to_datetime(schedule_df["end_date"])
    return schedule_df, medals_df, venues_df

try:
    df_schedule, df_medals, df_venues = load_data()
except FileNotFoundError:
    st.error("❌ Data files not found. Please ensure 'schedules.csv', 'medals.csv', and 'venues.csv' are in the working directory.")
    st.stop()

df_medals["continent"] = df_medals["country"].apply(get_continent)
df_medals.sort_values(by=[ "country"], inplace=True)
print(df_medals["country"].unique())
# -------------------------------------------------------
# Sidebar filters
# -------------------------------------------------------

st.sidebar.header("Global Filters")

all_countries_names = sorted(df_medals["country"].dropna().unique().astype(str))
selected_countries = st.sidebar.multiselect("Select Country", all_countries_names)

all_sports = sorted(df_schedule["discipline"].unique().astype(str))
selected_sports = st.sidebar.multiselect("Select Sport", all_sports)

if selected_sports:
    available_venues = df_schedule[df_schedule["discipline"].isin(selected_sports)]["venue"].dropna().unique()
else:
    available_venues = df_schedule["venue"].dropna().unique()

all_venues = sorted(available_venues.astype(str))
selected_venues = st.sidebar.multiselect("Select Venue", all_venues)

medal_types = ["Gold Medal", "Silver Medal", "Bronze Medal"]
selected_medals = st.sidebar.multiselect("Select Medal Type", medal_types, default=medal_types)

all_continents = sorted(df_medals["continent"].dropna().unique().tolist())
selected_continent = st.sidebar.selectbox(
    "Filter by Continent",
    all_continents,
    index=all_continents.index("Europe") if "Europe" in all_continents else 0,
)

# -------------------------------------------------------
# Event schedule
# -------------------------------------------------------

st.header("📅 Event Schedule")

schedule_filtered = df_schedule.copy()

if selected_sports:
    schedule_filtered = schedule_filtered[schedule_filtered["discipline"].isin(selected_sports)]

if selected_venues:
    schedule_filtered = schedule_filtered[schedule_filtered["venue"].isin(selected_venues)]

if len(schedule_filtered) > 2000 and not (selected_sports or selected_venues):
    st.info("ℹ️ The full schedule is very large. Please select a **Sport** or **Venue** in the sidebar to view the Timeline.")
elif schedule_filtered.empty:
    st.warning("⚠️ No events found for the selected combination of filters.")
else:
    schedule_filtered = schedule_filtered.sort_values(by="start_date")
    fig_timeline = px.timeline(
        schedule_filtered,
        x_start="start_date",
        x_end="end_date",
        y="event",
        color="discipline",
        hover_data=["venue", "phase", "status", "gender"],
        title=f"Event Timeline ({len(schedule_filtered)} events)",
        height=600 if len(schedule_filtered) < 50 else 1000,
    )
    fig_timeline.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_timeline, use_container_width=True)

st.divider()

# -------------------------------------------------------
# Medal count by sport
# -------------------------------------------------------

st.header("🥇 Medal Count by Sport")

medals_filtered = df_medals.copy()

if selected_medals:
    medals_filtered = medals_filtered[medals_filtered["medal_type"].isin(selected_medals)]

if selected_countries:
    medals_filtered = medals_filtered[medals_filtered["country"].isin(selected_countries)]

if selected_sports:
    medals_filtered = medals_filtered[medals_filtered["discipline"].isin(selected_sports)]

if medals_filtered.empty:
    st.warning("⚠️ No medal data available for the current filters.")
    st.caption(
        "**Debugging Tip:** Try clearing the **Sport** filter to view the total medal count for the selected country, as the combination of filters may be too restrictive."
    )
else:
    medals_counts = (
        medals_filtered
        .groupby(["discipline", "event"])
        .size()
        .reset_index(name="count")
    )

    fig_treemap = px.treemap(
        medals_counts,
        path=[px.Constant("Medals"), "discipline", "event"],
        values="count",
        color="count",
        color_continuous_scale="Viridis",
        title="Distribution of Medals across Sports and Events",
    )
    fig_treemap.update_traces(root_color="lightgrey")
    st.plotly_chart(fig_treemap, use_container_width=True)

st.divider()

# -------------------------------------------------------
# Venues map
# -------------------------------------------------------

st.header("🗺️ Olympic Venues Map")

if "latitude" not in df_venues.columns:
    df_venues[["latitude", "longitude"]] = df_venues.apply(add_coords, axis=1)

map_data = df_venues.dropna(subset=["latitude", "longitude"])

if not map_data.empty:
    fig_map = px.scatter_mapbox(
        map_data,
        lat="latitude",
        lon="longitude",
        hover_name="venue",
        hover_data=["sports", "tag"],
        zoom=10,
        center={"lat": 48.8566, "lon": 2.3522},
        title="Venue Locations",
        color_discrete_sequence=["#f63366"],
    )
    fig_map.update_layout(mapbox_style="open-street-map")
    fig_map.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.warning("⚠️ Could not generate map: Venue coordinates are missing.")

st.divider()

# -------------------------------------------------------
# Global medal distribution & continent comparison
# -------------------------------------------------------

st.header("🌎 Global Medal Distribution by Type")
st.markdown("Visualizes the total count of **selected medal types** for all countries.")

medal_analysis_df = df_medals.copy()

if selected_medals:
    medal_analysis_df = medal_analysis_df[medal_analysis_df["medal_type"].isin(selected_medals)]

if not medal_analysis_df.empty:
    world_map_data = (
        medal_analysis_df
        .groupby(["country", "country_code", "continent", "medal_type"])
        .size()
        .reset_index(name="total_medals")
    )

    world_map_pivot = world_map_data.pivot_table(
        index=["country", "country_code", "continent"],
        columns="medal_type",
        values="total_medals",
        fill_value=0,
    ).reset_index()

    world_map_pivot["Total Medals"] = world_map_pivot[selected_medals].sum(axis=1)

    fig_map_global = px.choropleth(
        world_map_pivot,
        locations="country_code",
        color="Total Medals",
        hover_name="country",
        hover_data=selected_medals + ["continent"],
        projection="natural earth",
        color_continuous_scale=px.colors.sequential.Plasma,
        title=f"Global Medal Distribution (Filtered Types: {', '.join([m.capitalize() for m in selected_medals])})",
    )

    fig_map_global.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
    st.plotly_chart(fig_map_global, use_container_width=True)
else:
    st.info("Please select at least one medal type in the sidebar to view the global map.")

st.subheader(f"📊 Medal Comparison for **{selected_continent}**")

continent_filtered_df = medal_analysis_df[medal_analysis_df["continent"] == selected_continent]

if not continent_filtered_df.empty:
    bar_chart_data = (
        continent_filtered_df
        .groupby(["country", "medal_type"])
        .size()
        .reset_index(name="total_medals")
    )

    fig_bar = px.bar(
        bar_chart_data,
        x="country",
        y="total_medals",
        color="medal_type",
        text_auto=True,
        color_discrete_map={
            "Gold Medal": "gold",
            "Silver Medal": "silver",
            "Bronze Medal": "#cd7f32",
        },
        title=f"Medal Count by Country in {selected_continent}",
        labels={"total_medals": "Total Medals", "country": "Country"},
    )
    fig_bar.update_layout(xaxis={"categoryorder": "total descending"})
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.warning(
        f"⚠️ No medal data available for the selected continent: **{selected_continent}** "
        "with the current medal type filters."
    )

st.divider()


st.header("🇨🇺🇫🇷 Head-to-Head Country Comparison")

countries = sorted(df_medals["country"].unique())
col_sel1, col_sel2 = st.columns(2)
with col_sel1:
    country_a = st.selectbox(
        "Country A",
        countries,
        key="country_a",
    )
countries_b_options = [c for c in countries if c != country_a]
with col_sel2:
    default_b_index = 0  
    country_b = st.selectbox(
        "Country B",
        countries_b_options,
        index=default_b_index,
        key="country_b",
    )
def country_summary(df, country):
    sub = df[df["country"] == country]
    return {
        "Total medals": len(sub),
        "Gold": (sub["medal_type"] == "Gold Medal").sum(),
        "Silver": (sub["medal_type"] == "Silver Medal").sum(),
        "Bronze": (sub["medal_type"] == "Bronze Medal").sum(),
        "Sports": sub["discipline"].nunique(),
        "Events": sub["event"].nunique(),
    }

if country_a and country_b:
    summary_a = country_summary(df_medals, country_a)
    summary_b = country_summary(df_medals, country_b)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(country_a)
        for k, v in summary_a.items():
            st.metric(k, v)
    with col2:
        st.subheader(country_b)
        for k, v in summary_b.items():
            st.metric(k, v)

# -------------------------------------------------------

st.header("🏅 Who Won the Day?")

# Normalized date columns
df_medals["medal_day"] = pd.to_datetime(df_medals["medal_date"]).dt.date
df_schedule["day"] = pd.to_datetime(df_schedule["start_date"]).dt.date

all_days = sorted(df_medals["medal_day"].dropna().unique())
selected_day = st.slider(
    "Select a day of the Games",
    min_value=min(all_days),
    max_value=max(all_days),
    value=min(all_days),
    format="YYYY-MM-DD",
)

# Medals on that day
day_medals = df_medals[df_medals["medal_day"] == selected_day]

st.subheader(f"Medals awarded on {selected_day}")
if day_medals.empty:
    st.info("No medals recorded for this day.")
else:
    medal_table = (
        day_medals
        .groupby(["country", "medal_type"])
        .size()
        .reset_index(name="count")
    )
    fig_day = px.bar(
        medal_table,
        x="country",
        y="count",
        color="medal_type",
        title=f"Medals by country on {selected_day}",
        text_auto=True,
    )
    st.plotly_chart(fig_day, use_container_width=True)

# Key events on that day
st.subheader(f"Key events on {selected_day}")
day_events = df_schedule[df_schedule["day"] == selected_day]

if day_events.empty:
    st.info("No events scheduled for this day.")
else:
    fig_day_timeline = px.timeline(
        day_events,
        x_start="start_date",
        x_end="end_date",
        y="event",
        color="discipline",
        hover_data=["venue", "phase", "status", "gender"],
        title=f"Event timeline on {selected_day}",
        height=600,
    )
    fig_day_timeline.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_day_timeline, use_container_width=True)
