# Projeto Final Cloud 25.2: IsCoolGPT - Instruções

## Objetivo
Desenvolver um backend de assistente inteligente (tipo ChatGPT voltado para educação), totalmente containerizado, com deploy automatizado na AWS e seguindo boas práticas de DevOps.

**Foco: apenas backend. Não é necessário desenvolver frontend.**

---

## Requisitos Técnicos

### 1. API Backend (Python/FastAPI recomendado)
- Criar endpoint principal `/ask` que recebe perguntas dos usuários e responde via integração com modelo de linguagem (OpenAI, Hugging Face, etc.)
- Organizar código em módulos claros:
  - Controllers
  - Services
  - Schemas

### 2. Containerização
- Dockerfile otimizado (multi-stage) para o backend
- Configuração por variáveis de ambiente

### 3. Git e CI/CD
- Repositório GitHub com histórico limpo
- GitHub Actions configurado para:
  - Build automático do Docker
  - Execução de testes
  - Push da imagem para AWS ECR
  - Deploy automático no ECS

### 4. AWS
- **ECR**: Docker Registry
- **ECS**: Orquestração de containers
- **API Gateway**: Configurar API pública
- **IAM**: Permissões mínimas necessárias
- Automatizar deploy para staging e produção

### 5. Documentação e Evidências
- README detalhado com:
  - Instruções de deploy/local
  - Variáveis de ambiente
  - Exemplos de uso da API
- Diagrama de arquitetura (draw.io ou similar)
- Prints/vídeo mostrando:
  - Pipeline rodando
  - Deploy na AWS
  - Logs funcionando
  - Testes automatizados

---

## Extras Recomendados
- Monitoramento com CloudWatch
- Script de testes automatizados
- Otimização de custo e performance:
  - Instâncias spot
  - Auto-scaling

---

## Entregáveis

1. **Repositório GitHub** contendo:
   - Backend API
   - Dockerfile
   - CI/CD (GitHub Actions)
   - Exemplos de uso da API

2. **Aplicação rodando em ambiente cloud AWS** (acesso público)

3. **Documentação completa**:
   - README detalhado
   - Evidências visuais e/ou vídeo da solução funcionando

---

## Checklist de Entrega

- [ ] API backend funcional com endpoint `/ask`
- [ ] Código organizado em módulos (controllers, services, schemas)
- [ ] Dockerfile multi-stage otimizado
- [ ] Configuração via variáveis de ambiente
- [ ] Repositório GitHub com histórico limpo
- [ ] GitHub Actions configurado (build, testes, deploy)
- [ ] ECR configurado
- [ ] ECS configurado com deploy automático
- [ ] API Gateway configurado (acesso público)
- [ ] IAM com permissões mínimas
- [ ] Deploy automatizado staging/produção
- [ ] README completo
- [ ] Diagrama de arquitetura
- [ ] Evidências visuais/vídeo

