#!/bin/bash
# Script de deploy para AWS ECS

set -e

# Configurações
AWS_REGION=${AWS_REGION:-us-east-1}
ECR_REPOSITORY=${ECR_REPOSITORY:-iscoolgpt}
ECS_CLUSTER=${ECS_CLUSTER:-iscoolgpt-cluster}
ECS_SERVICE=${ECS_SERVICE:-iscoolgpt-service}
IMAGE_TAG=${IMAGE_TAG:-latest}

echo "🚀 Iniciando deploy do IsCoolGPT..."

# 1. Login no ECR
echo "📦 Fazendo login no ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.$AWS_REGION.amazonaws.com

# 2. Build da imagem
echo "🔨 Construindo imagem Docker..."
docker build -t $ECR_REPOSITORY:$IMAGE_TAG .

# 3. Tag da imagem
ECR_REGISTRY=$(aws sts get-caller-identity --query Account --output text).dkr.ecr.$AWS_REGION.amazonaws.com
docker tag $ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
docker tag $ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:latest

# 4. Push para ECR
echo "📤 Enviando imagem para ECR..."
docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest

# 5. Deploy no ECS
echo "🚀 Fazendo deploy no ECS..."
aws ecs update-service \
  --cluster $ECS_CLUSTER \
  --service $ECS_SERVICE \
  --force-new-deployment \
  --region $AWS_REGION

echo "✅ Deploy concluído!"

