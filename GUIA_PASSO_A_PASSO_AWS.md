# 🚀 Guia Passo a Passo - Configurar AWS Completo

## 📋 Passo 1: Verificar GitHub Secrets (5 min)

### 1.1. Acessar GitHub Secrets

1. Acesse: `https://github.com/hhenrique7510/IsCoolGPT/settings/secrets/actions`
2. Verifique se existem:
   - ✅ `AWS_ACCESS_KEY_ID`
   - ✅ `AWS_SECRET_ACCESS_KEY`

### 1.2. Se Não Tiver, Adicionar:

1. Clique em **"New repository secret"**
2. **Secret 1:**
   - Name: `AWS_ACCESS_KEY_ID`
   - Value: Sua Access Key ID (formato: `AKIA...`)
   - Add secret

3. **Secret 2:**
   - Name: `AWS_SECRET_ACCESS_KEY`
   - Value: Sua Secret Access Key (formato: `wJalr...`)
   - Add secret

**Onde obter as credenciais:**
- Se já tem usuário IAM: AWS Console → IAM → Users → Seu usuário → Security credentials → Create access key
- Se não tem: Siga o guia em `COMO_CONECTAR_AWS.md`

---

## 📋 Passo 2: Preparar Task Definition (10 min)

### 2.1. Obter Account ID

```powershell
# Se AWS CLI estiver configurado
aws sts get-caller-identity

# Ou no AWS Console:
# Clique no seu nome (canto superior direito) → Account ID aparece
```

**Account ID encontrado:** `186639342634` (verifique se está correto)

### 2.2. Editar Task Definition

Edite o arquivo `aws/task-definition.json` e substitua:

- `ACCOUNT_ID` → `186639342634`
- `REGION` → `us-east-1`

**Arquivo já preparado:** Vou criar versões prontas para staging e produção.

---

## 📋 Passo 3: Criar ECS Services (30 min - 1 hora)

### 3.1. Via Console AWS (Recomendado - Mais Fácil)

#### A. Criar Cluster Staging

1. **Acesse:** AWS Console → ECS → Clusters
2. **Clique em:** "Create Cluster"
3. **Configurações:**
   - Cluster name: `iscoolgpt-cluster-staging`
   - Infrastructure: AWS Fargate (Serverless)
   - Clique em "Create"

#### B. Criar Cluster Produção (se não existir)

1. **Mesmo processo:**
   - Cluster name: `iscoolgpt-cluster`
   - Infrastructure: AWS Fargate (Serverless)
   - Clique em "Create"

#### C. Registrar Task Definition

1. **Acesse:** ECS → Task Definitions → Create new Task Definition
2. **Configurações:**
   - Family: `iscoolgpt-service-staging` (para staging) ou `iscoolgpt-service` (para produção)
   - Launch type: Fargate
   - Task size:
     - CPU: 0.25 vCPU (256)
     - Memory: 0.5 GB (512)
3. **Container:**
   - Container name: `iscoolgpt`
   - Image URI: `186639342634.dkr.ecr.us-east-1.amazonaws.com/iscoolgpt:latest`
   - Port mappings: 8000 (TCP)
   - Environment variables:
     - `LLM_PROVIDER`: `mock` (ou `openai` se tiver API key)
     - `OPENAI_MODEL`: `gpt-3.5-turbo`
   - Health check:
     - Command: `CMD-SHELL, python -c "import httpx; httpx.get('http://localhost:8000/health')" || exit 1`
     - Interval: 30
     - Timeout: 5
     - Retries: 3
     - Start period: 60
4. **Clique em:** "Create"

#### D. Criar ECS Service Staging

1. **Acesse:** ECS → Clusters → `iscoolgpt-cluster-staging` → Services → Create
2. **Configurações:**
   - Service name: `iscoolgpt-service-staging`
   - Task Definition: `iscoolgpt-service-staging` (ou a que criou)
   - Desired tasks: 1
   - VPC: Escolha uma VPC (ou use default)
   - Subnets: Escolha subnets públicas (marcadas como "Public subnet")
   - Security group: 
     - Criar novo ou usar existente
     - Inbound rules: Porta 8000 de qualquer lugar (0.0.0.0/0)
   - Auto-assign public IP: **Enabled** (importante!)
