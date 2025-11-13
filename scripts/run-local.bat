@echo off
REM Script para rodar a aplicação localmente no Windows

echo 🚀 Iniciando IsCoolGPT localmente...

REM Verificar se .env existe
if not exist .env (
    echo ⚠️  Arquivo .env não encontrado. Copiando de env.example...
    copy env.example .env
    echo 📝 Por favor, edite o arquivo .env com suas credenciais
    pause
    exit /b 1
)

REM Verificar se venv existe
if not exist venv (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
)

REM Ativar venv
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Instalar dependências
echo 📥 Instalando dependências...
pip install -r requirements.txt

REM Rodar aplicação
echo ✅ Iniciando servidor...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause

