"""
Unit tests for hardware_exists function.
Tests checking if hardware assets already exist in Snipe-IT.
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

hardware_exists = module.hardware_exists


class TestHardwareExists(unittest.TestCase):
    """Tests for hardware existence check."""

    @patch('snipe_it.retry_request')
    def test_hardware_exists_by_asset_tag(self, mock_retry):
        """Test detecting existing hardware by asset tag."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'rows': [{'asset_tag': 'TAG001', 'serial': 'SN001'}]
        }
        mock_retry.return_value = mock_response

        result = hardware_exists('TAG001', 'SN001', 'test-key')

        self.assertTrue(result)

    @patch('snipe_it.retry_request')
    def test_hardware_exists_by_serial(self, mock_retry):
        """Test detecting existing hardware by serial number."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'rows': [{'asset_tag': 'TAG001', 'serial': 'SN001'}]
        }
        mock_retry.return_value = mock_response

        result = hardware_exists('TAG002', 'SN001', 'test-key')

        self.assertTrue(result)

    @patch('snipe_it.retry_request')
    def test_hardware_does_not_exist(self, mock_retry):
        """Test when hardware doesn't exist."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'rows': []}
        mock_retry.return_value = mock_response

        result = hardware_exists('TAG001', 'SN001', 'test-key')

        self.assertFalse(result)

    @patch('snipe_it.retry_request')
    def test_hardware_exists_api_error(self, mock_retry):
        """Test API error response."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_retry.return_value = mock_response

        result = hardware_exists('TAG001', 'SN001', 'test-key')

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
