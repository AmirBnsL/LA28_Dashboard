"""
Gender Distribution Component
Displays gender distribution by World, Continent, or Country.
"""
import streamlit as st
import plotly.express as px
import pandas as pd


def render_gender_distribution(df_filtered: pd.DataFrame):
    """Render the Gender Distribution Analysis section."""
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
            if not gender_dist.empty:
                fig_pie = px.pie(
                    values=gender_dist.values,
                    names=gender_dist.index,
                    title='Global Gender Distribution',
                    color=gender_dist.index,
                    color_discrete_map={'Male': '#3498db', 'Female': '#e74c3c'}
                )
                st.plotly_chart(fig_pie, width='stretch')
            else:
                st.info("No data available.")
        
        with col2:
            if not gender_dist.empty:
                fig_bar = px.bar(
                    x=gender_dist.index,
                    y=gender_dist.values,
                    title='Global Gender Count',
                    labels={'x': 'Gender', 'y': 'Number of Athletes'},
                    color=gender_dist.index,
                    color_discrete_map={'Male': '#3498db', 'Female': '#e74c3c'}
                )
                st.plotly_chart(fig_bar, width='stretch')
            else:
                st.info("No data available.")

    elif continent_country_selector == "Continent":
        # Ensure Continent column exists
        if 'Continent' not in df_filtered.columns:
            st.error("Continent data is missing.")
            return

        available_continents = sorted(df_filtered['Continent'].dropna().unique())
        if not available_continents:
            st.warning("No continent data available.")
            return

        selected_continent = st.selectbox(
            "Select Continent:",
            available_continents
        )
        
        continent_data = df_filtered[df_filtered['Continent'] == selected_continent]
        gender_dist = continent_data['gender'].value_counts()
        
        col1, col2 = st.columns(2)
        with col1:
            if not gender_dist.empty:
                fig_pie = px.pie(
                    values=gender_dist.values,
                    names=gender_dist.index,
                    title=f'Gender Distribution in {selected_continent}',
                    color=gender_dist.index,
                    color_discrete_map={'Male': '#3498db', 'Female': '#e74c3c'}
                )
                st.plotly_chart(fig_pie, width='stretch')
            else:
                st.info(f"No data available for {selected_continent}.")
        
        with col2:
            # Country breakdown
            if not continent_data.empty:
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
            else:
                st.info(f"No data available for {selected_continent}.")

    else:  # Country
        available_countries = sorted(df_filtered['country'].dropna().unique())
        if not available_countries:
            st.warning("No country data available.")
            return

        selected_country_gender = st.selectbox(
            "Select Country:",
            available_countries
        )
        
        country_data = df_filtered[df_filtered['country'] == selected_country_gender]
        gender_dist = country_data['gender'].value_counts()
        
        col1, col2 = st.columns(2)
        with col1:
            if not gender_dist.empty:
                fig_pie = px.pie(
                    values=gender_dist.values,
                    names=gender_dist.index,
                    title=f'Gender Distribution in {selected_country_gender}',
                    color=gender_dist.index,
                    color_discrete_map={'Male': '#3498db', 'Female': '#e74c3c'}
                )
                st.plotly_chart(fig_pie, width='stretch')
            else:
                st.info(f"No data available for {selected_country_gender}.")
        
        with col2:
            # Sport breakdown
            if not country_data.empty:
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
            else:
                st.info(f"No data available for {selected_country_gender}.")
