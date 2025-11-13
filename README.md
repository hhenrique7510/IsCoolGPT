# IsCoolGPT - Assistente Educacional Inteligente

Assistente inteligente voltado para educação, desenvolvido com FastAPI, containerizado com Docker e deploy automatizado na AWS usando ECS/ECR.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Instalação Local](#instalação-local)
- [Uso da API](#uso-da-api)
- [Deploy na AWS](#deploy-na-aws)
- [CI/CD](#cicd)
- [Testes](#testes)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Estrutura do Projeto](#estrutura-do-projeto)

## 🎯 Visão Geral

IsCoolGPT é um backend de assistente inteligente focado em educação, que permite fazer perguntas e receber respostas através de integração com modelos de linguagem (OpenAI ou Hugging Face). O projeto segue boas práticas de DevOps, com containerização, CI/CD automatizado e deploy na AWS.

## 🏗️ Arquitetura

```
┌─────────────┐
│   GitHub    │
│ Repository  │
└──────┬──────┘
       │
       │ Push
       ▼
┌─────────────┐
│   GitHub    │
│   Actions   │──┐
│   (CI/CD)   │  │
└─────────────┘  │
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
┌─────────────┐   ┌─────────────┐
│   Tests     │   │  Build &    │
│   (pytest)  │   │  Push Image │
└─────────────┘   └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │  AWS ECR    │
                  │  (Registry) │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │  AWS ECS    │
                  │  (Fargate)  │
                  └──────┬──────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ API Gateway │
                  │  (Public)   │
                  └─────────────┘
```

### Componentes Principais

- **FastAPI**: Framework web assíncrono para Python
- **Docker**: Containerização da aplicação
- **AWS ECR**: Registry de imagens Docker
- **AWS ECS**: Orquestração de containers (Fargate)
- **API Gateway**: Exposição pública da API
- **GitHub Actions**: CI/CD automatizado
- **CloudWatch**: Monitoramento e logs

## 🛠️ Tecnologias

- **Python 3.11**
- **FastAPI** - Framework web
- **Docker** - Containerização
- **AWS ECS/ECR** - Deploy cloud
- **GitHub Actions** - CI/CD
- **OpenAI API** - Modelo de linguagem (padrão)
- **Hugging Face** - Alternativa de modelo de linguagem
- **pytest** - Testes automatizados

## 📦 Pré-requisitos

### Local
- Python 3.11+
- pip
- Docker (opcional, para containerização)

### AWS (para deploy)
- Conta AWS
- AWS CLI configurado
- Permissões IAM para:
  - ECR (push/pull imagens)
  - ECS (criar/atualizar serviços)
  - CloudWatch (logs)
  - Secrets Manager (se usar)

## 🚀 Instalação Local

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/IsCoolGPT.git
cd IsCoolGPT
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo `env.example` para `.env` e configure:

```bash
cp env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-3.5-turbo
```

### 5. Execute a aplicação

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: `http://localhost:8000`

### 6. Acesse a documentação interativa

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📡 Uso da API

### Endpoint Principal: `/api/v1/ask`

Faz uma pergunta ao assistente educacional.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "O que é Python?",
    "context": "Estou aprendendo programação",
    "max_tokens": 200
  }'
```

**Response:**
```json
{
  "answer": "Python é uma linguagem de programação de alto nível...",
  "question": "O que é Python?",
  "tokens_used": 150,
  "model": "gpt-3.5-turbo"
}
```

### Outros Endpoints

- `GET /` - Informações da API
- `GET /health` - Health check
- `GET /docs` - Documentação Swagger

## ☁️ Deploy na AWS

### 1. Configuração Inicial

Execute o script de setup:

```bash
chmod +x scripts/setup-aws.sh
./scripts/setup-aws.sh
```

Isso criará:
- Repositório ECR
- Cluster ECS

### 2. Configurar Secrets (AWS Secrets Manager)

Armazene a API key do OpenAI:

```bash
aws secretsmanager create-secret \
  --name iscoolgpt/openai-api-key \
  --secret-string "sua-chave-openai" \
  --region us-east-1
```

### 3. Criar Task Definition

Edite `aws/task-definition.json` substituindo:
- `ACCOUNT_ID`: Seu ID da conta AWS
- `REGION`: Sua região AWS

Registre a task definition:

```bash
aws ecs register-task-definition \
  --cli-input-json file://aws/task-definition.json \
  --region us-east-1
```

### 4. Criar Service ECS

```bash
aws ecs create-service \
  --cluster iscoolgpt-cluster \
  --service-name iscoolgpt-service \
  --task-definition iscoolgpt \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --region us-east-1
```

### 5. Deploy Manual (alternativa ao CI/CD)

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### 6. Configurar API Gateway (opcional)

Para expor a API publicamente via API Gateway, você pode:
- Criar um Application Load Balancer
- Conectar o ALB ao serviço ECS
- Criar API Gateway que aponta para o ALB

## 🔄 CI/CD

O projeto usa GitHub Actions para CI/CD automatizado. O pipeline:

1. **Test**: Executa testes automatizados
2. **Build**: Constrói imagem Docker
3. **Push**: Envia imagem para ECR
4. **Deploy**: Atualiza serviço ECS

### Configurar Secrets no GitHub

Adicione os seguintes secrets no repositório GitHub:

- `AWS_ACCESS_KEY_ID`: Sua chave de acesso AWS
- `AWS_SECRET_ACCESS_KEY`: Sua chave secreta AWS

### Workflow

O workflow está configurado em `.github/workflows/ci-cd.yml` e é acionado:
- Push para `main` ou `develop`
- Pull requests para `main`

## 🧪 Testes

### Executar testes

```bash
# Todos os testes
pytest

# Com coverage
pytest --cov=app --cov-report=html

# Testes específicos
pytest tests/test_main.py
```

### Estrutura de Testes

- `tests/test_main.py`: Testes dos endpoints principais
- `tests/test_llm_service.py`: Testes do serviço LLM

## 🔐 Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `LLM_PROVIDER` | Provedor LLM (openai/huggingface) | `openai` |
| `OPENAI_API_KEY` | Chave API OpenAI | - |
| `OPENAI_MODEL` | Modelo OpenAI | `gpt-3.5-turbo` |
| `HUGGINGFACE_API_KEY` | Chave API Hugging Face | - |
| `HUGGINGFACE_MODEL` | Modelo Hugging Face | `microsoft/DialoGPT-medium` |
| `MAX_TOKENS` | Máximo de tokens na resposta | `500` |
| `TEMPERATURE` | Temperatura do modelo | `0.7` |

## 📁 Estrutura do Projeto

```
IsCoolGPT/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicação FastAPI principal
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Configurações
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── ask.py              # Schemas Pydantic
│   ├── services/
│   │   ├── __init__.py
│   │   └── llm_service.py      # Serviço de integração LLM
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── ask_controller.py   # Controller de perguntas
│   └── routers/
│       ├── __init__.py
│       └── ask.py              # Rotas da API
├── tests/
│   ├── __init__.py
│   ├── test_main.py            # Testes principais
│   └── test_llm_service.py     # Testes do serviço LLM
├── scripts/
│   ├── deploy.sh               # Script de deploy
│   └── setup-aws.sh            # Script de setup AWS
├── aws/
│   ├── task-definition.json    # Task definition ECS
│   └── iam-policy.json         # Política IAM
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # GitHub Actions workflow
├── Dockerfile                  # Dockerfile multi-stage
├── .dockerignore               # Arquivos ignorados no Docker
├── requirements.txt            # Dependências Python
├── pytest.ini                  # Configuração pytest
├── env.example                 # Exemplo de variáveis de ambiente
└── README.md                   # Este arquivo
```

## 📊 Monitoramento

### CloudWatch Logs

Os logs da aplicação são enviados automaticamente para CloudWatch:
- Log Group: `/ecs/iscoolgpt`
- Stream: `ecs/iscoolgpt/{container-id}`

### Health Check

O endpoint `/health` pode ser usado para monitoramento:
```bash
curl http://localhost:8000/health
```

## 🔒 Segurança

- API keys armazenadas em AWS Secrets Manager
- IAM com permissões mínimas necessárias
- Imagens escaneadas no ECR (scanOnPush)
- Health checks configurados no ECS

## 🚀 Melhorias Futuras

- [ ] Auto-scaling baseado em métricas
- [ ] Cache de respostas frequentes
- [ ] Rate limiting
- [ ] Autenticação/autorização
- [ ] Suporte a múltiplos idiomas
- [ ] Dashboard de métricas
- [ ] Instâncias spot para redução de custos

## 📝 Licença

Este projeto é parte do Projeto Final Cloud 25.2.

## 👥 Contribuição

Este é um projeto acadêmico. Para sugestões ou melhorias, abra uma issue.

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação
2. Consulte os logs no CloudWatch
3. Abra uma issue no GitHub

---

**Desenvolvido com ❤️ para educação**
