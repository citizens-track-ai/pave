#!/usr/bin/env python3
"""
scripts/update_missing_locations_nocodb.py
Checks NocoDB Locations table for records missing country_code, latitude,
or longitude, geocodes them using OpenStreetMap Nominatim, and updates NocoDB.

Drop-in replacement for scripts/update_missing_locations.py targeting NocoDB.
"""

import os
import sys
import time
import json
import argparse
import urllib.parse
from pathlib import Path

# HTTP client with urllib fallback (no mandatory external requests dependency)
try:
    import requests
except ImportError:
    requests = None

import urllib.request
import urllib.error

try:
    import yaml
except ImportError:
    yaml = None

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k not in os.environ:
                    os.environ[k] = v

# Configuration & Defaults
NOCODB_API_TOKEN = os.getenv("NOCODB_API_TOKEN") or os.getenv("NC_TOKEN") or os.getenv("NOCODB_TOKEN")
NOCODB_BASE_ID = os.getenv("NOCODB_BASE_ID") or "p1t9vvz76dbkcv8"
NOCODB_URL = os.getenv("NOCODB_URL") or "https://app.nocodb.com"
DEFAULT_LOCATIONS_TABLE_ID = "m585w7nu1pegh83"

NOMINATIM_HEADERS = {
    'User-Agent': 'PAVE-NocoDB-Geocoder/1.0 (connectedbydata.org)'
}

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

# Optional direct overrides for specific locations that shouldn't rely on Nominatim
LOCATION_OVERRIDES = {
    # e.g., "europe": {"country_code": "EU"}
}


def find_locations_table_id():
    """Locate Locations table ID from schema map, or return default."""
    if yaml is not None:
        schema_candidate = Path("_data/schema_map.yml")
        if schema_candidate.exists():
            try:
                with open(schema_candidate, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                for tbl_id, tbl_info in data.items():
                    if isinstance(tbl_info, dict) and tbl_info.get("name") == "Locations":
                        return tbl_id
            except Exception:
                pass
    return DEFAULT_LOCATIONS_TABLE_ID


class NocoDBClient:
    """Client for interacting with NocoDB REST API (supporting v3 and v2 endpoints)."""

    def __init__(self, base_url, base_id, token):
        self.base_url = base_url.rstrip("/")
        self.base_id = base_id
        self.token = token

    def _get(self, path, params=None):
        url = f"{self.base_url}{path}"
        if params:
            query = urllib.parse.urlencode(params)
            url = f"{url}?{query}"

        if requests is not None:
            headers = {"xc-token": self.token, "Accept": "application/json"}
            resp = requests.get(url, headers=headers, timeout=60)
            resp.raise_for_status()
            return resp.json()
        else:
            req = urllib.request.Request(url, headers={
                "xc-token": self.token,
                "Accept": "application/json",
                "User-Agent": "PAVE-NocoDB-Geocoder/1.0"
            })
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))

    def _patch(self, path, payload):
        url = f"{self.base_url}{path}"
        body_bytes = json.dumps(payload).encode("utf-8")

        if requests is not None:
            headers = {
                "xc-token": self.token,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            resp = requests.patch(url, headers=headers, data=body_bytes, timeout=60)
            resp.raise_for_status()
            try:
                return resp.json()
            except Exception:
                return resp.text
        else:
            req = urllib.request.Request(url, data=body_bytes, headers={
                "xc-token": self.token,
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "PAVE-NocoDB-Geocoder/1.0"
            }, method="PATCH")
            with urllib.request.urlopen(req, timeout=60) as resp:
                content = resp.read().decode("utf-8")
                try:
                    return json.loads(content)
                except Exception:
                    return content

    def get_table_records(self, table_id, page_size=100):
        """Fetch all records for a table handling pagination."""
        records = []
        page = 1
        while True:
            params = {
                "page": page,
                "pageSize": page_size
            }
            v3_path = f"/api/v3/data/{self.base_id}/{table_id}/records"
            try:
                data = self._get(v3_path, params=params)
            except Exception:
                v2_path = f"/api/v2/tables/{table_id}/records"
                data = self._get(v2_path, params=params)

            rows = data.get("records") or data.get("list") or []
            if not rows:
                break
            records.extend(rows)

            if "next_page" in data and not data["next_page"]:
                break
            if "pageInfo" in data and data["pageInfo"].get("isLastPage"):
                break
            if len(rows) < page_size:
                break
            page += 1

        return records

    def update_record(self, table_id, record_id, fields_payload):
        """Update a single record in NocoDB, trying v3 first, then v2."""
        # Try v3 data API first
        v3_path = f"/api/v3/data/{self.base_id}/{table_id}/records"
        v3_payload = {
            "records": [
                {
                    "id": record_id,
                    "fields": fields_payload
                }
            ]
        }
        try:
            return self._patch(v3_path, v3_payload)
        except Exception as e_v3:
            # Fall back to v2 tables API (array body)
            v2_path = f"/api/v2/tables/{table_id}/records"
            v2_payload = [{
                "Id": record_id,
                **fields_payload
            }]
            try:
                return self._patch(v2_path, v2_payload)
            except Exception as e_v2:
                # Fall back to v2 tables API (single object body)
                try:
                    return self._patch(v2_path, {"Id": record_id, **fields_payload})
                except Exception:
                    raise RuntimeError(
                        f"Failed to update record {record_id}. v3 error: {e_v3}, v2 error: {e_v2}"
                    )


def geocode_location(name):
    """Query OpenStreetMap Nominatim for latitude, longitude, and country_code."""
    print(f"  Geocoding '{name}'...")
    encoded_query = urllib.parse.quote(name)
    url = f"https://nominatim.openstreetmap.org/search?q={encoded_query}&format=json&addressdetails=1&limit=1"
    try:
        if requests is not None:
            response = requests.get(url, headers=NOMINATIM_HEADERS, timeout=30)
            if response.status_code == 200:
                data = response.json()
            else:
                print(f"    Geocoding API HTTP error: {response.status_code}")
                return None
        else:
            req = urllib.request.Request(url, headers=NOMINATIM_HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))

        if data:
            result = data[0]
            lat = float(result['lat'])
            lon = float(result['lon'])
            country_code = result.get('address', {}).get('country_code', '').upper()
            return lat, lon, country_code
        else:
            print("    No geocoding results found.")
    except Exception as e:
        print(f"    Geocoding error: {e}")
    return None


