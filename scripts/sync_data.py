import os
import requests
import yaml
import json
import re
import hashlib
from dotenv import load_dotenv
from pyairtable import Api
from pathlib import Path
import argparse

# Load environment variables
load_dotenv()

AIRTABLE_PAT = os.getenv("AIRTABLE_PAT")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
SCHEMA_PATH = Path("_data/schema_map.yml")

if not AIRTABLE_PAT or not AIRTABLE_BASE_ID:
    print("Error: AIRTABLE_PAT and AIRTABLE_BASE_ID must be provided.")
    print("Ensure they are set in your .env file (local) or added as Repository Secrets (GitHub Actions).")
    exit(1)

if not SCHEMA_PATH.exists():
    print(f"Error: Schema map not found at {SCHEMA_PATH}. Run scripts/sync_schema.py first.")
    exit(1)

api = Api(AIRTABLE_PAT)
base = api.base(AIRTABLE_BASE_ID)

# Target tables
TABLE_CONFIG = {
    "Cases": {"dir": Path("_cases"), "collection": "cases"},
    "Organisations": {"dir": Path("_organisations"), "collection": "organisations"},
    "Resources": {"dir": Path("_resources"), "collection": "resources"},
    "Participants": {"dir": Path("_participants"), "collection": "participants"},
    "Locations": {"dir": Path("_locations"), "collection": "locations"},
    "Messages": {"dir": Path("_messages"), "collection": "messages"}
}
TABLE_NAMES = list(TABLE_CONFIG.keys())
ATTACHMENT_DIR = Path("assets/attachments")

# Sync Settings
FILTER_WORKFLOW_STATUS_FIELD_ID = "fldrM6RRk8easAxSq"  # Default: Workflow: Status
FILTER_WORKFLOW_STATUS_VALUES = ["Completed","Draft","Nomination","Submission"]            # Sync records matching these status values (empty list to disable)

FILTER_CURATION_DECISION_FIELD_ID = "fldyT0fI25iZQRBiH" # Default: Curation decision
FILTER_CURATION_DECISION_VALUES = ["Featured Full Case", "Full Case", "Mapping Entry"] # Sync records matching these curation decisions (empty list to disable)

# Logical operator to combine filters when both are active: "AND" or "OR"
FILTER_OPERATOR = "AND"

try:
    import anyascii
    def transliterate(text):
        return anyascii.anyascii(str(text or ""))
except ImportError:
    import unicodedata
    def transliterate(text):
        return unicodedata.normalize('NFKD', str(text or "")).encode('ascii', 'ignore').decode('utf-8')

def raw_slugify(text):
    """Generate slug without transliteration to preserve original characters for redirects."""
    text = str(text or "").lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = text.strip('-')
    return text[:100].rstrip('-')

def slugify(text):
    """Generate universal transliterated ASCII slug."""
    text = transliterate(str(text or ""))
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = text.strip('-')
    return text[:100].rstrip('-')

def hash_id(record_id):
    if not record_id:
        return record_id
    return hashlib.sha256(record_id.encode()).hexdigest()[:16]

def is_record_id(value):
    """Check if a value looks like a raw Airtable record ID."""
    if isinstance(value, str):
        return value.startswith("rec") and len(value) >= 14
    if isinstance(value, list) and len(value) > 0:
        return all(isinstance(v, str) and v.startswith("rec") and len(v) >= 14 for v in value)
    return False

def load_schema_map():
    with open(SCHEMA_PATH, "r") as f:
        return yaml.safe_load(f)

def download_attachment(url, filename, record_id, field_id, suffix="", attachment_id=None):
    ATTACHMENT_DIR.mkdir(parents=True, exist_ok=True)
    
    hashed_rec_id = hash_id(record_id)
    ext = Path(filename).suffix
    if attachment_id:
        local_filename = f"{hashed_rec_id}_{field_id}_{attachment_id}_{suffix}{ext}" if suffix else f"{hashed_rec_id}_{field_id}_{attachment_id}{ext}"
    else:
        local_filename = f"{hashed_rec_id}_{field_id}_{suffix}_{filename}" if suffix else f"{hashed_rec_id}_{field_id}_{filename}"
    
    local_path = ATTACHMENT_DIR / local_filename
    
    if not local_path.exists():
        print(f"    Downloading {attachment_id or filename} {suffix}..." if suffix else f"    Downloading {attachment_id or filename}...")
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
    return f"/assets/attachments/{local_filename}"

