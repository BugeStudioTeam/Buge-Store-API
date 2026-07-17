import unittest
import yaml
from pathlib import Path

class TestValidator(unittest.TestCase):
    
    def test_yaml_syntax_all_files(self):
        apps_dir = Path('apps')
        if not apps_dir.exists():
            self.skipTest("No apps directory found")
        
        yaml_files = list(apps_dir.rglob('*.yml')) + list(apps_dir.rglob('*.yaml'))
        if not yaml_files:
            self.skipTest("No YAML files found")
        
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    yaml.safe_load(f)
            except yaml.YAMLError as e:
                self.fail(f"YAML syntax error in {yaml_file}: {e}")
    
    def test_required_fields_all_files(self):
        apps_dir = Path('apps')
        if not apps_dir.exists():
            self.skipTest("No apps directory found")
        
        yaml_files = list(apps_dir.rglob('*.yml')) + list(apps_dir.rglob('*.yaml'))
        if not yaml_files:
            self.skipTest("No YAML files found")
        
        required = ['package_name', 'app_name', 'developer', 'versions', 'signature_fingerprint']
        
        for yaml_file in yaml_files:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            for field in required:
                self.assertIn(field, data, f"{yaml_file} missing '{field}'")
    
    def test_package_name_format(self):
        apps_dir = Path('apps')
        if not apps_dir.exists():
            self.skipTest("No apps directory found")
        
        yaml_files = list(apps_dir.rglob('*.yml')) + list(apps_dir.rglob('*.yaml'))
        if not yaml_files:
            self.skipTest("No YAML files found")
        
        import re
        pattern = r'^[a-z][a-z0-9_]*(\\.[a-z][a-z0-9_]*)+$'
        
        for yaml_file in yaml_files:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            package = data.get('package_name', '')
            self.assertTrue(re.match(pattern, package), 
                          f"{yaml_file}: package_name '{package}' does not follow Java naming conventions")

if __name__ == '__main__':
    unittest.main()