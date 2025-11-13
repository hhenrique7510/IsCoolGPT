#!/bin/bash
# Script para rodar a aplicação localmente

set -e

echo "🚀 Iniciando IsCoolGPT localmente..."

# Verificar se .env existe
if [ ! -f .env ]; then
    echo "⚠️  Arquivo .env não encontrado. Copiando de env.example..."
    cp env.example .env
    echo "📝 Por favor, edite o arquivo .env com suas credenciais"
    exit 1
fi

# Verificar se venv existe
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python -m venv venv
fi

# Ativar venv
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install -r requirements.txt

# Rodar aplicação
echo "✅ Iniciando servidor..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

