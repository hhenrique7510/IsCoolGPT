# 🔐 Criar Secret: OpenAI API Key

## ❌ Problema

O secret `iscoolgpt/openai-api-key` não existe no AWS Secrets Manager, mas a task definition de produção precisa dele.

**Erro:**
```
ResourceNotFoundException: Secrets Manager can't find the specified secret.
```

---

## ✅ Solução

Criar o secret no AWS Secrets Manager com sua chave da OpenAI.

---

## 📋 Passo a Passo

### Opção 1: Via AWS Console (Recomendado)

1. **Acessar Secrets Manager:**
   - Acesse: https://console.aws.amazon.com/secretsmanager/
   - Certifique-se de estar na região: **us-east-1**

2. **Criar Secret:**
   - Clique em **"Store a new secret"**
   - Selecione **"Other type of secret"**
   - Em **"Plaintext"**, cole sua chave da OpenAI:
     ```
     sk-proj-...sua-chave-openai-aqui...
     ```
   - Clique em **"Next"**

3. **Configurar Nome:**
   - **Secret name:** `iscoolgpt/openai-api-key`
   - **Description:** `OpenAI API Key for IsCoolGPT production`
   - Clique em **"Next"**

4. **Configurar Rotação (Opcional):**
   - Deixe **"Disable automatic rotation"** (ou configure se quiser)
   - Clique em **"Next"**

5. **Revisar e Criar:**
   - Revise as configurações
   - Clique em **"Store"**

---

### Opção 2: Via AWS CLI

```powershell
# Criar secret com sua chave da OpenAI
aws secretsmanager create-secret \
  --name iscoolgpt/openai-api-key \
  --secret-string "sk-proj-...sua-chave-openai-aqui..." \
  --description "OpenAI API Key for IsCoolGPT production" \
  --region us-east-1
```

**⚠️ IMPORTANTE:** Substitua `sk-proj-...sua-chave-openai-aqui...` pela sua chave real da OpenAI!

---

## 🔍 Verificar Secret Criado

```powershell
# Verificar se o secret existe
aws secretsmanager describe-secret --secret-id iscoolgpt/openai-api-key --region us-east-1
```

---

## 🚀 Forçar Novo Deploy

Depois de criar o secret, force um novo deploy:

```powershell
aws ecs update-service \
  --cluster iscoolgpt-cluster \
  --service iscoolgpt-service \
  --force-new-deployment \
  --region us-east-1
```

---

## ✅ Verificar Status

Aguarde alguns minutos e verifique:

```powershell
# Verificar tasks rodando
aws ecs list-tasks --cluster iscoolgpt-cluster --service-name iscoolgpt-service --desired-status RUNNING --region us-east-1

# Verificar status do serviço
aws ecs describe-services --cluster iscoolgpt-cluster --services iscoolgpt-service --region us-east-1 --query "services[0].[status,runningCount,desiredCount]" --output table
```

---

## 🔐 Onde Obter a Chave da OpenAI?

1. Acesse: https://platform.openai.com/api-keys
2. Faça login na sua conta OpenAI
3. Clique em **"Create new secret key"**
4. Copie a chave (ela só aparece uma vez!)

**⚠️ IMPORTANTE:** 
- Guarde a chave em local seguro
- Não compartilhe a chave publicamente
- Se perder, crie uma nova

---

## 📝 Nota sobre Segurança

O AWS Secrets Manager é a **melhor prática** para armazenar chaves de API porque:
- ✅ Criptografado automaticamente
- ✅ Rotação automática (se configurado)
- ✅ Auditoria de acesso
- ✅ Integração nativa com ECS

---

## 🎯 Resumo

1. ✅ Acessar AWS Secrets Manager Console
2. ✅ Criar secret: `iscoolgpt/openai-api-key`
3. ✅ Adicionar sua chave da OpenAI
4. ✅ Forçar novo deploy do serviço
5. ✅ Verificar tasks iniciando corretamente

**Tempo estimado:** 5 minutos

---

## ⚠️ Alternativa Temporária (Não Recomendado)

Se você não quiser usar Secrets Manager agora, pode:

1. **Remover a referência ao secret** da task definition
2. **Usar variável de ambiente** diretamente (menos seguro)
3. **Usar Systems Manager Parameter Store** (alternativa)

Mas o **Secrets Manager é a melhor prática**! 🔐

