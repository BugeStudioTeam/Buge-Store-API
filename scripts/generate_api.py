name: Index Builder

on:
  push:
    branches:
      - main
    paths:
      - 'apps/**/*.yml'
      - 'apps/**/*.yaml'
  workflow_dispatch:

concurrency:
  group: index-builder
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pyyaml requests

      - name: Generate API JSON
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/generate_api.py

      - name: Commit and push
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "chore: update API index [skip ci]"
          file_pattern: "api/v1/*.json"
          commit_user_name: "github-actions[bot]"
          commit_user_email: "github-actions[bot]@users.noreply.github.com"            
            if not data:
                continue
            
            package = data.get('package_name', 'unknown')
            latest_version = data.get('versions', [{}])[0] if data.get('versions') else {}
            apk = latest_version.get('apk', {})
            
            real_downloads = None
            source_code = data.get('source_code', '')
            if source_code:
                real_downloads = get_real_downloads(source_code, github_token)
            
            app_entry = {
                'package': package,
                'name': data.get('app_name', 'Unknown'),
                'icon': f"https://raw.githubusercontent.com/BugeStudioTeam/Buge-Store-API/main/apps/{package}/metadata/icon.webp",
                'banner': f"https://raw.githubusercontent.com/BugeStudioTeam/Buge-Store-API/main/apps/{package}/metadata/banner.webp",
                'categories': data.get('categories', []),
                'latest_version': latest_version.get('version_name', '0.0.0'),
                'download_url': apk.get('primary_url', ''),
                'size_mb': apk.get('file_size_mb', 0),
                'signature': data.get('signature_fingerprint', ''),
                'min_sdk': data.get('min_sdk', 0),
                'target_sdk': data.get('target_sdk', 0),
                'developer': data.get('developer', 'Unknown'),
                'changelog': latest_version.get('changelog', ''),
                'short_description': data.get('short_description', ''),
                'description': data.get('description', ''),
                'featured': data.get('featured', False),
                'rating': data.get('rating', 0),
                'rating_count': data.get('rating_count', 0),
                'website': data.get('website', ''),
                'source_code': source_code,
                'release_date': latest_version.get('release_date', ''),
                'downloads': real_downloads if real_downloads is not None else data.get('downloads', 0),
                'architectures': data.get('architectures', [])
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
    sorted_apps = sorted(
        apps,
        key=lambda x: (x.get('rating', 0) * 10 + x.get('downloads', 0)),
        reverse=True
    )
    trending = [
        {
            'package': app['package'],
            'name': app['name'],
            'downloads': app.get('downloads', 0),
            'rating': app.get('rating', 0),
            'trend_score': app.get('rating', 0) * 10 + app.get('downloads', 0)
        }
        for app in sorted_apps[:10]
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
    
    github_token = os.environ.get('GITHUB_TOKEN', None)
    
    apps = load_app_configs(apps_dir, github_token)
    
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
