# Global Weather Data Dashboard

A polished, animated Streamlit dashboard that visualizes weather data for cities around the world.

## Features

- KPI: Current temperature for the selected city
- Chart 1: 7-day precipitation probability bar chart
- Chart 2: Hourly wind speed line chart with a smooth rolling average
- Interactive city selector
- Responsive layout, glassmorphism, and animated background

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
streamlit run streamlit_app.py
```

## Notes

- Data source: Open-Meteo (no API key required)
- Caching with TTL=10 minutes to keep the app responsive
