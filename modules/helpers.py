"""
Helper functions for continent mapping and other utilities.
"""
import pandas as pd
from functools import lru_cache

# Complete mapping for ALL Olympic countries including special cases and name variations
COUNTRY_TO_CONTINENT = {
    # Special Olympic codes
    'AIN': 'Europe',  # Individual Neutral Athletes (mostly Russia)
    'EOR': 'Africa',  # Refugee Olympic Team (based in Africa for LA28)
    
    # Name variations and special territories
    'IR Iran': 'Asia',
    'Hong Kong, China': 'Asia',
    'Chinese Taipei': 'Asia',
    'Great Britain': 'Europe',
    'Korea': 'Asia',
    'DPR Korea': 'Asia',
    'Republic of Korea': 'Asia',
    'Republic of Moldova': 'Europe',
    'Türkiye': 'Europe',
    'Turkiye': 'Europe',
    'Turkey': 'Europe',
    'Lao PDR': 'Asia',
    'Virgin Islands, US': 'North America',
    'Virgin Islands, B': 'North America',
    'British Virgin Islands': 'North America',
    'US Virgin Islands': 'North America',
    'StVincent&Grenadines': 'North America',
    'St Vincent and the Grenadines': 'North America',
    'Saint Vincent and the Grenadines': 'North America',
    'St Kitts and Nevis': 'North America',
    'Saint Kitts and Nevis': 'North America',
    'Sao Tome & Principe': 'Africa',
    'Sao Tome and Principe': 'Africa',
    'São Tomé and Príncipe': 'Africa',
    'Bosnia & Herzegovina': 'Europe',
    'Bosnia and Herzegovina': 'Europe',
    'Centr Afric Re': 'Africa',
    'Central African Republic': 'Africa',
    "Côte d'Ivoire": 'Africa',
    "Cote d'Ivoire": 'Africa',
    'Ivory Coast': 'Africa',
    'UA Emirates': 'Asia',
    'United Arab Emirates': 'Asia',
    'UAE': 'Asia',
    
    # Standard country names - Africa
    'Algeria': 'Africa', 'Angola': 'Africa', 'Benin': 'Africa', 'Botswana': 'Africa',
    'Burkina Faso': 'Africa', 'Burundi': 'Africa', 'Cabo Verde': 'Africa', 'Cape Verde': 'Africa',
    'Cameroon': 'Africa', 'Chad': 'Africa', 'Comoros': 'Africa', 'Congo': 'Africa',
    'DR Congo': 'Africa', 'Democratic Republic of the Congo': 'Africa',
    'Djibouti': 'Africa', 'Egypt': 'Africa', 'Equatorial Guinea': 'Africa',
    'Eritrea': 'Africa', 'Eswatini': 'Africa', 'Swaziland': 'Africa', 'Ethiopia': 'Africa',
    'Gabon': 'Africa', 'Gambia': 'Africa', 'Ghana': 'Africa', 'Guinea': 'Africa',
    'Guinea-Bissau': 'Africa', 'Kenya': 'Africa', 'Lesotho': 'Africa', 'Liberia': 'Africa',
    'Libya': 'Africa', 'Madagascar': 'Africa', 'Malawi': 'Africa', 'Mali': 'Africa',
    'Mauritania': 'Africa', 'Mauritius': 'Africa', 'Morocco': 'Africa', 'Mozambique': 'Africa',
    'Namibia': 'Africa', 'Niger': 'Africa', 'Nigeria': 'Africa', 'Rwanda': 'Africa',
    'Senegal': 'Africa', 'Seychelles': 'Africa', 'Sierra Leone': 'Africa', 'Somalia': 'Africa',
    'South Africa': 'Africa', 'South Sudan': 'Africa', 'Sudan': 'Africa', 'Tanzania': 'Africa',
    'Togo': 'Africa', 'Tunisia': 'Africa', 'Uganda': 'Africa', 'Zambia': 'Africa', 'Zimbabwe': 'Africa',
    
    # Standard country names - Asia
    'Afghanistan': 'Asia', 'Armenia': 'Asia', 'Azerbaijan': 'Asia', 'Bahrain': 'Asia',
    'Bangladesh': 'Asia', 'Bhutan': 'Asia', 'Brunei': 'Asia', 'Brunei Darussalam': 'Asia',
    'Cambodia': 'Asia', 'China': 'Asia', 'Georgia': 'Asia', 'India': 'Asia', 'Indonesia': 'Asia',
    'Iran': 'Asia', 'Iraq': 'Asia', 'Israel': 'Asia', 'Japan': 'Asia', 'Jordan': 'Asia',
    'Kazakhstan': 'Asia', 'Kuwait': 'Asia', 'Kyrgyzstan': 'Asia', 'Laos': 'Asia',
    'Lebanon': 'Asia', 'Malaysia': 'Asia', 'Maldives': 'Asia', 'Mongolia': 'Asia',
    'Myanmar': 'Asia', 'Burma': 'Asia', 'Nepal': 'Asia', 'North Korea': 'Asia',
    'Oman': 'Asia', 'Pakistan': 'Asia', 'Palestine': 'Asia', 'Philippines': 'Asia',
    'Qatar': 'Asia', 'Saudi Arabia': 'Asia', 'Singapore': 'Asia', 'South Korea': 'Asia',
    'Sri Lanka': 'Asia', 'Syria': 'Asia', 'Syrian Arab Republic': 'Asia',
    'Taiwan': 'Asia', 'Tajikistan': 'Asia', 'Thailand': 'Asia', 'Timor-Leste': 'Asia',
    'East Timor': 'Asia', 'Turkmenistan': 'Asia', 'Uzbekistan': 'Asia', 'Vietnam': 'Asia',
    'Viet Nam': 'Asia', 'Yemen': 'Asia',
    
    # Standard country names - Europe
    'Albania': 'Europe', 'Andorra': 'Europe', 'Austria': 'Europe', 'Belarus': 'Europe',
    'Belgium': 'Europe', 'Bulgaria': 'Europe', 'Croatia': 'Europe', 'Cyprus': 'Europe',
    'Czechia': 'Europe', 'Czech Republic': 'Europe', 'Denmark': 'Europe', 'Estonia': 'Europe',
    'Finland': 'Europe', 'France': 'Europe', 'Germany': 'Europe', 'Greece': 'Europe',
    'Hungary': 'Europe', 'Iceland': 'Europe', 'Ireland': 'Europe', 'Italy': 'Europe',
    'Kosovo': 'Europe', 'Latvia': 'Europe', 'Liechtenstein': 'Europe', 'Lithuania': 'Europe',
    'Luxembourg': 'Europe', 'Malta': 'Europe', 'Moldova': 'Europe', 'Monaco': 'Europe',
    'Montenegro': 'Europe', 'Netherlands': 'Europe', 'North Macedonia': 'Europe',
    'Norway': 'Europe', 'Poland': 'Europe', 'Portugal': 'Europe', 'Romania': 'Europe',
    'Russia': 'Europe', 'Russian Federation': 'Europe', 'San Marino': 'Europe',
    'Serbia': 'Europe', 'Slovakia': 'Europe', 'Slovenia': 'Europe', 'Spain': 'Europe',
    'Sweden': 'Europe', 'Switzerland': 'Europe', 'Ukraine': 'Europe', 'United Kingdom': 'Europe',
    'UK': 'Europe', 'England': 'Europe', 'Scotland': 'Europe', 'Wales': 'Europe',
    
    # Standard country names - North America (includes Central America and Caribbean)
    'Antigua and Barbuda': 'North America', 'Aruba': 'North America', 'Bahamas': 'North America',
    'Barbados': 'North America', 'Belize': 'North America', 'Bermuda': 'North America',
    'Canada': 'North America', 'Cayman Islands': 'North America', 'Costa Rica': 'North America',
    'Cuba': 'North America', 'Dominica': 'North America', 'Dominican Republic': 'North America',
    'El Salvador': 'North America', 'Grenada': 'North America', 'Guatemala': 'North America',
    'Haiti': 'North America', 'Honduras': 'North America', 'Jamaica': 'North America',
    'Mexico': 'North America', 'Nicaragua': 'North America', 'Panama': 'North America',
    'Puerto Rico': 'North America', 'Saint Lucia': 'North America', 'St Lucia': 'North America',
    'Trinidad and Tobago': 'North America', 'United States': 'North America',
    'United States of America': 'North America', 'USA': 'North America',
    
    # Standard country names - South America
    'Argentina': 'South America', 'Bolivia': 'South America', 'Brazil': 'South America',
    'Chile': 'South America', 'Colombia': 'South America', 'Ecuador': 'South America',
    'Guyana': 'South America', 'Paraguay': 'South America', 'Peru': 'South America',
    'Suriname': 'South America', 'Uruguay': 'South America', 'Venezuela': 'South America',
    
    # Standard country names - Oceania
    'American Samoa': 'Oceania', 'Australia': 'Oceania', 'Cook Islands': 'Oceania',
    'Fiji': 'Oceania', 'Guam': 'Oceania', 'Kiribati': 'Oceania', 'Marshall Islands': 'Oceania',
    'Micronesia': 'Oceania', 'Federated States of Micronesia': 'Oceania',
    'Nauru': 'Oceania', 'New Zealand': 'Oceania', 'Palau': 'Oceania',
    'Papua New Guinea': 'Oceania', 'Samoa': 'Oceania', 'Solomon Islands': 'Oceania',
    'Tonga': 'Oceania', 'Tuvalu': 'Oceania', 'Vanuatu': 'Oceania',
}


