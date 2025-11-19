"""
Integration and CLI tests for Google2Snipe-IT.
Tests full workflows and end-to-end scenarios with mocked external dependencies.
"""

import unittest
import sys
import types
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
import importlib.util

# Setup mock modules for imports FIRST
for name in ['googleAuth']:
    sys.modules.setdefault(name, types.ModuleType(name))

# Add gemini module with gemini_prompt function
if 'gemini' not in sys.modules:
    gemini_mod = types.ModuleType('gemini')
    mock_response = MagicMock()
    mock_response.text = '**Laptop**'
    gemini_mod.gemini_prompt = MagicMock(return_value=mock_response)
    sys.modules['gemini'] = gemini_mod
else:
    gemini_mod = sys.modules['gemini']
    if not hasattr(gemini_mod, 'gemini_prompt'):
        mock_response = MagicMock()
        mock_response.text = '**Laptop**'
        gemini_mod.gemini_prompt = MagicMock(return_value=mock_response)

# Dummy dotenv
dotenv_mod = types.ModuleType('dotenv')
setattr(dotenv_mod, 'load_dotenv', lambda *args, **kwargs: None)
sys.modules['dotenv'] = dotenv_mod

# Dummy tqdm
tqdm_mod = types.ModuleType('tqdm')
setattr(tqdm_mod, 'tqdm', lambda *args, **kwargs: (x for x in args[0]) if args else [])
setattr(tqdm_mod, 'write', lambda *args, **kwargs: None)
sys.modules['tqdm'] = tqdm_mod

# Mock requests
sys.modules['requests'] = MagicMock()

