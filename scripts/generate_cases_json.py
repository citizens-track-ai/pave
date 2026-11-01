#!/usr/bin/env python3
import os
import yaml
import json
try:
    import pycountry_convert as pc
except ImportError:
    pc = None
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
CASES_DIR = BASE_DIR / "_cases"
PARTICIPANTS_DIR = BASE_DIR / "_participants"
LOCATIONS_DIR = BASE_DIR / "_locations"
MESSAGES_DIR = BASE_DIR / "_messages"
ORGANISATIONS_DIR = BASE_DIR / "_organisations"
OUTPUT_FILE = BASE_DIR / "assets/data/cases_aggregated.json"
METHODS_MAP_FILE = BASE_DIR / "_data/methods_map.yml"

def clean_int(val):
    if val is None:
        return 0
    if isinstance(val, (int, float)):
        return int(val)
    cleaned = str(val).replace(",", "").strip()
    try:
        return int(cleaned)
    except ValueError:
        try:
            return int(float(cleaned))
        except ValueError:
            return 0

def clean_float(val):
    if val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    cleaned = str(val).replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def get_continent(country_code):
    if not country_code or not pc:
        return None
    code_upper = str(country_code).upper().strip()
    try:
        continent_code = pc.country_alpha2_to_continent_code(code_upper)
        return pc.convert_continent_code_to_continent_name(continent_code)
    except Exception:
        return None

def load_collection(directory):
    data = {}
    if not directory.exists():
        return data
    for f in directory.glob("*.md"):
        if f.is_dir() or f.name.startswith("."):
            continue
        with open(f, "r", encoding="utf-8") as file:
            content = file.read()
            parts = content.split("---")
            if len(parts) >= 3:
                try:
                    fm = yaml.safe_load(parts[1])
                    if fm and "slug" in fm:
                        data[fm["slug"]] = fm
                except Exception as e:
                    print(f"Error parsing {f}: {e}")
    return data

