from flask import Flask, request, jsonify, render_template
import random
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import json
from importlib import import_module

app = Flask(__name__)

with open('countries_states_cities.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract unique continents
continents = list(set(country['region'] for country in data if country['region']))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_continents', methods=['GET'])
def get_continents():
    return jsonify(continents)

@app.route('/get_countries', methods=['GET'])
def get_countries():
    continent = request.args.get('continent')
    countries = [country['name'] for country in data if country['region'] == continent]
    return jsonify(countries)

@app.route('/get_cities', methods=['GET'])
def get_cities():
    country_name = request.args.get('country')
    country = next((country for country in data if country['name'] == country_name), None)
    cities = [city['name'] for state in country['states'] for city in state['cities']] if country else []
    return jsonify(cities)

@app.route('/generate', methods=['POST'])
def generate():
    request_data = request.json
    city_name = request_data['city']
    country_name = request_data['country']
    country = next((country for country in data if country['name'] == country_name), None)
    city = next((city for state in country['states'] for city in state['cities'] if city['name'] == city_name), None)

    if city:
        coordinates = (city['latitude'], city['longitude'])
        coordinates_list = [coordinates]
    
        results = []
        for lat, lon in coordinates_list:
            raw_result = reverse_geocode(lat, lon)
            if raw_result:
                address = raw_result.get('address', {})
                country_code = address.get('country_code', '').upper()
                country_module, branch = get_country_module(country_code)
                admin_levels = country_module.extract_admin_levels(address)
                results.append({
                    'Coordinates': (lat, lon),
                    'Address': address,
                    'Admin Levels': admin_levels,
                    'Branch': branch
                })
    
        return jsonify(results)
    else:
        return jsonify([])

def reverse_geocode(lat, lon, zoom=18):
    geolocator = Nominatim(user_agent="simple_reverse_geocoder")
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True, language='en', addressdetails=1, zoom=zoom, timeout=10)
        if location:
            return location.raw
        return None
    except (GeocoderTimedOut, GeocoderServiceError):
        return None

def get_country_module(country_code):
    try:
        country_module = import_module(country_code.lower())
        branch = country_code.lower()
    except ImportError:
        country_module = import_module('default')
        branch = 'default'
    return country_module, branch

if __name__ == '__main__':
    app.run(debug=True)
