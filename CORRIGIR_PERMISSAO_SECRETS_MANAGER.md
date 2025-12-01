# 🔐 Corrigir Permissão: Secrets Manager

## ❌ Problema

O serviço de **produção** está falhando ao iniciar tasks porque o `ecsTaskExecutionRole` não tem permissão para acessar o AWS Secrets Manager.

**Erro:**
```
AccessDeniedException: User: arn:aws:sts::186639342634:assumed-role/ecsTaskExecutionRole/... 
is not authorized to perform: secretsmanager:GetSecretValue on resource: 
arn:aws:secretsmanager:us-east-1:186639342634:secret:iscoolgpt/openai-api-key
```

---

## ✅ Solução

Adicionar permissão para o `ecsTaskExecutionRole` acessar o secret `iscoolgpt/openai-api-key` no AWS Secrets Manager.

---

## 📋 Passo a Passo

### 1. Acessar IAM Console

1. Acesse: https://console.aws.amazon.com/iam/
2. No menu lateral, clique em **"Roles"**
3. Procure e clique em **`ecsTaskExecutionRole`**

### 2. Adicionar Política

1. Na aba **"Permissions"**, clique em **"Add permissions"** → **"Create inline policy"**
2. Clique em **"JSON"**
3. Cole o seguinte JSON:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue",
                "secretsmanager:DescribeSecret"
            ],
            "Resource": [
                "arn:aws:secretsmanager:us-east-1:186639342634:secret:iscoolgpt/openai-api-key*"
            ]
        }
    ]
}
```

4. Clique em **"Next"**
5. Nome da política: `ECSTaskExecutionSecretsManagerAccess`
6. Clique em **"Create policy"**

---

## 🔍 Verificar Secret Existe

Antes de corrigir, verifique se o secret existe:

```powershell
aws secretsmanager describe-secret --secret-id iscoolgpt/openai-api-key --region us-east-1
```

Se não existir, você precisa criar o secret primeiro:

```powershell
aws secretsmanager create-secret \
  --name iscoolgpt/openai-api-key \
  --secret-string "sua-chave-openai-aqui" \
  --region us-east-1
```

---

## 🚀 Forçar Novo Deploy

Depois de adicionar a permissão, force um novo deploy:

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

## 📝 Nota

Se você não quiser usar Secrets Manager, pode:

1. **Remover a referência ao secret** da task definition
2. **Usar variáveis de ambiente** diretamente (menos seguro)
3. **Usar Systems Manager Parameter Store** (alternativa ao Secrets Manager)

Mas o **Secrets Manager é a melhor prática** para armazenar chaves de API! 🔐

---

## 🎯 Resumo

1. ✅ Acessar IAM → Roles → `ecsTaskExecutionRole`
2. ✅ Adicionar inline policy com permissão `secretsmanager:GetSecretValue`
3. ✅ Forçar novo deploy do serviço
4. ✅ Verificar tasks iniciando corretamente

**Tempo estimado:** 5 minutos

