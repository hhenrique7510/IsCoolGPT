# 💰 Corrigir Quota/Créditos da OpenAI

## ❌ Problema

Você está recebendo o erro:
```
Error code: 429 - You exceeded your current quota, please check your plan and billing details.
```

**Isso significa:**
- ✅ A chave da API está **correta** (não é mais erro 401)
- ❌ Mas você **excedeu a cota** ou **não tem créditos** na conta OpenAI

---

## ✅ Solução

Adicionar créditos ou verificar o plano na conta OpenAI.

---

## 📋 Passo a Passo

### 1. Verificar Créditos e Uso

1. Acesse: https://platform.openai.com/account/usage
2. Faça login na sua conta OpenAI
3. Verifique:
   - **Créditos disponíveis**
   - **Uso recente**
   - **Limite de requisições**

### 2. Verificar Plano e Billing

1. Acesse: https://platform.openai.com/account/billing
2. Verifique:
   - **Plano atual** (Free tier, Pay-as-you-go, etc.)
   - **Limite de requisições por minuto/hora/dia**
   - **Histórico de pagamentos**

### 3. Adicionar Créditos (Se Necessário)

1. Acesse: https://platform.openai.com/account/billing
2. Clique em **"Add payment method"** ou **"Add credits"**
3. Adicione um método de pagamento
4. Adicione créditos à conta

### 4. Verificar Limites de Rate

Mesmo com créditos, você pode ter limites de rate (requisições por minuto):

- **Free tier:** Limites muito baixos
- **Pay-as-you-go:** Limites maiores
- **Enterprise:** Limites customizados

---

## 🔍 Verificar Status da Conta

### Opção 1: Via Console Web

1. Acesse: https://platform.openai.com/account
2. Verifique:
   - **Usage:** https://platform.openai.com/account/usage
   - **Billing:** https://platform.openai.com/account/billing
   - **API Keys:** https://platform.openai.com/api-keys

### Opção 2: Via API (Teste Rápido)

```powershell
# Testar se a chave funciona (pode retornar erro de quota)
$headers = @{
    "Authorization" = "Bearer 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"
    "Content-Type" = "application/json"
}

$body = @{
    model = "gpt-3.5-turbo"
    messages = @(
        @{
            role = "user"
            content = "Hello"
        }
    )
    max_tokens = 10
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "https://api.openai.com/v1/chat/completions" -Method POST -Headers $headers -Body $body
    Write-Host "✅ Chave funciona! Resposta recebida."
} catch {
    Write-Host "❌ Erro: $($_.Exception.Message)"
}
```

---

## 💡 Soluções Rápidas

### Solução 1: Adicionar Créditos

1. Acesse: https://platform.openai.com/account/billing
2. Adicione método de pagamento
3. Adicione créditos ($5, $10, $20, etc.)

### Solução 2: Aguardar Reset do Rate Limit

Se você excedeu o rate limit (requisições por minuto):
- Aguarde alguns minutos
- Tente novamente

### Solução 3: Verificar Plano

Se estiver no **Free tier**:
- Considere fazer upgrade para **Pay-as-you-go**
- Free tier tem limites muito baixos

### Solução 4: Usar Mock Provider (Desenvolvimento)

Para desenvolvimento/testes sem usar créditos:

1. Altere a variável de ambiente `LLM_PROVIDER` para `mock`
2. A API retornará respostas simuladas
3. Não consome créditos da OpenAI

---

## 🔄 Alternativa: Usar Mock Provider Temporariamente

Se você quiser testar a API sem usar créditos da OpenAI:

### Atualizar Task Definition

Modifique a task definition para usar `LLM_PROVIDER=mock`:

```json
{
  "environment": [
    {
      "name": "LLM_PROVIDER",
      "value": "mock"
    }
  ]
}
```

Isso fará a API retornar respostas simuladas sem chamar a OpenAI.

---

## 📊 Entender os Erros

### Erro 401: Invalid API Key
- **Causa:** Chave incorreta
- **Solução:** Verificar/corrigir a chave

### Erro 429: Insufficient Quota
- **Causa:** Sem créditos ou excedeu limite
- **Solução:** Adicionar créditos ou aguardar reset

### Erro 429: Rate Limit
- **Causa:** Muitas requisições por minuto
- **Solução:** Aguardar alguns minutos

---

## 🎯 Checklist

- [ ] Verifiquei créditos em: https://platform.openai.com/account/usage
- [ ] Verifiquei billing em: https://platform.openai.com/account/billing
- [ ] Adicionei créditos (se necessário)
- [ ] Verifiquei o plano atual
- [ ] Aguardei reset do rate limit (se aplicável)
- [ ] Testei novamente a API

---

## 🔗 Links Úteis

- **Usage:** https://platform.openai.com/account/usage
- **Billing:** https://platform.openai.com/account/billing
- **API Keys:** https://platform.openai.com/api-keys
- **Pricing:** https://openai.com/pricing
- **Error Codes:** https://platform.openai.com/docs/guides/error-codes

---

## 💰 Preços Aproximados

- **GPT-3.5-turbo:** ~$0.001-0.002 por 1K tokens
- **GPT-4:** ~$0.03-0.06 por 1K tokens

**Exemplo:**
- 1000 perguntas com ~500 tokens cada = ~500K tokens
- Custo aproximado: $0.50 - $1.00 (GPT-3.5-turbo)

---

## 🎯 Resumo

1. ✅ A chave está correta (não é mais erro 401)
2. ❌ Você precisa adicionar créditos na conta OpenAI
3. 🔗 Acesse: https://platform.openai.com/account/billing
4. 💳 Adicione método de pagamento e créditos
5. 🧪 Teste novamente após adicionar créditos

**Ou use `LLM_PROVIDER=mock` para desenvolvimento sem custos!**

---

**Depois de adicionar créditos, me avise para testarmos juntos!** 🚀

