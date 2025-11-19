"""
Unit tests for assign_fieldset_to_model function.
Tests assigning fieldsets to hardware models.
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

assign_fieldset_to_model = module.assign_fieldset_to_model


class TestAssignFieldsetToModel(unittest.TestCase):
    """Tests for assigning fieldsets to models."""

    @patch('snipe_it.retry_request')
    def test_assign_fieldset_success(self, mock_retry):
        """Test successfully assigning fieldset to model."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_retry.return_value = mock_response

        # Should not raise an error
        assign_fieldset_to_model(42, 9, 'test-key')

        # Verify the correct endpoint was called
        call_args = mock_retry.call_args
        self.assertIn('/models/42', call_args[0][1])

    @patch('snipe_it.retry_request')
    def test_assign_fieldset_failure(self, mock_retry):
        """Test handling fieldset assignment failure."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = 'Server error'
        mock_retry.return_value = mock_response

        # Should not raise an error, just log it
        assign_fieldset_to_model(42, 9, 'test-key')

        mock_retry.assert_called_once()


if __name__ == '__main__':
    unittest.main()