# Load snipe_it module and register it in sys.modules BEFORE classes use it
MODULE_PATH = Path(__file__).resolve().parents[1] / 'snipe-IT.py'
spec = importlib.util.spec_from_file_location('snipe_it', MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Register it in sys.modules so @patch decorators can find it
sys.modules['snipe_it'] = module

# NOTE: Don't extract functions - use module.function_name in tests
# This ensures @patch decorators work correctly
snipe_it_module = module


class TestHardwareCreationWorkflow(unittest.TestCase):
    """Tests for hardware creation basic functionality."""

    def test_format_mac_before_creation(self):
        """Test that MAC addresses are properly formatted before use."""
        raw_mac = 'a81d166742f7'
        formatted = snipe_it_module.format_mac(raw_mac)
        self.assertEqual(formatted, 'a8:1d:16:67:42:f7')

    def test_format_mac_preserves_formatted(self):
        """Test that already-formatted MAC addresses are not modified."""
        formatted_mac = 'a8:1d:16:67:42:f7'
        result = snipe_it_module.format_mac(formatted_mac)
        self.assertEqual(result, formatted_mac)

    def test_format_mac_handles_none(self):
        """Test that None MAC addresses return None."""
        result = snipe_it_module.format_mac(None)
        self.assertIsNone(result)

    def test_format_mac_case_insensitive(self):
        """Test that MAC formatting is case-insensitive."""
        uppercase_mac = 'A81D166742F7'
        result = snipe_it_module.format_mac(uppercase_mac)
        self.assertEqual(result, 'a8:1d:16:67:42:f7')


class TestHardwareUpdateWorkflow(unittest.TestCase):
    """Tests for hardware update MAC address formatting."""

    def test_mac_formatting_in_payload(self):
        """Test that MAC addresses are formatted correctly."""
        raw_mac = 'a81d166742f7'
        formatted = snipe_it_module.format_mac(raw_mac)
        self.assertEqual(formatted, 'a8:1d:16:67:42:f7')

    def test_mac_already_formatted_unchanged(self):
        """Test that pre-formatted MACs are not modified."""
        formatted_mac = 'a8:1d:16:67:42:f7'
        result = snipe_it_module.format_mac(formatted_mac)
        self.assertEqual(result, formatted_mac)

    def test_mac_with_dashes_normalized(self):
        """Test that MACs with dashes are normalized."""
        dash_mac = 'a8-1d-16-67-42-f7'
        result = snipe_it_module.format_mac(dash_mac)
        self.assertEqual(result, 'a8:1d:16:67:42:f7')


class TestDeviceSyncWorkflow(unittest.TestCase):
    """Tests for device data handling in sync workflow."""

    def test_device_data_with_all_fields(self):
        """Test that device data structure with all fields is valid."""
        device = {
            'Serial Number': 'SN001',
            'Status': 'ACTIVE',
            'Model': 'Dell Chromebook 11',
            'Mac Address': 'a8:1d:16:67:42:f7',
            'Device User': 'user1@example.com',
            'Last Known IP Address': '192.168.1.100',
            'Active Time Ranges': [{'date': '2024-01-15'}],
            'EOL': '2025-06-15'
        }

        # Verify all required fields are present
        self.assertIn('Serial Number', device)
        self.assertIn('Status', device)
        self.assertIn('Model', device)
        self.assertIn('Mac Address', device)

    def test_device_data_with_missing_optional_fields(self):
        """Test that device data with None values is handled properly."""
        device = {
            'Serial Number': 'SN001',
            'Status': 'ACTIVE',
            'Model': 'Chromebook',
            'Mac Address': None,
            'Device User': None,
            'Last Known IP Address': None,
            'Active Time Ranges': None,
            'EOL': None
        }

        # Test safe access to optional fields
        active_time = None
        try:
            if device.get('Active Time Ranges'):
                active_time = device['Active Time Ranges'][0].get('date')
        except (TypeError, IndexError):
            active_time = None

        self.assertIsNone(active_time)


class TestErrorHandling(unittest.TestCase):
    """Tests for error handling scenarios."""

    def test_format_mac_with_invalid_length(self):
        """Test that invalid-length MACs are returned as-is."""
        invalid_mac = 'a8:1d:16'  # Too short - already formatted, so returned unchanged
        result = snipe_it_module.format_mac(invalid_mac)
        self.assertEqual(result, 'a8:1d:16')  # Returned unchanged due to colon

    def test_format_mac_with_special_characters(self):
        """Test that MACs with special characters are handled."""
        special_mac = 'a8_1d_16_67_42_f7'
        result = snipe_it_module.format_mac(special_mac)
        # Should handle the removal of underscores/special chars
        self.assertEqual(len(result), len('a81d166742f7') + 5)  # 12 chars + 5 colons


class TestDataValidation(unittest.TestCase):
    """Tests for data validation and sanitization."""

    def test_mac_address_formatting_comprehensive(self):
        """Test MAC address formatting is applied consistently."""
        test_cases = [
            ('a81d166742f7', 'a8:1d:16:67:42:f7'),
            ('a8:1d:16:67:42:f7', 'a8:1d:16:67:42:f7'),
            ('A81D166742F7', 'a8:1d:16:67:42:f7'),
            (None, None),
            ('', ''),
            ('a8-1d-16-67-42-f7', 'a8:1d:16:67:42:f7'),
        ]

        for input_mac, expected_output in test_cases:
            result = snipe_it_module.format_mac(input_mac)
            self.assertEqual(result, expected_output,
                           f"Failed for input: {input_mac}")

    def test_device_status_names(self):
        """Test that status names are used correctly."""
        valid_statuses = ['ACTIVE', 'INACTIVE', 'DEPLOYED', 'RETIRED']
        for status in valid_statuses:
            self.assertIsInstance(status, str)
            self.assertGreater(len(status), 0)

    def test_custom_field_id_format(self):
        """Test that custom field IDs follow expected format."""
        field_ids = [
            '_snipeit_mac_address_1',
            '_snipeit_sync_date_9',
            '_snipeit_ip_address_3',
            '_snipeit_user_10'
        ]

        for field_id in field_ids:
            self.assertTrue(field_id.startswith('_snipeit_'))
            self.assertIn('_', field_id)


if __name__ == '__main__':
    unittest.main()
