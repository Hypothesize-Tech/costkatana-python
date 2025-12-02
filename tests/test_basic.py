"""
Basic tests for Cost Katana Python SDK
"""

import pytest
from unittest.mock import Mock, patch
import cost_katana as ck
from cost_katana.client import CostKatanaClient
from cost_katana.config import Config
from cost_katana.exceptions import CostKatanaError, AuthenticationError


class TestConfiguration:
    """Test configuration management"""
    
    def test_config_creation(self):
        """Test basic config creation"""
        config = Config(api_key="test_key")
        assert config.api_key == "test_key"
        assert config.base_url == "https://api.costkatana.com"
    
    def test_model_mapping(self):
        """Test model name mapping"""
        config = Config()
        
        # Test default mappings
        assert config.get_model_mapping("gemini-2.0-flash") == "amazon.nova-lite-v1:0"
        assert config.get_model_mapping("claude-3-sonnet") == "anthropic.claude-3-sonnet-20240229-v1:0"
        
        # Test unmapped names (should return as-is)
        assert config.get_model_mapping("custom-model") == "custom-model"


class TestClient:
    """Test HTTP client functionality"""
    
    def test_client_initialization(self):
        """Test client initialization"""
        client = CostKatanaClient(api_key="test_key")
        assert client.config.api_key == "test_key"
        assert "Bearer test_key" in client.client.headers["Authorization"]
    
    def test_authentication_error(self):
        """Test authentication error"""
        with pytest.raises(AuthenticationError):
            CostKatanaClient()  # No API key provided


class TestModels:
    """Test model interface"""
    
    @patch('cost_katana.client.CostKatanaClient.get_available_models')
    @patch('cost_katana.client.CostKatanaClient.send_message')
    def test_generate_content(self, mock_send, mock_models):
        """Test content generation"""
        # Setup mocks
        mock_models.return_value = [{"id": "nova-lite", "name": "Nova Lite"}]
        mock_send.return_value = {
            "success": True,
            "data": {
                "response": "Hello, world!",
                "cost": 0.001,
                "latency": 1.5,
                "tokenCount": 10,
                "model": "nova-lite"
            }
        }
        
        # Configure first
        ck.configure(api_key="test_key")
        
        # Test generation
        model = ck.create_generative_model('nova-lite')
        response = model.generate_content("Hello")
        
        assert response.text == "Hello, world!"
        assert response.usage_metadata.cost == 0.001
        assert response.usage_metadata.latency == 1.5
        
        # Verify API call
        mock_send.assert_called_once()
        call_args = mock_send.call_args[1]
        assert call_args['message'] == "Hello"
        assert call_args['model_id'] == "amazon.nova-lite-v1:0"


class TestExceptions:
    """Test error handling"""
    
    def test_cost_katana_error_hierarchy(self):
        """Test exception hierarchy"""
        assert issubclass(AuthenticationError, CostKatanaError)
    
    def test_error_messages(self):
        """Test error messages"""
        error = CostKatanaError("Test error")
        assert str(error) == "Test error"


class TestIntegration:
    """Integration tests"""
    
    def test_import_structure(self):
        """Test that all public APIs are importable"""
        from cost_katana import configure, create_generative_model, CostKatanaClient
        from cost_katana.exceptions import CostKatanaError, AuthenticationError
        from cost_katana.config import Config
        
        # Test that classes exist
        assert configure is not None
        assert create_generative_model is not None
        assert CostKatanaClient is not None
        assert CostKatanaError is not None
        assert AuthenticationError is not None
        assert Config is not None
    
    def test_version_available(self):
        """Test that version is available"""
        assert hasattr(ck, '__version__')
        assert isinstance(ck.__version__, str)


# Run tests if called directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])