# 🔑 Como Obter a Chave da OpenAI

## 📋 Passo a Passo Completo

### 1. Acessar o Portal da OpenAI

1. Acesse: **https://platform.openai.com/**
2. Faça login na sua conta OpenAI
   - Se não tiver conta, crie uma em: https://platform.openai.com/signup

### 2. Navegar para API Keys

1. Após fazer login, clique no seu **perfil/avatar** no canto superior direito
2. Selecione **"API keys"** ou **"View API keys"**
   
   **OU**
   
   Acesse diretamente: **https://platform.openai.com/api-keys**

### 3. Criar Nova Chave

1. Na página de API Keys, você verá:
   - Lista de chaves existentes (se houver)
   - Botão **"Create new secret key"** ou **"+ Create new secret key"**

2. Clique em **"Create new secret key"**

3. Uma janela/modal aparecerá pedindo:
   - **Name** (opcional): Dê um nome para identificar a chave (ex: "IsCoolGPT Production")
   - Clique em **"Create secret key"**

### 4. Copiar a Chave

1. **⚠️ IMPORTANTE:** A chave será mostrada **APENAS UMA VEZ**!
2. A chave começa com `sk-proj-` ou `sk-`
3. **Copie a chave imediatamente** e guarde em local seguro
4. Clique em **"Done"** ou feche a janela

**⚠️ ATENÇÃO:** Se você perder a chave, precisará criar uma nova!

---

## 🔍 Como Identificar a Chave

A chave da OpenAI tem o formato:
```
sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Ou (versões antigas):
```
sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Exemplo:**
```
sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
```

---

## 💰 Verificar Créditos/Plano

Antes de usar, verifique se você tem créditos:

1. Acesse: **https://platform.openai.com/account/usage**
2. Verifique seu **plano** e **créditos disponíveis**
3. Se necessário, adicione créditos em: **https://platform.openai.com/account/billing**

---

## 🔐 Segurança

### ✅ Boas Práticas:

1. **Nunca compartilhe** a chave publicamente
2. **Não commite** a chave no Git
3. **Use AWS Secrets Manager** para armazenar (como estamos fazendo)
4. **Rotacione** a chave periodicamente
5. **Revogue** chaves antigas que não usa mais

### ❌ O Que NÃO Fazer:

- ❌ Colocar a chave em código fonte
- ❌ Compartilhar em chats/mensagens
- ❌ Usar a mesma chave em múltiplos projetos sem controle
- ❌ Deixar a chave em arquivos de configuração locais

---

## 📝 Depois de Obter a Chave

### 1. Criar Secret no AWS Secrets Manager

**Via Console:**
1. Acesse: https://console.aws.amazon.com/secretsmanager/
2. Região: **us-east-1**
3. Clique em **"Store a new secret"**
4. Selecione **"Other type of secret"**
5. Cole a chave em **"Plaintext"**
6. Nome: `iscoolgpt/openai-api-key`
7. Clique em **"Store"**

**Via CLI:**
```powershell
aws secretsmanager create-secret `
  --name iscoolgpt/openai-api-key `
  --secret-string "sk-proj-sua-chave-aqui" `
  --description "OpenAI API Key for IsCoolGPT production" `
  --region us-east-1
```

### 2. Forçar Novo Deploy

```powershell
aws ecs update-service `
  --cluster iscoolgpt-cluster `
  --service iscoolgpt-service `
  --force-new-deployment `
  --region us-east-1
```

---

## 🆘 Problemas Comuns

### "Invalid API Key"
- Verifique se copiou a chave completa
- Certifique-se de que não há espaços extras
- Verifique se a chave não expirou

### "Insufficient Quota"
- Você não tem créditos suficientes
- Adicione créditos em: https://platform.openai.com/account/billing

### "API Key Not Found"
- A chave pode ter sido revogada
- Crie uma nova chave

### "Rate Limit Exceeded"
- Você excedeu o limite de requisições
- Aguarde ou atualize seu plano

---

## 🔗 Links Úteis

- **Portal OpenAI:** https://platform.openai.com/
- **API Keys:** https://platform.openai.com/api-keys
- **Usage/Billing:** https://platform.openai.com/account/usage
- **Documentação API:** https://platform.openai.com/docs
- **Pricing:** https://openai.com/pricing

---

## ✅ Checklist

- [ ] Tenho conta na OpenAI
- [ ] Tenho créditos disponíveis
- [ ] Criei uma nova API key
- [ ] Copiei a chave (começa com `sk-proj-` ou `sk-`)
- [ ] Guardei a chave em local seguro
- [ ] Vou criar o secret no AWS Secrets Manager
- [ ] Vou forçar novo deploy após criar o secret

---

## 🎯 Resumo Rápido

1. **Acesse:** https://platform.openai.com/api-keys
2. **Login** na sua conta
3. **Clique** em "Create new secret key"
4. **Copie** a chave (mostrada apenas uma vez!)
5. **Crie** o secret no AWS Secrets Manager
6. **Force** novo deploy

**Tempo estimado:** 5 minutos

