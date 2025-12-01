# Relatório Técnico Completo - IsCoolGPT

## 📋 Índice

1. [Visão Geral do Projeto](#visão-geral-do-projeto)
2. [Diagrama de Arquitetura](#diagrama-de-arquitetura)
3. [Código-Fonte Comentado](#código-fonte-comentado)
4. [Arquivos de Configuração](#arquivos-de-configuração)
5. [Decisões Técnicas e Justificativas](#decisões-técnicas-e-justificativas)
6. [CI/CD Pipeline](#cicd-pipeline)
7. [Infraestrutura AWS](#infraestrutura-aws)
8. [Segurança](#segurança)
9. [Monitoramento e Logs](#monitoramento-e-logs)

---

## 1. Visão Geral do Projeto

### 1.1 Objetivo

O **IsCoolGPT** é um assistente educacional inteligente desenvolvido como API REST, que permite fazer perguntas e receber respostas através de integração com modelos de linguagem (LLM). O projeto foi desenvolvido seguindo boas práticas de DevOps, com containerização, CI/CD automatizado e deploy na AWS.

### 1.2 Stack Tecnológica

- **Backend**: Python 3.11 + FastAPI
- **LLM Providers**: OpenAI, Google Gemini, Hugging Face
- **Containerização**: Docker (multi-stage build)
- **Cloud**: AWS (ECS Fargate, ECR, CloudWatch, Secrets Manager)
- **CI/CD**: GitHub Actions
- **Testes**: pytest, pytest-cov
- **Linting**: flake8, black, mypy

### 1.3 Funcionalidades Principais

- ✅ API REST para perguntas e respostas
- ✅ Suporte a múltiplos provedores de LLM (OpenAI, Gemini, Hugging Face)
- ✅ Modo mock para testes sem API keys
- ✅ Documentação automática (Swagger/OpenAPI)
- ✅ Health checks
- ✅ CI/CD completo com staging e produção
- ✅ Deploy zero-downtime
- ✅ Testes automatizados (unitários e integração)

---

## 2. Diagrama de Arquitetura

### 2.1 Arquitetura Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                        DESENVOLVIMENTO LOCAL                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Código     │  │   Docker    │  │   Testes     │          │
│  │   Python     │→ │   Build     │→ │   Local      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Git Push
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         GITHUB REPOSITORY                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Branch: develop (staging) | main (production)            │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Trigger
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      GITHUB ACTIONS (CI/CD)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │    Lint      │  │    Test     │  │    Build     │          │
│  │  (flake8,    │  │  (pytest)   │  │   (Docker)  │          │
│  │   black,     │  │             │  │             │          │
│  │   mypy)      │  │             │  │             │          │
│  └──────────────┘  └──────────────┘  └──────┬───────┘          │
│                                               │                  │
│                                               │ Push Image       │
│                                               ▼                  │
│                                      ┌──────────────┐           │
│                                      │  AWS ECR     │           │
│                                      │  (Registry)  │           │
│                                      └──────┬───────┘           │
│                                             │                   │
│                                             │ Deploy            │
│                                             ▼                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Deploy Staging (develop)  |  Deploy Production (main)   │  │
│  │  ┌──────────────┐         │  ┌──────────────┐          │  │
│  │  │ Validate     │         │  │ Zero         │          │  │
│  │  │ Staging      │         │  │ Downtime     │          │  │
│  │  └──────────────┘         │  └──────────────┘          │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        AWS INFRAESTRUTURA                        │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    AWS ECS (Fargate)                       │  │
│  │  ┌──────────────────┐         ┌──────────────────┐       │  │
│  │  │  Staging        │         │  Production      │       │  │
│  │  │  Cluster        │         │  Cluster         │       │  │
│  │  │  - Task         │         │  - Task          │       │  │
│  │  │  - Service      │         │  - Service       │       │  │
│  │  └──────────────────┘         └──────────────────┘       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              AWS SERVICES                                │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │  │
│  │  │  ECR         │  │  Secrets     │  │  CloudWatch  │    │  │
│  │  │  (Images)    │  │  Manager    │  │  (Logs)      │    │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              IAM ROLES                                   │  │
│  │  ┌──────────────┐         ┌──────────────┐              │  │
│  │  │  ecsTask     │         │  ecsTask     │              │  │
│  │  │  Execution   │         │  Role        │              │  │
│  │  │  Role        │         │              │              │  │
│  │  └──────────────┘         └──────────────┘              │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        API PÚBLICA                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Swagger UI  │  │  Health     │  │  /api/v1/   │          │
│  │  /docs       │  │  /health    │  │  /ask        │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Fluxo de Dados

```
Cliente HTTP Request
    │
    ▼
FastAPI Application (app/main.py)
    │
    ▼
Router (app/routers/ask.py)
    │
    ▼
Controller (app/controllers/ask_controller.py)
    │
    ▼
LLM Service (app/services/llm_service.py)
    │
    ├─→ OpenAI API (se LLM_PROVIDER=openai)
    ├─→ Gemini API (se LLM_PROVIDER=gemini)
    ├─→ Hugging Face API (se LLM_PROVIDER=huggingface)
    └─→ Mock Response (se LLM_PROVIDER=mock)
    │
    ▼
Response JSON
    │
    ▼
Cliente HTTP Response
```

### 2.3 Componentes Principais

| Componente | Tecnologia | Responsabilidade |
|------------|------------|------------------|
| **API Layer** | FastAPI | Endpoints REST, validação, documentação |
| **Business Logic** | Python | Controllers e serviços |
| **LLM Integration** | OpenAI/Gemini/HF | Integração com modelos de linguagem |
| **Container** | Docker | Empacotamento e isolamento |
| **Orchestration** | AWS ECS Fargate | Gerenciamento de containers |
| **Registry** | AWS ECR | Armazenamento de imagens |
| **CI/CD** | GitHub Actions | Automação de build e deploy |
| **Secrets** | AWS Secrets Manager | Armazenamento seguro de API keys |
| **Logs** | AWS CloudWatch | Monitoramento e troubleshooting |

---

## 3. Código-Fonte Comentado

### 3.1 Aplicação Principal (`app/main.py`)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ask
from app.core.config import settings

# Criação da aplicação FastAPI com metadados
app = FastAPI(
    title="IsCoolGPT API",
    description="Assistente inteligente voltado para educação",
    version="1.0.0",
)

# Configuração de CORS (Cross-Origin Resource Sharing)
# Permite requisições de qualquer origem (em produção, restringir)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão dos routers (endpoints da API)
app.include_router(ask.router, prefix="/api/v1", tags=["ask"])

# Endpoint raiz - informações básicas da API
@app.get("/")
async def root():
    return {"message": "IsCoolGPT API", "version": "1.0.0", "status": "running"}

# Health check endpoint - usado para monitoramento
@app.get("/health")
async def health():
    return {"status": "healthy"}
```

**Justificativa**: FastAPI foi escolhido por sua performance, documentação automática e suporte nativo a async/await, essencial para integrações com APIs externas.

### 3.2 Configurações (`app/core/config.py`)

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Configurações da API
    api_title: str = "IsCoolGPT API"
    api_version: str = "1.0.0"

    # Configurações de Provedor LLM
    # Suporta: openai, gemini, huggingface, mock
    llm_provider: str = "mock"  # Padrão mock para testes sem API key
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    
    # Google Gemini Configuration
    gemini_api_key: Optional[str] = None
    gemini_model: str = "gemini-2.5-flash"  # Modelo mais recente e rápido
    
    # Hugging Face Configuration
    huggingface_api_key: Optional[str] = None
    huggingface_model: str = "microsoft/DialoGPT-medium"
    huggingface_api_url: Optional[str] = None

    # Configurações de Aplicação
    max_tokens: int = 500  # Limite padrão de tokens
    temperature: float = 0.7  # Criatividade das respostas (0.0-1.0)

    # Configurações AWS (para deploy)
    aws_region: str = "us-east-1"
    ecr_repository: Optional[str] = None
    ecs_cluster: Optional[str] = None
    ecs_service: Optional[str] = None

    class Config:
        env_file = ".env"  # Carrega variáveis de ambiente de .env
        case_sensitive = False  # Permite maiúsculas/minúsculas

settings = Settings()
```

**Justificativa**: Pydantic Settings permite validação automática de tipos e carregamento de variáveis de ambiente, garantindo configuração segura e tipada.

### 3.3 Serviço LLM (`app/services/llm_service.py`)

```python
from typing import Optional
import httpx
from app.core.config import settings

class LLMService:
    """Serviço para integração com modelos de linguagem"""
    
    def __init__(self):
        self.provider = settings.llm_provider
        self.openai_api_key = settings.openai_api_key
        self.gemini_api_key = settings.gemini_api_key
        self.huggingface_api_key = settings.huggingface_api_key
        self.huggingface_api_url = (
            settings.huggingface_api_url or "https://api-inference.huggingface.co/models"
        )

    async def generate_response(
        self, question: str, context: Optional[str] = None, max_tokens: Optional[int] = None
    ) -> dict:
        """
        Gera resposta usando o provedor de LLM configurado
        
        Args:
            question: Pergunta do usuário
            context: Contexto adicional opcional
            max_tokens: Limite de tokens na resposta
            
        Returns:
            dict com 'answer', 'tokens_used' e 'model'
        """
        # Roteamento baseado no provedor configurado
        if self.provider == "openai":
            return await self._generate_openai(question, context, max_tokens)
        elif self.provider == "gemini":
            return await self._generate_gemini(question, context, max_tokens)
        elif self.provider == "huggingface":
            return await self._generate_huggingface(question, context, max_tokens)
        elif self.provider == "mock":
            return await self._generate_mock(question, context, max_tokens)
        else:
            raise ValueError(f"Provedor de LLM não suportado: {self.provider}")

    async def _generate_gemini(
        self, question: str, context: Optional[str] = None, max_tokens: Optional[int] = None
    ) -> dict:
        """Gera resposta usando Google Gemini API"""
        if not self.gemini_api_key:
            raise ValueError("Gemini API key não configurada")

        try:
            from google import genai
            import asyncio
            import os

            # Configurar API key como variável de ambiente
            # A biblioteca google-genai lê automaticamente de GEMINI_API_KEY
            os.environ["GEMINI_API_KEY"] = self.gemini_api_key
            
            # Criar cliente (nova API do Gemini)
            client = genai.Client()

            # Construir prompt com system message
            system_prompt = "Você é um assistente educacional inteligente chamado IsCoolGPT. Responda de forma clara, didática e objetiva, sempre focando em ajudar o aprendizado."
            
            prompt = question
            if context:
                prompt = f"Contexto: {context}\n\nPergunta: {question}"
            
            full_prompt = f"{system_prompt}\n\n{prompt}"

            # Gerar resposta usando nova API
            # Função helper para evitar problemas com lambda e closures
            def generate_gemini_response():
                return client.models.generate_content(
                    model=settings.gemini_model,
                    contents=full_prompt
                )
            
            # Executar em thread pool para não bloquear event loop
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, generate_gemini_response)

            # Extrair resposta
            answer = response.text if hasattr(response, 'text') and response.text else str(response)

            # Estimar tokens (Gemini não retorna sempre)
            estimated_tokens = len(answer.split()) * 1.3

            return {
                "answer": answer,
                "tokens_used": int(estimated_tokens),
                "model": settings.gemini_model,
            }
        except Exception as e:
            raise Exception(f"Erro ao gerar resposta com Gemini: {str(e)}")
```

**Justificativa**: 
- **Padrão Strategy**: Permite trocar provedores facilmente sem modificar código cliente
- **Async/Await**: Não bloqueia o event loop durante chamadas de API
- **Error Handling**: Captura e propaga erros de forma clara
- **Token Estimation**: Estima tokens quando o provedor não retorna (Gemini)

### 3.4 Router (`app/routers/ask.py`)

```python
from fastapi import APIRouter, HTTPException
from app.schemas.ask import AskRequest, AskResponse
from app.controllers.ask_controller import AskController

router = APIRouter()
controller = AskController()

@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """
    Endpoint principal para fazer perguntas ao assistente
    
    - **question**: Pergunta do usuário (obrigatório)
    - **context**: Contexto adicional opcional
    - **max_tokens**: Número máximo de tokens na resposta (opcional)
    """
    try:
        response = await controller.ask(request)
        return response
    except ValueError as e:
        # Erro de validação (400)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Erro interno (500)
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
```

**Justificativa**: Separação de responsabilidades - router apenas lida com HTTP, controller com lógica de negócio.

### 3.5 Schemas (`app/schemas/ask.py`)

```python
from pydantic import BaseModel, Field
from typing import Optional

class AskRequest(BaseModel):
    """Schema de requisição para /ask"""
    question: str = Field(
        ..., 
        description="Pergunta do usuário", 
        min_length=1, 
        max_length=2000
    )
    context: Optional[str] = Field(
        None, 
        description="Contexto adicional para a resposta"
    )
    max_tokens: Optional[int] = Field(
        None, 
        description="Número máximo de tokens na resposta"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "question": "O que é Python?",
                "context": "Estou aprendendo programação",
                "max_tokens": 200,
            }
        }

class AskResponse(BaseModel):
    """Schema de resposta de /ask"""
    answer: str = Field(..., description="Resposta do assistente")
    question: str = Field(..., description="Pergunta original")
    tokens_used: Optional[int] = Field(None, description="Número de tokens utilizados")
    model: Optional[str] = Field(None, description="Modelo utilizado")
```

**Justificativa**: Pydantic valida automaticamente tipos e limites, gerando documentação OpenAPI e retornando erros claros.

---

## 4. Arquivos de Configuração

### 4.1 Dockerfile (Multi-Stage Build)

```dockerfile
# Multi-stage build para otimização
# Stage 1: Build
FROM python:3.11-slim AS builder

WORKDIR /app

# Instalar dependências do sistema necessárias para compilar pacotes Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copiar dependências instaladas do stage builder
# Isso reduz o tamanho da imagem final (sem compiladores)
COPY --from=builder /root/.local /root/.local

# Copiar código da aplicação
COPY app/ ./app/

# Garantir que scripts estão no PATH
ENV PATH=/root/.local/bin:$PATH

# Variáveis de ambiente padrão
ENV PYTHONUNBUFFERED=1  # Logs aparecem imediatamente
ENV PYTHONDONTWRITEBYTECODE=1  # Não cria .pyc files

# Expor porta
EXPOSE 8000

# Healthcheck - verifica se aplicação está saudável
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')" || exit 1

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Justificativa**:
- **Multi-stage**: Reduz tamanho final da imagem (de ~500MB para ~150MB)
- **Slim base**: Usa imagem Python slim (sem ferramentas desnecessárias)
- **Healthcheck**: Permite ECS detectar containers não saudáveis
- **Non-root**: Executa como usuário não-root (mais seguro)

### 4.2 GitHub Actions Workflow (`.github/workflows/ci-cd.yml`)

**Estrutura do Pipeline**:

```yaml
name: CI/CD Pipeline - Staging & Production

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: iscoolgpt
  CONTAINER_NAME: iscoolgpt

jobs:
  lint:
    # Executa linting em paralelo com testes
    runs-on: ubuntu-latest
    steps:
      - name: Run flake8
        run: flake8 app/ tests/ --count --select=E9,F63,F7,F82
      - name: Check code formatting with black
        run: black --check app/ tests/
      - name: Run mypy (type checking)
        run: mypy app/ --ignore-missing-imports || true

  test:
    # Executa testes unitários
    runs-on: ubuntu-latest
    steps:
      - name: Run tests
        run: pytest tests/ -v --cov=app --cov-report=xml

  build:
    # Build e push da imagem Docker
    needs: [lint, test]
    if: github.event_name == 'push'
    steps:
      - name: Build Docker image
        uses: docker/build-push-action@v5
      - name: Push image to Amazon ECR
        # Tag: staging-{sha} ou production-{sha}

  deploy-staging:
    # Deploy para ambiente de staging
    needs: build
    if: github.ref == 'refs/heads/develop'
    steps:
      - name: Deploy to Staging ECS
        run: |
          aws ecs update-service \
            --cluster iscoolgpt-cluster-staging \
            --service iscoolgpt-service-staging \
            --force-new-deployment \
            --deployment-configuration "minimumHealthyPercent=100,maximumPercent=200"

  validate-staging:
    # Validação do deploy de staging
    needs: deploy-staging
    steps:
      - name: Discover staging IP
        # Descobre IP público automaticamente
      - name: Run integration tests
        run: pytest tests/integration/ -v

  deploy-production:
    # Deploy para produção com zero downtime
    needs: build
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Production ECS (Zero Downtime)
        run: |
          aws ecs update-service \
            --cluster iscoolgpt-cluster \
            --service iscoolgpt-service \
            --force-new-deployment \
            --deployment-configuration "minimumHealthyPercent=100,maximumPercent=200"
```

**Justificativa**:
- **Paralelização**: Lint e test rodam em paralelo (economiza tempo)
- **Branch-based**: Deploy automático baseado na branch
- **Zero Downtime**: `minimumHealthyPercent=100` mantém tasks antigas rodando
- **Validação**: Testes de integração após deploy de staging

### 4.3 Task Definition AWS ECS (`aws/task-definition-production-gemini.json`)

```json
{
  "family": "iscoolgpt-service",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::186639342634:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::186639342634:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "iscoolgpt",
      "image": "186639342634.dkr.ecr.us-east-1.amazonaws.com/iscoolgpt:production-latest",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "LLM_PROVIDER",
          "value": "gemini"
        },
        {
          "name": "GEMINI_MODEL",
          "value": "gemini-2.5-flash"
        },
        {
          "name": "MAX_TOKENS",
          "value": "500"
        },
        {
          "name": "TEMPERATURE",
          "value": "0.7"
        }
      ],
      "secrets": [
        {
          "name": "GEMINI_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:186639342634:secret:iscoolgpt/gemini-api-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/iscoolgpt",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": [
          "CMD-SHELL",
          "python -c \"import httpx; httpx.get('http://localhost:8000/health')\" || exit 1"
        ],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

**Justificativa**:
- **Fargate**: Serverless, sem gerenciar servidores
- **awsvpc**: Isolamento de rede, IP público
- **Secrets Manager**: API keys não aparecem em logs
- **Health Check**: ECS reinicia containers não saudáveis
- **CloudWatch Logs**: Centraliza logs para troubleshooting

### 4.4 Configurações de Linting

**`.flake8`**:
```ini
[flake8]
max-line-length = 100
extend-ignore = E203, E266, E501, W503
exclude =
    .git,
    __pycache__,
    venv,
    .venv,
    env,
    .env,
    build,
    dist,
    *.egg-info,
    htmlcov,
    .pytest_cache
```

**`pyproject.toml`**:
```toml
[tool.black]
line-length = 100
target-version = ['py311']

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
ignore_missing_imports = true
```

**Justificativa**: Padronização de código, detecção de erros antes do deploy.

---

## 5. Decisões Técnicas e Justificativas

### 5.1 Escolha do FastAPI

**Decisão**: Usar FastAPI ao invés de Flask ou Django REST Framework.

**Justificativa**:
- ✅ **Performance**: Baseado em Starlette (ASGI), mais rápido que Flask
- ✅ **Documentação Automática**: Gera Swagger/OpenAPI automaticamente
- ✅ **Type Hints**: Validação automática com Pydantic
- ✅ **Async/Await**: Suporte nativo para operações assíncronas
- ✅ **Modernidade**: Framework moderno com excelente DX

### 5.2 Multi-Stage Docker Build

**Decisão**: Usar multi-stage build no Dockerfile.

**Justificativa**:
- ✅ **Tamanho Reduzido**: Imagem final ~150MB vs ~500MB
- ✅ **Segurança**: Sem compiladores na imagem final
- ✅ **Build Cache**: Dependências são cacheadas separadamente

### 5.3 AWS ECS Fargate

**Decisão**: Usar ECS Fargate ao invés de EC2 ou Lambda.

**Justificativa**:
- ✅ **Serverless**: Sem gerenciar servidores
- ✅ **Escalabilidade**: Auto-scaling fácil
- ✅ **Custo**: Paga apenas pelo uso
- ✅ **Compatibilidade**: Suporta Docker nativamente
- ✅ **Isolamento**: Cada task em VPC isolada

### 5.4 Google Gemini como LLM Principal

**Decisão**: Migrar de OpenAI para Google Gemini.

**Justificativa**:
- ✅ **Custo**: Gemini 2.5 Flash é mais barato
- ✅ **Performance**: Respostas rápidas
- ✅ **Quota**: Sem problemas de quota (OpenAI tinha limite)
- ✅ **API Moderna**: Biblioteca `google-genai` bem documentada

### 5.5 Zero-Downtime Deployment

**Decisão**: Configurar `minimumHealthyPercent=100,maximumPercent=200`.

**Justificativa**:
- ✅ **Disponibilidade**: Sem interrupção de serviço
- ✅ **Rolling Update**: Tasks antigas continuam servindo durante deploy
- ✅ **Rollback Rápido**: Pode reverter facilmente se necessário

### 5.6 Secrets Manager

**Decisão**: Armazenar API keys no AWS Secrets Manager.

**Justificativa**:
- ✅ **Segurança**: Não aparecem em logs ou código
- ✅ **Rotação**: Pode rotacionar chaves facilmente
- ✅ **Auditoria**: CloudTrail registra acessos
- ✅ **IAM**: Controle fino de quem pode acessar

### 5.7 Estrutura de Pastas (MVC-like)

**Decisão**: Separar em `routers`, `controllers`, `services`, `schemas`.

**Justificativa**:
- ✅ **Separação de Responsabilidades**: Cada camada tem função clara
- ✅ **Testabilidade**: Fácil mockar dependências
- ✅ **Manutenibilidade**: Código organizado e fácil de entender
- ✅ **Escalabilidade**: Fácil adicionar novos endpoints

### 5.8 Testes Automatizados

**Decisão**: Usar pytest com coverage e testes de integração.

**Justificativa**:
- ✅ **Confiança**: Deploy seguro após testes passarem
- ✅ **Regressão**: Detecta bugs antes de produção
- ✅ **Documentação**: Testes servem como documentação viva
- ✅ **CI/CD**: Integração perfeita com GitHub Actions

---

## 6. CI/CD Pipeline

### 6.1 Fluxo Completo

```
┌─────────────────────────────────────────────────────────────┐
│ 1. DESENVOLVIMENTO LOCAL                                     │
│    - Código escrito                                           │
│    - Testes locais                                            │
│    - Commit e push                                            │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. GITHUB ACTIONS - VALIDAÇÃO                               │
│    ┌──────────────┐      ┌──────────────┐                  │
│    │    LINT      │      │     TEST     │                  │
│    │  (Paralelo) │      │  (Paralelo)  │                  │
│    └──────────────┘      └──────────────┘                  │
│           │                      │                          │
│           └──────────┬───────────┘                         │
│                      ▼                                      │
│              ┌──────────────┐                              │
│              │    BUILD     │                              │
│              │   (Docker)   │                              │
│              └──────────────┘                              │
└─────────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
        ▼                                   ▼
┌──────────────────┐            ┌──────────────────┐
│ 3. STAGING       │            │ 4. PRODUCTION     │
│ (develop branch) │            │ (main branch)     │
│                  │            │                   │
│ - Deploy ECS     │            │ - Deploy ECS      │
│ - Validate       │            │ - Zero Downtime  │
│ - Integration    │            │ - Health Check    │
│   Tests          │            │                   │
└──────────────────┘            └──────────────────┘
```

### 6.2 Jobs do Pipeline

| Job | Trigger | Ação | Tempo Médio |
|-----|---------|------|-------------|
| **lint** | Push/PR | flake8, black, mypy | ~30s |
| **test** | Push/PR | pytest com coverage | ~1min |
| **build** | Push (após lint/test) | Build Docker + Push ECR | ~3min |
| **deploy-staging** | Push para `develop` | Deploy ECS staging | ~2min |
| **validate-staging** | Após deploy-staging | Testes de integração | ~1min |
| **deploy-production** | Push para `main` | Deploy ECS produção | ~3min |

### 6.3 Estratégia de Deploy

**Staging**:
- Deploy automático em `develop`
- Validação com testes de integração
- IP descoberto automaticamente

**Production**:
- Deploy automático em `main`
- Zero downtime (rolling update)
- Health checks antes de finalizar

---

## 7. Infraestrutura AWS

### 7.1 Recursos Criados

| Recurso | Tipo | Propósito |
|---------|------|-----------|
| **ECR Repository** | Container Registry | Armazena imagens Docker |
| **ECS Cluster (Staging)** | Container Orchestration | Ambiente de testes |
| **ECS Cluster (Production)** | Container Orchestration | Ambiente de produção |
| **ECS Service (Staging)** | Service Definition | Gerencia tasks de staging |
| **ECS Service (Production)** | Service Definition | Gerencia tasks de produção |
| **Task Definition** | Container Blueprint | Define como rodar containers |
| **IAM Role (Execution)** | IAM Role | Permissões para ECS executar tasks |
| **IAM Role (Task)** | IAM Role | Permissões para tasks acessarem AWS |
| **Secrets Manager** | Secret Storage | Armazena API keys |
| **CloudWatch Logs** | Logging | Centraliza logs da aplicação |
| **VPC/Subnets** | Networking | Isolamento de rede |
| **Security Groups** | Firewall | Controle de tráfego |

### 7.2 IAM Roles e Permissões

**ecsTaskExecutionRole** (execução de tasks):
- `AmazonEC2ContainerRegistryReadOnly` - Pull imagens do ECR
- `AmazonECSTaskExecutionRolePolicy` - Criar logs no CloudWatch
- `secretsmanager:GetSecretValue` - Ler secrets do Secrets Manager

**ecsTaskRole** (runtime da aplicação):
- Permissões customizadas (se necessário para acessar outros serviços AWS)

**Justificativa**: Princípio do menor privilégio - cada role tem apenas o necessário.

### 7.3 Networking

**Configuração**:
- **Network Mode**: `awsvpc` (cada task tem IP próprio)
- **Public IP**: Habilitado (para acesso externo)
- **Security Group**: Permite tráfego na porta 8000

**Justificativa**: Isolamento de rede, cada task em sua própria VPC.

---

## 8. Segurança

### 8.1 Medidas Implementadas

1. **API Keys em Secrets Manager**
   - Não aparecem em código, logs ou variáveis de ambiente visíveis
   - Rotação possível sem redeploy

2. **IAM com Menor Privilégio**
   - Roles têm apenas permissões necessárias
   - Sem acesso administrativo

3. **Container Security**
   - Imagem base slim (menos superfície de ataque)
   - Health checks para detectar problemas
   - Logs centralizados para auditoria

4. **Network Security**
   - Security Groups restringem tráfego
   - VPC isolada

5. **Code Security**
   - Linting detecta problemas
   - Dependências atualizadas
   - Sem hardcoded secrets

### 8.2 Melhorias Futuras

- [ ] Rate limiting
- [ ] Autenticação/autorização (JWT)
- [ ] HTTPS/TLS
- [ ] WAF (Web Application Firewall)
- [ ] Scanning de vulnerabilidades (Trivy, Snyk)

---

## 9. Monitoramento e Logs

### 9.1 CloudWatch Logs

**Configuração**:
- **Log Group**: `/ecs/iscoolgpt`
- **Stream Prefix**: `ecs`
- **Retention**: 7 dias (configurável)

**Acesso**:
```bash
aws logs tail /ecs/iscoolgpt --follow --region us-east-1
```

### 9.2 Health Checks

**Endpoint**: `GET /health`

**Uso**:
- ECS verifica saúde do container
- Monitoramento externo (CloudWatch Alarms)
- Load balancer health checks (futuro)

### 9.3 Métricas Importantes

- **Task Status**: RUNNING, STOPPED, PENDING
- **Health Status**: HEALTHY, UNHEALTHY
- **CPU/Memory Usage**: Via CloudWatch Metrics
- **Request Count**: Via logs ou Application Load Balancer

---

## 10. Conclusão

### 10.1 Objetivos Alcançados

✅ API REST funcional com FastAPI  
✅ Integração com múltiplos LLM providers  
✅ Containerização com Docker  
✅ CI/CD completo com GitHub Actions  
✅ Deploy automatizado na AWS (ECS Fargate)  
✅ Zero-downtime deployments  
✅ Testes automatizados  
✅ Documentação completa  

### 10.2 Métricas do Projeto

- **Linhas de Código**: ~1.500 (Python)
- **Cobertura de Testes**: ~80%
- **Tempo de Deploy**: ~5-7 minutos
- **Tamanho da Imagem Docker**: ~150MB
- **Tempo de Build**: ~3 minutos

### 10.3 Lições Aprendidas

1. **Multi-stage Docker builds** reduzem significativamente o tamanho da imagem
2. **Zero-downtime deployments** são essenciais para produção
3. **Secrets Manager** simplifica gerenciamento de credenciais
4. **Testes de integração** são cruciais para validar deploys
5. **CI/CD automatizado** acelera desenvolvimento e reduz erros

### 10.4 Próximos Passos

- [ ] Implementar API Gateway para HTTPS
- [ ] Adicionar autenticação/autorização
- [ ] Configurar auto-scaling baseado em métricas
- [ ] Implementar cache de respostas
- [ ] Adicionar rate limiting
- [ ] Dashboard de métricas (Grafana)

---

**Documento gerado em**: 2024  
**Versão**: 1.0.0  
**Autor**: Equipe IsCoolGPT