def extract_location_fields(record):
    """Extract standard location fields across v3 (nested fields) and v2 (flat) record structures."""
    if "fields" in record and isinstance(record["fields"], dict):
        f = record["fields"]
    else:
        f = record

    rec_id = record.get("id") or record.get("Id") or record.get("id_fields", {}).get("Id")
    name = f.get("Name") or f.get("name")
    country_code = f.get("Country Code") or f.get("country_code") or f.get("CountryCode")
    lat = f.get("Latitude") if f.get("Latitude") is not None else f.get("latitude")
    lng = f.get("Longitude") if f.get("Longitude") is not None else f.get("longitude")

    return rec_id, name, country_code, lat, lng


def main():
    parser = argparse.ArgumentParser(
        description="Update missing location coordinates and country codes in NocoDB via Nominatim geocoding."
    )
    parser.add_argument("--base-id", default=NOCODB_BASE_ID, help="NocoDB Base ID")
    parser.add_argument("--table-id", default=None, help="Locations table ID (auto-detected if omitted)")
    parser.add_argument("--url", default=NOCODB_URL, help="NocoDB URL (default: https://app.nocodb.com)")
    parser.add_argument("--token", default=NOCODB_API_TOKEN, help="NocoDB API Token / NC_TOKEN")
    parser.add_argument("--dry-run", action="store_true", help="Print updates without modifying NocoDB")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of missing records to process")
    parser.add_argument(
        "--rate-limit",
        type=float,
        default=1.2,
        help="Seconds to wait between Nominatim requests (default: 1.2 to respect Nominatim policy)"
    )

    args = parser.parse_args()

    token = args.token
    if not token:
        print("Error: NocoDB API token not found. Set NC_TOKEN or NOCODB_API_TOKEN in .env or pass --token.")
        sys.exit(1)

    table_id = args.table_id or find_locations_table_id()
    client = NocoDBClient(args.url, args.base_id, token)

    print(f"Connecting to NocoDB ({args.url}) - Base: {args.base_id}, Table: {table_id}...")
    try:
        records = client.get_table_records(table_id)
    except Exception as e:
        print(f"Error fetching records from NocoDB: {e}")
        sys.exit(1)

    print(f"Found {len(records)} total location records.")

    missing_records = []
    for r in records:
        rec_id, name, country_code, lat, lng = extract_location_fields(r)

        if not name:
            continue

        if not country_code or lat is None or lng is None:
            missing_records.append({
                "id": rec_id,
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

    if args.limit and args.limit > 0:
        missing_records = missing_records[:args.limit]
        print(f"Processing first {len(missing_records)} records due to --limit flag.")

    updated_count = 0
    for idx, r in enumerate(missing_records):
        rec_id = r["id"]
        name = r["name"]
        clean_name = name.strip().lower()

        # 1. Skip conceptual / non-geographic scopes
        if clean_name in IGNORED_LOCATIONS:
            print(f"  Skipping non-geographic/conceptual location '{name}'.")
            continue

        # 2. Check for manual coordinate/country overrides
        if clean_name in LOCATION_OVERRIDES:
            override = LOCATION_OVERRIDES[clean_name]
            lat = override.get("latitude")
            lng = override.get("longitude")
            country_code = override.get("country_code")
            geocoded = (lat, lng, country_code)
            print(f"  Using manual override for '{name}': {override}")
        else:
            # 3. Check for name aliases
            query_name = LOCATION_ALIASES.get(clean_name, name)
            if query_name != name:
                print(f"  Using alias '{query_name}' for '{name}'...")

            # Geocode the location
            geocoded = geocode_location(query_name)
        if geocoded:
            lat, lng, country_code = geocoded

            update_payload = {}
            if r["missing_fields"]["country_code"] and country_code:
                update_payload["Country Code"] = country_code
            if r["missing_fields"]["latitude"] and lat is not None:
                update_payload["Latitude"] = lat
            if r["missing_fields"]["longitude"] and lng is not None:
                update_payload["Longitude"] = lng

            if update_payload:
                if args.dry_run:
                    print(f"  [DRY RUN] Would update record {rec_id} ({name}) with: {update_payload}")
                    updated_count += 1
                else:
                    print(f"  Updating record {rec_id} ({name}) with: {update_payload}")
                    try:
                        client.update_record(table_id, rec_id, update_payload)
                        print(f"  Successfully updated record {rec_id}.")
                        updated_count += 1
                    except Exception as e:
                        print(f"  Error updating NocoDB record {rec_id}: {e}")
            else:
                print(f"  No updates to apply for '{name}'.")
        else:
            print(f"  Could not geocode '{name}'. Skipping.")

        # Respect Nominatim's usage policy of max 1 request/second
        if idx < len(missing_records) - 1:
            time.sleep(args.rate_limit)

    action_label = "Would update" if args.dry_run else "Updated"
    print(f"Updates complete. {action_label} {updated_count} record(s).")


if __name__ == "__main__":
    main()
