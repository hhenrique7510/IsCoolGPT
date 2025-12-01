# 🚀 Criar ECS Services - Guia Rápido

## ✅ O Que Você Já Tem

- ✅ GitHub Secrets configurados
- ✅ ECS Cluster criado
- ✅ Pipeline CI/CD funcionando

---

## 🎯 Próximo Passo: Criar ECS Services

### Opção 1: Via Console AWS (Mais Fácil) ⭐

#### Passo 1: Registrar Task Definitions

**Staging:**

1. **Acesse:** AWS Console → ECS → Task Definitions → Create new Task Definition
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

**Produção:**

1. **Mesmo processo, mas:**
   - Family: `iscoolgpt-service`
   - Image URI: `186639342634.dkr.ecr.us-east-1.amazonaws.com/iscoolgpt:production-latest`
   - Environment: `LLM_PROVIDER`: `openai` (ou `mock` se não tiver API key)

**OU usar arquivo JSON (mais rápido):**

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

#### Passo 2: Criar ECS Service Staging

1. **Acesse:** ECS → Clusters → Seu Cluster → Services → Create
2. **Configurações:**
   - Service name: `iscoolgpt-service-staging`
   - Task Definition: `iscoolgpt-service-staging` (a que você registrou)
   - Desired tasks: 1
   - VPC: Escolha uma VPC
   - Subnets: **Escolha subnets públicas** (marcadas como "Public subnet")
   - Security group: 
     - Criar novo: `iscoolgpt-sg-staging`
     - Inbound rule: 
       - Type: Custom TCP
       - Port: 8000
       - Source: 0.0.0.0/0 (qualquer lugar)
   - Auto-assign public IP: **Enabled** ⚠️ MUITO IMPORTANTE!
3. **Create**

#### Passo 3: Criar ECS Service Produção

1. **Mesmo processo:**
   - Service name: `iscoolgpt-service`
   - Task Definition: `iscoolgpt-service`
   - Cluster: Seu cluster de produção
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

# 3. Criar Security Group
aws ec2 create-security-group `
  --group-name iscoolgpt-sg-staging `
  --description "Security group for IsCoolGPT Staging" `
  --vpc-id vpc-xxxxx `
  --region us-east-1

# 4. Adicionar regra (porta 8000)
aws ec2 authorize-security-group-ingress `
  --group-id sg-xxxxx `
  --protocol tcp `
  --port 8000 `
  --cidr 0.0.0.0/0 `
  --region us-east-1

# 5. Criar ECS Service Staging
aws ecs create-service `
  --cluster iscoolgpt-cluster-staging `
  --service-name iscoolgpt-service-staging `
  --task-definition iscoolgpt-service-staging `
  --desired-count 1 `
  --launch-type FARGATE `
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" `
  --region us-east-1

# 6. Criar ECS Service Produção
aws ecs create-service `
  --cluster iscoolgpt-cluster `
  --service-name iscoolgpt-service `
  --task-definition iscoolgpt-service `
  --desired-count 1 `
  --launch-type FARGATE `
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" `
  --region us-east-1
```

---

## ⚠️ Pontos Importantes

1. **Subnets Públicas:** Use subnets marcadas como "Public subnet"
2. **Auto-assign Public IP:** Deve estar **Enabled**
3. **Security Group:** Porta 8000 aberta (0.0.0.0/0)
4. **Task Definition:** Use as imagens corretas:
   - Staging: `iscoolgpt:staging-latest`
   - Produção: `iscoolgpt:production-latest`

---

## 🧪 Testar Depois de Criar

### Testar Staging:

```bash
git checkout develop
git commit --allow-empty -m "test: testar deploy staging"
git push origin develop
```

**Verificar:**
- Pipeline deve fazer deploy staging
- ECS Service deve atualizar com nova imagem

### Testar Produção:

```bash
git checkout main
git commit --allow-empty -m "test: testar deploy produção"
git push origin main
```

**Verificar:**
- Pipeline deve fazer deploy produção
- Zero downtime deployment

---

## 📋 Checklist

- [ ] Task Definition staging registrada
- [ ] Task Definition produção registrada
- [ ] ECS Service staging criado
- [ ] ECS Service produção criado
- [ ] Security Groups configurados (porta 8000)
- [ ] Auto-assign public IP = Enabled
- [ ] Pipeline testado

---

## 🎯 Próximo Passo Imediato

**1. Registrar Task Definitions** (5 min)
- Use os arquivos JSON prontos ou crie no console

**2. Criar ECS Services** (15 min)
- Via console é mais fácil
- Lembre-se: Auto-assign public IP = Enabled!

**3. Testar** (5 min)
- Fazer commit e ver pipeline funcionar

---

**Precisa de ajuda em algum passo específico?** 🚀

