# -*- coding: utf-8 -*-
"""
Generates nested zip folders for each zip code for AllThePlaces data

@author: Kathryn Winglee
"""
import os
from os.path import isfile, join
import json
#os.chdir("C:/Users/kwing/Documents/GitHub/alltheplaces_curl")

def main():
    ##combine alltheplaces output
    alltheplaces_dir = 'output'
    files = [f for f in os.listdir(alltheplaces_dir) if isfile(join(alltheplaces_dir, f))]
    allthezipcodes = dict()
    countries = set()
    for file in files[0:10]:
        full_file = join(alltheplaces_dir, file)
        if(os.stat(full_file).st_size > 0):
            with open(full_file) as f:
                data = json.load(f)
            if(data['type'] != 'FeatureCollection'):
                print(file + " " + data['type'])
            feat = data['features']
            for feature in feat:
                prop = feature['properties']
                if 'addr:country' not in prop: # | prop['addr:country'] in ['US', "USA", "United States"]:
                    zipcode = prop.pop('addr:postcode') #removes postcode from the data at same time
                    if zipcode in allthezipcodes:
                        old_dict = allthezipcodes[zipcode]
                        old_dict[file.replace('.geojson', '')] = prop
                        allthezipcodes[zipcode] = old_dict
                    else:
                        new_dict = {file.replace('.geojson', '') : prop}
                        allthezipcodes[zipcode] = new_dict
                else:
                    countries.add(prop['addr:country'])
        else:
            print(full_file + " is empty")
    
    ##write out the zip files
    for z in allthezipcodes.keys():
        #make the filepath if needed
        zipcode_split = [char for char in z]
        filepath = "locations/postalcode/US/"
        for digit in zipcode_split:
            filepath += digit +"/"
            if not os.path.exists(filepath):
                os.mkdir(filepath)
                
         #write json file
        zip_dict = allthezipcodes[z]
        with open(filepath + 'zipinfo.json', 'w') as outfile:
            json.dump(zip_dict, outfile, indent=4)
            

if __name__== "__main__":
   main()