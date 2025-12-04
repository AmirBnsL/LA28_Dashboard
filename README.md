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

- `1_🏠_Overview.py`: The main entry point of the application.
- `pages/`: Contains additional pages for the multi-page Streamlit app.
- `data/`: Contains the CSV data files used by the application.
- `utils.py`: Utility functions for data loading and processing.
- `requirements.txt`: List of Python dependencies.