3. **Clique em:** "Create"

#### E. Criar ECS Service Produção

1. **Mesmo processo, mas:**
   - Cluster: `iscoolgpt-cluster`
   - Service name: `iscoolgpt-service`
   - Task Definition: `iscoolgpt-service`

### 3.2. Via CLI (Alternativa)

```powershell
# 1. Registrar Task Definition (já editada)
aws ecs register-task-definition `
  --cli-input-json file://aws/task-definition-staging.json `
  --region us-east-1

# 2. Obter VPC e Subnets
aws ec2 describe-vpcs --region us-east-1
aws ec2 describe-subnets --region us-east-1

# 3. Criar Security Group
aws ec2 create-security-group `
  --group-name iscoolgpt-sg `
  --description "Security group for IsCoolGPT" `
  --vpc-id vpc-xxxxx `
  --region us-east-1

# 4. Adicionar regra de entrada
aws ec2 authorize-security-group-ingress `
  --group-id sg-xxxxx `
  --protocol tcp `
  --port 8000 `
  --cidr 0.0.0.0/0 `
  --region us-east-1

# 5. Criar ECS Service
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

## 📋 Passo 4: Testar Deploy (10 min)

### 4.1. Testar Pipeline Staging

```bash
# Na branch develop
git checkout develop
git commit --allow-empty -m "test: testar deploy staging"
git push origin develop
```

**Verificar:**
- Acesse: `https://github.com/hhenrique7510/IsCoolGPT/actions`
- Veja o pipeline:
  - ✅ Lint
  - ✅ Testes
  - ✅ Build
  - ✅ Deploy Staging (deve funcionar agora!)
  - ✅ Validação Staging

### 4.2. Testar Pipeline Produção

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

## 📋 Passo 5: Obter URL Pública (30 min - 1 hora)

### Opção A: Application Load Balancer (Recomendado)

1. **Criar ALB:**
   - AWS Console → EC2 → Load Balancers → Create
   - Type: Application Load Balancer
   - Internet-facing
   - VPC e Subnets públicas
   - Security Group (porta 80/443)

2. **Criar Target Group:**
   - Type: IP
   - Port: 8000
   - Health check: `/health`

3. **Conectar ao ECS Service:**
   - No ECS Service, editar → Load balancing → Adicionar ALB

4. **Obter URL:**
   - ALB DNS name (ex: `iscoolgpt-alb-123456.us-east-1.elb.amazonaws.com`)

### Opção B: IP Público Direto (Mais Simples)

1. **No ECS Service:**
   - Tasks → Ver task rodando → Network → Public IP
   - URL: `http://<public-ip>:8000`

2. **Testar:**
   ```bash
   curl http://<public-ip>:8000/health
   ```

---

## ✅ Checklist Final

### Configuração Básica:
- [ ] GitHub Secrets configurados
- [ ] Task Definition editada (ACCOUNT_ID e REGION)
- [ ] ECS Cluster staging criado
- [ ] ECS Cluster produção criado
- [ ] ECS Service staging criado
- [ ] ECS Service produção criado

### Testes:
- [ ] Pipeline staging testado
- [ ] Pipeline produção testado
- [ ] Deploy funcionando

### API Pública:
- [ ] ALB ou IP público configurado
- [ ] URL pública obtida
- [ ] API acessível publicamente
- [ ] Health check funcionando

---

## 🎯 Próximos Passos

1. **Agora:** Verificar GitHub Secrets
2. **Hoje:** Criar ECS Services
3. **Esta Semana:** Configurar API Gateway/ALB
4. **Final:** Testar tudo e capturar evidências

---

**Precisa de ajuda em algum passo específico?** 🚀

