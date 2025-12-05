"""
Age Distribution Component
Displays box plot and violin plot for athlete age distribution.
"""
import streamlit as st
import plotly.express as px
import pandas as pd


def render_age_distribution(df_filtered: pd.DataFrame):
    """Render the Athlete Age Distribution section."""
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
        else:
            st.info("No age data available for the selected filters.")

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
        else:
            st.info("No age data available for the selected filters.")
