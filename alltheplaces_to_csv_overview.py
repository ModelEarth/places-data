import os
from os.path import isfile, join
import json
import csv
import re

# Data structures for overview data
overview_data = {}
country_overview_data = {}
state_overview_data = {}

def update_overview_data(country, state, place_name, city, prop):
    # Update global overview
    key = (country.upper(), state.upper(), place_name.replace(' ', '').lower())
    overview_data[key] = overview_data.get(key, 0) + 1
    
    # Update country overview
    country_key = (state.upper(), place_name.replace(' ', '').lower(), city)
    if country.upper() not in country_overview_data:
        country_overview_data[country.upper()] = {}
    country_overview_data[country.upper()][country_key] = country_overview_data[country.upper()].get(country_key, 0) + 1
    
    # Update state overview
    state_key = (city, place_name.replace(' ', '').lower(), prop.get("addr:full", "").replace(',', ''))
    if country.upper() not in state_overview_data:
        state_overview_data[country.upper()] = {}
    if state.upper() not in state_overview_data[country.upper()]:
        state_overview_data[country.upper()][state.upper()] = {}
    state_overview_data[country.upper()][state.upper()][state_key] = prop

def write_country_state_overviews():
    for country, states in state_overview_data.items():
        country_path = f'location/2023/{country}'
        # Write country overview
        with open(join(country_path, f'{country}_overview.csv'), 'w', newline='', encoding='utf-8') as country_file:
            country_writer = csv.writer(country_file)
            country_writer.writerow(['State', 'Place Name', 'City', 'Establishments'])
            for (state, place_name, city), count in country_overview_data[country].items():
                country_writer.writerow([state, place_name, city, count])
        
        for state, cities in states.items():
            state_path = join(country_path, state)
            # Write state overview
            with open(join(state_path, f'{state}_overview.csv'), 'w', newline='', encoding='utf-8') as state_file:
                state_writer = csv.writer(state_file)
                state_writer.writerow(['City', 'Place Name', 'Address', 'Name'])
                for (city, place_name, address), prop in cities.items():
                    state_writer.writerow([city, place_name, address, prop["name"]])

def write_overview_csv():
    for year in ['2023']:
        overview_csv_path = f'location/{year}/overview.csv'
        os.makedirs(os.path.dirname(overview_csv_path), exist_ok=True)
        with open(overview_csv_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Country', 'State', 'Place', 'Establishments'])
            for (country, state, place), count in overview_data.items():
                writer.writerow([country, state, place, count])

def main():
    alltheplaces_dir = 'output_2023'
    files = [f for f in os.listdir(alltheplaces_dir) if isfile(join(alltheplaces_dir, f))]
    for file in files:
        full_file = join(alltheplaces_dir, file)
        if os.stat(full_file).st_size > 0:
            try:
                with open(full_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in {full_file}: {e}")
                continue
                
            if data['type'] != 'FeatureCollection':
                print(f"{file} is not a FeatureCollection: {data['type']}")
                continue

            for feature in data['features']:
                prop = feature['properties']
                country = prop.get('addr:country', 'unknown')
                state = prop.get('addr:state', 'unknown').
                state = ''.join(state)
                state = state.replace(' ', '').replace('?', 'unknown').replace('|', '').replace('<', '').replace('>', '')
                place_name = prop.get('@spider', 'unknown')
                city = prop.get('addr:city', 'unknown')

                update_overview_data(country, state, place_name, city, prop)

                # The existing logic to write detailed CSV files for each place remains unchanged...

                if country != 'unknown':
                    country_folder = os.path.join('location/2023', country.upper())
                else:
                    country_folder = 'location/2023/unknown'

                zipcode = str(prop.pop('addr:postcode', "unknown"))                    
                
                # Replace special characters in zipcode
                zipcode = re.sub(r'\s+', '', zipcode)  # Remove whitespace characters
                zipcode = re.sub(r'<br>', '', zipcode)  # Remove '<br>'
                zipcode = re.sub(r'\r\n', '', zipcode)  # Remove '\r\n'
                zipcode = re.sub(r'[^\w\s]', '', zipcode)  # Remove non-alphanumeric characters
                
                # Remove any empty or invalid zipcodes
                if zipcode == "NULL":
                    zipcode = "unknown"
                
                # Determine the directory and filename based on the zipcode
                # if country == 'US':
                #     csv_dir = os.path.join(country_folder, state)
                # else:
                csv_dir = os.path.join(country_folder, state)

                csv_filename = f"{zipcode}.csv"
                csv_path = join(csv_dir, csv_filename)
                print(csv_dir)

                os.makedirs(csv_dir, exist_ok=True)
                    
                csv_data = {
                    "Ref": prop.get("ref", ""),
                    "Spider": prop.get("@spider", ""),
                    "Name": prop.get("name", ""),
                    "Address": prop.get("addr:full", ""),
                    "City": prop.get("addr:city", ""),
                    "State": prop.get("addr:state", ""),
                    "Country": country,  # Add country column
                    "Phone": prop.get("phone", ""),
                    "Website": prop.get("website", ""),
                    "Hours": prop.get("opening_hours", ""),
                    "Brand": prop.get("brand", ""),
                    "WikiData": prop.get("brand:wikidata", "")
                }
                    
                with open(csv_path, mode='a', newline='', encoding='utf-8') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=csv_data.keys())
                    if not os.path.isfile(csv_path) or os.stat(csv_path).st_size == 0:
                        writer.writeheader()
                    writer.writerow(csv_data)

    
    # After processing all files:
    write_overview_csv()  # Global overview
    write_country_state_overviews()
 # Generate overview CSV after processing all files

if __name__ == "__main__":
    main()


