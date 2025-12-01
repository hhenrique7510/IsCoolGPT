# 🔐 Como Adicionar Permissões AWS - Guia Visual

## ⚠️ Problema

Você não encontra as políticas `AmazonECS_FullAccess` ou `AmazonEC2ContainerServiceFullAccess` no console AWS.

Isso pode acontecer porque:
- Os nomes podem estar diferentes
- O console pode estar em português
- As políticas podem estar em outra categoria

---

## ✅ Solução: Passo a Passo Visual

### Passo 1: Acessar IAM

1. Acesse: https://console.aws.amazon.com/iam/
2. No menu lateral, clique em **Users** (Usuários)
3. Procure e clique em: **github-actions-iscoolgpt**

### Passo 2: Adicionar Permissões

1. Na página do usuário, clique na aba **Permissions** (Permissões)
2. Clique no botão **Add permissions** (Adicionar permissões)
3. Selecione **Attach policies directly** (Anexar políticas diretamente)

### Passo 3: Buscar Políticas

Na barra de busca, procure por estas políticas (uma de cada vez):

#### Política 1: ECR (Container Registry)
**Busque por:** `ECR` ou `Container Registry`

**Nomes possíveis:**
- ✅ `AmazonEC2ContainerRegistryFullAccess`
- ✅ `ECRFullAccess`
- ✅ `AmazonElasticContainerRegistryFullAccess`

**O que ela faz:** Permite push/pull de imagens Docker no ECR

---

#### Política 2: ECS (Container Service)
**Busque por:** `ECS` ou `Container Service` ou `Fargate`

**Nomes possíveis:**
- ✅ `AmazonECS_FullAccess`
- ✅ `AmazonEC2ContainerServiceFullAccess`
- ✅ `ECSFullAccess`
- ✅ `AmazonElasticContainerServiceFullAccess`

**O que ela faz:** Permite criar e gerenciar clusters e serviços ECS

---

### Passo 4: Selecionar e Anexar

1. Marque a checkbox ao lado de cada política encontrada
2. Clique em **Next: Review** (Próximo: Revisar)
3. Clique em **Add permissions** (Adicionar permissões)

---

## 🔍 Se Não Encontrar as Políticas

### Opção A: Buscar por Categoria

1. Na busca de políticas, clique em **Filter policies** (Filtrar políticas)
2. Selecione:
   - **AWS managed** (Gerenciadas pela AWS)
   - Categoria: **Compute** ou **Containers**

### Opção B: Usar Políticas Mais Específicas

Se não encontrar as políticas "FullAccess", use estas alternativas:

#### Para ECR:
- `AmazonEC2ContainerRegistryPowerUser`
- `AmazonEC2ContainerRegistryReadOnly` (só leitura - não recomendado)

#### Para ECS:
- `AmazonECS_TaskExecutionRolePolicy`
- `AmazonECS_ServiceRolePolicy`

**⚠️ Nota:** Essas são mais limitadas. Se possível, use as "FullAccess".

### Opção C: Criar Política Customizada (RECOMENDADO se não encontrar as outras)

Se ainda não encontrar, você pode criar uma política customizada. **Já existe um arquivo pronto!**

**Arquivo:** `aws/iscoolgpt-policy.json` ✅

**Como criar a política:**

1. **Acesse IAM → Policies:**
   - Vá em: https://console.aws.amazon.com/iam/
   - No menu lateral, clique em **Policies** (Políticas)
   - Clique em **Create policy** (Criar política)

2. **Selecione JSON:**
   - Clique na aba **JSON**
   - Delete o conteúdo padrão

3. **Cole o conteúdo do arquivo:**
   - Abra o arquivo `aws/iscoolgpt-policy.json` do projeto
   - Copie TODO o conteúdo
   - Cole no campo JSON do console AWS

4. **Configurar a política:**
   - Clique em **Next** (Próximo)
   - **Policy name:** `IsCoolGPT-FullAccess`
   - **Description:** `Full access to ECR, ECS, and CloudWatch Logs for IsCoolGPT project`
   - Clique em **Create policy** (Criar política)

5. **Anexar ao usuário:**
   - Volte em **Users** → `github-actions-iscoolgpt`
   - **Permissions** → **Add permissions** → **Attach policies directly**
   - Busque por: `IsCoolGPT-FullAccess`
   - Marque a checkbox e clique em **Add permissions**

**Pronto!** Agora o usuário tem todas as permissões necessárias.

---

## ✅ Verificar se Funcionou

Depois de adicionar as permissões, teste no terminal:

```powershell
# Testar ECR (já deve funcionar)
aws ecr describe-repositories --region us-east-1

# Testar ECS (agora deve funcionar)
aws ecs create-cluster --cluster-name iscoolgpt-cluster --region us-east-1
```

---

## 📋 Checklist

- [ ] Acessei IAM → Users → github-actions-iscoolgpt
- [ ] Cliquei em "Add permissions"
- [ ] Busquei e encontrei política de ECR
- [ ] Busquei e encontrei política de ECS
- [ ] Anexei ambas as políticas
- [ ] Testei criar cluster ECS (deve funcionar agora)

---

## 🎯 Políticas Mínimas Necessárias

Se quiser ser mais específico, estas são as ações mínimas necessárias:

### Para ECR:
- `ecr:GetAuthorizationToken`
- `ecr:BatchCheckLayerAvailability`
- `ecr:GetDownloadUrlForLayer`
- `ecr:BatchGetImage`
- `ecr:PutImage`
- `ecr:InitiateLayerUpload`
- `ecr:UploadLayerPart`
- `ecr:CompleteLayerUpload`

### Para ECS:
- `ecs:CreateCluster`
- `ecs:DescribeClusters`
- `ecs:RegisterTaskDefinition`
- `ecs:CreateService`
- `ecs:UpdateService`
- `ecs:DescribeServices`
- `ecs:DescribeTasks`

---

## 🆘 Ainda Não Funciona?

### Verifique:

1. **Você está logado como o usuário correto?**
   - No canto superior direito, veja qual usuário está logado
   - Precisa estar logado como um usuário ADMIN (não o github-actions-iscoolgpt)

2. **As políticas foram realmente anexadas?**
   - Volte em Users → github-actions-iscoolgpt → Permissions
   - Você deve ver as políticas listadas

3. **Tentou criar o cluster novamente?**
   ```powershell
   aws ecs create-cluster --cluster-name iscoolgpt-cluster --region us-east-1
   ```

---

## 💡 Dica

Se você tem acesso como **root** ou **admin**, pode usar uma política mais simples:

**Política:** `PowerUserAccess` (dá acesso a quase tudo, exceto IAM)

Mas para produção, é melhor usar as políticas específicas de ECR/ECS.

---

**Precisa de mais ajuda? Me avise! 🚀**