def get_record_title(fields, table_id, schema_map, record_id):
    """Determine the title for a record based on schema and common field names."""
    table_fields = schema_map.get(table_id, {}).get("fields", {})
    
    # Try primary field
    primary_id = schema_map.get(table_id, {}).get("primaryFieldId")
    if primary_id and primary_id in fields:
        return str(fields[primary_id])
        
    # Fallback to common name fields
    for f_id, f_val in fields.items():
        f_info = table_fields.get(f_id)
        if f_info:
            clean_name = f_info["name"].strip().lower().replace("\ufeff", "")
            if clean_name in ["title", "name", "project title", "case name"]:
                return str(f_val)
    
    return record_id

def resolve_fields(data, schema_map, current_table_id, rec_id, id_to_slug, synced_ids):
    resolved = {}
    table_fields = schema_map.get(current_table_id, {}).get("fields", {})
    
    for field_id, value in data.items():
        field_info = table_fields.get(field_id)
        
        # Only process if field is in schema and marked for sync
        if not field_info or not field_info.get("sync", False):
            continue

        # Skip if value is solely a record ID and not a link
        if is_record_id(value) and field_info["type"] != "multipleRecordLinks":
            continue

        key_name = field_info.get("slug", field_id)

        # Check if it's a multiple record link
        if field_info["type"] == "multipleRecordLinks":
            linked_slugs = []
            for l_rec_id in value:
                # ONLY include links to records that are actually being synced
                if l_rec_id in synced_ids and l_rec_id in id_to_slug:
                    linked_slugs.append(id_to_slug[l_rec_id])
            resolved[key_name] = linked_slugs
        
        # Handle attachments
        elif field_info["type"] == "multipleAttachments":
            local_attachments = []
            for att in value:
                att_id = att.get("id")
                local_url = download_attachment(att["url"], att["filename"], rec_id, field_id, attachment_id=att_id)
                new_att = {**att, "url": local_url}
                if "thumbnails" in att:
                    new_thumbnails = {}
                    for size, thumb in att["thumbnails"].items():
                        thumb_url = download_attachment(thumb["url"], att["filename"], rec_id, field_id, suffix=size, attachment_id=att_id)
                        new_thumbnails[size] = {**thumb, "url": thumb_url}
                    new_att["thumbnails"] = new_thumbnails
                local_attachments.append(new_att)
            resolved[key_name] = local_attachments
        else:
            resolved[key_name] = value
    return resolved

def clean_markdown_to_plain_text(text):
    if not text:
        return ""
    text = str(text)
    # Remove markdown links [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove images ![alt](url)
    text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', text)
    # Remove bold, italics, code: **, *, __, _, `
    text = re.sub(r'[*_`#>]', '', text)
    # Collapse multiple whitespace/newlines to single space
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def truncate_text(text, max_length=160):
    if not text or len(text) <= max_length:
        return text
    truncated = text[:max_length].rsplit(' ', 1)[0]
    return truncated.rstrip('.,;:') + '...'

