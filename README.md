# Buge-Store-API

Buge Store API - A lightweight open-source app store index that stores YAML configurations only, with APK files distributed via GitHub Releases. Features automated PR validation, 30-second merge workflow, and unified API endpoints for both Android clients and web interfaces. Built for speed, transparency, and community contributions.

## Features

- YAML-only configuration storage
- Automated PR validation and merge within 30 seconds
- Unified API for Android and web clients
- Community-driven application catalog
- GitHub Releases based APK distribution

## Repository Structure

```
BugeStore-API/
├── .github/workflows/     # GitHub Actions automation
├── apps/                  # Application YAML configurations
├── api/v1/               # Generated JSON APIs
├── scripts/              # Validation and generation scripts
├── schemas/              # JSON Schema specifications
├── templates/            # Configuration templates
└── tests/                # Unit and integration tests
```

## Quick Start

### For Android Users

Request the API endpoint to get the application list:

```
https://raw.githubusercontent.com/BugeStudioTeam/Buge-Store-API/main/api/v1/apps.json
```

### For Developers

1. Fork this repository
2. Add your application YAML in `apps/` directory
3. Submit a Pull Request
4. Automated validation will merge within 30 seconds

## API Endpoints

All API endpoints are available at:

```
https://raw.githubusercontent.com/BugeStudioTeam/Buge-Store-API/main/api/v1/
```

| Endpoint | Description |
|----------|-------------|
| `apps.json` | Full application list with metadata |
| `categories.json` | Category grouping with app counts |
| `trending.json` | Trending applications list |

### Response Format

```
{
  "version": 1,
  "last_updated": "2026-07-18T10:00:00Z",
  "total_apps": 2,
  "apps": [
    {
      "package": "com.example.package",
      "name": "Example App",
      "icon": "https://raw.githubusercontent.com/BugeStudioTeam/Buge-Store-API/main/apps/com.example.package/metadata/icon.webp",
      "banner": "https://raw.githubusercontent.com/BugeStudioTeam/Buge-Store-API/main/apps/com.example.package/metadata/banner.webp",
      "categories": ["Tools", "Utilities"],
      "latest_version": "1.0.0",
      "download_url": "https://github.com/example/repo/releases/download/v1.0.0/app.apk",
      "size_mb": 5.2,
      "signature": "AB:CD:EF:12:34:56:78:90:AB:CD:EF:12:34:56:78:90",
      "min_sdk": 21,
      "target_sdk": 34,
      "developer": "Example Developer",
      "short_description": "A brief description for list view",
      "description": "A full detailed description for the app detail page. Supports multiple lines.",
      "featured": false,
      "rating": 0.0,
      "rating_count": 0,
      "website": "https://example.com",
      "source_code": "https://github.com/example/repo",
      "release_date": "2026-07-17",
      "downloads": 0,
      "architectures": ["arm64-v8a", "armeabi-v7a"]
    }
  ]
}
```

## Adding an Application

### Step 1: Create Application Directory

```
apps/com.example.package/
```

### Step 2: Create YAML Configuration

Copy the template from `templates/app-template.yml` and fill in your application details.

```
package_name: com.example.package
app_name: Example App
developer: Example Developer
website: https://example.com
source_code: https://github.com/example/repo
short_description: "A brief description for list view"
description: |
  A full detailed description for the app detail page.
  Supports multiple lines.

featured: false
rating: 0.0
rating_count: 0
downloads: 0

versions:
  - version_code: 20260717
    version_name: "1.0.0"
    release_date: "2026-07-17"
    changelog: |
      - Initial release
    apk:
      primary_url: https://github.com/example/repo/releases/download/v1.0.0/app.apk
      mirror_url: https://ghproxy.net/https://github.com/example/repo/releases/download/v1.0.0/app.apk
      sha256_hash: a4f5c8d9e2b1c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8
      file_size_mb: 5.2

signature_fingerprint: "AB:CD:EF:12:34:56:78:90:AB:CD:EF:12:34:56:78:90"

min_sdk: 21
target_sdk: 34
architectures:
  - arm64-v8a

categories:
  - Tools
```

### Step 3: Add Metadata

Place your application icon and banner in the metadata directory:

```
apps/com.example.package/metadata/icon.webp
apps/com.example.package/metadata/banner.webp
```

### Step 4: Submit Pull Request

Create a pull request with your changes. The automated system will:

1. Validate YAML syntax
2. Check signature fingerprint format
3. Verify APK URLs are accessible
4. Scan for dangerous permissions
5. Validate against JSON Schema
6. Merge automatically if all checks pass

## Guidelines

### Package Name

- Must be unique
- Must follow Java package naming conventions
- Should match the actual APK package name

### APK Hosting

- APK files should be hosted on GitHub Releases
- Recommended format: `https://github.com/owner/repo/releases/download/tag/app.apk`
- Ensure the URL is accessible without authentication

### Signature Fingerprint

- Generate using: `keytool -list -v -keystore your.keystore`
- Must be in SHA-1 format: `AB:CD:EF:12:34:56:78:90:AB:CD:EF:12:34:56:78:90:AB:CD:EF:12`

### Categories

Choose from existing categories or suggest new ones:

- Tools
- Utilities
- Communication
- Entertainment
- Productivity
- Education
- Games

## Automation Workflows

### PR Validator

Triggered on pull requests that modify YAML files in `apps/`. Runs syntax checks, security scans, URL validation, and schema validation.

### Index Builder

Triggered on pushes to the `main` branch. Generates JSON API files from all YAML configurations and commits them to `api/v1/`.

## Development

### Prerequisites

- Python 3.11 or higher
- pip

### Install Dependencies

```
pip install pyyaml jsonschema requests
```

### Run Tests

```
python -m unittest discover tests/
```

### Manual API Generation

```
python scripts/generate_api.py
```

## Contributing

Please read the contribution guidelines before submitting pull requests.

## License

This project is licensed under the MIT License.