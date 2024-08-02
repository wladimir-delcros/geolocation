def extract_admin_levels(address):
    admin_hierarchy = ['country', 'archipelago', 'state', 'province', 'county', 'state_district', 'city', 'town', 'village', 'municipality', 'city_district', 'district', 'borough', 'suburb', 'subdivision', 'neighbourhood']
    admin_levels = {}

    levels_found = 0
    for level in admin_hierarchy:
        if level in address and address[level]:
            levels_found += 1
            admin_levels[f'Level {levels_found}'] = address[level]
            if levels_found == 4:
                break

    # Ensure city is prioritized over state_district for Level 4
    if 'city' in address and 'Level 4' in admin_levels and admin_levels['Level 4'] == address.get('state_district'):
        admin_levels['Level 4'] = address['city']

    for i in range(levels_found + 1, 5):
        admin_levels[f'Level {i}'] = 'Not found'

    return admin_levels
