"""
Unit tests for retry_request function.
Tests HTTP request retry logic with rate limiting.
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

retry_request = module.retry_request


class TestRetryRequest(unittest.TestCase):
    """Tests for HTTP request retry logic with rate limiting."""

    @patch('snipe_it.requests.request')
    def test_successful_request_on_first_try(self, mock_request):
        """Test successful request returns immediately."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"status": "success"}'
        mock_request.return_value = mock_response

        result = retry_request('GET', 'http://test.com/api', retries=3, delay=1)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(mock_request.call_count, 1)

    @patch('snipe_it.time.sleep')
    @patch('snipe_it.requests.request')
    def test_retries_on_rate_limit(self, mock_request, mock_sleep):
        """Test that 429 responses trigger retries."""
        rate_limited = Mock(status_code=429, text='Rate limited')
        success = Mock(status_code=200, text='Success')
        mock_request.side_effect = [rate_limited, success]

        result = retry_request('GET', 'http://test.com/api', retries=2, delay=1)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(mock_request.call_count, 2)
        mock_sleep.assert_called_once_with(1)

    @patch('snipe_it.time.sleep')
    @patch('snipe_it.requests.request')
    def test_max_retries_exceeded(self, mock_request, mock_sleep):
        """Test that function returns None after max retries exceeded."""
        mock_response = Mock(status_code=429, text='Rate limited')
        mock_request.return_value = mock_response

        result = retry_request('GET', 'http://test.com/api', retries=2, delay=1)

        self.assertIsNone(result)
        self.assertEqual(mock_request.call_count, 2)
        # Should sleep after each attempt except the last
        self.assertEqual(mock_sleep.call_count, 2)

    @patch('snipe_it.time.sleep')
    @patch('snipe_it.requests.request')
    def test_handles_request_exception(self, mock_request, mock_sleep):
        """Test handling of request exceptions."""
        mock_request.side_effect = [
            Exception('Connection error'),
            Mock(status_code=200, text='Success')
        ]

        result = retry_request('GET', 'http://test.com/api', retries=2, delay=1)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(mock_request.call_count, 2)

    @patch('snipe_it.requests.request')
    def test_request_with_json_payload(self, mock_request):
        """Test request with JSON payload."""
        mock_response = Mock(status_code=200)
        mock_request.return_value = mock_response
        payload = {'key': 'value'}

        retry_request('POST', 'http://test.com/api', json=payload, retries=1)

        mock_request.assert_called_once_with(
            'POST', 'http://test.com/api',
            headers=None, json=payload, params=None
        )

    @patch('snipe_it.requests.request')
    def test_request_with_headers(self, mock_request):
        """Test request with custom headers."""
        mock_response = Mock(status_code=200)
        mock_request.return_value = mock_response
        headers = {'Authorization': 'Bearer token'}

        retry_request('GET', 'http://test.com/api', headers=headers, retries=1)

        mock_request.assert_called_once_with(
            'GET', 'http://test.com/api',
            headers=headers, json=None, params=None
        )


if __name__ == '__main__':
    unittest.main()
