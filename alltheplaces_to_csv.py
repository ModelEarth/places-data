"""
Generates CSV files from JSON files.

@author: Chen (Carolyn)
"""

import os
from os.path import isfile, join
import json
import csv
import re

def main():
    alltheplaces_dir = 'output'
    files = [f for f in os.listdir(alltheplaces_dir) if isfile(join(alltheplaces_dir, f))]
    for file in files:
        full_file = join(alltheplaces_dir, file)
        if os.stat(full_file).st_size > 0:
            try:
                with open(full_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in {full_file}: {e}")
                continue  # Skip this file and move to the next
                
            if data['type'] != 'FeatureCollection':
                print(f"{file} is not a FeatureCollection: {data['type']}")
                continue

            for feature in data['features']:
                prop = feature['properties']
                country = prop.get('addr:country', 'unknown')

                if country != 'unknown':
                    country_folder = os.path.join('location', 'postalcode', country.upper())
                else:
                    country_folder = 'location/postalcode/unknown'

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
                if country == 'US':
                    csv_dir = os.path.join(country_folder, zipcode[:3])
                else:
                    csv_dir = country_folder

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

if __name__ == "__main__":
    main()
