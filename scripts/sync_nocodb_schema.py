#!/usr/bin/env python3
import os
import re
import json
import yaml
try:
    import requests
except ImportError:
    requests = None
import urllib.request
import urllib.error
import urllib.parse
import argparse
from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

NOCODB_API_TOKEN = os.getenv("NOCODB_API_TOKEN") or os.getenv("NC_TOKEN") or os.getenv("NOCODB_TOKEN")
NOCODB_BASE_ID = os.getenv("NOCODB_BASE_ID") or "p1t9vvz76dbkcv8"
NOCODB_URL = os.getenv("NOCODB_URL") or "https://app.nocodb.com"
DEFAULT_SCHEMA_PATH = Path("_data/schema_map.yml")

def generate_field_slug(name):
    """Generate a clean URL/YAML-friendly slug from a field name."""
    name = name.replace("\ufeff", "")
    name = name.lower()
    name = re.sub(r'[^a-z0-9\s-]', '', name)
    slug = re.sub(r'[\s_-]+', '-', name).strip('-')
    if len(slug) > 50:
        truncated = slug[:50]
        if '-' in truncated:
            slug = truncated.rsplit('-', 1)[0]
        else:
            slug = truncated
    return slug

def _http_get_json(url, token):
    if requests is not None:
        headers = {
            "xc-token": token,
            "Accept": "application/json"
        }
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        return None
    else:
        req = urllib.request.Request(url, headers={
            "xc-token": token,
            "Accept": "application/json",
            "User-Agent": "PAVE-Sync/1.0"
        })
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status == 200:
                    return json.loads(response.read().decode('utf-8'))
        except Exception:
            return None
    return None

def fetch_nocodb_tables(base_url, base_id, token):
    """Fetch tables and their full field schemas from NocoDB REST API."""
    candidates = [
        f"{base_url.rstrip('/')}/api/v2/meta/bases/{base_id}/tables",
        f"{base_url.rstrip('/')}/api/v3/meta/bases/{base_id}/tables",
        f"{base_url.rstrip('/')}/api/v1/db/meta/projects/{base_id}/tables"
    ]
    tables_list = None
    for url in candidates:
        try:
            data = _http_get_json(url, token)
            if data:
                tables_list = data.get("list") or data.get("tables") or (data if isinstance(data, list) else None)
                if tables_list:
                    break
        except Exception:
            continue

    if not tables_list:
        raise RuntimeError(f"Failed to fetch NocoDB tables list. Check your NC_TOKEN/NOCODB_API_TOKEN and NOCODB_BASE_ID.")

    populated_tables = []
    for t in tables_list:
        t_id = t.get("id")
        t_name = t.get("title") or t.get("name")
        # If table already has fields/columns, keep it
        if t.get("fields") or t.get("columns"):
            populated_tables.append(t)
            continue

        # In NocoDB, table list does not include column schemas.
        # Fetch detailed table schema containing fields.
        table_detail = None
        for detail_url in [
            f"{base_url.rstrip('/')}/api/v2/meta/tables/{t_id}",
            f"{base_url.rstrip('/')}/api/v3/meta/bases/{base_id}/tables/{t_id}"
        ]:
            try:
                table_detail = _http_get_json(detail_url, token)
                if table_detail and (table_detail.get("fields") or table_detail.get("columns")):
                    break
            except Exception:
                continue

        if table_detail:
            populated_tables.append(table_detail)
        else:
            populated_tables.append(t)

    return populated_tables

