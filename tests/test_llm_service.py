import pytest
from app.services.llm_service import LLMService
from app.core.config import settings

@pytest.mark.asyncio
async def test_llm_service_initialization():
    """Testa inicialização do serviço LLM"""
    service = LLMService()
    assert service.provider == settings.llm_provider

@pytest.mark.asyncio
async def test_llm_service_invalid_provider():
    """Testa erro com provedor inválido"""
    service = LLMService()
    service.provider = "invalid_provider"
    
    with pytest.raises(ValueError, match="não suportado"):
        await service.generate_response("test question")

@pytest.mark.asyncio
async def test_llm_service_openai_no_key():
    """Testa erro quando OpenAI API key não está configurada"""
    service = LLMService()
    service.provider = "openai"
    service.openai_api_key = None
    
    with pytest.raises(ValueError, match="OpenAI API key não configurada"):
        await service.generate_response("test question")

@pytest.mark.asyncio
async def test_llm_service_huggingface_no_key():
    """Testa erro quando Hugging Face API key não está configurada"""
    service = LLMService()
    service.provider = "huggingface"
    service.huggingface_api_key = None
    
    with pytest.raises(ValueError, match="Hugging Face API key não configurada"):
        await service.generate_response("test question")

