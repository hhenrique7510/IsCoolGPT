# 🔄 Migrar para Google Gemini API

## ✅ Suporte ao Gemini Adicionado!

O código agora suporta Google Gemini API! Siga os passos abaixo para migrar.

---

## 📋 Passo a Passo

### 1. Obter Chave da API Gemini

1. Acesse: https://aistudio.google.com/app/apikey
2. Faça login com sua conta Google
3. Clique em **"Create API Key"**
4. Selecione um projeto Google Cloud (ou crie um novo)
5. **Copie a chave** (começa com `AIza...`)

**⚠️ IMPORTANTE:** A chave é mostrada apenas uma vez! Guarde em local seguro.

---

### 2. Criar Secret no AWS Secrets Manager

#### Via Console:

1. Acesse: https://console.aws.amazon.com/secretsmanager/
2. Região: **us-east-1**
3. Clique em **"Store a new secret"**
4. Selecione **"Other type of secret"**
5. Cole sua chave do Gemini em **"Plaintext"**
6. Nome do secret: `iscoolgpt/gemini-api-key`
7. Clique em **"Store"**

#### Via CLI:

```powershell
aws secretsmanager create-secret `
  --name iscoolgpt/gemini-api-key `
  --secret-string "AIzaSuaChaveAqui" `
  --description "Google Gemini API Key for IsCoolGPT production" `
  --region us-east-1
```

---

### 3. Atualizar Task Definition

A task definition precisa ser atualizada para:
- Usar `LLM_PROVIDER=gemini`
- Referenciar o secret `iscoolgpt/gemini-api-key`

#### Atualizar via Console:

1. Acesse: https://console.aws.amazon.com/ecs/
2. Região: **us-east-1**
3. Clique em **"Task Definitions"**
4. Selecione: `iscoolgpt-service`
5. Clique em **"Create new revision"**
6. Na seção **"Environment variables"**, altere:
   - `LLM_PROVIDER`: `openai` → `gemini`
7. Na seção **"Secrets"**, altere:
   - `OPENAI_API_KEY` → Remover
   - Adicionar: `GEMINI_API_KEY` com valueFrom: `arn:aws:secretsmanager:us-east-1:186639342634:secret:iscoolgpt/gemini-api-key`
8. Clique em **"Create"**

#### Atualizar via CLI:

Atualize o arquivo `aws/task-definition-production.json` e registre:

```powershell
# Registrar nova revisão da task definition
aws ecs register-task-definition `
  --cli-input-json file://aws/task-definition-production.json `
  --region us-east-1
```

---

### 4. Atualizar Código (Já Feito!)

✅ Suporte ao Gemini já foi adicionado ao código:
- `app/core/config.py` - Configurações do Gemini
- `app/services/llm_service.py` - Método `_generate_gemini`
- `requirements.txt` - Biblioteca `google-generativeai`

---

### 5. Fazer Deploy

#### Opção A: Via Pipeline (Recomendado)

1. Commit e push para `main`:
   ```bash
   git add .
   git commit -m "feat: adicionar suporte ao Google Gemini API"
   git push origin main
   ```

2. O pipeline vai:
   - ✅ Build da imagem com nova dependência
   - ✅ Push para ECR
   - ✅ Deploy automático

#### Opção B: Deploy Manual

1. Build local:
   ```bash
   docker build -t iscoolgpt:gemini .
   ```

2. Tag e push:
   ```bash
   docker tag iscoolgpt:gemini 186639342634.dkr.ecr.us-east-1.amazonaws.com/iscoolgpt:production-latest
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 186639342634.dkr.ecr.us-east-1.amazonaws.com
   docker push 186639342634.dkr.ecr.us-east-1.amazonaws.com/iscoolgpt:production-latest
   ```

3. Atualizar task definition e forçar deploy:
   ```powershell
   aws ecs update-service `
     --cluster iscoolgpt-cluster `
     --service iscoolgpt-service `
     --task-definition iscoolgpt-service `
     --force-new-deployment `
     --region us-east-1
   ```

---

## 🔍 Verificar Funcionamento

Após o deploy, teste:

```powershell
$body = @{
    question = "O que é Python?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://54.167.87.101:8000/api/v1/ask" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

---

## 📝 Arquivos Modificados

- ✅ `app/core/config.py` - Adicionado `gemini_api_key` e `gemini_model`
- ✅ `app/services/llm_service.py` - Adicionado método `_generate_gemini`
- ✅ `requirements.txt` - Adicionado `google-generativeai>=0.3.0`

---

## 🎯 Resumo Rápido

1. ✅ Obter chave: https://aistudio.google.com/app/apikey
2. ✅ Criar secret: `iscoolgpt/gemini-api-key` no AWS Secrets Manager
3. ✅ Atualizar task definition: `LLM_PROVIDER=gemini` + secret `GEMINI_API_KEY`
4. ✅ Fazer deploy (via pipeline ou manual)
5. ✅ Testar API

---

## 💰 Vantagens do Gemini

- ✅ **Gratuito** (com limites generosos)
- ✅ **Sem necessidade de cartão de crédito** inicialmente
- ✅ **Boa qualidade** de respostas
- ✅ **API simples** e fácil de usar

---

## 🔗 Links Úteis

- **API Keys:** https://aistudio.google.com/app/apikey
- **Documentação:** https://ai.google.dev/docs
- **Pricing:** https://ai.google.dev/pricing
- **Console:** https://console.cloud.google.com/

---

**Depois de configurar, me avise para testarmos juntos!** 🚀

