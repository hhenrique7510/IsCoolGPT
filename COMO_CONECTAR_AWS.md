# ☁️ Como Conectar à AWS - Guia Completo

Este guia vai te ajudar a conectar seu projeto IsCoolGPT à AWS para fazer deploy automatizado.

---

## 📋 Índice

1. [Criar Conta AWS](#1-criar-conta-aws)
2. [Instalar AWS CLI](#2-instalar-aws-cli)
3. [Criar Usuário IAM](#3-criar-usuário-iam)
4. [Configurar AWS CLI Localmente](#4-configurar-aws-cli-localmente)
5. [Criar Recursos AWS](#5-criar-recursos-aws)
6. [Configurar GitHub Secrets](#6-configurar-github-secrets)
7. [Testar Conexão](#7-testar-conexão)

---

## 1. Criar Conta AWS

### Passo 1.1: Acessar AWS

1. Acesse: https://aws.amazon.com/
2. Clique em **"Sign In to the Console"** ou **"Create an AWS Account"**
3. Siga o processo de criação de conta
4. **Importante:** Você precisará de um cartão de crédito (mas há tier gratuito)

### Passo 1.2: Verificar Conta

- Faça login no AWS Console: https://console.aws.amazon.com/
- Anote seu **Account ID** (aparece no canto superior direito ao clicar no seu nome)

---

## 2. Instalar AWS CLI

### Windows (PowerShell)

**Opção A: Com Chocolatey (Recomendado)**
```powershell
# Se não tiver Chocolatey, instale primeiro:
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar AWS CLI
choco install awscli
```

**Opção B: Download Manual**
1. Baixe o instalador: https://awscli.amazonaws.com/AWSCLIV2.msi
2. Execute o instalador
3. Siga as instruções

**Opção C: Com pip**
```powershell
pip install awscli
```

### Verificar Instalação

```powershell
aws --version
# Deve mostrar algo como: aws-cli/2.x.x
```

---

## 3. Criar Usuário IAM

### Passo 3.1: Acessar IAM

1. No AWS Console, procure por **"IAM"** na barra de busca
2. Clique em **IAM** → **Users** (no menu lateral)
3. Clique em **"Add users"**

### Passo 3.2: Criar Usuário

1. **Nome do usuário:** `github-actions-iscoolgpt`
2. **Tipo de acesso:** Selecione **"Access key - Programmatic access"**
3. Clique em **"Next: Permissions"**

### Passo 3.3: Adicionar Permissões

1. Selecione **"Attach policies directly"**
2. Adicione as seguintes políticas:
   - ✅ `AmazonEC2ContainerRegistryFullAccess`
   - ✅ `AmazonECS_FullAccess`
   - ✅ `AmazonEC2ContainerServiceFullAccess`
   - ✅ `SecretsManagerReadWrite` (opcional, se usar Secrets Manager)

3. Clique em **"Next: Tags"** (pode pular)
4. Clique em **"Next: Review"**
5. Clique em **"Create user"**

### Passo 3.4: Salvar Credenciais ⚠️ IMPORTANTE

**Você verá uma tela com:**
- **Access Key ID:** `AKIA...` (copie e salve!)
- **Secret Access Key:** `wJalr...` (copie e salve!)

⚠️ **ATENÇÃO:** Esta é a ÚNICA vez que você verá a Secret Access Key. Salve em local seguro!

**Salve em um arquivo temporário:**
```
Access Key ID: AKIA...
Secret Access Key: wJalr...
```

---

## 4. Configurar AWS CLI Localmente

### Passo 4.1: Configurar Credenciais

```powershell
aws configure
```

Você será perguntado:

1. **AWS Access Key ID:** Cole a Access Key ID que salvou
2. **AWS Secret Access Key:** Cole a Secret Access Key que salvou
3. **Default region name:** Digite `us-east-1` (ou outra região de preferência)
4. **Default output format:** Digite `json`

### Passo 4.2: Verificar Configuração

```powershell
# Testar conexão
aws sts get-caller-identity

# Deve retornar algo como:
# {
#     "UserId": "...",
#     "Account": "123456789012",
#     "Arn": "arn:aws:iam::123456789012:user/github-actions-iscoolgpt"
# }
```

✅ Se funcionou, você está conectado!

---

## 5. Criar Recursos AWS

### Passo 5.1: Criar ECR Repository

```powershell
aws ecr create-repository `
  --repository-name iscoolgpt `
  --region us-east-1 `
  --image-scanning-configuration scanOnPush=true `
  --image-tag-mutability MUTABLE
```

**Resultado esperado:**
```json
{
    "repository": {
        "repositoryUri": "123456789012.dkr.ecr.us-east-1.amazonaws.com/iscoolgpt",
        ...
    }
}
```

**Anote o `repositoryUri`!** Você precisará dele depois.

### Passo 5.2: Criar ECS Cluster

```powershell
aws ecs create-cluster `
  --cluster-name iscoolgpt-cluster `
  --region us-east-1
```

### Passo 5.3: Criar Secrets Manager (Opcional)

Se quiser armazenar a API key da OpenAI no AWS Secrets Manager:

```powershell
aws secretsmanager create-secret `
  --name iscoolgpt/openai-api-key `
  --secret-string "sk-sua-chave-openai-aqui" `
  --region us-east-1
```

---

## 6. Configurar GitHub Secrets

### Passo 6.1: Acessar GitHub

1. Vá para seu repositório no GitHub
2. Clique em **Settings** (no topo)
3. No menu lateral, clique em **Secrets and variables** → **Actions**

### Passo 6.2: Adicionar Secrets

**Secret 1: AWS_ACCESS_KEY_ID**
1. Clique em **"New repository secret"**
2. **Name:** `AWS_ACCESS_KEY_ID`
3. **Secret:** Cole sua Access Key ID (AKIA...)
4. Clique em **"Add secret"**

**Secret 2: AWS_SECRET_ACCESS_KEY**
1. Clique em **"New repository secret"** novamente
2. **Name:** `AWS_SECRET_ACCESS_KEY`
3. **Secret:** Cole sua Secret Access Key (wJalr...)
4. Clique em **"Add secret"**

### Passo 6.3: Verificar

Você deve ver os dois secrets listados:
- ✅ `AWS_ACCESS_KEY_ID`
- ✅ `AWS_SECRET_ACCESS_KEY`

⚠️ Os valores aparecem mascarados por segurança (isso é normal).

---

## 7. Testar Conexão

### Passo 7.1: Testar Localmente

```powershell
# Verificar se consegue acessar ECR
aws ecr describe-repositories --region us-east-1

# Verificar se consegue acessar ECS
aws ecs describe-clusters --clusters iscoolgpt-cluster --region us-east-1
```

### Passo 7.2: Testar GitHub Actions

1. Faça um commit vazio para triggerar o pipeline:
```powershell
git commit --allow-empty -m "test: trigger CI/CD with AWS"
git push origin main
```

2. Vá em **Actions** no GitHub
3. Clique no workflow mais recente
4. Agora deve passar em:
   - ✅ Run Tests
   - ✅ Build Docker Image
   - ✅ Push to ECR (se AWS configurado)
   - ✅ Deploy to ECS (se ECS configurado)

---

## 🎯 Próximos Passos (Opcional)

### Criar Task Definition e ECS Service

Se quiser fazer deploy completo no ECS, você precisará:

1. **Editar `aws/task-definition.json`:**
   - Substituir `ACCOUNT_ID` pelo seu Account ID
   - Substituir `REGION` por `us-east-1` (ou sua região)

2. **Registrar Task Definition:**
```powershell
aws ecs register-task-definition `
  --cli-input-json file://aws/task-definition.json `
  --region us-east-1
```

3. **Criar ECS Service:**
```powershell
aws ecs create-service `
  --cluster iscoolgpt-cluster `
  --service-name iscoolgpt-service `
  --task-definition iscoolgpt `
  --desired-count 1 `
  --launch-type FARGATE `
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" `
  --region us-east-1
```

⚠️ **Nota:** Para criar o service, você precisará de VPC, Subnets e Security Groups configurados. Isso é mais avançado.

---

## ✅ Checklist de Configuração

Marque conforme for completando:

- [ ] Conta AWS criada
- [ ] AWS CLI instalado (`aws --version`)
- [ ] Usuário IAM criado com permissões
- [ ] Credenciais AWS salvas em local seguro
- [ ] AWS CLI configurado localmente (`aws configure`)
- [ ] Conexão testada (`aws sts get-caller-identity`)
- [ ] ECR Repository criado
- [ ] ECS Cluster criado
- [ ] GitHub Secrets configurados
- [ ] Pipeline GitHub Actions testado

---

## 🐛 Problemas Comuns

### Erro: "Unable to locate credentials"

**Solução:**
```powershell
aws configure
# Configure novamente com suas credenciais
```

### Erro: "Access Denied"

**Solução:**
- Verifique se o usuário IAM tem as permissões corretas
- Verifique se as políticas foram anexadas corretamente

### Erro: "Repository already exists"

**Solução:**
- Isso é normal! O repositório já existe, pode continuar.

### Erro no GitHub Actions: "Invalid credentials"

**Solução:**
- Verifique se os secrets no GitHub estão com os nomes exatos:
  - `AWS_ACCESS_KEY_ID` (não `AWS_ACCESS_KEY`)
  - `AWS_SECRET_ACCESS_KEY` (não `AWS_SECRET_KEY`)
- Verifique se não há espaços extras ao copiar/colar

---

## 💰 Custos AWS

### Tier Gratuito (Free Tier)

- **ECR:** 500 MB de armazenamento por mês (gratuito)
- **ECS Fargate:** Primeiros 20 GB-hora por mês (gratuito)
- **CloudWatch Logs:** Primeiros 5 GB por mês (gratuito)

### Estimativa de Custo (após free tier)

Para um projeto pequeno como este:
- **ECR:** ~$0.10/mês (armazenamento de imagem)
- **ECS Fargate:** ~$15-30/mês (se rodar 24/7)
- **CloudWatch:** ~$0.50/mês (logs)

💡 **Dica:** Para testes, você pode parar o serviço quando não estiver usando.

---

## 🎓 Para Entrega Acadêmica

### Opção 1: Sem AWS (Suficiente)

- ✅ Pipeline CI/CD funciona (testes + build)
- ✅ Demonstra conhecimento de DevOps
- ✅ **Isso já é suficiente para a maioria dos projetos!**

### Opção 2: Com AWS (Bônus)

- ✅ Deploy automatizado
- ✅ Demonstra conhecimento completo de cloud
- ✅ Pode impressionar mais na apresentação

---

## 📚 Recursos Úteis

- **AWS Console:** https://console.aws.amazon.com/
- **Documentação AWS CLI:** https://docs.aws.amazon.com/cli/
- **Documentação ECR:** https://docs.aws.amazon.com/ecr/
- **Documentação ECS:** https://docs.aws.amazon.com/ecs/

---

**Pronto! Agora você está conectado à AWS! 🚀**

Se tiver dúvidas, consulte a documentação ou me pergunte!

