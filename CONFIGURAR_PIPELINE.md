# 🚀 Guia de Configuração do Pipeline CI/CD

## 📋 Pré-requisitos

### 1. GitHub Secrets

Configure os seguintes secrets no GitHub:
- **Settings** → **Secrets and variables** → **Actions**

**Obrigatórios:**
```
AWS_ACCESS_KEY_ID: <sua-chave-aws>
AWS_SECRET_ACCESS_KEY: <sua-chave-secreta-aws>
```

**Opcionais (para testes de integração):**
```
STAGING_API_URL: http://staging-api.iscoolgpt.example.com
PRODUCTION_API_URL: https://api.iscoolgpt.example.com
```

### 2. Branches

Certifique-se de ter as branches:
```bash
# Criar branch develop se não existir
git checkout -b develop
git push origin develop
```

### 3. Recursos AWS

**Staging:**
- ECS Cluster: `iscoolgpt-cluster-staging`
- ECS Service: `iscoolgpt-service-staging`
- Task Definition: `iscoolgpt-service-staging`

**Produção:**
- ECS Cluster: `iscoolgpt-cluster`
- ECS Service: `iscoolgpt-service`
- Task Definition: `iscoolgpt-service`

---

## 🔧 Como Criar Recursos AWS

### Criar Cluster ECS Staging:

```bash
aws ecs create-cluster \
  --cluster-name iscoolgpt-cluster-staging \
  --region us-east-1
```

### Criar Cluster ECS Produção:

```bash
aws ecs create-cluster \
  --cluster-name iscoolgpt-cluster \
  --region us-east-1
```

### Criar Task Definition:

1. Editar `aws/task-definition.json`
2. Substituir `ACCOUNT_ID` e `REGION`
3. Registrar:

```bash
# Staging
aws ecs register-task-definition \
  --cli-input-json file://aws/task-definition.json \
  --region us-east-1

# Produção (usar mesmo arquivo ou criar separado)
aws ecs register-task-definition \
  --cli-input-json file://aws/task-definition.json \
  --region us-east-1
```

### Criar ECS Service:

**Staging:**
```bash
aws ecs create-service \
  --cluster iscoolgpt-cluster-staging \
  --service-name iscoolgpt-service-staging \
  --task-definition iscoolgpt-service-staging \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --region us-east-1
```

**Produção:**
```bash
aws ecs create-service \
  --cluster iscoolgpt-cluster \
  --service-name iscoolgpt-service \
  --task-definition iscoolgpt-service \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --deployment-configuration "minimumHealthyPercent=100,maximumPercent=200" \
  --region us-east-1
```

---

## 🔄 Fluxo do Pipeline

### Desenvolvimento → Staging:

1. **Fazer alterações** no código
2. **Commit e push** para branch `develop`:
   ```bash
   git checkout develop
   git add .
   git commit -m "feat: nova funcionalidade"
   git push origin develop
   ```

3. **Pipeline executa automaticamente:**
   - ✅ Lint (flake8, black, mypy)
   - ✅ Testes unitários
   - ✅ Build Docker image
   - ✅ Deploy para staging
   - ✅ Validação (testes de integração + smoke tests)

### Staging → Produção:

1. **Merge** `develop` para `main`:
   ```bash
   git checkout main
   git merge develop
   git push origin main
   ```

2. **Pipeline executa automaticamente:**
   - ✅ Lint
   - ✅ Testes unitários
   - ✅ Build Docker image
   - ✅ Deploy para produção (zero downtime)
   - ✅ Health check

---

## 🧪 Testar Localmente

### Linting:

```bash
# Instalar ferramentas
pip install -r requirements-dev.txt

# Rodar flake8
flake8 app/ tests/

# Verificar formatação
black --check app/ tests/

# Type checking
mypy app/
```

### Testes:

```bash
# Testes unitários
pytest tests/ -v

# Testes de integração (requer API rodando)
STAGING_API_URL=http://localhost:8000 pytest tests/integration/ -v
```

### Build Docker:

```bash
# Build local
docker build -t iscoolgpt:latest .

# Testar
docker run -p 8000:8000 --env LLM_PROVIDER=mock iscoolgpt:latest
```

---

## 📊 Monitoramento

### Verificar Pipeline:

1. Acesse: `https://github.com/seu-usuario/IsCoolGPT/actions`
2. Veja os jobs executando:
   - `lint` - Verificação de código
   - `test` - Testes unitários
   - `build` - Build Docker
   - `deploy-staging` - Deploy staging (se branch develop)
   - `validate-staging` - Validação staging (se branch develop)
   - `deploy-production` - Deploy produção (se branch main)

### Verificar Deploy AWS:

```bash
# Ver status do serviço staging
aws ecs describe-services \
  --cluster iscoolgpt-cluster-staging \
  --services iscoolgpt-service-staging \
  --region us-east-1

# Ver status do serviço produção
aws ecs describe-services \
  --cluster iscoolgpt-cluster \
  --services iscoolgpt-service \
  --region us-east-1

# Ver logs
aws logs tail /ecs/iscoolgpt --follow --region us-east-1
```

---

## ⚠️ Troubleshooting

### Pipeline falha no lint:

```bash
# Rodar localmente para ver erros
flake8 app/ tests/
black --check app/ tests/
```

### Pipeline falha nos testes:

```bash
# Rodar testes localmente
pytest tests/ -v
```

### Deploy falha:

1. Verificar se AWS credentials estão configuradas
2. Verificar se ECS Service existe
3. Verificar logs no CloudWatch
4. Verificar permissões IAM

### Testes de integração falham:

1. Verificar se `STAGING_API_URL` está correto
2. Verificar se serviço está rodando
3. Verificar se health endpoint responde

---

## ✅ Checklist de Configuração

- [ ] GitHub Secrets configurados (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
- [ ] Branch `develop` criada
- [ ] ECS Cluster staging criado
- [ ] ECS Cluster produção criado
- [ ] Task Definitions registradas
- [ ] ECS Service staging criado
- [ ] ECS Service produção criado
- [ ] Pipeline testado (fazer commit e verificar Actions)
- [ ] Testes de integração funcionando (se configurado STAGING_API_URL)

---

## 🎯 Próximos Passos

1. **Configurar GitHub Secrets**
2. **Criar recursos AWS** (clusters, services)
3. **Fazer primeiro commit** e verificar pipeline
4. **Ajustar URLs** nos secrets se necessário
5. **Monitorar deploys** e ajustar conforme necessário

---

**Pronto para usar! 🚀**