@lru_cache(maxsize=None)
def get_continent(country: str) -> str:
    """
    Convert a country name to its continent.
    Uses a comprehensive hardcoded mapping for Olympic countries.
    Falls back to pycountry for any edge cases.
    """
    if pd.isna(country) or country is None:
        return "Unknown"
    
    country_str = str(country).strip()
    
    # First check our comprehensive mapping
    if country_str in COUNTRY_TO_CONTINENT:
        return COUNTRY_TO_CONTINENT[country_str]
    
    # Try pycountry as fallback
    try:
        import pycountry
        from pycountry_convert import (
            country_alpha2_to_continent_code,
            convert_continent_code_to_continent_name
        )
        country_obj = pycountry.countries.lookup(country_str)
        country_alpha2 = country_obj.alpha_2
        continent_code = country_alpha2_to_continent_code(country_alpha2)
        continent_name = convert_continent_code_to_continent_name(continent_code)
        return continent_name
    except Exception:
        # If still not found, return Unknown (not "Other/Special")
        # But we should never reach here with the comprehensive mapping
        return "Unknown"


def country_summary(df: pd.DataFrame, country: str) -> dict:
    """
    Generate a summary of medal statistics for a given country.
    """
    sub = df[df["country"] == country]
    return {
        "Total medals": len(sub),
        "Gold": (sub["medal_type"] == "Gold Medal").sum(),
        "Silver": (sub["medal_type"] == "Silver Medal").sum(),
        "Bronze": (sub["medal_type"] == "Bronze Medal").sum(),
        "Sports": sub["discipline"].nunique(),
        "Events": sub["event"].nunique(),
    }
