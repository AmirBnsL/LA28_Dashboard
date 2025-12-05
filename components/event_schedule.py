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
        # Ensure dates are datetime objects
        schedule_filtered["start_date"] = pd.to_datetime(schedule_filtered["start_date"])
        schedule_filtered["end_date"] = pd.to_datetime(schedule_filtered["end_date"])
        
        # Create a day column for grouping
        schedule_filtered["day_group"] = schedule_filtered["start_date"].dt.date
        
        # Get unique sorted days
        unique_days = sorted(schedule_filtered["day_group"].unique())
        
        # Create tabs: "All Events" + one for each day
        day_labels = [day.strftime("%b %d") for day in unique_days]
        all_labels = ["All Events"] + day_labels
        
        tabs = st.tabs(all_labels)
        
        for i, tab_label in enumerate(all_labels):
            with tabs[i]:
                if i == 0:
                    # All Events
                    current_data = schedule_filtered.sort_values(by="start_date")
                    chart_title = f"<b>Full Schedule</b> <br><sup>{len(current_data)} events scheduled</sup>"
                else:
                    # Specific Day
                    target_day = unique_days[i-1]
                    current_data = schedule_filtered[schedule_filtered["day_group"] == target_day].sort_values(by="start_date")
                    chart_title = f"<b>Schedule for {tab_label}</b> <br><sup>{len(current_data)} events scheduled</sup>"
                
                if current_data.empty:
                    st.info(f"No events found for {tab_label}.")
                    continue

                # Calculate dynamic height based on number of unique events
                # 40px per event track + 100px buffer for axis/title
                n_events = current_data['event'].nunique()
                dynamic_height = max(200, n_events * 40 + 100)

                fig_timeline = px.timeline(
                    current_data,
                    x_start="start_date",
                    x_end="end_date",
                    y="event",
                    color="discipline",
                    hover_data={
                        "venue": True,
                        "phase": True,
                        "status": True,
                        "gender": True,
                        "start_date": "|%b %d %H:%M",
                        "end_date": "|%H:%M",
                        "discipline": False
                    },
                    title=chart_title,
                    height=dynamic_height,
                    color_discrete_sequence=px.colors.qualitative.Prism
                )
                
                fig_timeline.update_yaxes(
                    autorange="reversed",
                    title_text="",
                    showgrid=True,
                    gridcolor='rgba(200,200,200,0.2)',
                    tickfont=dict(size=12)
                )
                
                fig_timeline.update_xaxes(
                    title_text="",
                    showgrid=True,
                    gridcolor='rgba(200,200,200,0.2)',
                    rangeslider_visible=True,
                    tickformat="%b %d\n%H:%M"
                )

                fig_timeline.update_layout(
                    template="plotly_white",
                    hovermode="closest",
                    title_font_family="Arial",
                    title_font_size=20,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1,
                        title_text=""
                    ),
                    margin=dict(l=20, r=20, t=60, b=20),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                fig_timeline.update_traces(
                    marker_line_color='white',
                    marker_line_width=1,
                    opacity=0.9,
                    hovertemplate="<b>%{y}</b><br>" +
                                  "Start: %{base|%b %d %H:%M}<br>" +
                                  "End: %{x|%b %d %H:%M}<br>" +
                                  "Venue: %{customdata[0]}<br>" +
                                  "Phase: %{customdata[1]}<br>" +
                                  "Status: %{customdata[2]}"
                )
                
                st.plotly_chart(fig_timeline, width='stretch')
