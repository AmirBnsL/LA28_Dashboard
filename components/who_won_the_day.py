"""
Who Won the Day Component
Shows medals and events for a specific day of the Games.
"""
import streamlit as st
import plotly.express as px
import pandas as pd


def render_who_won_the_day(df_medals: pd.DataFrame, df_schedule: pd.DataFrame):
    """Render the Who Won the Day section with daily medal and event breakdown."""
    st.header("🏅 Who Won the Day?")

    df_medals = df_medals.copy()
    df_schedule = df_schedule.copy()
    
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
            color_discrete_map={
                "Gold Medal": "gold",
                "Silver Medal": "silver",
                "Bronze Medal": "#cd7f32",
            },
        )
        fig_day.update_layout(xaxis={"categoryorder": "total descending"})
        st.plotly_chart(fig_day, use_container_width=True)

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
