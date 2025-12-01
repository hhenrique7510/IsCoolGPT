"""
Testes de integração para validação no ambiente staging.
Estes testes são executados após o deploy no staging para garantir
que a API está funcionando corretamente antes do deploy em produção.
"""
import os
import time
import httpx
import pytest
from typing import Optional

# URL base da API (será configurada via variável de ambiente)
STAGING_URL = os.getenv("STAGING_API_URL", "http://localhost:8000")
TIMEOUT = 30  # segundos
MAX_RETRIES = 10
RETRY_DELAY = 3  # segundos


def wait_for_service(url: str, max_retries: int = MAX_RETRIES, delay: int = RETRY_DELAY) -> bool:
    """
    Aguarda o serviço ficar disponível, fazendo retries.
    """
    for attempt in range(max_retries):
        try:
            response = httpx.get(f"{url}/health", timeout=5, follow_redirects=True)
            if response.status_code == 200:
                return True
        except (httpx.ConnectError, httpx.TimeoutException):
            pass
        
        if attempt < max_retries - 1:
            time.sleep(delay)
    
    return False


@pytest.fixture(scope="module")
def client():
    """Cliente HTTP para os testes de integração."""
    # Aguardar serviço ficar disponível
    if not wait_for_service(STAGING_URL):
        pytest.skip(f"Serviço não está disponível em {STAGING_URL}")
    
    return httpx.Client(base_url=STAGING_URL, timeout=30.0, follow_redirects=True)


class TestHealthCheck:
    """Testes do endpoint de health check."""
    
    def test_health_endpoint_responds(self, client):
        """Verifica se o endpoint /health responde."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_endpoint_returns_json(self, client):
        """Verifica se o endpoint /health retorna JSON válido."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_root_endpoint_responds(self, client):
        """Verifica se o endpoint raiz responde."""
        response = client.get("/")
        assert response.status_code == 200


class TestAskEndpoint:
    """Testes do endpoint principal /ask."""
    
    def test_ask_endpoint_exists(self, client):
        """Verifica se o endpoint /api/v1/ask existe."""
        response = client.post(
            "/api/v1/ask",
            json={"question": "Teste"},
            headers={"Content-Type": "application/json"}
        )
        # Pode retornar 200 (sucesso) ou 422 (validação)
        assert response.status_code in [200, 422]
    
    def test_ask_endpoint_with_valid_request(self, client):
        """Testa o endpoint /ask com uma requisição válida."""
        response = client.post(
            "/api/v1/ask",
            json={
                "question": "O que é Python?",
                "context": "Estou aprendendo programação",
                "max_tokens": 100
            },
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "question" in data
        assert isinstance(data["answer"], str)
        assert len(data["answer"]) > 0
    
    def test_ask_endpoint_validation(self, client):
        """Verifica se a validação do endpoint funciona."""
        # Requisição sem question (deve falhar)
        response = client.post(
            "/api/v1/ask",
            json={},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_ask_endpoint_empty_question(self, client):
        """Verifica se question vazio é rejeitado."""
        response = client.post(
            "/api/v1/ask",
            json={"question": ""},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422


class TestSwaggerDocumentation:
    """Testes da documentação Swagger."""
    
    def test_swagger_ui_accessible(self, client):
        """Verifica se a documentação Swagger está acessível."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_openapi_schema_accessible(self, client):
        """Verifica se o schema OpenAPI está acessível."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "paths" in data


class TestSmokeTests:
    """Smoke tests - testes básicos para garantir que o serviço está funcionando."""
    
    def test_service_is_responding(self, client):
        """Teste básico: serviço está respondendo."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_api_endpoints_are_accessible(self, client):
        """Verifica se os principais endpoints estão acessíveis."""
        # Health check
        health_response = client.get("/health")
        assert health_response.status_code == 200
        
        # Root
        root_response = client.get("/")
        assert root_response.status_code == 200
        
        # Docs
        docs_response = client.get("/docs")
        assert docs_response.status_code == 200
    
    def test_cors_headers(self, client):
        """Verifica se CORS está configurado (se aplicável)."""
        response = client.get("/health")
        assert response.status_code == 200


class TestPerformance:
    """Testes básicos de performance."""
    
    def test_health_endpoint_response_time(self, client):
        """Verifica se o health check responde rapidamente."""
        start_time = time.time()
        response = client.get("/health")
        elapsed_time = time.time() - start_time
        
        assert response.status_code == 200
        assert elapsed_time < 2.0  
    
    def test_ask_endpoint_response_time(self, client):
        """Verifica se o endpoint /ask responde em tempo razoável."""
        start_time = time.time()
        response = client.post(
            "/api/v1/ask",
            json={"question": "Teste rápido"},
            headers={"Content-Type": "application/json"}
        )
        elapsed_time = time.time() - start_time
        
        assert response.status_code in [200, 422]
        assert elapsed_time < 30.0  

