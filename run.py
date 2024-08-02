import sys
import random
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from tqdm import tqdm
from importlib import import_module

def generate_random_coordinates_in_france(num_points):
    min_lat, max_lat = 41.0, 51.0
    min_lon, max_lon = -5.0, 9.0
    coordinates = [(random.uniform(min_lat, max_lat), random.uniform(min_lon, max_lon)) for _ in range(num_points)]
    return coordinates

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
    print(f"Using module: {branch} for country code: {country_code}")
    return country_module, branch

def default_extract_admin_levels(address):
    admin_hierarchy = ['country', 'state', 'province', 'county', 'state_district', 'city', 'town', 'village', 'municipality', 'city_district', 'district', 'borough', 'suburb', 'subdivision', 'neighbourhood']
    admin_levels = {}
    
    levels_found = 0
    for level in admin_hierarchy:
        if level in address and address[level]:
            levels_found += 1
            admin_levels[f'Level {levels_found}'] = address[level]
            if levels_found == 4:
                break

    for i in range(levels_found + 1, 5):
        admin_levels[f'Level {i}'] = 'Not found'

    return admin_levels

if __name__ == "__main__":
    args = sys.argv[1:]
    
    coordinates_flag_index = args.index('--coordinates') if '--coordinates' in args else None
    zoom_flag_index = args.index('--zoom') if '--zoom' in args else None
    
    coordinates_list = []
    zoom_level = 18

    if coordinates_flag_index is not None:
        coordinates_list = args[coordinates_flag_index + 1 : zoom_flag_index if zoom_flag_index else None]
        coordinates_list = [(float(coord.split(',')[0]), float(coord.split(',')[1])) for coord in coordinates_list]
    
    if zoom_flag_index is not None:
        zoom_level = int(args[zoom_flag_index + 1])
    
    if not coordinates_list:
        coordinates_list = generate_random_coordinates_in_france(10)
    
    print(f"Coordinates list: {coordinates_list}")
    print(f"Zoom level: {zoom_level}")
    
    results = []
    level_counts = {'Level 1': 0, 'Level 2': 0, 'Level 3': 0, 'Level 4': 0}
    total_count = 0

    for lat, lon in tqdm(coordinates_list, desc="Processing coordinates"):
        start_time = time.time()
        raw_result = reverse_geocode(lat, lon, zoom=zoom_level)
        end_time = time.time()
        elapsed_time = end_time - start_time

        if raw_result:
            address = raw_result.get('address', {})
            country_code = address.get('country_code', '').upper()
            country_module, branch = get_country_module(country_code)
            admin_levels = country_module.extract_admin_levels(address)
            for level in admin_levels:
                if admin_levels[level] != 'Not found':
                    level_counts[level] += 1
            total_count += 1
            results.append({
                'Coordinates': (lat, lon),
                'Address': address,
                'Admin Levels': admin_levels,
                'Branch': branch,
                'Response Time': f"{elapsed_time:.2f} seconds"
            })
        else:
            total_count += 1
            results.append({
                'Coordinates': (lat, lon),
                'Address': 'Not found',
                'Admin Levels': {
                    'Level 1': 'Not found',
                    'Level 2': 'Not found',
                    'Level 3': 'Not found',
                    'Level 4': 'Not found'
                },
                'Branch': 'default',
                'Response Time': f"{elapsed_time:.2f} seconds"
            })

    for result in results:
        print(f"Coordinates: {result['Coordinates']}")
        print("Address:")
        if result['Address'] == 'Not found':
            print("  Address not found")
        else:
            for key, value in result['Address'].items():
                print(f"  {key.replace('_', ' ').title()}: {value}")
        print("Admin Levels:")
        for level, value in result['Admin Levels'].items():
            print(f"  {level}: {value}")
        print(f"Branch: {result['Branch']}")
        print(f"Response Time: {result['Response Time']}")
        print("  ---------")
    
    print("\nCompletion Rates:")
    for level, count in level_counts.items():
        completion_rate = (count / total_count) * 100 if total_count else 0
        print(f"{level}: {completion_rate:.2f}%")
