#!/usr/bin/env python3
"""
scripts/sync_nocodb.py
Drop-in replacement for scripts/sync_data.py to sync NocoDB data to Jekyll markdown files.

Supports:
  - Full database sync (matching sync_data.py behavior)
  - Granular sync for a single case (--case-id <ID>) or a list of cases (--case-ids <ID1,ID2,...>)
  - Backward-compatible permalink hashes for cases migrated from Airtable (using AirTable ID)
    and new cases created directly on NocoDB (using deterministic NocoDB ID hash)
  - Automatic linked record fetching (Organisations, Locations, Participants, Messages, Resources)
  - Attachment downloading to assets/attachments/ with thumbnail resolution
  - Automatic compilation of assets/data/cases_aggregated.json
"""

import os
import sys
import re
import json
import yaml
import hashlib
import argparse
import mimetypes
from pathlib import Path

# HTTP client with urllib fallback (no mandatory external requests dependency)
try:
    import requests
except ImportError:
    requests = None

import urllib.request
import urllib.error
import urllib.parse

# Cloudflare R2 S3 SDK
try:
    import boto3
    from botocore.config import Config
    from botocore.exceptions import ClientError
except ImportError:
    boto3 = None
    Config = None
    ClientError = Exception

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configuration & Defaults
NOCODB_API_TOKEN = os.getenv("NOCODB_API_TOKEN") or os.getenv("NC_TOKEN") or os.getenv("NOCODB_TOKEN")
NOCODB_BASE_ID = os.getenv("NOCODB_BASE_ID") or "p1t9vvz76dbkcv8"
NOCODB_URL = os.getenv("NOCODB_URL") or "https://app.nocodb.com"

# Cloudflare R2 Configuration (S3-compatible API)
R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID") or os.getenv("CLOUDFLARE_ACCOUNT_ID")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID") or os.getenv("AWS_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY") or os.getenv("AWS_SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
R2_PUBLIC_URL = os.getenv("R2_PUBLIC_URL")  # e.g. https://media.pave.pairs.site or https://cdn.pairs.site
R2_JURISDICTION = os.getenv("R2_JURISDICTION", "").strip().lower()
R2_ENDPOINT_URL = os.getenv("R2_ENDPOINT_URL")
R2_PREFIX = os.getenv("R2_PREFIX", "attachments").strip("/")

SCHEMA_PATH = Path("_data/schema_map_nocodb.yml")
if not SCHEMA_PATH.exists():
    SCHEMA_PATH = Path("_data/schema_map.yml")

ATTACHMENT_DIR = Path("assets/attachments")

TABLE_CONFIG = {
    "Cases": {"dir": Path("_cases"), "collection": "cases", "layout": "case"},
    "Organisations": {"dir": Path("_organisations"), "collection": "organisations", "layout": "organisation"},
    "Resources": {"dir": Path("_resources"), "collection": "resources", "layout": "generic"},
    "Participants": {"dir": Path("_participants"), "collection": "participants", "layout": "generic"},
    "Locations": {"dir": Path("_locations"), "collection": "locations", "layout": "generic"},
    "Messages": {"dir": Path("_messages"), "collection": "messages", "layout": "generic"}
}

# Sync filter defaults (matches Airtable sync defaults)
FILTER_WORKFLOW_STATUS_FIELD = "Workflow: Status"
FILTER_WORKFLOW_STATUS_VALUES = ["Completed", "Draft", "Nomination", "Submission"]

FILTER_CURATION_DECISION_FIELD = "Curation decision"
FILTER_CURATION_DECISION_VALUES = ["Featured Full Case", "Full Case", "Mapping Entry"]

FILTER_OPERATOR = "AND"

GLOBAL_STATS = {"downloaded": 0, "uploaded": 0, "cached": 0}

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
        return ""
    return hashlib.sha256(str(record_id).encode()).hexdigest()[:16]

def get_case_permalink_id(fields, record_id):
    """
    Generate a permalink identifier:
    - If 'AirTable ID' is present and non-empty, hash it (keeps exact historical permalinks).
    - If 'AirTable ID' is blank/null, hash the NocoDB record ID deterministically.
    """
    airtable_id = (
        fields.get("AirTable ID")
        or fields.get("Airtable ID")
        or fields.get("airtable_id")
        or fields.get("airtable-id")
        or fields.get("AirtableID")
    )
    if airtable_id and str(airtable_id).strip():
        return hash_id(str(airtable_id).strip())
    return hash_id(f"nc_{record_id}")

def get_record_permalink_id(table_name, fields, record_id):
    """Generate permalink identifier for any table."""
    if table_name == "Cases":
        return get_case_permalink_id(fields, record_id)
    airtable_id = (
        fields.get("AirTable ID")
        or fields.get("Airtable ID")
        or fields.get("airtable_id")
        or fields.get("airtable-id")
    )
    if airtable_id and str(airtable_id).strip():
        return hash_id(str(airtable_id).strip())
    return hash_id(f"nc_{table_name.lower()}_{record_id}")

def load_schema_map(schema_file=None):
    target = Path(schema_file) if schema_file else SCHEMA_PATH
    if not target.exists() and SCHEMA_PATH.exists():
        target = SCHEMA_PATH
    if not target.exists():
        raise FileNotFoundError(f"Schema map not found at {target}. Run scripts/sync_nocodb_schema.py first.")
    with open(target, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

class NocoDBClient:
    def __init__(self, base_url, base_id, token):
        self.base_url = base_url.rstrip("/")
        self.base_id = base_id
        self.token = token

    def _request(self, path, params=None):
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
                "User-Agent": "PAVE-NocoDB-Sync/1.0"
            })
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))

    def get_table_records(self, table_id, page_size=100, where=None, view_id=None):
        """Fetch all records for a table, handling pagination."""
        records = []
        page = 1
        while True:
            params = {
                "page": page,
                "pageSize": page_size
            }
            if where:
                params["where"] = where
            if view_id:
                params["viewId"] = view_id

            # Try v3 data endpoint first, then v2
            v3_path = f"/api/v3/data/{self.base_id}/{table_id}/records"
            try:
                data = self._request(v3_path, params=params)
            except Exception:
                v2_path = f"/api/v2/tables/{table_id}/records"
                data = self._request(v2_path, params=params)

            rows = data.get("records") or data.get("list") or []
            if not rows:
                break
            records.extend(rows)

            # Check if there are more pages
            if "next_page" in data and not data["next_page"]:
                break
            if "pageInfo" in data and data["pageInfo"].get("isLastPage"):
                break
            if len(rows) < page_size:
                break
            page += 1

        return records

    def get_record(self, table_id, record_id):
        """Fetch a single record by ID."""
        v3_path = f"/api/v3/data/{self.base_id}/{table_id}/records/{record_id}"
        try:
            return self._request(v3_path)
        except Exception:
            v2_path = f"/api/v2/tables/{table_id}/records/{record_id}"
            return self._request(v2_path)

