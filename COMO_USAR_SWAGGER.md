# 📚 Como Usar o Swagger para Fazer Perguntas

## 🎯 Endpoint Principal

**URL:** `/api/v1/ask`  
**Método:** `POST`

---

## 📋 Passo a Passo no Swagger

### 1. Acessar o Swagger

1. Acesse a API em produção: `http://54.173.47.194:8000/docs`
   - Ou staging: `http://<IP-STAGING>:8000/docs`
   - Ou local: `http://localhost:8000/docs`

2. Você verá a documentação interativa do Swagger

### 2. Encontrar o Endpoint

1. Procure pela seção **"ask"**
2. Expanda o endpoint **`POST /api/v1/ask`**
3. Clique em **"Try it out"**

### 3. Preencher a Requisição

No campo **"Request body"**, você verá um JSON. Preencha assim:

#### Exemplo Básico (Mínimo Necessário):

```json
{
  "question": "O que é Python?"
}
```

#### Exemplo Completo (Com Todos os Campos):

```json
{
  "question": "O que é Python?",
  "context": "Estou aprendendo programação e quero entender melhor",
  "max_tokens": 200
}
```

### 4. Executar

1. Clique em **"Execute"**
2. Aguarde a resposta
3. Veja o resultado na seção **"Responses"**

---

## 📝 Campos da Requisição

### `question` (Obrigatório)
- **Tipo:** String
- **Descrição:** A pergunta que você quer fazer
- **Limites:** 
  - Mínimo: 1 caractere
  - Máximo: 2000 caracteres
- **Exemplo:** `"O que é Python?"`

### `context` (Opcional)
- **Tipo:** String
- **Descrição:** Contexto adicional para ajudar na resposta
- **Exemplo:** `"Estou aprendendo programação"`

### `max_tokens` (Opcional)
- **Tipo:** Integer
- **Descrição:** Número máximo de tokens na resposta
- **Exemplo:** `200`

---

## ✅ Exemplos de Perguntas

### Exemplo 1: Pergunta Simples

```json
{
  "question": "O que é Python?"
}
```

**Resposta esperada:**
```json
{
  "answer": "Python é uma linguagem de programação...",
  "question": "O que é Python?",
  "tokens_used": 150,
  "model": "gpt-3.5-turbo"
}
```

### Exemplo 2: Com Contexto

```json
{
  "question": "Como aprender Python?",
  "context": "Sou iniciante em programação"
}
```

### Exemplo 3: Com Limite de Tokens

```json
{
  "question": "Explique o que é machine learning",
  "max_tokens": 100
}
```

### Exemplo 4: Completo

```json
{
  "question": "Qual a diferença entre Python e JavaScript?",
  "context": "Estou escolhendo qual linguagem aprender primeiro",
  "max_tokens": 300
}
```

---

## 🔍 Resposta da API

### Estrutura da Resposta:

```json
{
  "answer": "Resposta do assistente...",
  "question": "Sua pergunta original",
  "tokens_used": 150,
  "model": "gpt-3.5-turbo"
}
```

### Campos da Resposta:

- **`answer`**: A resposta do assistente
- **`question`**: Sua pergunta (echo)
- **`tokens_used`**: Quantidade de tokens usados
- **`model`**: Modelo usado (ex: "gpt-3.5-turbo")

---

## ⚠️ Erros Comuns

### Erro 422: Validation Error

**Causa:** Campo `question` vazio ou muito longo

**Solução:**
```json
{
  "question": "Sua pergunta aqui"  // Não pode estar vazio!
}
```

### Erro 400: Bad Request

**Causa:** Formato JSON inválido ou campo incorreto

**Solução:** Verifique se o JSON está correto:
- Use aspas duplas `"` não simples `'`
- Vírgulas corretas
- Chaves e valores corretos

### Erro 500: Internal Server Error

**Causa:** Problema com a API da OpenAI ou configuração

**Solução:** 
- Verifique se o secret `iscoolgpt/openai-api-key` existe
- Verifique se há créditos na conta OpenAI
- Verifique os logs do ECS

---

## 🧪 Testando no Swagger

### Passo a Passo Visual:

1. **Acesse:** `http://54.173.47.194:8000/docs`

2. **Encontre:** Seção "ask" → `POST /api/v1/ask`

3. **Clique:** "Try it out"

4. **Preencha:**
   ```json
   {
     "question": "O que é inteligência artificial?"
   }
   ```

5. **Execute:** Clique em "Execute"

6. **Veja:** A resposta aparecerá abaixo

---

## 📱 Testando via cURL (Alternativa)

Se preferir testar via terminal:

```bash
curl -X POST "http://54.173.47.194:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "O que é Python?",
    "context": "Estou aprendendo programação"
  }'
```

### PowerShell:

```powershell
$body = @{
    question = "O que é Python?"
    context = "Estou aprendendo programação"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://54.173.47.194:8000/api/v1/ask" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

---

## 🎯 Dicas

1. **Perguntas Claras:** Faça perguntas específicas para melhores respostas
2. **Use Contexto:** O campo `context` ajuda o assistente a dar respostas mais relevantes
3. **Limite Tokens:** Use `max_tokens` para controlar o tamanho da resposta
4. **Teste Primeiro:** Use perguntas simples primeiro para verificar se está funcionando

---

## 📊 Exemplos Práticos

### Educação:

```json
{
  "question": "Explique o que é fotossíntese",
  "context": "Estou estudando biologia no ensino médio"
}
```

### Programação:

```json
{
  "question": "Como criar uma função em Python?",
  "context": "Sou iniciante em programação"
}
```

### Matemática:

```json
{
  "question": "Como calcular a derivada de x²?",
  "context": "Estou aprendendo cálculo"
}
```

---

## 🔗 Links Úteis

- **Swagger UI:** `http://54.173.47.194:8000/docs`
- **OpenAPI Schema:** `http://54.173.47.194:8000/openapi.json`
- **Health Check:** `http://54.173.47.194:8000/health`

---

## ✅ Resumo

1. **Acesse:** `/docs` na sua API
2. **Encontre:** `POST /api/v1/ask`
3. **Preencha:** JSON com `question` (obrigatório)
4. **Execute:** Clique em "Execute"
5. **Veja:** A resposta do assistente!

**Campo mínimo necessário:** `question` ✅

