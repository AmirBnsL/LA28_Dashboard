"""
Event Schedule Component
Displays the timeline of Olympic events.
"""
import streamlit as st
import plotly.express as px
import pandas as pd


def render_event_schedule(df_schedule: pd.DataFrame, selected_sports: list, selected_venues: list):
    """Render the Event Schedule section with timeline visualization."""
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
        # Map event types to user-friendly names
        event_type_map = {
            "ATH": "Individual",
            "TEAM": "Team",
            "HTEAM": "Team Match",
            "HATH": "Individual Match",
            "COUP": "Pair/Couple",
            "HCOUP": "Pair Match"
        }
        
        # Create friendly label column
        if "event_type" in schedule_filtered.columns:
            schedule_filtered["event_type_label"] = schedule_filtered["event_type"].map(event_type_map).fillna("Other")
        else:
            schedule_filtered["event_type_label"] = "All Events"

        # Get unique event types present in the filtered data
        available_types = sorted(schedule_filtered["event_type_label"].unique())
        
        # Create tabs for each event type
        tabs = st.tabs(available_types)
        
        for i, event_type in enumerate(available_types):
            with tabs[i]:
                type_data = schedule_filtered[schedule_filtered["event_type_label"] == event_type].sort_values(by="start_date")
                
                if type_data.empty:
                    st.info(f"No {event_type} events found.")
                    continue
                
                # Calculate dynamic height to avoid huge bars for few events
                # Base height of 100px + 40px per event, capped at 1200px
                dynamic_height = min(1200, max(250, 100 + len(type_data) * 40))

                fig_timeline = px.timeline(
                    type_data,
                    x_start="start_date",
                    x_end="end_date",
                    y="event",
                    color="discipline",
                    hover_data=["venue", "phase", "status", "gender"],
                    title=f"{event_type} Timeline ({len(type_data)} events)",
                    height=dynamic_height,
                )
                fig_timeline.update_yaxes(autorange="reversed")
                st.plotly_chart(fig_timeline, use_container_width=True)
