def extract_admin_levels(address):
    admin_levels = {}

    admin_levels['Level 1'] = address.get('country', 'Not found')

    if 'yes' in address:
        admin_levels['Level 2'] = address['yes']

        if 'county' in address:
            admin_levels['Level 3'] = address['county']

            if 'city' in address:
                admin_levels['Level 4'] = address['city']
            elif 'town' in address:
                admin_levels['Level 4'] = address['town']
            elif 'village' in address:
                admin_levels['Level 4'] = address['village']
            elif 'hamlet' in address:
                admin_levels['Level 4'] = address['hamlet']
            elif 'neighbourhood' in address:
                admin_levels['Level 4'] = address['neighbourhood']
            elif 'suburb' in address:
                admin_levels['Level 4'] = address['suburb']
            elif 'city_district' in address:
                admin_levels['Level 4'] = address['city_district']
            else:
                admin_levels['Level 4'] = 'Not found'
        else:
            admin_levels['Level 3'] = 'Not found'
            admin_levels['Level 4'] = 'Not found'
    else:
        if 'state' in address:
            admin_levels['Level 2'] = address['state']

            if 'county' in address:
                admin_levels['Level 3'] = address['county']

                if 'city' in address:
                    admin_levels['Level 4'] = address['city']
                elif 'town' in address:
                    admin_levels['Level 4'] = address['town']
                elif 'village' in address:
                    admin_levels['Level 4'] = address['village']
                elif 'hamlet' in address:
                    admin_levels['Level 4'] = address['hamlet']
                elif 'neighbourhood' in address:
                    admin_levels['Level 4'] = address['neighbourhood']
                elif 'suburb' in address:
                    admin_levels['Level 4'] = address['suburb']
                elif 'city_district' in address:
                    admin_levels['Level 4'] = address['city_district']
                else:
                    admin_levels['Level 4'] = 'Not found'
            else:
                admin_levels['Level 3'] = 'Not found'
                admin_levels['Level 4'] = 'Not found'
        elif 'county' in address:
            admin_levels['Level 2'] = address['county']
            admin_levels['Level 3'] = 'Not found'
            admin_levels['Level 4'] = 'Not found'
        else:
            admin_levels['Level 2'] = 'Not found'
            admin_levels['Level 3'] = 'Not found'
            admin_levels['Level 4'] = 'Not found'

    return admin_levels
