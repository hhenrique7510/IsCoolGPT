# 🎯 Próximos Passos Práticos - GitHub Secrets ✅

## ✅ O Que Já Está Pronto

- ✅ Pipeline CI/CD completo
- ✅ Branch `develop` criada
- ✅ GitHub Secrets configurados
- ✅ Linting passando
- ✅ Testes passando
- ✅ Build funcionando

---

## 🔴 AGORA: Criar ECS Services (30 min - 1 hora)

### Opção 1: Via Console AWS (Mais Fácil) ⭐ RECOMENDADO

#### Passo 1: Criar Clusters

1. **Acesse:** AWS Console → ECS → Clusters
2. **Criar Cluster Staging:**
   - Clique em "Create Cluster"
   - Name: `iscoolgpt-cluster-staging`
   - Infrastructure: AWS Fargate (Serverless)
   - Create

3. **Criar Cluster Produção** (se não existir):
   - Name: `iscoolgpt-cluster`
   - Infrastructure: AWS Fargate (Serverless)
   - Create

#### Passo 2: Registrar Task Definitions

**Para Staging:**

1. **Acesse:** ECS → Task Definitions → Create new Task Definition
2. **Configurações:**
   - Family: `iscoolgpt-service-staging`
   - Launch type: Fargate
   - Task size:
     - CPU: 0.25 vCPU (256)
     - Memory: 0.5 GB (512)
3. **Container:**
   - Container name: `iscoolgpt`
   - Image URI: `186639342634.dkr.ecr.us-east-1.amazonaws.com/iscoolgpt:staging-latest`
   - Port mappings: 8000 (TCP)
   - Environment variables:
     - `LLM_PROVIDER`: `mock`
     - `OPENAI_MODEL`: `gpt-3.5-turbo`
   - Health check:
     - Command: `CMD-SHELL, python -c "import httpx; httpx.get('http://localhost:8000/health')" || exit 1`
     - Interval: 30
     - Timeout: 5
     - Retries: 3
     - Start period: 60
4. **Create**

**Para Produção:**

1. **Mesmo processo, mas:**
   - Family: `iscoolgpt-service`
   - Image URI: `186639342634.dkr.ecr.us-east-1.amazonaws.com/iscoolgpt:production-latest`
   - Environment: `LLM_PROVIDER`: `openai` (se tiver API key)

**OU usar os arquivos JSON prontos:**

```powershell
# Staging
aws ecs register-task-definition `
  --cli-input-json file://aws/task-definition-staging.json `
  --region us-east-1

# Produção
aws ecs register-task-definition `
  --cli-input-json file://aws/task-definition-production.json `
  --region us-east-1
```

#### Passo 3: Criar ECS Services

**Staging:**

1. **Acesse:** ECS → Clusters → `iscoolgpt-cluster-staging` → Services → Create
2. **Configurações:**
   - Service name: `iscoolgpt-service-staging`
   - Task Definition: `iscoolgpt-service-staging`
   - Desired tasks: 1
   - VPC: Escolha uma VPC (ou use default)
   - Subnets: Escolha subnets públicas (importante!)
   - Security group: 
     - Criar novo: `iscoolgpt-sg-staging`
     - Inbound rule: Porta 8000 de qualquer lugar (0.0.0.0/0)
   - Auto-assign public IP: **Enabled** ⚠️ IMPORTANTE!
3. **Create**

**Produção:**

1. **Mesmo processo:**
   - Cluster: `iscoolgpt-cluster`
   - Service name: `iscoolgpt-service`
   - Task Definition: `iscoolgpt-service`
   - Security group: `iscoolgpt-sg-production`

---

### Opção 2: Via CLI (Alternativa)

```powershell
# 1. Registrar Task Definitions
aws ecs register-task-definition `
  --cli-input-json file://aws/task-definition-staging.json `
  --region us-east-1

aws ecs register-task-definition `
  --cli-input-json file://aws/task-definition-production.json `
  --region us-east-1

# 2. Obter VPC e Subnets
aws ec2 describe-vpcs --region us-east-1
aws ec2 describe-subnets --region us-east-1 --filters "Name=map-public-ip-on-launch,Values=true"

# 3. Criar Security Groups
aws ec2 create-security-group `
  --group-name iscoolgpt-sg-staging `
  --description "Security group for IsCoolGPT Staging" `
  --vpc-id vpc-xxxxx `
  --region us-east-1

# 4. Adicionar regra de entrada
aws ec2 authorize-security-group-ingress `
  --group-id sg-xxxxx `
  --protocol tcp `
  --port 8000 `
  --cidr 0.0.0.0/0 `
  --region us-east-1

# 5. Criar ECS Services
aws ecs create-service `
  --cluster iscoolgpt-cluster-staging `
  --service-name iscoolgpt-service-staging `
  --task-definition iscoolgpt-service-staging `
  --desired-count 1 `
  --launch-type FARGATE `
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" `
  --region us-east-1
```

---

## 🧪 Testar Deploy (10 min)

### Testar Staging

```bash
# Na branch develop
git checkout develop
git commit --allow-empty -m "test: testar deploy staging"
git push origin develop
```

**Verificar:**
- Acesse: `https://github.com/hhenrique7510/IsCoolGPT/actions`
- Pipeline deve:
  - ✅ Lint
  - ✅ Testes
  - ✅ Build
  - ✅ Push para ECR
  - ✅ Deploy Staging (agora deve funcionar!)
  - ✅ Validação Staging

### Testar Produção

```bash
# Na branch main
git checkout main
git commit --allow-empty -m "test: testar deploy produção"
git push origin main
```

**Verificar:**
- Pipeline deve fazer deploy produção
- Zero downtime deployment

---

## 📋 Checklist

### Criar Recursos:
- [ ] ECS Cluster staging criado
- [ ] ECS Cluster produção criado (ou já existe)
- [ ] Task Definition staging registrada
- [ ] Task Definition produção registrada
- [ ] ECS Service staging criado
- [ ] ECS Service produção criado

### Testar:
- [ ] Pipeline staging testado
- [ ] Pipeline produção testado
- [ ] Deploy funcionando

---

## 🎯 Próximo Passo Imediato

**1. Criar ECS Services via Console AWS** (mais fácil)

Siga o **Passo 3** acima - leva cerca de 30 minutos.

**2. Depois testar:**

```bash
git checkout develop
git commit --allow-empty -m "test: testar deploy"
git push origin develop
```

---

## 💡 Dicas

- **Subnets públicas:** Importante para ter IP público
- **Security Group:** Porta 8000 aberta
- **Auto-assign public IP:** Deve estar Enabled
- **Task Definition:** Use os arquivos JSON prontos que criei

**Precisa de ajuda em algum passo específico?** 🚀