def derive_case_description(data, max_length=160):
    """
    Extract a concise plain-text description for a case study from either
    'describe-the-subject-matter-in-your-own-words-one' or
    'provide-a-brief-description-of-the-project'.
    """
    subject = clean_markdown_to_plain_text(data.get("describe-the-subject-matter-in-your-own-words-one"))
    if subject:
        if len(subject) <= max_length:
            return subject
        truncated = subject[:max_length].rsplit(' ', 1)[0]
        return truncated.rstrip('.,;:') + '...'

    brief = clean_markdown_to_plain_text(data.get("provide-a-brief-description-of-the-project"))
    if brief:
        if len(brief) <= max_length:
            return brief
        truncated = brief[:max_length].rsplit(' ', 1)[0]
        return truncated.rstrip('.,;:') + '...'

    # Fallback to project title and theme if available
    title = clean_markdown_to_plain_text(data.get("title") or data.get("project-title"))
    if title:
        theme = data.get("theme")
        if isinstance(theme, list) and theme:
            theme_str = f" in {clean_markdown_to_plain_text(theme[0])}"
        elif isinstance(theme, str) and theme:
            theme_str = f" in {clean_markdown_to_plain_text(theme)}"
        else:
            theme_str = ""
        fallback = f"Case study on {title}{theme_str}, exploring public voice and participatory engagement in AI governance."
        return truncate_text(fallback, max_length)

    return None

def annotate_yaml(yaml_str, field_map):
    lines = yaml_str.splitlines()
    new_lines = []
    skip_keys = {"layout", "title", "description", "airtable_id", "slug", "redirect_from"}
    for line in lines:
        # Match "some-key:" or "  some-key:" or "- some-key:"
        match = re.search(r'^(\s*)(?:-\s+)?([a-zA-Z0-9_-]+):', line)
        if match:
            indent, key = match.groups()
            if key not in skip_keys and key in field_map:
                # Always prepend the comment on the line before
                new_lines.append(f"{indent}# {field_map[key]}")
        new_lines.append(line)
    return "\n".join(new_lines)

