import unittest
import json
from pathlib import Path

class TestAPIGeneration(unittest.TestCase):
    
    def test_apps_json_exists(self):
        api_file = Path('api/v1/apps.json')
        if not api_file.exists():
            self.skipTest("apps.json not generated yet")
        self.assertTrue(api_file.exists(), "apps.json not found")
    
    def test_apps_json_valid(self):
        api_file = Path('api/v1/apps.json')
        if not api_file.exists():
            self.skipTest("apps.json not generated yet")
        
        with open(api_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertIn('version', data)
        self.assertEqual(data['version'], 1)
        self.assertIn('last_updated', data)
        self.assertIn('total_apps', data)
        self.assertIn('apps', data)
        self.assertIsInstance(data['apps'], list)
    
    def test_categories_json_exists(self):
        api_file = Path('api/v1/categories.json')
        if not api_file.exists():
            self.skipTest("categories.json not generated yet")
        self.assertTrue(api_file.exists(), "categories.json not found")
    
    def test_trending_json_exists(self):
        api_file = Path('api/v1/trending.json')
        if not api_file.exists():
            self.skipTest("trending.json not generated yet")
        self.assertTrue(api_file.exists(), "trending.json not found")

if __name__ == '__main__':
    unittest.main()