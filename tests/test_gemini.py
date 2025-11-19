"""
Unit tests for gemini.py module.
Tests AI-powered model categorization functionality.
"""

import unittest
import sys
import types
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Mock dotenv before importing config
if 'dotenv' not in sys.modules:
    dotenv_mod = types.ModuleType('dotenv')
    setattr(dotenv_mod, 'load_dotenv', MagicMock())
    sys.modules['dotenv'] = dotenv_mod

# Create proper mock structure for google.generativeai BEFORE any imports
if 'google' not in sys.modules:
    google_mod = types.ModuleType('google')
    sys.modules['google'] = google_mod

if 'google.generativeai' not in sys.modules:
    genai_mod = types.ModuleType('google.generativeai')

    # Create mock classes that can be instantiated
    mock_model_instance = MagicMock()
    mock_model_instance.generate_content = MagicMock()

    # GenerativeModel should be a class that returns our mock instance
    genai_mod.GenerativeModel = MagicMock(return_value=mock_model_instance)
    genai_mod.configure = MagicMock()

    sys.modules['google.generativeai'] = genai_mod
    sys.modules['google'].generativeai = genai_mod


@unittest.skip("Requires google.generativeai library - install with: pip install google-generativeai")
class TestGeminiPrompt(unittest.TestCase):
    """Tests for Gemini API prompt functionality."""

    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_gemini_prompt_success(self, mock_configure, mock_model_class):
        """Test successful Gemini API call."""
        # Reload gemini module to pick up patched dependencies
        import importlib
        if 'gemini' in sys.modules:
            del sys.modules['gemini']

        import gemini
        importlib.reload(gemini)

        mock_response = MagicMock()
        mock_response.text = '**Chromebook**'

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        result = gemini.gemini_prompt('What category is this device?')

        self.assertEqual(result.text, '**Chromebook**')
        mock_configure.assert_called_once()

    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_gemini_prompt_returns_response_object(self, mock_configure, mock_model_class):
        """Test that gemini_prompt returns the full response object."""
        import importlib
        if 'gemini' in sys.modules:
            del sys.modules['gemini']

        import gemini
        importlib.reload(gemini)

        mock_response = MagicMock()
        mock_response.text = 'Some response'
        mock_response.usage_metadata = {'prompt_tokens': 10, 'candidates_tokens': 5}

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        result = gemini.gemini_prompt('Test prompt')

        # Should return the actual response object, not just text
        self.assertEqual(result, mock_response)

    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_gemini_prompt_with_category_formatting(self, mock_configure, mock_model_class):
        """Test Gemini prompt returns formatted category in asterisks."""
        import importlib
        if 'gemini' in sys.modules:
            del sys.modules['gemini']

        import gemini
        importlib.reload(gemini)

        mock_response = MagicMock()
        mock_response.text = 'The device is a **Laptop** category device.'

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        result = gemini.gemini_prompt('Categorize this device')

        self.assertIn('**Laptop**', result.text)

    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_gemini_prompt_handles_empty_response(self, mock_configure, mock_model_class):
        """Test handling of empty or whitespace response."""
        import importlib
        if 'gemini' in sys.modules:
            del sys.modules['gemini']

        import gemini
        importlib.reload(gemini)

        mock_response = MagicMock()
        mock_response.text = ''

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        result = gemini.gemini_prompt('Test prompt')

        self.assertEqual(result.text, '')

    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_gemini_prompt_with_long_prompt(self, mock_configure, mock_model_class):
        """Test Gemini prompt with a long input prompt."""
        import importlib
        if 'gemini' in sys.modules:
            del sys.modules['gemini']

        import gemini
        importlib.reload(gemini)

        mock_response = MagicMock()
        mock_response.text = '**Chromebook**'

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        long_prompt = "Given the following technology model, Model: Dell Chromebook 11 (3180) select the most appropriate category from this list: IMac,Tablets,Mobile Devices,Servers,Networking Equipment,Printers & Scanners,Desktop,Chromebook"

        result = gemini.gemini_prompt(long_prompt)

        mock_model.generate_content.assert_called_once_with(long_prompt)
        self.assertEqual(result.text, '**Chromebook**')

    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_gemini_prompt_various_category_formats(self, mock_configure, mock_model_class):
        """Test Gemini handling various response formats."""
        import importlib
        if 'gemini' in sys.modules:
            del sys.modules['gemini']

        import gemini
        importlib.reload(gemini)

        test_cases = [
            '**Desktop**',
            'The category is **Laptop**.',
            '**Mobile Devices** are the best fit.',
            'I recommend **Tablets** for this device.',
        ]

        for test_response in test_cases:
            mock_response = MagicMock()
            mock_response.text = test_response

            mock_model = MagicMock()
            mock_model.generate_content.return_value = mock_response
            mock_model_class.return_value = mock_model

            result = gemini.gemini_prompt('Test')

            self.assertEqual(result.text, test_response)

    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_gemini_prompt_passes_prompt_to_model(self, mock_configure, mock_model_class):
        """Test that prompt is correctly passed to the model."""
        import importlib
        if 'gemini' in sys.modules:
            del sys.modules['gemini']

        import gemini
        importlib.reload(gemini)

        mock_response = MagicMock()
        mock_response.text = '**Category**'

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        test_prompt = 'Custom prompt for categorization'
        gemini.gemini_prompt(test_prompt)

        mock_model.generate_content.assert_called_once_with(test_prompt)

    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_gemini_prompt_uses_configured_model(self, mock_configure, mock_model_class):
        """Test that Gemini uses the configured model."""
        import importlib
        if 'gemini' in sys.modules:
            del sys.modules['gemini']

        import gemini
        importlib.reload(gemini)

        mock_response = MagicMock()
        mock_response.text = '**Category**'

        mock_model = MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model

        gemini.gemini_prompt('Test')

        # Verify GenerativeModel was called with a model name
        mock_model_class.assert_called()


@unittest.skip("Requires google.generativeai library - install with: pip install google-generativeai")
class TestGeminiIntegration(unittest.TestCase):
    """Integration tests for Gemini module."""

    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_gemini_initialization(self, mock_configure, mock_model_class):
        """Test Gemini API initialization."""
        import importlib
        if 'gemini' in sys.modules:
            del sys.modules['gemini']

        import gemini
        importlib.reload(gemini)

        # Verify configure was called
        mock_configure.assert_called_once()

        # Verify GenerativeModel was instantiated
        mock_model_class.assert_called_once()

    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_gemini_prompt_multiple_calls(self, mock_configure, mock_model_class):
        """Test multiple sequential Gemini prompts."""
        import importlib
        if 'gemini' in sys.modules:
            del sys.modules['gemini']

        import gemini
        importlib.reload(gemini)

        responses = [
            '**Chromebook**',
            '**Desktop**',
            '**Laptop**'
        ]

        for response_text in responses:
            mock_response = MagicMock()
            mock_response.text = response_text

            mock_model = MagicMock()
            mock_model.generate_content.return_value = mock_response
            mock_model_class.return_value = mock_model

            result = gemini.gemini_prompt(f'Categorize device')

            self.assertEqual(result.text, response_text)


if __name__ == '__main__':
    unittest.main()
