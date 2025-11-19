"""
Unit tests for get_model_id function.
Tests model ID lookup by name.
"""

import unittest
import importlib.util
import sys
import types
from pathlib import Path
from unittest.mock import Mock, patch

# Provide dummy modules for external dependencies so snipe-IT.py can be imported
for name in ['googleAuth', 'gemini']:
    if name not in sys.modules:
        sys.modules[name] = types.ModuleType(name)

# Dummy dotenv with load_dotenv function
if 'dotenv' not in sys.modules:
    dotenv_mod = types.ModuleType('dotenv')
    setattr(dotenv_mod, 'load_dotenv', lambda *args, **kwargs: None)
    sys.modules['dotenv'] = dotenv_mod

# Dummy tqdm - module-level functions
if 'tqdm' not in sys.modules:
    tqdm_mod = types.ModuleType('tqdm')
    setattr(tqdm_mod, 'tqdm', lambda *args, **kwargs: (x for x in args[0]) if args else [])
    setattr(tqdm_mod, 'write', lambda *args, **kwargs: None)
    sys.modules['tqdm'] = tqdm_mod

# Mock requests module with proper RequestException
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

get_model_id = module.get_model_id


class TestGetModelId(unittest.TestCase):
    """Tests for model ID lookup."""

    @patch('snipe_it.retry_request')
    def test_get_model_id_exact_match(self, mock_retry):
        """Test retrieving model ID with exact name match."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'rows': [{'id': 42, 'name': 'Dell Latitude 7420'}]
        }
        mock_retry.return_value = mock_response

        result = get_model_id('Dell Latitude 7420', 'test-key')

        self.assertEqual(result, 42)

    @patch('snipe_it.retry_request')
    def test_get_model_id_case_insensitive(self, mock_retry):
        """Test case-insensitive model name matching."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'rows': [{'id': 42, 'name': 'Dell Latitude 7420'}]
        }
        mock_retry.return_value = mock_response

        result = get_model_id('dell latitude 7420', 'test-key')

        self.assertEqual(result, 42)

    @patch('snipe_it.retry_request')
    def test_get_model_id_fallback_to_first(self, mock_retry):
        """Test fallback to first result when exact match not found."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'rows': [
                {'id': 42, 'name': 'Dell Latitude 7420'},
                {'id': 43, 'name': 'Dell Latitude 7430'}
            ]
        }
        mock_retry.return_value = mock_response

        result = get_model_id('Different Model', 'test-key')

        self.assertEqual(result, 42)

    @patch('snipe_it.retry_request')
    def test_get_model_id_not_found(self, mock_retry):
        """Test when model is not found."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'rows': []}
        mock_retry.return_value = mock_response

        result = get_model_id('Nonexistent Model', 'test-key')

        self.assertIsNone(result)

    @patch('snipe_it.retry_request')
    def test_get_model_id_api_error(self, mock_retry):
        """Test handling API errors."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = 'Server error'
        mock_retry.return_value = mock_response

        result = get_model_id('Dell Latitude', 'test-key')

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
