# Exemplos de Uso da API IsCoolGPT

Este documento contém exemplos práticos de como usar a API IsCoolGPT.

## Pré-requisitos

- API rodando em `http://localhost:8000` (local) ou URL pública (AWS)
- API key do OpenAI ou Hugging Face configurada

## Exemplos com cURL

### 1. Pergunta Simples

```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "O que é Python?"
  }'
```

**Resposta esperada:**
```json
{
  "answer": "Python é uma linguagem de programação de alto nível...",
  "question": "O que é Python?",
  "tokens_used": 150,
  "model": "gpt-3.5-turbo"
}
```

### 2. Pergunta com Contexto

```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Como posso melhorar meu código?",
    "context": "Estou aprendendo Python e meu código está muito longo"
  }'
```

### 3. Pergunta com Limite de Tokens

```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explique o que é uma API REST",
    "max_tokens": 200
  }'
```

### 4. Health Check

```bash
curl http://localhost:8000/health
```

**Resposta:**
```json
{
  "status": "healthy"
}
```

### 5. Informações da API

```bash
curl http://localhost:8000/
```

**Resposta:**
```json
{
  "message": "IsCoolGPT API",
  "version": "1.0.0",
  "status": "running"
}
```

## Exemplos com Python

### 1. Cliente Python Simples

```python
import requests

url = "http://localhost:8000/api/v1/ask"

payload = {
    "question": "O que é FastAPI?",
    "context": "Estou desenvolvendo uma API",
    "max_tokens": 300
}

response = requests.post(url, json=payload)
print(response.json())
```

### 2. Cliente Python com Tratamento de Erros

```python
import requests
from requests.exceptions import RequestException

def ask_question(question: str, context: str = None):
    url = "http://localhost:8000/api/v1/ask"
    
    payload = {
        "question": question,
        "context": context
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

# Uso
result = ask_question("O que é Docker?")
if result:
    print(f"Resposta: {result['answer']}")
```

### 3. Cliente Assíncrono com httpx

```python
import httpx
import asyncio

async def ask_async(question: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/ask",
            json={"question": question},
            timeout=30.0
        )
        return response.json()

# Uso
result = asyncio.run(ask_async("O que é CI/CD?"))
print(result)
```

## Exemplos com JavaScript/Node.js

### 1. Cliente Node.js com fetch

```javascript
async function askQuestion(question, context = null) {
  const url = 'http://localhost:8000/api/v1/ask';
  
  const payload = {
    question: question,
    context: context
  };
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload)
    });
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro:', error);
    return null;
  }
}

// Uso
askQuestion('O que é AWS?')
  .then(result => console.log(result))
  .catch(error => console.error(error));
```

### 2. Cliente Node.js com axios

```javascript
const axios = require('axios');

async function askWithAxios(question) {
  try {
    const response = await axios.post('http://localhost:8000/api/v1/ask', {
      question: question
    });
    return response.data;
  } catch (error) {
    console.error('Erro:', error.message);
    return null;
  }
}

askWithAxios('Explique o que é Kubernetes')
  .then(result => console.log(result));
```

## Exemplos de Perguntas Educacionais

### Programação

```bash
# Conceitos básicos
curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "O que é uma variável em programação?"}'

# Algoritmos
curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Explique o algoritmo de ordenação quicksort"}'

# Estruturas de dados
curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Qual a diferença entre lista e tupla em Python?"}'
```

### Cloud Computing

```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "O que é containerização e qual a diferença para virtualização?"}'

curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Explique o que é CI/CD e sua importância"}'
```

### Matemática

```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "Como calcular a derivada de uma função?"}'
```

## Testando com Postman

1. **Criar nova requisição POST**
   - URL: `http://localhost:8000/api/v1/ask`
   - Headers: `Content-Type: application/json`

2. **Body (raw JSON):**
```json
{
  "question": "O que é IsCoolGPT?",
  "context": "Estou testando a API",
  "max_tokens": 200
}
```

3. **Enviar requisição**

## Testando com Swagger UI

1. Acesse `http://localhost:8000/docs`
2. Expanda o endpoint `POST /api/v1/ask`
3. Clique em "Try it out"
4. Preencha o JSON:
```json
{
  "question": "Teste via Swagger"
}
```
5. Clique em "Execute"

## Tratamento de Erros

### Erro 400 - Bad Request
```json
{
  "detail": "Validation error"
}
```

### Erro 500 - Internal Server Error
```json
{
  "detail": "Erro interno: [mensagem]"
}
```

### Exemplo de tratamento em Python

```python
import requests

try:
    response = requests.post(
        "http://localhost:8000/api/v1/ask",
        json={"question": ""}  # Erro proposital
    )
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    print(f"Erro HTTP: {e}")
    print(f"Resposta: {response.json()}")
```

## Performance

Para testar performance com múltiplas requisições:

```python
import asyncio
import httpx
import time

async def make_request(client, question):
    response = await client.post(
        "http://localhost:8000/api/v1/ask",
        json={"question": question}
    )
    return response.json()

async def test_performance():
    questions = [
        "O que é Python?",
        "O que é Docker?",
        "O que é AWS?",
        "O que é FastAPI?",
        "O que é CI/CD?"
    ]
    
    start = time.time()
    async with httpx.AsyncClient() as client:
        tasks = [make_request(client, q) for q in questions]
        results = await asyncio.gather(*tasks)
    
    elapsed = time.time() - start
    print(f"Tempo total: {elapsed:.2f}s")
    print(f"Requisições por segundo: {len(questions)/elapsed:.2f}")

asyncio.run(test_performance())
```

