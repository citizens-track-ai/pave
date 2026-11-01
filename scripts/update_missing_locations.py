import os
import time
import urllib.parse
import requests
from dotenv import load_dotenv
from pyairtable import Api

# Load environment variables
load_dotenv()

# We use WRITE_PAT since it has write permissions as verified by our test
WRITE_PAT = os.getenv("WRITE_PAT")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

if not WRITE_PAT or not AIRTABLE_BASE_ID:
    print("Error: WRITE_PAT and AIRTABLE_BASE_ID must be provided.")
    exit(1)

api = Api(WRITE_PAT)
base = api.base(AIRTABLE_BASE_ID)
LOCATIONS_TABLE_ID = "tblg0E17yrYVgCDOw"
table = base.table(LOCATIONS_TABLE_ID)

# Field IDs from schema_map.yml
NAME_FIELD_ID = "fldNDwfliTbwWYd4l"
COUNTRY_CODE_FIELD_ID = "fldy0zqeilb2NSEOB"
LATITUDE_FIELD_ID = "fldWtvMukYmq1IuWq"
LONGITUDE_FIELD_ID = "fldCdYZ8Ay6f6ulq1"

# Conceptual, global, or non-geographic locations that should not be assigned map coordinates
IGNORED_LOCATIONS = {
    "global",
    "worldwide",
    "international",
    "online",
    "various",
    "remote",
    "virtual",
    "n/a",
    "none",
}

# Aliases to map abbreviated or informal place names to queries Nominatim understands
LOCATION_ALIASES = {
    "antigua & deps": "Antigua and Barbuda",
    "antigua and deps": "Antigua and Barbuda",
    "usa": "United States",
    "uk": "United Kingdom",
    "uae": "United Arab Emirates",
}

headers = {
    'User-Agent': 'PAVE-Airtable-Geocoder/1.0 (connectedbydata.org)'
}

def geocode_location(name):
    print(f"  Geocoding '{name}'...")
    encoded_query = urllib.parse.quote(name)
    url = f"https://nominatim.openstreetmap.org/search?q={encoded_query}&format=json&addressdetails=1&limit=1"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                result = data[0]
                lat = float(result['lat'])
                lon = float(result['lon'])
                country_code = result.get('address', {}).get('country_code', '').upper()
                return lat, lon, country_code
            else:
                print("    No geocoding results found.")
        else:
            print(f"    Geocoding API HTTP error: {response.status_code}")
    except Exception as e:
        print(f"    Geocoding error: {e}")
    return None

def main():
    print("Fetching location records from Airtable...")
    try:
        records = table.all(use_field_ids=True)
    except Exception as e:
        print(f"Error fetching records from Airtable: {e}")
        exit(1)
        
    print(f"Found {len(records)} total location records.")
    
    missing_records = []
    for r in records:
        fields = r.get("fields", {})
        name = fields.get(NAME_FIELD_ID)
        country_code = fields.get(COUNTRY_CODE_FIELD_ID)
        lat = fields.get(LATITUDE_FIELD_ID)
        lng = fields.get(LONGITUDE_FIELD_ID)
        
        if not name:
            continue
            
        if not country_code or lat is None or lng is None:
            missing_records.append({
                "id": r["id"],
                "name": name,
                "missing_fields": {
                    "country_code": not country_code,
                    "latitude": lat is None,
                    "longitude": lng is None
                }
            })
            
    if not missing_records:
        print("All location records are complete! No updates needed.")
        return
        
    print(f"Found {len(missing_records)} records missing location information.")
    
    updated_count = 0
    for idx, r in enumerate(missing_records):
        rec_id = r["id"]
        name = r["name"]
        clean_name = name.strip().lower()

        # Skip conceptual / non-geographic scopes
        if clean_name in IGNORED_LOCATIONS:
            print(f"  Skipping non-geographic/conceptual location '{name}'.")
            continue

        # Check for name aliases
        query_name = LOCATION_ALIASES.get(clean_name, name)
        if query_name != name:
            print(f"  Using alias '{query_name}' for '{name}'...")

        # Geocode the location
        geocoded = geocode_location(query_name)
        if geocoded:
            lat, lng, country_code = geocoded
            
            update_payload = {}
            if r["missing_fields"]["country_code"] and country_code:
                update_payload[COUNTRY_CODE_FIELD_ID] = country_code
            if r["missing_fields"]["latitude"] and lat is not None:
                update_payload[LATITUDE_FIELD_ID] = lat
            if r["missing_fields"]["longitude"] and lng is not None:
                update_payload[LONGITUDE_FIELD_ID] = lng
                
            if update_payload:
                print(f"  Updating record {rec_id} with: {update_payload}")
                try:
                    table.update(rec_id, update_payload, use_field_ids=True)
                    print(f"  Successfully updated record {rec_id}.")
                    updated_count += 1
                except Exception as e:
                    print(f"  Error updating Airtable record {rec_id}: {e}")
            else:
                print(f"  No updates to apply for '{name}'.")
        else:
            print(f"  Could not geocode '{name}'. Skipping.")
            
        # Respect Nominatim's usage policy of max 1 request/second
        if idx < len(missing_records) - 1:
            time.sleep(1.2)
            
    print(f"Updates complete. Updated {updated_count} records.")

if __name__ == "__main__":
    main()
