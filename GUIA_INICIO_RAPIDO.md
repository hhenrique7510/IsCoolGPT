# 🚀 Guia de Início Rápido - IsCoolGPT

## Passo 1: Configurar Variáveis de Ambiente

Crie o arquivo `.env` a partir do exemplo:

```bash
# Windows (PowerShell)
Copy-Item env.example .env

# Linux/Mac
cp env.example .env
```

**IMPORTANTE**: Edite o arquivo `.env` e adicione sua chave da OpenAI:

```env
OPENAI_API_KEY=sk-sua-chave-aqui
```

> 💡 **Como obter a chave OpenAI?**
> 1. Acesse https://platform.openai.com/api-keys
> 2. Faça login ou crie uma conta
> 3. Clique em "Create new secret key"
> 4. Copie a chave e cole no arquivo `.env`

## Passo 2: Instalar Dependências

### Opção A: Ambiente Virtual (Recomendado)

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Opção B: Usar Script Automatizado

```bash
# Windows
scripts\run-local.bat

# Linux/Mac
chmod +x scripts/run-local.sh
./scripts/run-local.sh
```

## Passo 3: Testar Localmente

### Opção A: Comando Direto

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Opção B: Usar Makefile

```bash
make run
```

### Opção C: Docker Compose

```bash
docker-compose up --build
```

## Passo 4: Verificar se Está Funcionando

1. **Acesse a documentação interativa:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

2. **Teste o endpoint de health:**
   ```bash
   curl http://localhost:8000/health
   ```

3. **Teste o endpoint principal:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "O que é Python?"}'
   ```

   Ou use o Swagger UI em http://localhost:8000/docs para testar visualmente!

## Passo 5: Executar Testes

```bash
# Todos os testes
pytest

# Com coverage
pytest --cov=app --cov-report=html

# Ou usando Makefile
make test
```

## Passo 6: Preparar para Deploy (Opcional)

### 6.1. Configurar GitHub Secrets

Se você vai usar CI/CD, adicione no GitHub:
1. Vá em Settings → Secrets and variables → Actions
2. Adicione:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

### 6.2. Configurar AWS

```bash
# Instalar AWS CLI (se ainda não tiver)
# Windows: choco install awscli
# Linux: sudo apt install awscli
# Mac: brew install awscli

# Configurar credenciais
aws configure

# Executar setup inicial
chmod +x scripts/setup-aws.sh
./scripts/setup-aws.sh
```

## ✅ Checklist de Verificação

- [ ] Arquivo `.env` criado e configurado
- [ ] Chave OpenAI adicionada no `.env`
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Aplicação rodando localmente (porta 8000)
- [ ] Documentação acessível em `/docs`
- [ ] Teste do endpoint `/ask` funcionando
- [ ] Testes passando (`pytest`)

## 🐛 Problemas Comuns

### Erro: "ModuleNotFoundError"
**Solução**: Instale as dependências:
```bash
pip install -r requirements.txt
```

### Erro: "OPENAI_API_KEY não configurada"
**Solução**: Verifique se o arquivo `.env` existe e tem a chave correta.

### Erro: "Port 8000 already in use"
**Solução**: Use outra porta:
```bash
uvicorn app.main:app --reload --port 8001
```

### Erro no Windows: "venv\Scripts\Activate.ps1 cannot be loaded"
**Solução**: Execute no PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📚 Próximos Passos

1. ✅ Testar a API localmente
2. ✅ Ler `EXEMPLOS_USO.md` para mais exemplos
3. ✅ Configurar AWS para deploy (se necessário)
4. ✅ Fazer commit e push para GitHub
5. ✅ Configurar CI/CD no GitHub Actions

## 🆘 Precisa de Ajuda?

- Consulte o `README.md` para documentação completa
- Veja `EXEMPLOS_USO.md` para exemplos de uso
- Verifique `ARQUITETURA.md` para entender a arquitetura