def build_schema_map(tables, existing_schema, default_sync=False, reset_all=None):
    """Build a unified schema map preserving existing sync flags and field slugs."""
    # Build old lookup: (table_name_lower, clean_field_name) -> old_field_dict
    old_fields_lookup = {}
    for t_id, t_info in existing_schema.items():
        t_name = t_info.get("name", "").strip().lower()
        for f_id, f_info in t_info.get("fields", {}).items():
            clean_name = f_info.get("name", "").strip().lower().replace("\ufeff", "")
            old_fields_lookup[(t_name, clean_name)] = f_info

    new_schema = {}

    for table in tables:
        t_id = table.get("id")
        t_name = table.get("title") or table.get("name")
        if not t_name or t_name.startswith("PAVE Data Commons"):
            continue

        existing_table = existing_schema.get(t_id, {})
        fields = table.get("fields") or table.get("columns") or []

        # Safeguard: if API returns 0 fields but we have existing fields, retain them!
        if not fields and existing_table.get("fields"):
            print(f"  Warning: No fields returned for table '{t_name}'. Retaining existing schema fields.")
            new_schema[t_id] = existing_table
            continue

        primary_field_id = table.get("display_field_id")
        if not primary_field_id:
            for f in fields:
                if f.get("primary_value") or f.get("pv"):
                    primary_field_id = f.get("id")
                    break
        if not primary_field_id:
            for f in fields:
                if f.get("primary_key") or f.get("pk"):
                    primary_field_id = f.get("id")
                    break
        if not primary_field_id and fields:
            primary_field_id = fields[0].get("id")

        # Collect used slugs to avoid collisions
        used_slugs = set()
        for f in fields:
            f_id = f.get("id")
            existing_f = existing_table.get("fields", {}).get(f_id, {})
            if existing_f.get("slug"):
                used_slugs.add(existing_f["slug"])

        new_table_fields = {}
        for f in fields:
            f_id = f.get("id")
            f_name = f.get("title") or f.get("name") or f_id
            f_type = f.get("type") or f.get("uidt") or "SingleLineText"

            # Check existing field by field_id first, then by table_name + clean field name
            existing_f = existing_table.get("fields", {}).get(f_id)
            if not existing_f:
                clean_name = f_name.strip().lower().replace("\ufeff", "")
                existing_f = old_fields_lookup.get((t_name.strip().lower(), clean_name), {})

            # Sync flag
            if reset_all is not None:
                sync_status = reset_all
            elif "sync" in existing_f:
                sync_status = existing_f["sync"]
            else:
                sync_status = default_sync

            # Slug
            slug = existing_f.get("slug")
            if not slug:
                base_slug = generate_field_slug(f_name) or "field"
                slug = base_slug
                counter = 1
                while slug in used_slugs:
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                used_slugs.add(slug)

            field_data = {
                "name": f_name,
                "type": f_type,
                "sync": sync_status,
                "slug": slug
            }

            # Comments and choices
            if "comment" in existing_f:
                field_data["comment"] = existing_f["comment"]
            
            # Options / choices
            options = f.get("options") or {}
            if "choices" in existing_f:
                field_data["choices"] = existing_f["choices"]
            elif "choices" in options and isinstance(options["choices"], list):
                field_data["choices"] = [
                    c.get("title") or c.get("name") for c in options["choices"] if isinstance(c, dict)
                ]

            if "related_table_id" in options:
                field_data["options"] = {"related_table_id": options["related_table_id"]}
            elif "fk_related_model_id" in options:
                field_data["options"] = {"related_table_id": options["fk_related_model_id"]}

            new_table_fields[f_id] = field_data

        new_schema[t_id] = {
            "name": t_name,
            "primaryFieldId": primary_field_id,
            "fields": new_table_fields
        }

    return new_schema

def main():
    parser = argparse.ArgumentParser(description="Sync NocoDB schema and update schema_map.yml.")
    parser.add_argument("--output", default=str(DEFAULT_SCHEMA_PATH), help=f"Path to schema output file (default: {DEFAULT_SCHEMA_PATH})")
    parser.add_argument("--default-sync", choices=["on", "off"], default="off", help="Default sync status for new fields (default: off)")
    parser.add_argument("--reset-all", choices=["on", "off"], help="Force reset all fields to on or off")
    parser.add_argument("--base-id", default=NOCODB_BASE_ID, help=f"NocoDB Base ID (default: {NOCODB_BASE_ID})")
    parser.add_argument("--schema-cache", help="Optional path to pre-dumped NocoDB schema JSON file (offline mode)")
    args = parser.parse_args()

    output_path = Path(args.output)
    default_sync_bool = (args.default_sync == "on")
    reset_all_bool = (args.reset_all == "on") if args.reset_all else None

    # Load existing schema map to preserve slugs and sync flags
    existing_schema = {}
    for candidate_path in [output_path, DEFAULT_SCHEMA_PATH]:
        if candidate_path.exists():
            try:
                with open(candidate_path, "r", encoding="utf-8") as f:
                    loaded = yaml.safe_load(f) or {}
                    for t_id, t_info in loaded.items():
                        curr_cnt = len(existing_schema.get(t_id, {}).get("fields", {}))
                        new_cnt = len(t_info.get("fields", {}))
                        if t_id not in existing_schema or new_cnt > curr_cnt:
                            existing_schema[t_id] = t_info
            except Exception:
                pass

    tables = None
    if args.schema_cache and Path(args.schema_cache).exists():
        print(f"Loading schema from cache file: {args.schema_cache}")
        with open(args.schema_cache, "r", encoding="utf-8") as f:
            cached_data = json.load(f)
            tables = cached_data.get("tables") or cached_data.get("list") or cached_data
    else:
        if not NOCODB_API_TOKEN:
            print("Error: NOCODB_API_TOKEN (or NC_TOKEN) must be provided in your .env or environment.")
            print("Alternatively, pass --schema-cache with a pre-downloaded schema JSON file.")
            exit(1)
        print(f"Fetching schema from NocoDB base {args.base_id} at {NOCODB_URL}...")
        tables = fetch_nocodb_tables(NOCODB_URL, args.base_id, NOCODB_API_TOKEN)

    if not tables:
        print("Error: No tables returned from NocoDB schema fetch.")
        exit(1)

    new_schema = build_schema_map(tables, existing_schema, default_sync=default_sync_bool, reset_all=reset_all_bool)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(new_schema, f, sort_keys=False)

    print(f"Successfully updated schema map at {output_path} with {len(new_schema)} tables.")
    for t_id, t_info in new_schema.items():
        sync_cnt = sum(1 for f in t_info["fields"].values() if f.get("sync"))
        print(f"  {t_info['name']} ({t_id}): {len(t_info['fields'])} fields ({sync_cnt} marked for sync)")

if __name__ == "__main__":
    main()
