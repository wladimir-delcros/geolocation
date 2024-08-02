# Geolocation Project

This project allows users to reverse geocode coordinates and extract administrative levels using a Flask web application. The data for countries, states, and cities is sourced from the countries-states-cities-database.

## Features

- Dynamic selection of continent, country, and city.
- Reverse geocoding to obtain detailed address information.
- Extraction of administrative levels (country, state, county, city).
- Display of results in a user-friendly table format.

## Installation

### Clone the Repository

```bash
git clone https://github.com/wladimir-delcros/geolocation.git
cd geolocation
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
python app.py
