# LA28 Dashboard

This is a Streamlit application for the LA28 Volunteer Selection Dashboard, providing an overview and analysis of Olympic data.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1.  Navigate to the project directory:
    ```bash
    cd LA28_Dashboard
    ```

2.  (Optional but recommended) Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To start the Streamlit application, run the following command:

```bash
streamlit run 1_🏠_Overview.py
```

## Project Structure

The application follows a modular architecture with clear separation of concerns:

### Core Files
- `1_🏠_Overview.py`: The main entry point of the application, displaying key Olympic metrics and visualizations.
- `utils.py`: Core utility functions for data loading, filtering, and sidebar controls.
- `requirements.txt`: List of Python dependencies.

### Pages (`pages/`)
Multi-page Streamlit application structure:
- `2_🗺️_Global_Analysis.py`: Global medal distribution and country-level analysis.
- `3_👤_Athlete_Performance.py`: Athlete profiles, demographics, and performance metrics.
- `4_🏟️_Sports_and_Events.py`: Sports-specific analysis and event schedules.

### Components (`components/`)
Reusable UI components for visualizations and data presentation:
- `overview_metrics.py`: KPI metrics display (athletes, countries, sports, medals, events).
- `overview_medal_distribution.py`: Global medal distribution pie chart.
- `overview_top_standings.py`: Top 10 countries medal standings bar chart.
- `global_medal_distribution.py`: Detailed global medal analysis.
- `athlete_profile.py`: Individual athlete profile display.
- `age_distribution.py`: Athlete age distribution visualization.
- `gender_distribution.py`: Gender distribution analysis.
- `top_athletes.py`: Top performing athletes table.
- `athlete_summary.py`: Athlete statistics summary.
- `continent_medals_bar.py`: Continent-level medal comparison.
- `event_schedule.py`: Event scheduling visualization.
- `medal_hierarchy.py`: Medal hierarchy visualization.
- `medal_count_sport.py`: Sport-specific medal counts.
- `top_countries_medals.py`: Top countries medal comparison.
- `venues_map.py`: Venue location mapping.
- `watch_highlights.py`: Event highlights display.
- `who_won_the_day.py`: Daily medal winners.
- `head_to_head.py`: Country comparison analysis.
- `summary_statistics.py`: Statistical summaries.

### Modules (`modules/`)
Backend logic and data processing:
- `data_loader.py`: Centralized data loading with caching for athletes, medals, events, NOCs, coaches, teams, and medallists.
- `helpers.py`: Helper functions and utilities.
- `venue_geocoder.py`: Geocoding utilities for venue locations.

### Data (`data/`)
CSV data files containing Olympic information:
- `athletes.csv`: Athlete information and profiles.
- `coaches.csv`: Coach information.
- `events.csv`: Event details and schedules.
- `medals_total.csv`: Total medal counts by country.
- `medals.csv`: Detailed medal information.
- `medallists.csv`: Medal winners data.
- `nocs.csv`: National Olympic Committees information.
- `teams.csv`: Team composition data.
- `venues.csv`: Venue locations and details.
- `torch_route.csv`: Olympic torch route information.
- `schedules.csv` / `schedules_preliminary.csv`: Event schedules.
- `technical_officials.csv`: Officials information.
- `results/`: Directory containing sport-specific results (e.g., `Athletics.csv`, `Swimming.csv`, etc.).

## Architecture

The application uses a component-based architecture:
- **Data Layer**: Centralized data loading and caching in `modules/data_loader.py`.
- **Logic Layer**: Filtering and processing utilities in `utils.py`.
- **Component Layer**: Reusable visualization components in `components/`.
- **Page Layer**: High-level page orchestration in main file and `pages/` directory.

This structure promotes code reusability, maintainability, and separation of concerns.
