"""
Unit tests for config.py customization.
Tests configuration customization via environment variables.
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


class TestConfigCustomization(unittest.TestCase):
    """Tests for configuration customization via environment variables."""

    @patch.dict(os.environ, {
        'API_TOKEN': 'test-token',
        'ENDPOINT_URL': 'http://test.local/api/v1',
        'DELEGATED_ADMIN': 'admin@example.com',
        'Gemini_APIKEY': 'gemini-key',
        'GOOGLE_SERVICE_ACCOUNT_FILE': '/tmp/service_account.json',
        'SNIPE_IT_FIELD_MAC_ADDRESS': 'custom_mac_field',
        'SNIPE_IT_DEFAULT_MODEL_ID': '99',
        'MAX_RETRIES': '10'
    }, clear=True)
    def test_custom_field_ids(self):
        """Test customizing field IDs via environment variables."""
        import importlib
        import config
        importlib.reload(config)

        self.assertEqual(config.Config.SNIPE_IT_FIELD_MAC_ADDRESS, 'custom_mac_field')
        self.assertEqual(config.Config.SNIPE_IT_DEFAULT_MODEL_ID, 99)
        self.assertEqual(config.Config.MAX_RETRIES, 10)

    @patch.dict(os.environ, {
        'API_TOKEN': 'test-token',
        'ENDPOINT_URL': 'http://test.local/api/v1',
        'DELEGATED_ADMIN': 'admin@example.com',
        'Gemini_APIKEY': 'gemini-key',
        'GOOGLE_SERVICE_ACCOUNT_FILE': '/tmp/service_account.json',
        'DRY_RUN': 'true',
        'DEBUG': 'true'
    }, clear=True)
    def test_dry_run_and_debug_flags(self):
        """Test DRY_RUN and DEBUG flags."""
        import importlib
        import config
        importlib.reload(config)

        self.assertTrue(config.Config.DRY_RUN)
        self.assertTrue(config.Config.DEBUG)

    @patch.dict(os.environ, {
        'API_TOKEN': 'test-token',
        'ENDPOINT_URL': 'http://test.local/api/v1',
        'DELEGATED_ADMIN': 'admin@example.com',
        'Gemini_APIKEY': 'gemini-key',
        'GOOGLE_SERVICE_ACCOUNT_FILE': '/tmp/service_account.json',
        'ENVIRONMENT': 'production'
    }, clear=True)
    def test_environment_setting(self):
        """Test ENVIRONMENT setting."""
        import importlib
        import config
        importlib.reload(config)

        self.assertEqual(config.Config.ENVIRONMENT, 'production')


if __name__ == '__main__':
    unittest.main()
