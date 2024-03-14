# Places Data

Uses a Github Action to fetch and uncompress the All the Place tar.gz file to the output folder.

Data from alltheplaces.xyz

	python3 -m venv env &&
	source env/bin/activate

	python alltheplaces_to_csv.py

Output resides in "location" within this [places-data](https://github.com/ModelEarth/places-data) repo.

We are currently excluding "location" within .gitignore until we've cleaned up 2-char country matches.

The US folder was manually copied from location/postacodes/US to: /places/2024/US
It's 78 MB.


class CountryAbbreviationConverter:
    def __init__(self):
        # Dictionary mapping country names to their two-character abbreviations
        self.country_abbreviations = {
            "united states": "US",
            "usa": "US",
            "u s a": "US",
            "united kingdom": "UK",
            "uk": "UK",
            "great britain": "UK",
            "england": "UK",
            "scotland": "UK",
            "wales": "UK",
            "ireland": "IE",
            "republic of ireland": "IE",
            "ire": "IE",
            "france": "FR",
            "germany": "DE",
            "italy": "IT",
            "spain": "ES",
            "portugal": "PT",
            "netherlands": "NL",
            "belgium": "BE",
            "switzerland": "CH",
            "sweden": "SE",
            "norway": "NO",
            "denmark": "DK",
            "finland": "FI",
            "iceland": "IS",
            "austria": "AT",
            "greece": "GR",
            "poland": "PL",
            "russia": "RU",
            "turkey": "TR",
            "canada": "CA",
            "mexico": "MX",
            "brazil": "BR",
            "argentina": "AR",
            "australia": "AU",
            "new zealand": "NZ",
            "japan": "JP",
            "china": "CN",
            "india": "IN",
            "south korea": "KR",
            "north korea": "KP",
            "south africa": "ZA",
            "egypt": "EG",
            "morocco": "MA",
            "kenya": "KE",
            "nigeria": "NG",
            "ethiopia": "ET",
            "ghana": "GH",
            "cameroon": "CM",
            "tanzania": "TZ",
            "uganda": "UG",
            "zambia": "ZM",
            "zimbabwe": "ZW",
            "mozambique": "MZ",
            "angola": "AO",
            "botswana": "BW",
            "namibia": "NA",
            "senegal": "SN",
            "mali": "ML",
            "liberia": "LR",
            "ivory coast": "CI",
            "congo": "CG",
            "democratic republic of the congo": "CD",
            "uganda": "UG",
            "rwanda": "RW",
            "madagascar": "MG",
            "sudan": "SD",
            "south sudan": "SS",
            "eritrea": "ER",
            "somalia": "SO",
            "afghanistan": "AF",
            "pakistan": "PK",
            "bangladesh": "BD",
            "sri lanka": "LK",
            "nepal": "NP",
            "bhutan": "BT",
            "iran": "IR",
            "iraq": "IQ",
            "syria": "SY",
            "lebanon": "LB",
            "israel": "IL",
            "jordan": "JO",
            "saudi arabia": "SA",
            "united arab emirates": "AE",
            "uae": "AE",
            "qatar": "QA",
            "kuwait": "KW",
            "bahrain": "BH",
            "oman": "OM",
            "yemen": "YE",
            "turkmenistan": "TM",
            "uzbekistan": "UZ",
            "kazakhstan": "KZ",
            "kyrgyzstan": "KG",
            "tajikistan": "TJ",
            "mongolia": "MN",
            "vietnam": "VN",
            "laos": "LA",
            "thailand": "TH",
            "myanmar": "MM",
            "burma": "MM",
            "malaysia": "MY",
            "indonesia": "ID",
            "philippines": "PH",
            "singapore": "SG",
            "brunei": "BN",
            "papua new guinea": "PG",
            "fiji": "FJ",
            "solomon islands": "SB",
            "vanuatu": "VU",
            "samoa": "WS",
            "tonga": "TO",
            "tuvalu": "TV",
            "kiribati": "KI",
            "nauru": "NR",
            "marshall islands": "MH",
            "palau": "PW",
            "micronesia": "FM",
            "cook islands": "CK",
            "niue": "NU",
            "tokelau": "TK",
            "tonga": "TO",
            "federated states of micronesia": "FM",
            "republic of the marshall islands": "MH",
            "sao tome and principe": "ST",
            "saint kitts and nevis": "KN",
            "saint lucia": "LC",
            "saint vincent and the grenadines": "VC",
            "antigua and barbuda": "AG",
            "barbados": "BB",
            "grenada": "GD",
            "dominica": "DM",
            "dominican republic": "DO",
            "haiti": "HT",
            "bahamas": "BS",
            "jamaica": "JM",
            "trinidad and tobago": "TT",
            "suriname": "SR",
            "guyana": "GY",
            "belize": "BZ",
            "honduras": "HN",
            "guatemala": "GT",
            "el salvador": "SV",
            "nicaragua": "NI",
            "costa rica": "CR",
            "panama": "PA",
            "colombia": "CO",
            "venezuela": "VE",
            "ecuador": "EC",
            "peru": "PE",
            "bolivia": "BO",
            "paraguay": "PY",
            "uruguay": "UY",
            "chile": "CL",
            "gambia": "GM",
            "sierra leone": "SL",
            "cape verde": "CV",
            "comoros": "KM",
            "mauritius": "MU",
            "seychelles": "SC",
            "maldives": "MV",
            "kiribati": "KI",
            "timor-leste": "TL",
            "djibouti": "DJ",
            "luxembourg": "LU",
            "singapore": "SG",
            "monaco": "MC",
            "andorra": "AD",
            "liechtenstein": "LI",
            "san marino": "SM",
            "vatican city": "VA",
            "tuvalu": "TV",
            "nauru": "NR",
            "palau": "PW",
            "marshall islands": "MH",
            "saint kitts and nevis": "KN",
            "saint vincent and the grenadines": "VC",
            "sao tome and principe": "ST",
            "trinidad and tobago": "TT",
            "solomon islands": "SB",
            "federated states of micronesia": "FM",
            "antigua and barbuda": "AG",
            "grenada": "GD",
            "saint lucia": "LC",
            "samoa": "WS",
            "vanuatu": "VU",
            "barbados": "BB",
            "belize": "BZ",
            "dominica": "DM",
            "marshall islands": "MH",
            "tuvalu": "TV",
            "nauru": "NR",
            "palau": "PW",
            "vanuatu": "VU",
            "andorra": "AD",
        }
        self.countries_not_found = []

    def convert_to_abbreviation(self, country_name):
        # Convert incoming country name to lowercase for case-insensitive matching
        country_name_lower = country_name.lower()

        # Check if the country name or its abbreviation is in the mapping
        if country_name_lower in self.country_abbreviations:
            return self.country_abbreviations[country_name_lower].upper()
    	else:
            self.countries_not_found.append(country_name)
            return 'Unknown'

        # Check for 3-character abbreviations
        for name, abbrev in self.country_abbreviations.items():
            if len(name) > 2 and country_name_lower in name:
                return abbrev.upper()

        # If no match found, return None
        return None

    def print_countries_not_found(self):
        print("Countries not found:")
        for country in self.countries_not_found:
            print(country)

if __name__ == "__main__":

    converter.print_countries_not_found()

# Example usage
converter = CountryAbbreviationConverter()
country_name = input("Enter country name: ")
abbreviation = converter.convert_to_abbreviation(country_name)
if abbreviation:
    print("Country abbreviation:", abbreviation)
else:
    print("Country abbreviation not found.")
This implementation includes a class CountryAbbreviationConverter with a method convert_to_abbreviation that takes an incoming country name, converts it to lowercase, and returns the corresponding uppercase two-character abbreviation if found. It also checks for common abbreviations and alternative spellings. If no matching abbreviation is found, it returns None.




