import yaml
import sys
import re
from pathlib import Path

DANGEROUS_PERMISSIONS = [
    'android.permission.READ_SMS',
    'android.permission.SEND_SMS',
    'android.permission.RECEIVE_SMS',
    'android.permission.READ_CONTACTS',
    'android.permission.WRITE_CONTACTS',
    'android.permission.ACCESS_FINE_LOCATION',
    'android.permission.ACCESS_COARSE_LOCATION',
    'android.permission.CAMERA',
    'android.permission.RECORD_AUDIO',
    'android.permission.READ_EXTERNAL_STORAGE',
    'android.permission.WRITE_EXTERNAL_STORAGE',
    'android.permission.READ_PHONE_STATE',
    'android.permission.PROCESS_OUTGOING_CALLS',
    'android.permission.SYSTEM_ALERT_WINDOW',
    'android.permission.REQUEST_INSTALL_PACKAGES',
]

SUSPICIOUS_KEYWORDS = [
    'obfuscated',
    'encrypted',
    'remote_control',
    'background_service',
    'accessibility_service',
    'device_admin',
    'overlay_permission',
]

def check_permissions_in_yaml(content):
    found = []
    for perm in DANGEROUS_PERMISSIONS:
        if perm in content:
            found.append(perm)
    return found

def check_suspicious_keywords(content):
    found = []
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword.lower() in content.lower():
            found.append(keyword)
    return found

def main():
    apps_dir = Path('apps')
    if not apps_dir.exists():
        print("No apps directory found.")
        sys.exit(0)
    
    yaml_files = list(apps_dir.rglob('*.yml')) + list(apps_dir.rglob('*.yaml'))
    if not yaml_files:
        print("No YAML files found.")
        sys.exit(0)
    
    warnings = []
    
    for yaml_file in yaml_files:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        dangerous = check_permissions_in_yaml(content)
        suspicious = check_suspicious_keywords(content)
        
        if dangerous:
            warnings.append(f"{yaml_file}: Uses dangerous permissions - {', '.join(dangerous)}")
        if suspicious:
            warnings.append(f"{yaml_file}: Contains suspicious keywords - {', '.join(suspicious)}")
    
    if warnings:
        print("\nSecurity warnings (non-blocking):")
        for warning in warnings:
            print(f"  - {warning}")
        print("\nThese warnings are for informational purposes only.")
        sys.exit(0)
    else:
        print("\nNo security issues found.")
        sys.exit(0)

if __name__ == "__main__":
    main()