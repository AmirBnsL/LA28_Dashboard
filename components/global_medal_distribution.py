"""
Global Medal Distribution Component
Displays a choropleth map and bar chart of medal distribution by country/continent.
"""
import streamlit as st
import plotly.express as px
import pandas as pd


# NOC (Olympic) to ISO-3 country code mapping for codes that differ
NOC_TO_ISO3 = {
    "GER": "DEU",  # Germany
    "GRE": "GRC",  # Greece
    "SUI": "CHE",  # Switzerland
    "NED": "NLD",  # Netherlands
    "POR": "PRT",  # Portugal
    "DEN": "DNK",  # Denmark
    "CRO": "HRV",  # Croatia
    "SLO": "SVN",  # Slovenia
    "RSA": "ZAF",  # South Africa
    "CHI": "CHL",  # Chile
    "IRI": "IRN",  # Iran
    "TPE": "TWN",  # Taiwan
    "KOR": "KOR",  # South Korea (same)
    "PRK": "PRK",  # North Korea (same)
    "MAS": "MYS",  # Malaysia
    "INA": "IDN",  # Indonesia
    "PHI": "PHL",  # Philippines
    "VIE": "VNM",  # Vietnam
    "SIN": "SGP",  # Singapore (actually SGP is used)
    "SGP": "SGP",  # Singapore
    "THA": "THA",  # Thailand (same)
    "UAE": "ARE",  # United Arab Emirates
    "KSA": "SAU",  # Saudi Arabia
    "BRN": "BHR",  # Bahrain
    "KUW": "KWT",  # Kuwait
    "OMA": "OMN",  # Oman
    "LIB": "LBN",  # Lebanon
    "SYR": "SYR",  # Syria (same)
    "BUL": "BGR",  # Bulgaria
    "ROU": "ROU",  # Romania (same)
    "SRB": "SRB",  # Serbia (same)
    "MNE": "MNE",  # Montenegro (same)
    "BIH": "BIH",  # Bosnia (same)
    "MKD": "MKD",  # North Macedonia (same)
    "LAT": "LVA",  # Latvia
    "LTU": "LTU",  # Lithuania (same)
    "EST": "EST",  # Estonia (same)
    "GEO": "GEO",  # Georgia (same)
    "ARM": "ARM",  # Armenia (same)
    "AZE": "AZE",  # Azerbaijan (same)
    "KAZ": "KAZ",  # Kazakhstan (same)
    "UZB": "UZB",  # Uzbekistan (same)
    "KGZ": "KGZ",  # Kyrgyzstan (same)
    "TJK": "TJK",  # Tajikistan (same)
    "TKM": "TKM",  # Turkmenistan (same)
    "MGL": "MNG",  # Mongolia
    "NGR": "NGA",  # Nigeria
    "ALG": "DZA",  # Algeria
    "MAR": "MAR",  # Morocco (same)
    "TUN": "TUN",  # Tunisia (same)
    "EGY": "EGY",  # Egypt (same)
    "ETH": "ETH",  # Ethiopia (same)
    "KEN": "KEN",  # Kenya (same)
    "UGA": "UGA",  # Uganda (same)
    "TAN": "TZA",  # Tanzania
    "ZIM": "ZWE",  # Zimbabwe
    "BOT": "BWA",  # Botswana
    "NAM": "NAM",  # Namibia (same)
    "ANG": "AGO",  # Angola
    "MOZ": "MOZ",  # Mozambique (same)
    "CMR": "CMR",  # Cameroon (same)
    "CIV": "CIV",  # Ivory Coast (same)
    "SEN": "SEN",  # Senegal (same)
    "GHA": "GHA",  # Ghana (same)
    "PUR": "PRI",  # Puerto Rico
    "ISV": "VIR",  # US Virgin Islands
    "IVB": "VGB",  # British Virgin Islands
    "BAH": "BHS",  # Bahamas
    "BAR": "BRB",  # Barbados
    "TTO": "TTO",  # Trinidad (same)
    "JAM": "JAM",  # Jamaica (same)
    "HAI": "HTI",  # Haiti
    "DOM": "DOM",  # Dominican Republic (same)
    "CUB": "CUB",  # Cuba (same)
    "GUA": "GTM",  # Guatemala
    "HON": "HND",  # Honduras
    "ESA": "SLV",  # El Salvador
    "NCA": "NIC",  # Nicaragua
    "CRC": "CRI",  # Costa Rica
    "PAN": "PAN",  # Panama (same)
    "VEN": "VEN",  # Venezuela (same)
    "COL": "COL",  # Colombia (same)
    "ECU": "ECU",  # Ecuador (same)
    "PER": "PER",  # Peru (same)
    "BOL": "BOL",  # Bolivia (same)
    "PAR": "PRY",  # Paraguay
    "URU": "URY",  # Uruguay
    "ARG": "ARG",  # Argentina (same)
    "BRA": "BRA",  # Brazil (same)
    "MEX": "MEX",  # Mexico (same)
    "CAN": "CAN",  # Canada (same)
    "USA": "USA",  # USA (same)
    "GBR": "GBR",  # Great Britain (same)
    "FRA": "FRA",  # France (same)
    "ITA": "ITA",  # Italy (same)
    "ESP": "ESP",  # Spain (same)
    "AUS": "AUS",  # Australia (same)
    "NZL": "NZL",  # New Zealand (same)
    "JPN": "JPN",  # Japan (same)
    "CHN": "CHN",  # China (same)
    "IND": "IND",  # India (same)
    "PAK": "PAK",  # Pakistan (same)
    "BAN": "BGD",  # Bangladesh
    "SRI": "LKA",  # Sri Lanka
    "NEP": "NPL",  # Nepal
    "HKG": "HKG",  # Hong Kong (same)
    "FIJ": "FJI",  # Fiji
    "SAM": "WSM",  # Samoa
    "PNG": "PNG",  # Papua New Guinea (same)
    "SOL": "SLB",  # Solomon Islands
    "VAN": "VUT",  # Vanuatu
    "GUM": "GUM",  # Guam (same)
    "ASA": "ASM",  # American Samoa
    "COK": "COK",  # Cook Islands (same)
    "AIN": "AIN",  # Individual Neutral Athletes (no mapping)
    "EOR": "EOR",  # Refugee Olympic Team (no mapping)
    "CPV": "CPV",  # Cape Verde (same)
    "GRN": "GRD",  # Grenada
    "LCA": "LCA",  # Saint Lucia (same)
    "DMA": "DMA",  # Dominica (same)
    "ANT": "ATG",  # Antigua and Barbuda
    "SKN": "KNA",  # Saint Kitts and Nevis
    "VIN": "VCT",  # Saint Vincent
    "GUY": "GUY",  # Guyana (same)
    "SUR": "SUR",  # Suriname (same)
    "BER": "BMU",  # Bermuda
    "CAY": "CYM",  # Cayman Islands
    "ARU": "ABW",  # Aruba
    "CUR": "CUW",  # Curacao
    "AHO": "ANT",  # Netherlands Antilles
    "MDA": "MDA",  # Moldova (same)
    "UKR": "UKR",  # Ukraine (same)
    "BLR": "BLR",  # Belarus (same)
    "POL": "POL",  # Poland (same)
    "CZE": "CZE",  # Czech Republic (same)
    "SVK": "SVK",  # Slovakia (same)
    "HUN": "HUN",  # Hungary (same)
    "AUT": "AUT",  # Austria (same)
    "BEL": "BEL",  # Belgium (same)
    "LUX": "LUX",  # Luxembourg (same)
    "IRL": "IRL",  # Ireland (same)
    "ISL": "ISL",  # Iceland (same)
    "NOR": "NOR",  # Norway (same)
    "SWE": "SWE",  # Sweden (same)
    "FIN": "FIN",  # Finland (same)
    "ISR": "ISR",  # Israel (same)
    "TUR": "TUR",  # Turkey (same)
    "CYP": "CYP",  # Cyprus (same)
    "MLT": "MLT",  # Malta (same)
    "AND": "AND",  # Andorra (same)
    "MON": "MCO",  # Monaco
    "SMR": "SMR",  # San Marino (same)
    "LIE": "LIE",  # Liechtenstein (same)
    "ALB": "ALB",  # Albania (same)
    "KOS": "XKX",  # Kosovo
    "JOR": "JOR",  # Jordan (same)
    "QAT": "QAT",  # Qatar (same)
}


