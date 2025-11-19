"""
Unit tests for get_category_id function.
Tests category ID lookup by name.
"""

import unittest
import importlib.util
import sys
import types
from pathlib import Path
from unittest.mock import Mock, patch

# Provide dummy modules for external dependencies
for name in ['googleAuth', 'gemini']:
    if name not in sys.modules:
        sys.modules[name] = types.ModuleType(name)

if 'dotenv' not in sys.modules:
    dotenv_mod = types.ModuleType('dotenv')
    setattr(dotenv_mod, 'load_dotenv', lambda *args, **kwargs: None)
    sys.modules['dotenv'] = dotenv_mod

if 'tqdm' not in sys.modules:
    tqdm_mod = types.ModuleType('tqdm')
    setattr(tqdm_mod, 'tqdm', lambda *args, **kwargs: (x for x in args[0]) if args else [])
    setattr(tqdm_mod, 'write', lambda *args, **kwargs: None)
    sys.modules['tqdm'] = tqdm_mod

if 'requests' not in sys.modules:
    class RequestException(Exception):
        pass
    requests_mod = types.ModuleType('requests')
    requests_mod.RequestException = RequestException
    sys.modules['requests'] = requests_mod

MODULE_PATH = Path(__file__).resolve().parents[1] / 'snipe-IT.py'
spec = importlib.util.spec_from_file_location('snipe_it', MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

get_category_id = module.get_category_id


class TestGetCategoryId(unittest.TestCase):
    """Tests for category ID lookup."""

    @patch('snipe_it.retry_request')
    def test_get_category_id_success(self, mock_retry):
        """Test retrieving category ID."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'rows': [{'id': 5, 'name': 'Laptops'}]
        }
        mock_retry.return_value = mock_response

        result = get_category_id('Laptops', 'test-key')

        self.assertEqual(result, 5)

    @patch('snipe_it.retry_request')
    def test_get_category_id_not_found(self, mock_retry):
        """Test when category is not found."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'rows': []}
        mock_retry.return_value = mock_response

        result = get_category_id('Nonexistent', 'test-key')

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
