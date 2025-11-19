"""
Unit tests for get_user_id function.
Tests user ID lookup by email address.
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

get_user_id = module.get_user_id


class TestGetUserId(unittest.TestCase):
    """Tests for user ID lookup by email."""

    @patch('snipe_it.retry_request')
    def test_get_user_id_success(self, mock_retry):
        """Test retrieving user ID by email."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'rows': [{'id': 10, 'email': 'user@example.com'}]
        }
        mock_retry.return_value = mock_response

        result = get_user_id('user@example.com', 'test-key')

        self.assertEqual(result, 10)

    @patch('snipe_it.retry_request')
    def test_get_user_id_not_found(self, mock_retry):
        """Test when user is not found."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'rows': []}
        mock_retry.return_value = mock_response

        result = get_user_id('nonexistent@example.com', 'test-key')

        self.assertIsNone(result)

    @patch('snipe_it.retry_request')
    def test_get_user_id_api_error(self, mock_retry):
        """Test API error handling."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = 'Server error'
        mock_retry.return_value = mock_response

        result = get_user_id('user@example.com', 'test-key')

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
