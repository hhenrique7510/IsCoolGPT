#!/bin/bash
# Script para configurar recursos AWS (ECR, ECS, etc.)

set -e

AWS_REGION=${AWS_REGION:-us-east-1}
ECR_REPOSITORY=${ECR_REPOSITORY:-iscoolgpt}
ECS_CLUSTER=${ECS_CLUSTER:-iscoolgpt-cluster}
ECS_SERVICE=${ECS_SERVICE:-iscoolgpt-service}

echo "🔧 Configurando recursos AWS para IsCoolGPT..."

# 1. Criar repositório ECR
echo "📦 Criando repositório ECR..."
aws ecr create-repository \
  --repository-name $ECR_REPOSITORY \
  --region $AWS_REGION \
  --image-scanning-configuration scanOnPush=true \
  --image-tag-mutability MUTABLE \
  2>/dev/null || echo "Repositório ECR já existe"

# 2. Criar cluster ECS (Fargate)
echo "🏗️  Criando cluster ECS..."
aws ecs create-cluster \
  --cluster-name $ECS_CLUSTER \
  --region $AWS_REGION \
  2>/dev/null || echo "Cluster ECS já existe"

echo "✅ Configuração inicial concluída!"
echo ""
echo "⚠️  Próximos passos manuais:"
echo "1. Criar Task Definition no ECS"
echo "2. Criar Service no ECS"
echo "3. Configurar Application Load Balancer (se necessário)"
echo "4. Configurar API Gateway (se necessário)"
echo "5. Configurar IAM roles com permissões mínimas"

