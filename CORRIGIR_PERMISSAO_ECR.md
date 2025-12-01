# 🔧 Corrigir Permissão ECR - Problema Identificado

## ❌ Problema

O deploy está travado porque a role `ecsTaskExecutionRole` não tem permissão para acessar o ECR.

**Erro:**
```
AccessDeniedException: User: arn:aws:sts::186639342634:assumed-role/ecsTaskExecutionRole/... 
is not authorized to perform: ecr:GetAuthorizationToken
```

---

## ✅ Solução: Adicionar Permissão ECR à Role

### Opção 1: Via Console AWS (Mais Fácil) ⭐

1. **Acesse:** AWS Console → IAM → Roles
2. **Procure:** `ecsTaskExecutionRole`
3. **Clique na role**
4. **Vá em:** "Add permissions" → "Attach policies"
5. **Procure e adicione:**
   - ✅ `AmazonEC2ContainerRegistryReadOnly` (ou `AmazonEC2ContainerRegistryFullAccess` se quiser)
6. **Add permissions**

### Opção 2: Via CLI (Se tiver permissão)

```powershell
aws iam attach-role-policy `
  --role-name ecsTaskExecutionRole `
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
```

---

## 🚀 Depois de Corrigir

Depois de adicionar a permissão:

1. **As tasks vão tentar iniciar novamente automaticamente**
2. **Ou force um novo deploy:**

```bash
# Forçar novo deploy
aws ecs update-service `
  --cluster iscoolgpt-cluster-staging `
  --service iscoolgpt-service-staging `
  --force-new-deployment `
  --region us-east-1
```

---

## ⚠️ Importante

A role `ecsTaskExecutionRole` precisa de:
- ✅ `AmazonECSTaskExecutionRolePolicy` (já deve ter)
- ✅ `AmazonEC2ContainerRegistryReadOnly` (FALTA - precisa adicionar)

---

**Adicione a permissão ECR e as tasks vão iniciar!** 🚀