class R2StorageClient:
    def __init__(self, account_id, access_key, secret_key, bucket_name, public_url, endpoint_url=None, prefix="attachments", jurisdiction=None):
        if not boto3:
            raise ImportError("boto3 is required for Cloudflare R2 upload. Install with: pip install boto3")
        self.bucket = bucket_name
        self.public_url = public_url.rstrip("/") if public_url else ""
        self.prefix = prefix.strip("/") if prefix else ""
        
        jur = (jurisdiction or R2_JURISDICTION or "").strip().lower()
        if endpoint_url:
            endpoint = endpoint_url
        elif jur in ["eu", "eeur"]:
            endpoint = f"https://{account_id}.eu.r2.cloudflarestorage.com"
        elif jur in ["fedramp"]:
            endpoint = f"https://{account_id}.fedramp.r2.cloudflarestorage.com"
        elif account_id:
            endpoint = f"https://{account_id}.r2.cloudflarestorage.com"
        else:
            raise ValueError("Cloudflare R2 requires R2_ACCOUNT_ID (or R2_ENDPOINT_URL).")

        self.s3 = boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version="s3v4"),
            region_name="eeur" if jur in ["eu", "eeur"] else "auto"
        )

        # Automatic jurisdictional fallback: probe EU endpoint if global endpoint returns 404/NoSuchBucket
        if not jur and not endpoint_url and account_id:
            try:
                self.s3.head_bucket(Bucket=self.bucket)
            except ClientError as e:
                code = str(e.response.get("Error", {}).get("Code", ""))
                if code in ["404", "NoSuchBucket"]:
                    eu_endpoint = f"https://{account_id}.eu.r2.cloudflarestorage.com"
                    try:
                        s3_eu = boto3.client(
                            "s3",
                            endpoint_url=eu_endpoint,
                            aws_access_key_id=access_key,
                            aws_secret_access_key=secret_key,
                            config=Config(signature_version="s3v4"),
                            region_name="auto"
                        )
                        s3_eu.head_bucket(Bucket=self.bucket)
                        self.s3 = s3_eu
                        print(f"  Note: Bucket '{self.bucket}' detected in EU jurisdiction. Using {eu_endpoint}")
                    except Exception:
                        pass
            except Exception:
                pass

    def object_exists(self, key):
        try:
            self.s3.head_object(Bucket=self.bucket, Key=key)
            return True
        except ClientError as e:
            code = str(e.response.get("Error", {}).get("Code", ""))
            if code in ["404", "NoSuchKey"]:
                return False
            return False
        except Exception:
            return False

    def upload_file_from_url(self, url, key, filename):
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

        if requests is not None:
            resp = requests.get(url, stream=True, timeout=60)
            resp.raise_for_status()
            remote_ct = resp.headers.get("Content-Type")
            if remote_ct and "octet-stream" not in remote_ct:
                content_type = remote_ct.split(";")[0].strip()
            self.s3.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=resp.content,
                ContentType=content_type
            )
        else:
            req = urllib.request.Request(url, headers={"User-Agent": "PAVE-Sync/1.0"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
                remote_ct = resp.headers.get("Content-Type")
                if remote_ct and "octet-stream" not in remote_ct:
                    content_type = remote_ct.split(";")[0].strip()
                self.s3.put_object(
                    Bucket=self.bucket,
                    Key=key,
                    Body=data,
                    ContentType=content_type
                )

    def upload_local_file(self, local_path, key):
        content_type = mimetypes.guess_type(str(local_path))[0] or "application/octet-stream"
        with open(local_path, "rb") as f:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=f.read(),
                ContentType=content_type
            )

    def get_public_url(self, key):
        if self.public_url:
            return f"{self.public_url}/{key}"
        return f"https://{self.bucket}.r2.cloudflarestorage.com/{key}"

def process_attachment(url, filename, perm_id, field_slug, suffix="", attachment_id=None, r2_client=None):
    """
    Process attachment: uploads directly to Cloudflare R2 if configured,
    or falls back to local assets/attachments/ if in local mode.
    """
    ext = Path(filename).suffix
    if not ext and "?" in filename:
        ext = Path(filename.split("?")[0]).suffix

    clean_filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    if attachment_id:
        file_stem = f"{perm_id}_{field_slug}_{attachment_id}_{suffix}{ext}" if suffix else f"{perm_id}_{field_slug}_{attachment_id}{ext}"
    else:
        file_stem = f"{perm_id}_{field_slug}_{suffix}_{clean_filename}" if suffix else f"{perm_id}_{field_slug}_{clean_filename}"

    # Cloudflare R2 Mode
    if r2_client:
        r2_key = f"{r2_client.prefix}/{file_stem}" if r2_client.prefix else file_stem
        public_url = r2_client.get_public_url(r2_key)

        if r2_client.object_exists(r2_key):
            return public_url, False

        try:
            r2_client.upload_file_from_url(url, r2_key, filename)
            return public_url, True
        except Exception as e:
            print(f"    Warning: Failed to upload {filename} to Cloudflare R2: {e}")
            return public_url, False

    # Local storage fallback
    ATTACHMENT_DIR.mkdir(parents=True, exist_ok=True)
    local_path = ATTACHMENT_DIR / file_stem
    downloaded = False

    if not local_path.exists() and url:
        try:
            if requests is not None:
                r = requests.get(url, stream=True, timeout=30)
                if r.status_code == 200:
                    with open(local_path, "wb") as f:
                        for chunk in r.iter_content(4096):
                            f.write(chunk)
                    downloaded = True
            else:
                req = urllib.request.Request(url, headers={"User-Agent": "PAVE-Sync/1.0"})
                with urllib.request.urlopen(req, timeout=30) as r:
                    with open(local_path, "wb") as f:
                        f.write(r.read())
                    downloaded = True
        except Exception as e:
            print(f"    Warning: Failed to download {filename}: {e}")
    elif local_path.exists():
        downloaded = False

    return f"/assets/attachments/{file_stem}", downloaded

def clean_markdown_to_plain_text(text):
    if not text:
        return ""
    text = str(text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', text)
    text = re.sub(r'[*_`#>]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def truncate_text(text, max_length=160):
    if not text or len(text) <= max_length:
        return text
    truncated = text[:max_length].rsplit(' ', 1)[0]
    return truncated.rstrip('.,;:') + '...'

def derive_case_description(data, max_length=160):
    subject = clean_markdown_to_plain_text(data.get("describe-the-subject-matter-in-your-own-words-one"))
    if subject:
        if len(subject) <= max_length:
            return subject
        return subject[:max_length].rsplit(' ', 1)[0].rstrip('.,;:') + '...'

    brief = clean_markdown_to_plain_text(data.get("provide-a-brief-description-of-the-project"))
    if brief:
        if len(brief) <= max_length:
            return brief
        return brief[:max_length].rsplit(' ', 1)[0].rstrip('.,;:') + '...'

    title = clean_markdown_to_plain_text(data.get("title") or data.get("project-title"))
    if title:
        theme = data.get("theme")
        theme_str = f" in {clean_markdown_to_plain_text(theme[0] if isinstance(theme, list) else theme)}" if theme else ""
        fallback = f"Case study on {title}{theme_str}, exploring public voice and participatory engagement in AI governance."
        return truncate_text(fallback, max_length)

    return None

def annotate_yaml(yaml_str, field_slug_to_name):
    lines = yaml_str.splitlines()
    new_lines = []
    skip_keys = {"layout", "title", "description", "airtable_id", "slug", "redirect_from"}
    for line in lines:
        match = re.search(r'^(\s*)(?:-\s+)?([a-zA-Z0-9_-]+):', line)
        if match:
            indent, key = match.groups()
            if key not in skip_keys and key in field_slug_to_name:
                new_lines.append(f"{indent}# {field_slug_to_name[key]}")
        new_lines.append(line)
    return "\n".join(new_lines)

def get_record_title(fields, table_id, schema_map, record_id):
    t_info = schema_map.get(table_id, {})
    table_fields = t_info.get("fields", {})

    primary_id = t_info.get("primaryFieldId")
    if primary_id and primary_id in table_fields:
        f_name = table_fields[primary_id].get("name")
        if f_name and f_name in fields and fields[f_name]:
            return str(fields[f_name])

    for f_name, f_val in fields.items():
        if f_val and f_name.strip().lower() in ["title", "project title", "name", "case name"]:
            return str(f_val)

    return f"record-{record_id}"

def get_link_target_table_id(source_table_name, field_name, field_slug, field_info, name_to_table_id):
    """
    Determine which table a link field points to based on field schema or PAVE relationships.
    """
    if field_info:
        for opt_key in ["related_table_id", "fk_related_model_id", "colOptions"]:
            val = field_info.get(opt_key)
            if isinstance(val, str) and val in name_to_table_id.values():
                return val
            if isinstance(val, dict):
                rel = val.get("fk_related_model_id") or val.get("related_table_id")
                if rel and rel in name_to_table_id.values():
                    return rel

    fn_lower = (field_name or "").lower()
    fs_lower = (field_slug or "").lower()
    combined = f"{fn_lower} {fs_lower}"

    if "organisation" in combined:
        return name_to_table_id.get("Organisations")
    if "location" in combined:
        return name_to_table_id.get("Locations")
    if "participant" in combined:
        return name_to_table_id.get("Participants")
    if "resource" in combined:
        return name_to_table_id.get("Resources")
    if "message" in combined:
        return name_to_table_id.get("Messages")
    if "case" in combined:
        return name_to_table_id.get("Cases")

    return None

def resolve_record_fields(fields, table_id, schema_map, perm_id, id_to_slug, referenced_records, name_to_table_id, r2_client=None):
    """
    Resolve NocoDB fields into normalized YAML frontmatter dictionary based on schema map.
    """
    t_info = schema_map.get(table_id, {})
    t_name = t_info.get("name", "")
    table_fields = t_info.get("fields", {})

    # Create mapping: clean_field_name -> field_info
    name_to_field_info = {}
    for f_id, f_info in table_fields.items():
        clean = f_info.get("name", "").strip().lower().replace("\ufeff", "")
        name_to_field_info[clean] = f_info

    resolved = {}

    for f_name, f_val in fields.items():
        if f_val is None:
            continue

        clean_name = f_name.strip().lower().replace("\ufeff", "")
        f_info = name_to_field_info.get(clean_name)
        if not f_info or not f_info.get("sync", False):
            continue

        key_slug = f_info.get("slug") or slugify(f_name)
        f_type = f_info.get("type", "")

        # Linked records
        if f_type in ["LinkToAnotherRecord", "multipleRecordLinks", "Links"]:
            linked_slugs = []
            target_t_id = get_link_target_table_id(
                t_name, f_name, f_info.get("slug", ""), f_info, name_to_table_id
            )
            if target_t_id and isinstance(f_val, list):
                for item in f_val:
                    raw_id = (item.get("id") or item.get("Id")) if isinstance(item, dict) else item
                    if raw_id is not None:
                        target_id_str = str(raw_id)
                        if (target_t_id, target_id_str) in referenced_records:
                            target_slug = id_to_slug.get((target_t_id, target_id_str))
                            if target_slug:
                                linked_slugs.append(target_slug)
            if linked_slugs:
                resolved[key_slug] = linked_slugs

        # Attachments
        elif f_type in ["Attachment", "multipleAttachments"]:
            attachments_list = f_val if isinstance(f_val, list) else [f_val]
            local_attachments = []
            for att in attachments_list:
                if not isinstance(att, dict):
                    continue
                att_url = att.get("signedUrl") or att.get("url")
                att_name = att.get("title") or att.get("filename") or "attachment"
                att_id = att.get("id")
                if not att_url:
                    continue

                target_url, is_new = process_attachment(
                    att_url, att_name, perm_id, key_slug, attachment_id=att_id, r2_client=r2_client
                )
                if is_new:
                    if r2_client:
                        GLOBAL_STATS["uploaded"] += 1
                    else:
                        GLOBAL_STATS["downloaded"] += 1
                else:
                    GLOBAL_STATS["cached"] += 1

                new_att = {
                    "id": att_id or hash_id(att_name),
                    "url": target_url,
                    "filename": att_name
                }
                for prop in ["width", "height", "size"]:
                    if prop in att and att[prop] is not None:
                        new_att[prop] = att[prop]
                if "mimetype" in att:
                    new_att["type"] = att["mimetype"]

                # Thumbnails
                new_thumbs_count = 0
                if "thumbnails" in att and isinstance(att["thumbnails"], dict):
                    new_thumbs = {}
                    for size, thumb in att["thumbnails"].items():
                        if isinstance(thumb, dict):
                            t_url = thumb.get("signedUrl") or thumb.get("url")
                            if t_url:
                                t_target, t_is_new = process_attachment(
                                    t_url, att_name, perm_id, key_slug, suffix=size, attachment_id=att_id, r2_client=r2_client
                                )
                                if t_is_new:
                                    if r2_client:
                                        GLOBAL_STATS["uploaded"] += 1
                                    else:
                                        GLOBAL_STATS["downloaded"] += 1
                                    new_thumbs_count += 1
                                else:
                                    GLOBAL_STATS["cached"] += 1
                                new_thumbs[size] = {
                                    "url": t_target,
                                    "width": thumb.get("width"),
                                    "height": thumb.get("height")
                                }
                    if new_thumbs:
                        new_att["thumbnails"] = new_thumbs

                if is_new or new_thumbs_count > 0:
                    thumb_info = f" (+ {new_thumbs_count} thumbnails)" if new_thumbs_count > 0 else ""
                    dest_info = "to Cloudflare R2" if r2_client else "attachment"
                    print(f"    {'↑ Uploaded' if r2_client else '↓ Downloaded'} {dest_info}: {att_name}{thumb_info}")

                local_attachments.append(new_att)

            if local_attachments:
                resolved[key_slug] = local_attachments

        else:
            resolved[key_slug] = f_val

    return resolved

def update_existing_cases_descriptions():
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
        data = yaml.safe_load(parts[1]) or {}
        case_desc = derive_case_description(data)
        if case_desc:
            data["description"] = case_desc
            fm_yaml = yaml.dump(data, sort_keys=False)
            case_file.write_text(f"---\n{fm_yaml}\n---\n", encoding="utf-8")
            count += 1
    print(f"Updated description in {count} case files.")

def main():
    parser = argparse.ArgumentParser(description="Sync NocoDB data to Jekyll markdown files.")
    parser.add_argument("--case-id", help="Sync a single case by NocoDB ID (e.g. 130)")
    parser.add_argument("--case-ids", help="Sync specific comma-separated case IDs (e.g. 39,130)")
    parser.add_argument("--all", action="store_true", help="Sync all active cases from NocoDB")
    parser.add_argument("--clean", action="store_true", help="Remove orphaned markdown files when doing full sync")
    parser.add_argument("--workflow-status", help="Comma-separated workflow status values. Use 'none' to disable.")
    parser.add_argument("--curation-decision", help="Comma-separated curation decisions. Use 'none' to disable.")
    parser.add_argument("--operator", choices=["AND", "OR"], default=FILTER_OPERATOR)
    parser.add_argument("--update-cases-only", action="store_true", help="Update case descriptions locally without network.")
    parser.add_argument("--records-cache", help="Optional path to pre-dumped NocoDB records JSON (offline mode)")
    parser.add_argument("--schema-path", help="Path to schema_map.yml")
    parser.add_argument("--local-attachments", action="store_true", help="Store attachments locally in assets/attachments/ instead of Cloudflare R2")
    parser.add_argument("--r2-bucket", help="Override R2 bucket name")
    parser.add_argument("--r2-jurisdiction", choices=["eu", "fedramp", "default"], help="Cloudflare R2 jurisdiction (e.g. eu)")
    parser.add_argument("--r2-public-url", help="Override R2 public URL (e.g. https://media.pave.pairs.site)")
    parser.add_argument("--upload-existing-attachments", action="store_true", help="Migrate all existing files from assets/attachments/ to Cloudflare R2")
    args = parser.parse_args()

    if args.update_cases_only:
        update_existing_cases_descriptions()
        return

    schema_map = load_schema_map(args.schema_path)

    # Initialize Cloudflare R2 client if configured
    r2_client = None
    if not args.local_attachments:
        bucket_name = args.r2_bucket or R2_BUCKET_NAME
        public_url = args.r2_public_url or R2_PUBLIC_URL
        if R2_ACCOUNT_ID and R2_ACCESS_KEY_ID and R2_SECRET_ACCESS_KEY and bucket_name:
            try:
                r2_client = R2StorageClient(
                    account_id=R2_ACCOUNT_ID,
                    access_key=R2_ACCESS_KEY_ID,
                    secret_key=R2_SECRET_ACCESS_KEY,
                    bucket_name=bucket_name,
                    public_url=public_url,
                    endpoint_url=R2_ENDPOINT_URL,
                    prefix=R2_PREFIX,
                    jurisdiction=args.r2_jurisdiction or R2_JURISDICTION
                )
                print(f"Cloudflare R2 storage enabled: bucket '{bucket_name}', prefix '{R2_PREFIX}', public URL: {public_url or '(direct R2)'}")
            except Exception as e:
                print(f"Warning: Failed to initialize Cloudflare R2 client: {e}")
                print("Falling back to local assets/attachments/ storage.")
        else:
            print("Note: Cloudflare R2 credentials not fully specified in .env.")
            print("To enable R2, set R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME, and R2_PUBLIC_URL in .env.")
            print("Defaulting to local assets/attachments/ storage (or pass --local-attachments).")

    if args.upload_existing_attachments:
        if not r2_client:
            print("Error: Cloudflare R2 client is not configured. Provide R2 credentials in .env to upload.")
            sys.exit(1)
        if not ATTACHMENT_DIR.exists():
            print(f"Directory {ATTACHMENT_DIR} does not exist.")
            return
        files = [f for f in ATTACHMENT_DIR.glob("*") if f.is_file()]
        print(f"Migrating {len(files)} files from {ATTACHMENT_DIR} to Cloudflare R2...")
        uploaded_count = 0
        cached_count = 0
        for f in files:
            key = f"{r2_client.prefix}/{f.name}" if r2_client.prefix else f.name
            if r2_client.object_exists(key):
                cached_count += 1
            else:
                r2_client.upload_local_file(f, key)
                uploaded_count += 1
                print(f"  ↑ Uploaded: {f.name}")
        print(f"Migration complete! {uploaded_count} uploaded, {cached_count} already existed in R2.")
        return

    # Build field_slug_to_name for annotating frontmatter comments
    field_slug_to_name = {}
    name_to_table_id = {}
    for t_id, t_info in schema_map.items():
        t_name = t_info.get("name")
        if t_name:
            name_to_table_id[t_name] = t_id
        for f_id, f_info in t_info.get("fields", {}).items():
            slug = f_info.get("slug")
            if slug:
                field_slug_to_name[slug] = f_info.get("name")

    # Determine filter lists
    if args.workflow_status is not None:
        workflow_values = [] if args.workflow_status.lower() in ["none", ""] else [s.strip() for s in args.workflow_status.split(",") if s.strip()]
    else:
        workflow_values = FILTER_WORKFLOW_STATUS_VALUES

    if args.curation_decision is not None:
        curation_values = [] if args.curation_decision.lower() in ["none", ""] else [s.strip() for s in args.curation_decision.split(",") if s.strip()]
    else:
        curation_values = FILTER_CURATION_DECISION_VALUES

    operator = args.operator

    # Target specific case IDs if specified (normalized as strings)
    target_case_ids = None
    if args.case_id:
        target_case_ids = {str(args.case_id).strip()}
    elif args.case_ids:
        target_case_ids = {str(x).strip() for x in args.case_ids.split(",") if x.strip()}

    all_tables_data = {}
    
    if args.records_cache and Path(args.records_cache).exists():
        print(f"Loading table records from cache: {args.records_cache}...")
        with open(args.records_cache, "r", encoding="utf-8") as f:
            raw_cache = json.load(f)
            all_tables_data = {
                t_id: {str(r_id): r_flds for r_id, r_flds in recs.items()}
                for t_id, recs in raw_cache.items()
            }
    else:
        if not NOCODB_API_TOKEN:
            print("Error: NOCODB_API_TOKEN (or NC_TOKEN) must be provided.")
            print("Set in .env or provide via environment variable.")
            sys.exit(1)

        client = NocoDBClient(NOCODB_URL, NOCODB_BASE_ID, NOCODB_API_TOKEN)
        print(f"Fetching records from NocoDB base {NOCODB_BASE_ID}...")

        for table_name in TABLE_CONFIG.keys():
            t_id = name_to_table_id.get(table_name)
            if not t_id:
                print(f"  Warning: Table '{table_name}' not found in schema map.")
                continue

            print(f"  Fetching {table_name} ({t_id})...")
            records = client.get_table_records(t_id)
            all_tables_data[t_id] = {}
            for r in records:
                r_id = r.get("id") or r.get("id_fields", {}).get("Id") or r.get("Id")
                r_fields = r.get("fields") or r
                all_tables_data[t_id][str(r_id)] = r_fields

    # Generate slugs and permalinks (namespaced by table ID)
    case_table_id = name_to_table_id.get("Cases")
    id_to_slug = {}
    id_to_perm = {}
    used_slugs_by_table = {t_id: set() for t_id in all_tables_data.keys()}

    for t_id, records in all_tables_data.items():
        t_name = schema_map.get(t_id, {}).get("name", "generic")
        for rec_id_str, fields in records.items():
            title = get_record_title(fields, t_id, schema_map, rec_id_str)
            perm_id = get_record_permalink_id(t_name, fields, rec_id_str)
            id_to_perm[(t_id, rec_id_str)] = perm_id

            base_slug = slugify(title)
            if not base_slug:
                base_slug = perm_id

            slug = base_slug
            counter = 1
            while slug in used_slugs_by_table[t_id]:
                slug = f"{base_slug}-{counter}"
                counter += 1
            used_slugs_by_table[t_id].add(slug)
            id_to_slug[(t_id, rec_id_str)] = slug

    # Filter active cases
    active_case_ids = set()
    if case_table_id and case_table_id in all_tables_data:
        for rec_id_str, fields in all_tables_data[case_table_id].items():
            # If target_case_ids specified, filter strictly to them
            if target_case_ids is not None:
                if rec_id_str in target_case_ids:
                    active_case_ids.add(rec_id_str)
                continue

            # Workflow status check
            workflow_match = True
            if workflow_values:
                status = fields.get(FILTER_WORKFLOW_STATUS_FIELD)
                status_list = status if isinstance(status, list) else ([status] if status else [])
                workflow_match = any(s in workflow_values for s in status_list)

            # Curation decision check
            curation_match = True
            if curation_values:
                curation = fields.get(FILTER_CURATION_DECISION_FIELD)
                curation_list = curation if isinstance(curation, list) else ([curation] if curation else [])
                curation_match = any(s in curation_values for s in curation_list)

            if workflow_values and curation_values:
                keep = (workflow_match and curation_match) if operator == "AND" else (workflow_match or curation_match)
            elif workflow_values:
                keep = workflow_match
            elif curation_values:
                keep = curation_match
            else:
                keep = True

            if keep:
                active_case_ids.add(rec_id_str)

    print(f"Identified {len(active_case_ids)} active case(s) to sync.")

    # Expand referenced non-case records using (table_id, record_id) tuples
    referenced_records = set((case_table_id, c_id) for c_id in active_case_ids)
    to_expand = list(referenced_records)

    while to_expand:
        curr_t_id, curr_rec_id = to_expand.pop()
        curr_fields = all_tables_data.get(curr_t_id, {}).get(curr_rec_id)
        if not curr_fields:
            continue

        curr_t_info = schema_map.get(curr_t_id, {})
        curr_t_name = curr_t_info.get("name", "")
        table_fields = curr_t_info.get("fields", {})

        clean_name_to_finfo = {}
        for f_id, f_info in table_fields.items():
            cname = f_info.get("name", "").strip().lower().replace("\ufeff", "")
            clean_name_to_finfo[cname] = f_info

        for f_name, f_val in curr_fields.items():
            if not isinstance(f_val, list):
                continue

            cname = f_name.strip().lower().replace("\ufeff", "")
            f_info = clean_name_to_finfo.get(cname)
            if not f_info or not f_info.get("sync"):
                continue

            f_type = f_info.get("type", "")
            if f_type not in ["LinkToAnotherRecord", "multipleRecordLinks", "Links"]:
                continue

            target_t_id = get_link_target_table_id(
                curr_t_name, f_name, f_info.get("slug", ""), f_info, name_to_table_id
            )
            if not target_t_id or target_t_id not in all_tables_data:
                continue

            for item in f_val:
                raw_target_id = (item.get("id") or item.get("Id")) if isinstance(item, dict) else item
                if raw_target_id is None:
                    continue
                target_id_str = str(raw_target_id)

                if (target_t_id, target_id_str) not in referenced_records:
                    # Don't expand into cases that are inactive
                    if target_t_id == case_table_id:
                        if target_id_str in active_case_ids:
                            referenced_records.add((target_t_id, target_id_str))
                    else:
                        referenced_records.add((target_t_id, target_id_str))
                        to_expand.append((target_t_id, target_id_str))

    # Process and write files
    total_written = 0
    for table_name, config in TABLE_CONFIG.items():
        t_id = name_to_table_id.get(table_name)
        if not t_id or t_id not in all_tables_data:
            continue

        config["dir"].mkdir(parents=True, exist_ok=True)
        
        # When doing full sync (or if --clean), remove old files in the collection directory
        if target_case_ids is None or args.clean:
            for f in config["dir"].glob("*.md"):
                f.unlink()

        table_records_to_sync = [
            (rec_id_str, fields) for rec_id_str, fields in all_tables_data[t_id].items()
            if (t_id, rec_id_str) in referenced_records
        ]

        if not table_records_to_sync:
            continue

        print(f"\nProcessing {table_name} ({len(table_records_to_sync)} records)...")

        sync_count = 0
        for idx, (rec_id_str, fields) in enumerate(table_records_to_sync, start=1):
            perm_id = id_to_perm.get((t_id, rec_id_str)) or get_record_permalink_id(table_name, fields, rec_id_str)
            title = get_record_title(fields, t_id, schema_map, rec_id_str)
            slug = id_to_slug.get((t_id, rec_id_str)) or slugify(title)

            if table_name == "Cases":
                print(f"  [{idx}/{len(table_records_to_sync)}] {title}")

            final_data = resolve_record_fields(
                fields, t_id, schema_map, perm_id, id_to_slug, referenced_records, name_to_table_id, r2_client=r2_client
            )

            layout = config["layout"]
            redirects = [f"/c/{perm_id}/"] if table_name == "Cases" else None
            if table_name == "Cases":
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

            case_desc = derive_case_description(final_data) if table_name == "Cases" else None

            front_matter = {
                "layout": layout,
                "title": title,
                "airtable_id": perm_id,
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
            fm_yaml = yaml.dump(front_matter, sort_keys=False)
            annotated_content = annotate_yaml(fm_yaml, field_slug_to_name)

            file_path.write_text(f"---\n{annotated_content}\n---\n", encoding="utf-8")
            sync_count += 1
            total_written += 1

        print(f"  Completed {sync_count} records for {table_name}.")

    print(f"\nSync complete!")
    print(f"  Markdown files written: {total_written}")
    if GLOBAL_STATS.get("uploaded", 0) > 0 or GLOBAL_STATS.get("downloaded", 0) > 0 or GLOBAL_STATS.get("cached", 0) > 0:
        if r2_client:
            print(f"  Cloudflare R2: {GLOBAL_STATS.get('uploaded', 0)} uploaded, {GLOBAL_STATS.get('cached', 0)} already in R2.")
        else:
            print(f"  Attachments (Local): {GLOBAL_STATS.get('downloaded', 0)} downloaded, {GLOBAL_STATS.get('cached', 0)} already cached.")

    # Run case aggregation compilation
    try:
        from generate_cases_json import aggregate
        print("\nCompiling aggregated cases JSON...")
        aggregate()
        print("Aggregation complete.")
    except Exception as e:
        print(f"Warning: generate_cases_json aggregation failed: {e}")

if __name__ == "__main__":
    main()
