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

    # Adjust levels if archipelago is found
    if 'archipelago' in address and address['archipelago']:
        archipelago_level = {k: v for k, v in admin_levels.items() if v == address['archipelago']}
        if archipelago_level:
            archipelago_key = list(archipelago_level.keys())[0]
            del admin_levels[archipelago_key]
            admin_levels = {f'Level {int(k.split()[1]) + 1}': v for k, v in admin_levels.items()}
            admin_levels['Level 2'] = address['archipelago']

    # Specific case for France
    if address.get('country_code', '').upper() == 'FR':
        if address.get('city') in ['Paris', 'Marseille', 'Lyon'] and 'suburb' in address:
            admin_levels['Level 4'] = f"{address['city']} - {address['suburb']}"
        elif 'city' in address and 'Level 4' in admin_levels and admin_levels['Level 4'] == address.get('state_district'):
            admin_levels['Level 4'] = address['city']

    for i in range(levels_found + 1, 5):
        admin_levels[f'Level {i}'] = 'Not found'

    return admin_levels
