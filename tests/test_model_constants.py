"""
Tests for model constants
"""
import pytest
import warnings
import cost_katana as ck
from cost_katana import (
    openai, anthropic, google, aws_bedrock, xai, deepseek,
    mistral, cohere, groq, meta,
    is_model_constant, get_all_model_constants, get_provider_from_model
)


class TestModelConstants:
    """Test model constants functionality"""
    
    def test_openai_constants(self):
        """Test OpenAI model constants"""
        assert openai.gpt_4 == 'gpt-4'
        assert openai.gpt_4_turbo == 'gpt-4-turbo'
        assert openai.gpt_3_5_turbo == 'gpt-3.5-turbo'
        assert openai.gpt_4o == 'gpt-4o'
        assert openai.gpt_4o_mini == 'gpt-4o-mini'
    
    def test_anthropic_constants(self):
        """Test Anthropic model constants"""
        assert anthropic.claude_3_5_sonnet_20241022 == 'claude-3-5-sonnet-20241022'
        assert anthropic.claude_3_opus_20240229 == 'claude-3-opus-20240229'
        assert anthropic.claude_3_haiku_20240307 == 'claude-3-haiku-20240307'
        assert anthropic.claude_3_5_haiku_20241022 == 'claude-3-5-haiku-20241022'
    
    def test_google_constants(self):
        """Test Google model constants"""
        assert google.gemini_2_5_pro == 'gemini-2.5-pro'
        assert google.gemini_1_5_flash == 'gemini-1.5-flash'
        assert google.gemini_1_5_pro == 'gemini-1.5-pro'
        assert google.gemini_2_0_flash == 'gemini-2.0-flash'
    
    def test_aws_bedrock_constants(self):
        """Test AWS Bedrock model constants"""
        assert aws_bedrock.nova_pro == 'amazon.nova-pro-v1:0'
        assert aws_bedrock.nova_lite == 'amazon.nova-lite-v1:0'
        assert aws_bedrock.nova_micro == 'amazon.nova-micro-v1:0'
    
    def test_xai_constants(self):
        """Test xAI model constants"""
        assert xai.grok_2_1212 == 'grok-2-1212'
        assert xai.grok_beta == 'grok-beta'
    
    def test_deepseek_constants(self):
        """Test DeepSeek model constants"""
        assert deepseek.deepseek_chat == 'deepseek-chat'
        assert deepseek.deepseek_reasoner == 'deepseek-reasoner'
    
    def test_mistral_constants(self):
        """Test Mistral model constants"""
        assert mistral.mistral_large_latest == 'mistral-large-latest'
        assert mistral.mistral_small_latest == 'mistral-small-latest'
    
    def test_cohere_constants(self):
        """Test Cohere model constants"""
        assert cohere.command_r_plus == 'command-r-plus'
        assert cohere.command_r == 'command-r'
    
    def test_groq_constants(self):
        """Test Grok model constants"""
        assert groq.llama_3_3_70b_versatile == 'llama-3.3-70b-versatile'
        assert groq.mixtral_8x7b_32768 == 'mixtral-8x7b-32768'
    
    def test_meta_constants(self):
        """Test Meta model constants"""
        assert meta.llama_3_3_70b_instruct == 'llama-3.3-70b-instruct'
        assert meta.llama_3_1_8b_instruct == 'llama-3.1-8b-instruct'
    
    def test_is_model_constant_valid(self):
        """Test is_model_constant utility with valid models"""
        assert is_model_constant('gpt-4') == True
        assert is_model_constant('gpt-4-turbo') == True
        assert is_model_constant('claude-3-5-sonnet-20241022') == True
        assert is_model_constant('gemini-2.5-pro') == True
        assert is_model_constant('grok-2-1212') == True
    
    def test_is_model_constant_invalid(self):
        """Test is_model_constant utility with invalid models"""
        assert is_model_constant('invalid-model') == False
        assert is_model_constant('') == False
        assert is_model_constant('gpt-999') == False
        assert is_model_constant('fake-model') == False
    
    def test_get_all_model_constants(self):
        """Test get_all_model_constants utility"""
        all_models = get_all_model_constants()
        assert isinstance(all_models, list)
        assert len(all_models) > 0
        
        # Check some expected models are in the list
        assert 'gpt-4' in all_models
        assert 'claude-3-5-sonnet-20241022' in all_models
        assert 'gemini-2.5-pro' in all_models
        assert 'grok-2-1212' in all_models
    
    def test_get_provider_from_model_openai(self):
        """Test get_provider_from_model utility for OpenAI"""
        assert get_provider_from_model('gpt-4') == 'OpenAI'
        assert get_provider_from_model('gpt-4-turbo') == 'OpenAI'
        assert get_provider_from_model('gpt-3.5-turbo') == 'OpenAI'
    
    def test_get_provider_from_model_anthropic(self):
        """Test get_provider_from_model utility for Anthropic"""
        assert get_provider_from_model('claude-3-5-sonnet-20241022') == 'Anthropic'
        assert get_provider_from_model('claude-3-opus-20240229') == 'Anthropic'
    
    def test_get_provider_from_model_google(self):
        """Test get_provider_from_model utility for Google"""
        assert get_provider_from_model('gemini-2.5-pro') == 'Google AI'
        assert get_provider_from_model('gemini-1.5-flash') == 'Google AI'
    
    def test_get_provider_from_model_aws_bedrock(self):
        """Test get_provider_from_model utility for AWS Bedrock"""
        assert get_provider_from_model('amazon.nova-pro-v1:0') == 'AWS Bedrock'
        assert get_provider_from_model('amazon.nova-lite-v1:0') == 'AWS Bedrock'
    
    def test_get_provider_from_model_xai(self):
        """Test get_provider_from_model utility for xAI"""
        assert get_provider_from_model('grok-2-1212') == 'xAI'
        assert get_provider_from_model('grok-beta') == 'xAI'
    
    def test_get_provider_from_model_deepseek(self):
        """Test get_provider_from_model utility for DeepSeek"""
        assert get_provider_from_model('deepseek-chat') == 'DeepSeek'
        assert get_provider_from_model('deepseek-reasoner') == 'DeepSeek'
    
    def test_get_provider_from_model_mistral(self):
        """Test get_provider_from_model utility for Mistral"""
        assert get_provider_from_model('mistral-large-latest') == 'Mistral AI'
        assert get_provider_from_model('mistral-small-latest') == 'Mistral AI'
    
    def test_get_provider_from_model_cohere(self):
        """Test get_provider_from_model utility for Cohere"""
        assert get_provider_from_model('command-r-plus') == 'Cohere'
        assert get_provider_from_model('command-r') == 'Cohere'
    
    def test_get_provider_from_model_groq(self):
        """Test get_provider_from_model utility for Grok"""
        assert get_provider_from_model('llama-3.3-70b-versatile') == 'Grok'
        assert get_provider_from_model('mixtral-8x7b-32768') == 'Grok'
    
    def test_get_provider_from_model_meta(self):
        """Test get_provider_from_model utility for Meta"""
        assert get_provider_from_model('llama-3.3-70b-instruct') == 'Meta'
        assert get_provider_from_model('llama-3.1-8b-instruct') == 'Meta'
    
    def test_get_provider_from_model_unknown(self):
        """Test get_provider_from_model utility with unknown model"""
        assert get_provider_from_model('invalid-model') == 'unknown'
        assert get_provider_from_model('') == 'unknown'
    
    def test_deprecation_warning_for_string_in_ai(self):
        """Test that string model names show deprecation warning in ai()"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # This should trigger a deprecation warning
            # Note: actual API call will fail without config, but we only care about the warning
            try:
                ck.ai('gpt-4', 'test')
            except:
                pass  # We only care about the warning, not the result
            
            # Check that a deprecation warning was issued
            assert len(w) >= 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert 'deprecated' in str(w[0].message).lower()
    
    def test_no_warning_for_constant_in_ai(self):
        """Test that constants don't show deprecation warning in ai()"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            try:
                ck.ai(openai.gpt_4, 'test')
            except:
                pass
            
            # Filter out any non-deprecation warnings
            deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
            assert len(deprecation_warnings) == 0
    
    def test_deprecation_warning_for_string_in_chat(self):
        """Test that string model names show deprecation warning in chat()"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            # This should trigger a deprecation warning
            try:
                ck.chat('gpt-4', system_message='test')
            except:
                pass
            
            # Check that a deprecation warning was issued
            assert len(w) >= 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert 'deprecated' in str(w[0].message).lower()
    
    def test_no_warning_for_constant_in_chat(self):
        """Test that constants don't show deprecation warning in chat()"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            try:
                ck.chat(openai.gpt_4, system_message='test')
            except:
                pass
            
            # Filter out any non-deprecation warnings
            deprecation_warnings = [warning for warning in w if issubclass(warning.category, DeprecationWarning)]
            assert len(deprecation_warnings) == 0
    
    def test_constants_are_strings(self):
        """Test that all constants are strings"""
        # Check a few from each provider
        assert isinstance(openai.gpt_4, str)
        assert isinstance(anthropic.claude_3_5_sonnet_20241022, str)
        assert isinstance(google.gemini_2_5_pro, str)
        assert isinstance(aws_bedrock.nova_pro, str)
        assert isinstance(xai.grok_2_1212, str)
    
    def test_namespace_immutability(self):
        """Test that namespaces exist and have the expected attributes"""
        # Check that namespaces have model attributes
        assert hasattr(openai, 'gpt_4')
        assert hasattr(anthropic, 'claude_3_5_sonnet_20241022')
        assert hasattr(google, 'gemini_2_5_pro')
        assert hasattr(aws_bedrock, 'nova_pro')
        assert hasattr(xai, 'grok_2_1212')
        assert hasattr(deepseek, 'deepseek_chat')
        assert hasattr(mistral, 'mistral_large_latest')
        assert hasattr(cohere, 'command_r_plus')
        assert hasattr(groq, 'llama_3_3_70b_versatile')
        assert hasattr(meta, 'llama_3_3_70b_instruct')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

