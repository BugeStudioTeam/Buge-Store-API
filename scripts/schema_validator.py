import os
import yaml
import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("jsonschema not installed. Run: pip install jsonschema")
    sys.exit(1)

def load_schema():
    schema_path = Path('schemas/app-config-schema.json')
    if not schema_path.exists():
        print("Schema file not found.")
        return None
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    schema = load_schema()
    if not schema:
        sys.exit(1)
    
    apps_dir = Path('apps')
    if not apps_dir.exists():
        print("No apps directory found.")
        sys.exit(0)
    
    yaml_files = list(apps_dir.rglob('*.yml')) + list(apps_dir.rglob('*.yaml'))
    if not yaml_files:
        print("No YAML files found.")
        sys.exit(0)
    
    errors = []
    
    for yaml_file in yaml_files:
        print(f"Validating schema: {yaml_file}")
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            jsonschema.validate(data, schema)
            print(f"  Valid")
            
        except jsonschema.ValidationError as e:
            errors.append(f"{yaml_file}: Schema validation failed - {e.message}")
            print(f"  FAILED: {e.message}")
        except Exception as e:
            errors.append(f"{yaml_file}: Unexpected error - {str(e)}")
    
    if errors:
        print("\nSchema validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("\nAll YAML files match the schema.")
        sys.exit(0)

if __name__ == "__main__":
    main()