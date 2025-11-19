"""
Unit tests for config.py defaults.
Tests that configuration defaults are set correctly.
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


class TestConfigDefaults(unittest.TestCase):
    """Tests for configuration defaults."""

    @patch.dict(os.environ, {
        'API_TOKEN': 'test-token',
        'ENDPOINT_URL': 'http://test.local/api/v1',
        'DELEGATED_ADMIN': 'admin@example.com',
        'Gemini_APIKEY': 'gemini-key',
        'GOOGLE_SERVICE_ACCOUNT_FILE': '/tmp/service_account.json'
    }, clear=True)
    def test_default_mac_address_field(self):
        """Test default MAC address field ID."""
        import importlib
        import config
        importlib.reload(config)

        self.assertEqual(config.Config.SNIPE_IT_FIELD_MAC_ADDRESS, '_snipeit_mac_address_1')

    @patch.dict(os.environ, {
        'API_TOKEN': 'test-token',
        'ENDPOINT_URL': 'http://test.local/api/v1',
        'DELEGATED_ADMIN': 'admin@example.com',
        'Gemini_APIKEY': 'gemini-key',
        'GOOGLE_SERVICE_ACCOUNT_FILE': '/tmp/service_account.json'
    }, clear=True)
    def test_default_sync_date_field(self):
        """Test default sync date field ID."""
        import importlib
        import config
        importlib.reload(config)

        self.assertEqual(config.Config.SNIPE_IT_FIELD_SYNC_DATE, '_snipeit_sync_date_9')

    @patch.dict(os.environ, {
        'API_TOKEN': 'test-token',
        'ENDPOINT_URL': 'http://test.local/api/v1',
        'DELEGATED_ADMIN': 'admin@example.com',
        'Gemini_APIKEY': 'gemini-key',
        'GOOGLE_SERVICE_ACCOUNT_FILE': '/tmp/service_account.json'
    }, clear=True)
    def test_default_ip_address_field(self):
        """Test default IP address field ID."""
        import importlib
        import config
        importlib.reload(config)

        self.assertEqual(config.Config.SNIPE_IT_FIELD_IP_ADDRESS, '_snipeit_ip_address_3')

    @patch.dict(os.environ, {
        'API_TOKEN': 'test-token',
        'ENDPOINT_URL': 'http://test.local/api/v1',
        'DELEGATED_ADMIN': 'admin@example.com',
        'Gemini_APIKEY': 'gemini-key',
        'GOOGLE_SERVICE_ACCOUNT_FILE': '/tmp/service_account.json'
    }, clear=True)
    def test_default_user_field(self):
        """Test default user field ID."""
        import importlib
        import config
        importlib.reload(config)

        self.assertEqual(config.Config.SNIPE_IT_FIELD_USER, '_snipeit_user_10')

    @patch.dict(os.environ, {
        'API_TOKEN': 'test-token',
        'ENDPOINT_URL': 'http://test.local/api/v1',
        'DELEGATED_ADMIN': 'admin@example.com',
        'Gemini_APIKEY': 'gemini-key',
        'GOOGLE_SERVICE_ACCOUNT_FILE': '/tmp/service_account.json'
    }, clear=True)
    def test_default_model_id(self):
        """Test default model ID."""
        import importlib
        import config
        importlib.reload(config)

        self.assertEqual(config.Config.SNIPE_IT_DEFAULT_MODEL_ID, 87)

    @patch.dict(os.environ, {
        'API_TOKEN': 'test-token',
        'ENDPOINT_URL': 'http://test.local/api/v1',
        'DELEGATED_ADMIN': 'admin@example.com',
        'Gemini_APIKEY': 'gemini-key',
        'GOOGLE_SERVICE_ACCOUNT_FILE': '/tmp/service_account.json'
    }, clear=True)
    def test_default_fieldset_id(self):
        """Test default fieldset ID."""
        import importlib
        import config
        importlib.reload(config)

        self.assertEqual(config.Config.SNIPE_IT_FIELDSET_ID, 9)

    @patch.dict(os.environ, {
        'API_TOKEN': 'test-token',
        'ENDPOINT_URL': 'http://test.local/api/v1',
        'DELEGATED_ADMIN': 'admin@example.com',
        'Gemini_APIKEY': 'gemini-key',
        'GOOGLE_SERVICE_ACCOUNT_FILE': '/tmp/service_account.json'
    }, clear=True)
    def test_default_status_id(self):
        """Test default status ID."""
        import importlib
        import config
        importlib.reload(config)

        self.assertEqual(config.Config.SNIPE_IT_DEFAULT_STATUS_ID, 2)

    @patch.dict(os.environ, {
        'API_TOKEN': 'test-token',
        'ENDPOINT_URL': 'http://test.local/api/v1',
        'DELEGATED_ADMIN': 'admin@example.com',
        'Gemini_APIKEY': 'gemini-key',
        'GOOGLE_SERVICE_ACCOUNT_FILE': '/tmp/service_account.json'
    }, clear=True)
    def test_default_log_file(self):
        """Test default log file."""
        import importlib
        import config
        importlib.reload(config)

        self.assertEqual(config.Config.LOG_FILE, 'snipeit_errors.log')

    @patch.dict(os.environ, {
        'API_TOKEN': 'test-token',
        'ENDPOINT_URL': 'http://test.local/api/v1',
        'DELEGATED_ADMIN': 'admin@example.com',
        'Gemini_APIKEY': 'gemini-key',
        'GOOGLE_SERVICE_ACCOUNT_FILE': '/tmp/service_account.json'
    }, clear=True)
    def test_default_max_retries(self):
        """Test default max retries."""
        import importlib
        import config
        importlib.reload(config)

        self.assertEqual(config.Config.MAX_RETRIES, 4)

    @patch.dict(os.environ, {
        'API_TOKEN': 'test-token',
        'ENDPOINT_URL': 'http://test.local/api/v1',
        'DELEGATED_ADMIN': 'admin@example.com',
        'Gemini_APIKEY': 'gemini-key',
        'GOOGLE_SERVICE_ACCOUNT_FILE': '/tmp/service_account.json'
    }, clear=True)
    def test_default_retry_delay(self):
        """Test default retry delay."""
        import importlib
        import config
        importlib.reload(config)

        self.assertEqual(config.Config.RETRY_DELAY_SECONDS, 20)


if __name__ == '__main__':
    unittest.main()
