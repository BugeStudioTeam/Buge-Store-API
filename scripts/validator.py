import os
import yaml
import sys
from pathlib import Path

def validate_yaml_syntax(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        return True, None
    except yaml.YAMLError as e:
        return False, str(e)

def check_required_fields(data, file_path):
    required = ['package_name', 'app_name', 'developer', 'versions', 'signature_fingerprint']
    missing = [f for f in required if f not in data]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, None

def check_version_fields(data, file_path):
    versions = data.get('versions', [])
    if not versions:
        return False, "No versions defined"
    
    required_version_fields = ['version_code', 'version_name', 'apk']
    for idx, version in enumerate(versions):
        missing = [f for f in required_version_fields if f not in version]
        if missing:
            return False, f"Version {idx + 1} missing: {', '.join(missing)}"
        
        apk = version.get('apk', {})
        if 'primary_url' not in apk:
            return False, f"Version {idx + 1} missing apk.primary_url"
        if 'sha256_hash' not in apk:
            return False, f"Version {idx + 1} missing apk.sha256_hash"
    
    return True, None

def main():
    apps_dir = Path('apps')
    if not apps_dir.exists():
        print("No apps directory found.")
        sys.exit(0)
    
    yaml_files = list(apps_dir.rglob('*.yml')) + list(apps_dir.rglob('*.yaml'))
    if not yaml_files:
        print("No YAML files found in apps/ directory.")
        sys.exit(0)
    
    errors = []
    
    for yaml_file in yaml_files:
        print(f"Validating: {yaml_file}")
        
        valid, error = validate_yaml_syntax(yaml_file)
        if not valid:
            errors.append(f"{yaml_file}: YAML syntax error - {error}")
            continue
        
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            valid, error = check_required_fields(data, yaml_file)
            if not valid:
                errors.append(f"{yaml_file}: {error}")
                continue
            
            valid, error = check_version_fields(data, yaml_file)
            if not valid:
                errors.append(f"{yaml_file}: {error}")
                continue
                
        except Exception as e:
            errors.append(f"{yaml_file}: Unexpected error - {str(e)}")
    
    if errors:
        print("\nValidation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("\nAll YAML files are valid.")
        sys.exit(0)

if __name__ == "__main__":
    main()