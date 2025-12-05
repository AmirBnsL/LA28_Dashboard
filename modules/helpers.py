"""
Helper functions for continent mapping and other utilities.
"""
import pandas as pd
from functools import lru_cache
import pycountry
from pycountry_convert import (
    country_alpha2_to_continent_code,
    convert_continent_code_to_continent_name
)


@lru_cache(maxsize=None)
def get_continent(country: str) -> str:
    """
    Convert a country name to its continent.
    Uses caching for performance.
    """
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
