# Diagrama de Arquitetura - IsCoolGPT

## Visão Geral

Este documento descreve a arquitetura do sistema IsCoolGPT, um assistente educacional inteligente com deploy automatizado na AWS.

## Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                         DESENVOLVIMENTO                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ git push
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         GITHUB REPOSITORY                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Código Fonte:                                            │  │
│  │  - FastAPI Backend                                        │  │
│  │  - Dockerfile                                             │  │
│  │  - GitHub Actions Workflow                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Trigger
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      GITHUB ACTIONS (CI/CD)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  1. TEST     │→ │  2. BUILD    │→ │  3. DEPLOY   │         │
│  │  (pytest)    │  │  (Docker)    │  │  (ECS)       │         │
│  └──────────────┘  └──────┬───────┘  └──────────────┘         │
└────────────────────────────┼────────────────────────────────────┘
                             │
                             │ Push Image
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         AWS ECR                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Docker Registry:                                        │  │
│  │  - iscoolgpt:latest                                      │  │
│  │  - iscoolgpt:{commit-sha}                                │  │
│  │  - Image Scanning (vulnerabilities)                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │ Pull Image
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         AWS ECS (FARGATE)                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Cluster: iscoolgpt-cluster                              │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Service: iscoolgpt-service                       │  │  │
│  │  │  ┌──────────────────────────────────────────────┐ │  │  │
│  │  │  │  Task Definition: iscoolgpt                  │ │  │  │
│  │  │  │  ┌────────────────────────────────────────┐  │ │  │  │
│  │  │  │  │  Container: iscoolgpt                  │  │ │  │  │
│  │  │  │  │  - Port: 8000                          │  │ │  │  │
│  │  │  │  │  - Health Check: /health               │  │ │  │  │
│  │  │  │  └────────────────────────────────────────┘  │ │  │  │
│  │  │  └──────────────────────────────────────────────┘ │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │ Network
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LOAD BALANCER                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  - Target Group: ECS Service                             │  │
│  │  - Health Checks                                         │  │
│  │  - SSL/TLS Termination                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        API GATEWAY                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  - REST API                                              │  │
│  │  - Endpoints:                                            │  │
│  │    - POST /api/v1/ask                                    │  │
│  │    - GET /health                                         │  │
│  │  - Rate Limiting                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │ Public Internet
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                           USUÁRIOS                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  - Aplicações Cliente                                    │  │
│  │  - Postman/curl                                          │  │
│  │  - Frontend (futuro)                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      SERVIÇOS EXTERNOS                          │
│  ┌──────────────┐              ┌──────────────┐                │
│  │   OpenAI     │              │   Hugging    │                │
│  │   API        │              │   Face API   │                │
│  │              │              │              │                │
│  │  GPT Models  │              │  Open Models │                │
│  └──────────────┘              └──────────────┘                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      SERVIÇOS AWS AUXILIARES                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Secrets     │  │  CloudWatch  │  │     IAM      │         │
│  │  Manager     │  │   Logs       │  │   Roles      │         │
│  │              │  │              │  │              │         │
│  │  API Keys    │  │  Monitoring  │  │  Permissions │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

## Componentes Detalhados

### 1. Código Fonte (GitHub)
- **FastAPI Backend**: Aplicação Python assíncrona
- **Estrutura Modular**: Controllers, Services, Schemas, Routers
- **Dockerfile**: Multi-stage build otimizado
- **Testes**: pytest com coverage

### 2. CI/CD Pipeline (GitHub Actions)
- **Test Stage**: Executa testes automatizados
- **Build Stage**: Constrói imagem Docker
- **Deploy Stage**: Push para ECR e atualiza ECS

### 3. AWS ECR (Elastic Container Registry)
- **Repositório**: Armazena imagens Docker
- **Image Scanning**: Verifica vulnerabilidades
- **Versionamento**: Tags por commit SHA e latest

### 4. AWS ECS (Elastic Container Service)
- **Cluster**: iscoolgpt-cluster
- **Service**: iscoolgpt-service
- **Launch Type**: Fargate (serverless)
- **Task Definition**: Especifica container, recursos, variáveis
- **Auto Scaling**: Configurável (futuro)

### 5. Application Load Balancer
- **Target Group**: Aponta para ECS Service
- **Health Checks**: Monitora saúde dos containers
- **SSL/TLS**: Terminação de certificados

### 6. API Gateway
- **REST API**: Endpoints públicos
- **Rate Limiting**: Proteção contra abuso
- **CORS**: Configurado para permitir acesso

### 7. Serviços Externos
- **OpenAI API**: Modelo GPT (padrão)
- **Hugging Face**: Alternativa de modelo open-source

### 8. Serviços AWS Auxiliares
- **Secrets Manager**: Armazena API keys de forma segura
- **CloudWatch**: Logs e monitoramento
- **IAM**: Permissões mínimas necessárias

## Fluxo de Dados

### 1. Requisição do Usuário
```
Usuário → API Gateway → ALB → ECS Service → Container FastAPI
```

### 2. Processamento
```
Container → LLM Service → OpenAI/Hugging Face API → Resposta
```

### 3. Resposta
```
Container → ECS → ALB → API Gateway → Usuário
```

## Segurança

1. **API Keys**: Armazenadas em AWS Secrets Manager
2. **IAM Roles**: Permissões mínimas (princípio do menor privilégio)
3. **Network**: Containers em VPC privada com acesso controlado
4. **HTTPS**: SSL/TLS em todas as comunicações públicas
5. **Image Scanning**: ECR escaneia imagens para vulnerabilidades

## Escalabilidade

- **Horizontal**: Múltiplas tasks no ECS Service
- **Auto Scaling**: Baseado em CPU/Memory (configurável)
- **Fargate**: Escala automaticamente sem gerenciar servidores

## Monitoramento

- **CloudWatch Logs**: Todos os logs da aplicação
- **Health Checks**: Endpoint `/health` monitorado
- **Métricas**: CPU, Memory, Request Count (CloudWatch)

## Custos

- **Fargate**: Pago por uso (CPU/Memory)
- **ECR**: Armazenamento de imagens
- **ALB**: Por hora + transferência de dados
- **API Gateway**: Por requisição
- **CloudWatch**: Logs e métricas

## Melhorias Futuras

1. **Auto Scaling**: Baseado em métricas de requisição
2. **Cache**: Redis para respostas frequentes
3. **CDN**: CloudFront para distribuição global
4. **Multi-region**: Alta disponibilidade
5. **Spot Instances**: Redução de custos (se usar EC2)