def aggregate():
    print("Loading collections...")
    cases = load_collection(CASES_DIR)
    participants = load_collection(PARTICIPANTS_DIR)
    locations = load_collection(LOCATIONS_DIR)
    organisations = load_collection(ORGANISATIONS_DIR)
    messages = load_collection(MESSAGES_DIR)

    print(f"Loaded: {len(cases)} cases, {len(participants)} participants, {len(locations)} locations, {len(organisations)} organisations, {len(messages)} messages.")

    # Load methods map
    methods_map = {}
    if METHODS_MAP_FILE.exists():
        try:
            with open(METHODS_MAP_FILE, "r", encoding="utf-8") as f:
                methods_map = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Error loading methods map: {e}")
            
    deliberated_list = [str(m).strip().lower() for m in methods_map.get("deliberated", []) or []]
    participated_list = [str(m).strip().lower() for m in methods_map.get("participated", []) or []]

    # Pre-index messages by case
    case_to_messages = {}
    for msg_slug, msg in messages.items():
        msg_cases = msg.get("cases", [])
        if not isinstance(msg_cases, list):
            msg_cases = [msg_cases]
        for c_slug in msg_cases:
            if c_slug not in case_to_messages:
                case_to_messages[c_slug] = []
            case_to_messages[c_slug].append(msg)

    aggregated_cases = []

    for case_slug, case in cases.items():
        if case.get("curation-decision") == "Do not include":
            continue

        linked_part_slugs = case.get("participants", [])
        if not isinstance(linked_part_slugs, list):
            linked_part_slugs = [linked_part_slugs]

        linked_msg_slugs = case.get("messages", [])
        if not isinstance(linked_msg_slugs, list):
            linked_msg_slugs = [linked_msg_slugs]

        linked_org_slugs = case.get("lead-organisations", [])
        if not isinstance(linked_org_slugs, list):
            linked_org_slugs = [linked_org_slugs]

        case_modalities = set()
        case_methods = set()
        total_participants = 0
        max_average_hours = 0.0
        participant_countries = set()
        participant_continents = set()
        case_participants = []
        case_organisations = []

        # Process participants
        for p_slug in linked_part_slugs:
            part = participants.get(p_slug)
            if not part:
                continue

            # Modalities
            p_mods = part.get("where-did-engagement-take-place", [])
            if isinstance(p_mods, list):
                case_modalities.update(p_mods)
            elif p_mods:
                case_modalities.add(p_mods)

            # Methods
            p_methods = part.get("which-of-the-following-methods-were-used-to", [])
            if isinstance(p_methods, list):
                case_methods.update(p_methods)
            elif p_methods:
                case_methods.add(p_methods)

            # Participant count
            p_count = clean_int(part.get("how-many-people-took-part"))
            total_participants += p_count

            # Average hours - max average hours for any of the associated participants
            p_hours = clean_float(part.get("on-average-how-many-hours-did-each-participant"))
            if p_hours > max_average_hours:
                max_average_hours = p_hours

            # Locations & Participant markers
            p_loc_slugs = part.get("locations", [])
            if not isinstance(p_loc_slugs, list):
                p_loc_slugs = [p_loc_slugs]

            p_loc_titles = []
            for l_slug in p_loc_slugs:
                loc = locations.get(l_slug)
                if loc:
                    p_loc_titles.append(loc.get("title") or loc.get("name") or l_slug)
            locations_list_str = ", ".join(p_loc_titles)

            p_points = []
            for l_slug in p_loc_slugs:
                loc = locations.get(l_slug)
                if loc and loc.get("latitude") and loc.get("longitude"):
                    lat = clean_float(loc.get("latitude"))
                    lng = clean_float(loc.get("longitude"))
                    country_code = str(loc.get("country-code", "")).upper().strip()
                    if country_code:
                        participant_countries.add(country_code)
                        continent = get_continent(country_code)
                        if continent:
                            participant_continents.add(continent)

                    p_points.append({
                        "lat": lat,
                        "lng": lng,
                        "location_name": loc.get("title") or loc.get("name") or l_slug
                    })
            
            if p_points:
                case_participants.append({
                    "title": part.get("title") or part.get("name") or "Participant Group",
                    "count": part.get("how-many-people-took-part") or "",
                    "locations_list": locations_list_str,
                    "locations": p_points
                })

        # Process organisations
        for o_slug in linked_org_slugs:
            org = organisations.get(o_slug)
            if not org:
                continue
            o_loc_slugs = org.get("main-location", [])
            if not isinstance(o_loc_slugs, list):
                o_loc_slugs = [o_loc_slugs]
            
            o_points = []
            for l_slug in o_loc_slugs:
                loc = locations.get(l_slug)
                if loc and loc.get("latitude") and loc.get("longitude"):
                    lat = clean_float(loc.get("latitude"))
                    lng = clean_float(loc.get("longitude"))
                    
                    o_points.append({
                        "lat": lat,
                        "lng": lng,
                        "location_name": loc.get("title") or loc.get("name") or l_slug
                    })
            
            if o_points:
                case_organisations.append({
                    "title": org.get("name") or org.get("title") or "Lead Organisation",
                    "url": f"/organisations/{o_slug}/",
                    "locations": o_points
                })

        # Count recommendations and issues
        case_messages = []
        for m_slug in linked_msg_slugs:
            msg = messages.get(m_slug)
            if msg and msg not in case_messages:
                case_messages.append(msg)
        for msg in case_to_messages.get(case_slug, []):
            if msg not in case_messages:
                case_messages.append(msg)

        message_count = 0
        for msg in case_messages:
            msg_type = str(msg.get("type", "")).strip().lower()
            if msg_type in ["recommendation", "issue"]:
                message_count += 1

        case_themes = case.get("theme", [])
        if case_themes is None:
            case_themes = []
        elif not isinstance(case_themes, list):
            case_themes = [case_themes]

        # Determine method categories based on methods_map.yml rules
        method_categories = set()
        for m in case_methods:
            m_lower = str(m).strip().lower()
            if m_lower in deliberated_list:
                method_categories.add("deliberation")
            elif m_lower in participated_list:
                method_categories.add("participation")
            else:
                method_categories.add("research")

        if not method_categories:
            method_categories.add("research")

        aggregated_cases.append({
            "title": case.get("title") or case.get("project-title") or case_slug,
            "slug": case_slug,
            "url": case.get("url") or f"/cases/{case_slug}.html",
            "curation_decision": case.get("curation-decision") or "Mapping Entry",
            "themes": case_themes,
            "level_of_engagement": case.get("level-of-engagement") or "",
            "modalities": sorted(list(case_modalities)),
            "methods": sorted(list(case_methods)),
            "total_participants": total_participants,
            "average_hours": max_average_hours,
            "message_count": message_count,
            "countries": sorted(list(participant_countries)),
            "continents": sorted(list(participant_continents)),
            "method_categories": sorted(list(method_categories)),
            "participants": case_participants,
            "organisations": case_organisations
        })

    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(aggregated_cases, f, indent=2, ensure_ascii=False)
    print(f"Aggregated data written to {OUTPUT_FILE}")

if __name__ == "__main__":
    aggregate()
