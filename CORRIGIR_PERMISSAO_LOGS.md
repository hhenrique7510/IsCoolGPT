# 🔧 Corrigir Permissão CloudWatch Logs

## ❌ Novo Problema Identificado

Agora o problema é com CloudWatch Logs:

**Erro:**
```
AccessDeniedException: User: ...ecsTaskExecutionRole... 
is not authorized to perform: logs:CreateLogStream
```

A role precisa de permissão para criar log streams no CloudWatch.

---

## ✅ Solução: Adicionar Permissão CloudWatch Logs

### Via Console AWS:

1. **Acesse:** AWS Console → IAM → Roles
2. **Procure:** `ecsTaskExecutionRole`
3. **Clique na role**
4. **Vá em:** "Add permissions" → "Attach policies"
5. **Procure e adicione:**
   - ✅ `CloudWatchLogsFullAccess` (ou `CloudWatchLogsReadOnlyAccess` + permissões específicas)
   
   **OU melhor ainda:**
   - ✅ `AmazonECSTaskExecutionRolePolicy` (esta política já inclui permissões de logs)

6. **Add permissions**

---

## 🔍 Verificar Políticas Atuais

A role `ecsTaskExecutionRole` deve ter:
- ✅ `AmazonECSTaskExecutionRolePolicy` (inclui logs)
- ✅ `AmazonEC2ContainerRegistryReadOnly` (já tem)

Se não tiver `AmazonECSTaskExecutionRolePolicy`, adicione!

---

## 🚀 Depois de Corrigir

Force um novo deploy:

```powershell
aws ecs update-service `
  --cluster iscoolgpt-cluster-staging `
  --service iscoolgpt-service-staging `
  --force-new-deployment `
  --region us-east-1
```

---

**Adicione a política `AmazonECSTaskExecutionRolePolicy` e as tasks devem iniciar!** 🚀