def update_existing_cases():
    schema_map = load_schema_map()
    field_slug_to_name = {}
    for t_data in schema_map.values():
        for f_id, f_info in t_data.get("fields", {}).items():
            slug = f_info.get("slug")
            if slug:
                field_slug_to_name[slug] = f_info["name"]
            else:
                field_slug_to_name[f_id] = f_info["name"]
                
    cases_dir = Path("_cases")
    if not cases_dir.exists():
        print(f"Directory {cases_dir} does not exist.")
        return

    count = 0
    for case_file in sorted(cases_dir.glob("*.md")):
        content = case_file.read_text(encoding="utf-8")
        if not content.startswith("---"):
            continue
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue
        fm_raw = parts[1]
        data = yaml.safe_load(fm_raw) or {}
        case_desc = derive_case_description(data)
        if case_desc:
            new_fm = {}
            for k, v in data.items():
                new_fm[k] = v
                if k == "title":
                    new_fm["description"] = case_desc
            if "description" not in new_fm:
                new_fm["description"] = case_desc
            fm_yaml = yaml.dump(new_fm, sort_keys=False)
            case_file.write_text(f"---\n{annotate_yaml(fm_yaml, field_slug_to_name)}\n---\n", encoding="utf-8")
            count += 1
    print(f"Updated description in {count} case files.")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Sync Airtable data to markdown files with filter options.")
    parser.add_argument(
        "--update-cases-only",
        action="store_true",
        help="Update description field in existing _cases/*.md files without contacting Airtable."
    )
    parser.add_argument(
        "--workflow-status", 
        help="Comma-separated list of workflow status values to filter by (default: Completed). Use 'none' or '' to disable."
    )
    parser.add_argument(
        "--curation-decision", 
        help="Comma-separated list of curation decision values to filter by (default: Featured Full Case, Full Case, Mapping Entry). Use 'none' or '' to disable."
    )
    parser.add_argument(
        "--operator", 
        choices=["AND", "OR"], 
        default=FILTER_OPERATOR,
        help=f"Logical operator to combine filters when both are active (default: {FILTER_OPERATOR})"
    )
    args = parser.parse_args()

    if args.update_cases_only:
        update_existing_cases()
        return

    # Determine workflow status values to filter by
    if args.workflow_status is not None:
        if args.workflow_status.lower() in ("none", ""):
            workflow_values = []
        else:
            workflow_values = [s.strip() for s in args.workflow_status.split(",") if s.strip()]
    else:
        workflow_values = FILTER_WORKFLOW_STATUS_VALUES

    # Determine curation decision values to filter by
    if args.curation_decision is not None:
        if args.curation_decision.lower() in ("none", ""):
            curation_values = []
        else:
            curation_values = [s.strip() for s in args.curation_decision.split(",") if s.strip()]
    else:
        curation_values = FILTER_CURATION_DECISION_VALUES

    operator = args.operator

    schema_map = load_schema_map()
    
    # Map all field slugs and IDs to names for comment addition
    field_slug_to_name = {}
    for t_data in schema_map.values():
        for f_id, f_info in t_data.get("fields", {}).items():
            slug = f_info.get("slug")
            if slug:
                field_slug_to_name[slug] = f_info["name"]
            else:
                field_slug_to_name[f_id] = f_info["name"]

    # Map names to IDs for easier fetching
    name_to_id = {table_data["name"]: t_id for t_id, table_data in schema_map.items()}
    
    print("Fetching records from Airtable...")
    all_tables_data = {}
    id_to_slug = {}
    used_slugs_by_table = {}

    for name in TABLE_NAMES:
        if name in name_to_id:
            t_id = name_to_id[name]
            print(f"  Fetching {name} ({t_id})...")
            records = base.table(t_id).all(use_field_ids=True)
            all_tables_data[t_id] = {r["id"]: r["fields"] for r in records}
            
            # Generate slugs first for cross-referencing
            used_slugs_by_table[t_id] = set()
            for rec_id, fields in all_tables_data[t_id].items():
                title = get_record_title(fields, t_id, schema_map, rec_id)
                base_slug = slugify(title)
                if not base_slug:
                    base_slug = hash_id(rec_id)
                
                slug = base_slug
                counter = 1
                while slug in used_slugs_by_table[t_id]:
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                used_slugs_by_table[t_id].add(slug)
                id_to_slug[rec_id] = slug
        else:
            print(f"  Warning: Table '{name}' not found in schema map.")

    # 1. Identify active cases
    case_table_id = name_to_id.get("Cases")
    active_case_ids = set()
    
    if case_table_id and case_table_id in all_tables_data:
        for rec_id, fields in all_tables_data[case_table_id].items():
            # Check Workflow Status match
            workflow_match = True
            if FILTER_WORKFLOW_STATUS_FIELD_ID and workflow_values:
                current_status = fields.get(FILTER_WORKFLOW_STATUS_FIELD_ID)
                status_list = current_status if isinstance(current_status, list) else ([current_status] if current_status is not None else [])
                workflow_match = any(s in workflow_values for s in status_list)

            # Check Curation Decision match
            curation_match = True
            if FILTER_CURATION_DECISION_FIELD_ID and curation_values:
                current_curation = fields.get(FILTER_CURATION_DECISION_FIELD_ID)
                curation_list = current_curation if isinstance(current_curation, list) else ([current_curation] if current_curation is not None else [])
                curation_match = any(s in curation_values for s in curation_list)

            # Combine filters based on operator
            has_workflow_filter = bool(FILTER_WORKFLOW_STATUS_FIELD_ID and workflow_values)
            has_curation_filter = bool(FILTER_CURISION_DECISION_FIELD_ID if 'FILTER_CURISION_DECISION_FIELD_ID' in globals() else FILTER_CURATION_DECISION_FIELD_ID and curation_values)

            if has_workflow_filter and has_curation_filter:
                if operator == "AND":
                    keep = workflow_match and curation_match
                else:
                    keep = workflow_match or curation_match
            elif has_workflow_filter:
                keep = workflow_match
            elif has_curation_filter:
                keep = curation_match
            else:
                keep = True

            if not keep:
                continue

            active_case_ids.add(rec_id)

    # 2. Recursively find all reachable non-case records
    referenced_ids = set(active_case_ids)
    to_expand = list(active_case_ids)
    
    while to_expand:
        current_id = to_expand.pop()
        
        # Find which table this record belongs to
        found_fields = None
        found_table_id = None
        for t_id, t_data in all_tables_data.items():
            if current_id in t_data:
                found_fields = t_data[current_id]
                found_table_id = t_id
                break
        
        if found_fields:
            table_fields = schema_map.get(found_table_id, {}).get("fields", {})
            for f_id, f_val in found_fields.items():
                f_info = table_fields.get(f_id)
                # Only follow links if the field itself is marked for sync
                if f_info and f_info.get("sync") and f_info["type"] == "multipleRecordLinks" and isinstance(f_val, list):
                    for ref in f_val:
                        # Determine if the reference is to a Case or something else
                        is_ref_case = False
                        for t_id, t_data in all_tables_data.items():
                            if ref in t_data:
                                if t_id == case_table_id:
                                    is_ref_case = True
                                break
                        
                        # Rules:
                        # - If it's a Case, only include if it's already an ACTIVE case
                        # - If it's not a Case, include it and continue expanding
                        if is_ref_case:
                            if ref in active_case_ids:
                                referenced_ids.add(ref)
                        else:
                            if ref not in referenced_ids:
                                referenced_ids.add(ref)
                                to_expand.append(ref)

    # 3. Process each table and write only referenced records
    for table_name, config in TABLE_CONFIG.items():
        t_id = name_to_id.get(table_name)
        if not t_id or t_id not in all_tables_data:
            continue

        print(f"Processing {table_name}...")
        config["dir"].mkdir(exist_ok=True)
        # Clear existing
        for f in config["dir"].glob("*.md"):
            f.unlink()
        
        sync_count = 0
        for rec_id, fields in all_tables_data[t_id].items():
            # Only sync if it's in our discovered referenced set
            if rec_id not in referenced_ids:
                continue

            # Resolve fields (cross-references use slugs, filtered by referenced_ids)
            final_data = resolve_fields(fields, schema_map, t_id, rec_id, id_to_slug, referenced_ids)
            
            title = get_record_title(fields, t_id, schema_map, rec_id)
            slug = id_to_slug[rec_id]

            if table_name == "Cases":
                layout = "case"
                redirects = [f"/c/{hash_id(rec_id)}/"]
                raw_slug = raw_slugify(title)
                if raw_slug and raw_slug != slug:
                    quoted = urllib.parse.quote(raw_slug)
                    candidate_redirects = [
                        f"/cases/{raw_slug}.html",
                        f"/cases/{raw_slug}/",
                        f"/cases/{raw_slug}",
                    ]
                    if quoted != raw_slug:
                        candidate_redirects.extend([
                            f"/cases/{quoted}.html",
                            f"/cases/{quoted}/",
                            f"/cases/{quoted}",
                        ])
                    for r_path in candidate_redirects:
                        if r_path not in redirects:
                            redirects.append(r_path)
                case_desc = derive_case_description(final_data)
            elif table_name == "Organisations":
                layout = "organisation"
                redirects = None
                case_desc = None
            else:
                layout = "generic"
                redirects = None
                case_desc = None
            
            front_matter = {
                "layout": layout,
                "title": title,
                "airtable_id": hash_id(rec_id),
                "slug": slug,
            }
            if redirects:
                front_matter["redirect_from"] = redirects
            if case_desc:
                front_matter["description"] = case_desc
            front_matter.update(final_data)
            if case_desc:
                front_matter["description"] = case_desc
            
            file_path = config["dir"] / f"{slug}.md"
            with open(file_path, "w") as f:
                f.write("---\n")
                fm_yaml = yaml.dump(front_matter, sort_keys=False)
                f.write(annotate_yaml(fm_yaml, field_slug_to_name))
                f.write("\n---\n")
            sync_count += 1
        print(f"  {sync_count} records processed for {table_name}.")

    print(f"Sync complete!")
    
    # Run the cases aggregation compilation
    try:
        from generate_cases_json import aggregate
        aggregate()
    except Exception as e:
        print(f"Warning: Failed to run generate_cases_json aggregation: {e}")

if __name__ == "__main__":
    main()
