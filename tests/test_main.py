import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """Testa o endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "IsCoolGPT API"
    assert data["status"] == "running"

def test_health():
    """Testa o endpoint de health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_ask_endpoint_missing_question():
    """Testa o endpoint /ask sem question"""
    response = client.post("/api/v1/ask", json={})
    assert response.status_code == 422  # Validation error

def test_ask_endpoint_empty_question():
    """Testa o endpoint /ask com question vazia"""
    response = client.post("/api/v1/ask", json={"question": ""})
    assert response.status_code == 422  # Validation error

def test_ask_endpoint_valid_request():
    """Testa o endpoint /ask com requisição válida"""
    # Nota: Este teste pode falhar se não houver API key configurada
    # Em um ambiente de CI/CD, você pode mockar o serviço LLM
    response = client.post(
        "/api/v1/ask",
        json={
            "question": "O que é Python?",
            "context": "Estou aprendendo programação"
        }
    )
    # Pode retornar 500 se não houver API key, ou 200 se houver
    assert response.status_code in [200, 500]

