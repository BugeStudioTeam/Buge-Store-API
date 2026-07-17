# Contributing to Buge Store API

Thank you for your interest in contributing to Buge Store API. This document outlines the process for adding applications and making changes.

## Adding an Application

### Step 1: Create Application Directory

Create a directory under `apps/` using your application's package name:

```
apps/com.yourcompany.yourapp/
```

### Step 2: Create YAML Configuration

Copy the template from `templates/app-template.yml` and fill in your application details.

Key fields:

- `package_name`: Unique package name
- `app_name`: Display name
- `developer`: Your name or organization
- `versions`: List of releases
- `signature_fingerprint`: APK signing certificate SHA-1

### Step 3: Add Metadata

Place your application icon and banner in the metadata directory:

```
apps/com.yourcompany.yourapp/metadata/icon.webp
apps/com.yourcompany.yourapp/metadata/banner.webp
```

### Step 4: Submit Pull Request

Create a pull request with your changes. Our automated system will:

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

## Code of Conduct

Be respectful and constructive in all interactions. This is a community-driven project, and we value collaboration.

## Questions

Open an issue or contact the maintainers.