def convert_noc_to_iso3(noc_code: str) -> str:
    """Convert Olympic NOC code to ISO-3 country code."""
    return NOC_TO_ISO3.get(noc_code, noc_code)


def render_global_medal_distribution(
    df_medals: pd.DataFrame,
    selected_medals: list,
    selected_continent: str
):
    """Render the Global Medal Distribution section with choropleth and bar chart."""
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

        # Convert NOC codes to ISO-3 for proper map display
        world_map_pivot["iso3_code"] = world_map_pivot["country_code"].apply(convert_noc_to_iso3)

        # Ensure all selected medal columns exist
        for medal in selected_medals:
            if medal not in world_map_pivot.columns:
                world_map_pivot[medal] = 0

        world_map_pivot["Total Medals"] = world_map_pivot[selected_medals].sum(axis=1)

        fig_map_global = px.choropleth(
            world_map_pivot,
            locations="iso3_code",
            locationmode="ISO-3",
            color="Total Medals",
            hover_name="country",
            hover_data={col: True for col in selected_medals if col in world_map_pivot.columns},
            projection="natural earth",
            color_continuous_scale=px.colors.sequential.Plasma,
            title=f"Global Medal Distribution (Filtered: {', '.join([m.split()[0] for m in selected_medals])})",
        )
        fig_map_global.update_layout(
            margin={"r": 0, "t": 40, "l": 0, "b": 0},
            geo=dict(
                showframe=False,
                showcoastlines=True,
            )
        )
        st.plotly_chart(fig_map_global, use_container_width=True)
    else:
        st.info("Please select at least one medal type in the sidebar.")

    # Continent comparison
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
        st.warning(f"⚠️ No medal data for **{selected_continent}** with current filters.")
