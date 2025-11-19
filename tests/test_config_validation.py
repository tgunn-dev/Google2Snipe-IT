"""
Unit tests for config.py validation.
Tests configuration validation with required and optional variables.
"""

import unittest
import os
import sys
import types
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Mock dotenv before importing config
if 'dotenv' not in sys.modules:
    dotenv_mod = types.ModuleType('dotenv')
    setattr(dotenv_mod, 'load_dotenv', MagicMock())
    sys.modules['dotenv'] = dotenv_mod


class TestConfigValidation(unittest.TestCase):
    """Tests for configuration validation."""

    @patch.dict(os.environ, {
        'API_TOKEN': 'test-token',
        'ENDPOINT_URL': 'http://test.local/api/v1',
        'DELEGATED_ADMIN': 'admin@example.com',
        'Gemini_APIKEY': 'gemini-key',
        'GOOGLE_SERVICE_ACCOUNT_FILE': '/tmp/service_account.json'
    })
    @patch('config.os.path.exists')
    def test_validate_success_with_all_required_vars(self, mock_exists):
        """Test validation succeeds when all required variables are set."""
        mock_exists.return_value = True

        # Reimport config to pick up mocked environment
        import importlib
        import config
        importlib.reload(config)

        is_valid, errors = config.Config.validate()

        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    @patch.dict(os.environ, {}, clear=True)
    @patch('config.os.path.exists')
    def test_validate_fails_missing_api_token(self, mock_exists):
        """Test validation fails when API_TOKEN is missing."""
        mock_exists.return_value = True

        import importlib
        import config
        importlib.reload(config)

        is_valid, errors = config.Config.validate()

        self.assertFalse(is_valid)
        self.assertIn("API_TOKEN environment variable is required", errors)

    @patch.dict(os.environ, {
        'API_TOKEN': 'test-token',
        'DELEGATED_ADMIN': 'admin@example.com',
        'Gemini_APIKEY': 'gemini-key',
        'GOOGLE_SERVICE_ACCOUNT_FILE': '/tmp/service_account.json'
    }, clear=True)
    @patch('config.os.path.exists')
    def test_validate_fails_missing_endpoint_url(self, mock_exists):
        """Test validation fails when ENDPOINT_URL is missing."""
        mock_exists.return_value = True

        import importlib
        import config
        importlib.reload(config)

        is_valid, errors = config.Config.validate()

        self.assertFalse(is_valid)
        self.assertIn("ENDPOINT_URL environment variable is required", errors)

    @patch.dict(os.environ, {
        'API_TOKEN': 'test-token',
        'ENDPOINT_URL': 'http://test.local/api/v1',
        'Gemini_APIKEY': 'gemini-key',
        'GOOGLE_SERVICE_ACCOUNT_FILE': '/tmp/service_account.json'
    }, clear=True)
    @patch('config.os.path.exists')
    def test_validate_fails_missing_delegated_admin(self, mock_exists):
        """Test validation fails when DELEGATED_ADMIN is missing."""
        mock_exists.return_value = True

        import importlib
        import config
        importlib.reload(config)

        is_valid, errors = config.Config.validate()

        self.assertFalse(is_valid)
        self.assertIn("DELEGATED_ADMIN environment variable is required", errors)

    @patch.dict(os.environ, {
        'API_TOKEN': 'test-token',
        'ENDPOINT_URL': 'http://test.local/api/v1',
        'DELEGATED_ADMIN': 'admin@example.com',
        'Gemini_APIKEY': 'gemini-key'
    }, clear=True)
    @patch('config.os.path.exists')
    def test_validate_fails_missing_service_account_file(self, mock_exists):
        """Test validation fails when service account file doesn't exist."""
        mock_exists.return_value = False

        import importlib
        import config
        importlib.reload(config)

        is_valid, errors = config.Config.validate()

        self.assertFalse(is_valid)
        self.assertIn("Google service account file not found", errors[0])

    @patch.dict(os.environ, {
        'API_TOKEN': 'test-token',
        'ENDPOINT_URL': 'http://test.local/api/v1',
        'DELEGATED_ADMIN': 'admin@example.com',
        'GOOGLE_SERVICE_ACCOUNT_FILE': '/tmp/service_account.json'
    }, clear=True)
    @patch('config.os.path.exists')
    def test_validate_fails_missing_gemini_api_key(self, mock_exists):
        """Test validation fails when Gemini_APIKEY is missing."""
        mock_exists.return_value = True

        import importlib
        import config
        importlib.reload(config)

        is_valid, errors = config.Config.validate()

        self.assertFalse(is_valid)
        self.assertIn("Gemini_APIKEY environment variable is required", errors)

    @patch.dict(os.environ, {}, clear=True)
    @patch('config.os.path.exists')
    def test_validate_multiple_errors(self, mock_exists):
        """Test validation collects multiple errors."""
        mock_exists.return_value = False

        import importlib
        import config
        importlib.reload(config)

        is_valid, errors = config.Config.validate()

        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 1)


if __name__ == '__main__':
    unittest.main()
