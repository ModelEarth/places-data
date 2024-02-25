import os
from os.path import isfile, join
import json
import csv

def main():
    alltheplaces_dir = 'output'
    files = [f for f in os.listdir(alltheplaces_dir) if isfile(join(alltheplaces_dir, f))]
    for file in files:
        full_file = join(alltheplaces_dir, file)
        if os.stat(full_file).st_size > 0:
            print(full_file)  # Helpful for identifying the problematic file
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
                if 'addr:country' not in prop:
                    try:
                        zipcode = str(prop.pop('addr:postcode')).replace(" ", "")
                    except KeyError as e:
                        print(f"KeyError for 'addr:postcode' in file {file}: {e}")
                        continue  # Skip if 'addr:postcode' is missing
                    
                    # Determine the directory and filename based on the zipcode
                    if zipcode[:3].isdigit() and len(zipcode) >= 5:
                        csv_dir = f"location/postalcode/US/{zipcode[:3]}/"
                        csv_filename = f"{zipcode}.csv"
                    else:
                        csv_dir = "location/postalcode/international/"
                        csv_filename = "international.csv"
                    
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
