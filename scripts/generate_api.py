import os
import yaml
import json
from pathlib import Path
from datetime import datetime

def load_app_configs(apps_dir):
    apps = []
    yaml_files = list(apps_dir.rglob('*.yml')) + list(apps_dir.rglob('*.yaml'))
    
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if not data:
                continue
            
            package = data.get('package_name', 'unknown')
            latest_version = data.get('versions', [{}])[0] if data.get('versions') else {}
            apk = latest_version.get('apk', {})
            
            app_entry = {
                'package': package,
                'name': data.get('app_name', 'Unknown'),
                'icon': f"https://raw.githubusercontent.com/BugeStudioTeam/Buge-Store-API/main/apps/{package}/metadata/icon.webp",
                'categories': data.get('categories', []),
                'latest_version': latest_version.get('version_name', '0.0.0'),
                'download_url': apk.get('primary_url', ''),
                'size_mb': apk.get('file_size_mb', 0),
                'signature': data.get('signature_fingerprint', ''),
                'min_sdk': data.get('min_sdk', 0),
                'developer': data.get('developer', 'Unknown')
            }
            apps.append(app_entry)
            
        except Exception as e:
            print(f"Error parsing {yaml_file}: {e}")
    
    return apps

def generate_apps_json(apps):
    return {
        'version': 1,
        'last_updated': datetime.utcnow().isoformat() + 'Z',
        'total_apps': len(apps),
        'apps': apps
    }

def generate_categories_json(apps):
    categories_map = {}
    for app in apps:
        for cat in app.get('categories', []):
            if cat not in categories_map:
                categories_map[cat] = {'count': 0, 'apps': []}
            categories_map[cat]['count'] += 1
            categories_map[cat]['apps'].append(app['package'])
    
    categories = [
        {'name': name, 'count': info['count'], 'apps': info['apps']}
        for name, info in categories_map.items()
    ]
    categories.sort(key=lambda x: x['count'], reverse=True)
    
    return {'categories': categories}

def generate_trending_json(apps):
    trending = [
        {
            'package': app['package'],
            'name': app['name'],
            'downloads': 0,
            'trend_score': 0
        }
        for app in apps
    ]
    
    return {
        'last_updated': datetime.utcnow().isoformat() + 'Z',
        'trending': trending
    }

def main():
    apps_dir = Path('apps')
    api_dir = Path('api/v1')
    
    if not apps_dir.exists():
        print("No apps directory found. Nothing to generate.")
        return
    
    api_dir.mkdir(parents=True, exist_ok=True)
    
    apps = load_app_configs(apps_dir)
    
    if not apps:
        print("No valid applications found.")
        return
    
    with open(api_dir / 'apps.json', 'w', encoding='utf-8') as f:
        json.dump(generate_apps_json(apps), f, indent=2, ensure_ascii=False)
    
    with open(api_dir / 'categories.json', 'w', encoding='utf-8') as f:
        json.dump(generate_categories_json(apps), f, indent=2, ensure_ascii=False)
    
    with open(api_dir / 'trending.json', 'w', encoding='utf-8') as f:
        json.dump(generate_trending_json(apps), f, indent=2, ensure_ascii=False)
    
    print(f"Generated API files for {len(apps)} apps:")
    print(f"  - {api_dir / 'apps.json'}")
    print(f"  - {api_dir / 'categories.json'}")
    print(f"  - {api_dir / 'trending.json'}")

if __name__ == "__main__":
    main()