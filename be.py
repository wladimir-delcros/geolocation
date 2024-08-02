def extract_admin_levels(address):
    admin_hierarchy = ['country', 'region', 'state', 'province', 'county', 'state_district', 'city', 'town', 'village', 'municipality', 'city_district', 'district', 'borough', 'suburb', 'subdivision', 'neighbourhood']
    admin_levels = {}

    levels_found = 0
    for level in admin_hierarchy:
        if level in address and address[level]:
            levels_found += 1
            admin_levels[f'Level {levels_found}'] = address[level]
            if levels_found == 4:
                break

    # Specific handling for Belgium
    if admin_levels.get('Level 1') == 'Belgium':
        if 'region' in address:
            admin_levels['Level 2'] = address['region']
        if 'state' in address:
            admin_levels['Level 3'] = address['state']
        if 'city' in address:
            admin_levels['Level 4'] = address['city']
        elif 'county' in address:
            admin_levels['Level 4'] = address['county']
        elif 'town' in address:
            admin_levels['Level 4'] = address['town']
        elif 'village' in address:
            admin_levels['Level 4'] = address['village']
        elif 'municipality' in address:
            admin_levels['Level 4'] = address['municipality']
    
    for i in range(levels_found + 1, 5):
        admin_levels[f'Level {i}'] = 'Not found'

    return admin_levels
