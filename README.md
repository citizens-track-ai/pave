# PAVE (Participatory AI Casebook)

The **Participatory AI Casebook (PAVE)** documents global participatory approaches to artificial intelligence governance, research, and deployment.

- **Live Site**: [https://pavecasebook.org](https://pave.pairs.site)
- **CDN Media**: [https://cdn.pavecasebook.org](https://cdn.pavecasebook.org)

---

## Architecture Overview

The site is built with [Jekyll](https://jekyllrb.com/) and powered by a headless CMS workflow:

```
┌─────────────────────────┐       ┌───────────────────────────┐
│     NocoDB Database     │       │    Cloudflare R2 (CDN)    │
│  (Cases, Orgs, Locs,    │       │  (Uploaded attachments,   │
│   Messages, Resources)  │       │   thumbnails, images)     │
└────────────┬────────────┘       └─────────────▲─────────────┘
             │                                  │
             │ python scripts/sync_nocodb.py    │
             ▼                                  │
┌─────────────────────────┐                     │
│ Jekyll Markdown / Data  │─────────────────────┘
│ (_cases, _organisations,│   (Markdown frontmatter embeds
│  _locations, etc. +     │    direct CDN attachment URLs)
│  cases_aggregated.json) │
└────────────┬────────────┘
             │ bundle exec jekyll build
             ▼
┌─────────────────────────┐
│ Static Site Distribution│
│        (_site/)         │
└─────────────────────────┘
```

1. **Database (NocoDB)**: Stores editorial data for Cases, Organisations, Resources, Participants, Locations, and Messages.
2. **Object Storage (Cloudflare R2)**: Stores all media and attachments under bucket `pave-attachments` and serves them globally via `https://cdn.pavecasebook.org/attachments/...`. This avoids binary bloat in the Git repository.
3. **Static Generation (Jekyll)**: Python sync scripts fetch data from NocoDB, generate markdown files with YAML frontmatter, and compile an aggregated JSON database for the interactive map.

---

## Environment Configuration

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Key variables:

| Variable | Description | Example |
| :--- | :--- | :--- |
| `NOCODB_URL` | Base URL of the NocoDB instance | `https://app.nocodb.com` |
| `NOCODB_BASE_ID` | NocoDB base identifier | `p1t9vvz76dbkcv8` |
| `NC_TOKEN` | NocoDB API token with read/write access | `xc-token ...` |
| `R2_ACCOUNT_ID` | Cloudflare Account ID | *(Cloudflare dashboard)* |
| `R2_ACCESS_KEY_ID` | Cloudflare R2 API token Access Key | *(R2 token)* |
| `R2_SECRET_ACCESS_KEY` | Cloudflare R2 API token Secret Key | *(R2 token)* |
| `R2_BUCKET_NAME` | R2 bucket name | `pave-attachments` |
| `R2_JURISDICTION` | Jurisdiction if bucket was created with EU restrictions | `eu` |
| `R2_PUBLIC_URL` | Custom CDN domain mapping to the bucket | `https://cdn.pavecasebook.org` |
| `R2_PREFIX` | Prefix/folder for assets inside bucket (default: `attachments`) | `attachments` |

---

## How Sync Tasks Work

The synchronization pipeline is managed by scripts in the [`scripts/`](scripts/) directory:

### 1. `scripts/sync_nocodb.py` (Primary Data Sync)

This script pulls records from NocoDB and transforms them into Jekyll collections:

- **Case Selection & Active Filtering**: Filters cases based on curation decisions and workflow status (matches the publishing logic used in editorial review).
- **Relational Expansion**: Discovers and resolves linked records across tables (`Cases` → `Organisations`, `Locations`, `Participants`, `Messages`, `Resources`) ensuring only referenced entities are published.
- **Slug Generation & Universal Transliteration**:
  - Uses `anyascii` to transliterate non-Latin and accented characters (e.g., `Café AI` becomes `cafe-ai`) ensuring clean, valid URL slugs.
  - Automatically writes `redirect_from` aliases in frontmatter for untransliterated and percent-encoded paths (e.g. `/cases/café-ai.html` and `/cases/caf%C3%A9-ai.html`) to prevent broken external links.
- **Deterministic Permalinks**:
  - Preserves legacy Airtable hashed IDs for historical cases (via the `AirTable ID` column).
  - Computes a deterministic MD5 hash (`nc_<record_id>`) for newly created NocoDB cases, generating `/c/<hash>/` shortlinks.
- **Cloudflare R2 Asset Streaming**:
  - Checks if attachments already exist in R2 via cached S3 `HeadObject` checks.
  - Downloads new or modified attachments from NocoDB directly to Cloudflare R2.
  - Rewrites attachment URLs in frontmatter to point directly to `https://cdn.pavecasebook.org/...`.
- **Map Data Compilation**:
  - Automatically triggers `scripts/generate_cases_json.py` to compile `assets/data/cases_aggregated.json` containing geocoded locations, participants, and case metadata used by `map.markdown`.

### 2. `scripts/sync_nocodb_schema.py` (Schema Mapping)

Extracts table metadata and column configurations from the NocoDB base and updates `_data/schema_map.yml`.

- Maps internal NocoDB column titles to YAML-friendly slugs and UI field names.
- Preserves manual overrides (such as field exclusion rules or custom choices).
- Run this whenever columns, select options, or table relations are modified in NocoDB.

### 3. `scripts/update_missing_locations_nocodb.py` (Geocoding)

Scans the NocoDB `Locations` table for records missing geographical coordinates (`latitude`, `longitude`, or `country_code`):

- Queries OpenStreetMap Nominatim for coordinates.
- Recognizes conceptual / non-geographic scopes (e.g. `Global`, `Online`, `Remote`) and skips coordinate assignment.
- Applies standard aliases (e.g. `UK` → `United Kingdom`, `USA` → `United States`).
- Writes the resolved coordinates and country codes back to NocoDB via its REST API.

---

## Sync Usage & CLI Commands

Activate the Python virtual environment:

```bash
source .ve/bin/activate
```

### Full Data Sync

Sync all published cases, linked records, and recompile `assets/data/cases_aggregated.json`:

```bash
python scripts/sync_nocodb.py
```

Clean out orphaned markdown files before syncing:

```bash
python scripts/sync_nocodb.py --clean
```

### Granular Sync (Single or Multiple Cases)

Sync a single case by its NocoDB Record ID:

```bash
python scripts/sync_nocodb.py --case-id 130
```

Sync multiple specific cases:

```bash
python scripts/sync_nocodb.py --case-ids 39,130
```

### Attachment & R2 Flags

Store attachments locally in `assets/attachments/` instead of uploading to R2:

```bash
python scripts/sync_nocodb.py --local-attachments
```

Migrate existing local attachments from `assets/attachments/` to Cloudflare R2:

```bash
python scripts/sync_nocodb.py --upload-existing-attachments
```

Override R2 bucket or custom URL via CLI:

```bash
python scripts/sync_nocodb.py --r2-bucket pave-attachments --r2-public-url https://cdn.pavecasebook.org
```

### Schema & Geocoding Tasks

Update schema map from NocoDB:

```bash
python scripts/sync_nocodb_schema.py
```

Geocode missing locations in NocoDB:

```bash
python scripts/update_missing_locations_nocodb.py
```

---

## Local Development & Jekyll Preview

Ensure Ruby dependencies are installed:

```bash
bundle install
```

Start the local Jekyll development server:

```bash
bundle exec jekyll serve
```

Browse the site locally at `http://localhost:4000`.

To test a full production build:

```bash
bundle exec jekyll build
```

---

## Repository Notes

- **Generated Collections**: Jekyll collection directories (`_cases/`, `_organisations/`, `_locations/`, `_participants/`, `_resources/`, `_messages/`) are generated dynamically by `scripts/sync_nocodb.py`.
- **Local Excludes**: Check `.git/info/exclude` and `.gitignore` if specific generated files or directories are hidden from Git tracking in your local environment.
- **Legacy Airtable Scripts**: `scripts/sync_data.py` and `scripts/sync_schema.py` are preserved for historical reference from the original Airtable implementation.
