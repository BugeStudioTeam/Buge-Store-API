import yaml
import requests
import sys
from pathlib import Path

def check_url(url):
    if not url:
        return False, "Empty URL"
    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        return response.status_code == 200, f"HTTP {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Connection error"
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def main():
    apps_dir = Path('apps')
    if not apps_dir.exists():
        print("No apps directory found.")
        sys.exit(0)
    
    yaml_files = list(apps_dir.rglob('*.yml')) + list(apps_dir.rglob('*.yaml'))
    if not yaml_files:
        print("No YAML files found.")
        sys.exit(0)
    
    errors = []
    warnings = []
    
    for yaml_file in yaml_files:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        versions = data.get('versions', [])
        for idx, version in enumerate(versions):
            apk = version.get('apk', {})
            primary_url = apk.get('primary_url', '')
            mirror_url = apk.get('mirror_url', '')
            
            if not primary_url and not mirror_url:
                errors.append(f"{yaml_file}: No download URL provided for version {idx + 1}")
                continue
            
            if primary_url:
                print(f"Checking: {primary_url}")
                ok, msg = check_url(primary_url)
                if ok:
                    print(f"  OK")
                else:
                    warnings.append(f"{yaml_file}: Primary URL not accessible - {msg}")
                    print(f"  FAILED: {msg}")
            
            if mirror_url:
                print(f"Checking mirror: {mirror_url}")
                ok, msg = check_url(mirror_url)
                if ok:
                    print(f"  OK")
                else:
                    warnings.append(f"{yaml_file}: Mirror URL not accessible - {msg}")
                    print(f"  FAILED: {msg}")
    
    if errors:
        print("\nURL check failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    if warnings:
        print("\nURL warnings (non-blocking):")
        for warning in warnings:
            print(f"  - {warning}")
        sys.exit(0)
    else:
        print("\nAll APK URLs are accessible.")
        sys.exit(0)

if __name__ == "__main__":
    main()