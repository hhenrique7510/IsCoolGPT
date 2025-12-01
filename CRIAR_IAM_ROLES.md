# 🔐 Criar IAM Roles Necessárias

## ⚠️ Problema

As task definitions precisam de IAM roles, mas o usuário atual não tem permissão para criá-las.

## ✅ Solução: Criar Roles no Console AWS

### Passo 1: Criar ecsTaskExecutionRole

1. **Acesse:** AWS Console → IAM → Roles → Create role
2. **Trusted entity type:** AWS service
3. **Use case:** Elastic Container Service → Elastic Container Service Task
4. **Next**
5. **Permissions:** 
   - Adicione: `AmazonECSTaskExecutionRolePolicy`
   - (Esta política já vem selecionada)
6. **Next**
7. **Role name:** `ecsTaskExecutionRole`
8. **Create role**

### Passo 2: Criar ecsTaskRole

1. **Acesse:** AWS Console → IAM → Roles → Create role
2. **Trusted entity type:** AWS service
3. **Use case:** Elastic Container Service → Elastic Container Service Task
4. **Next**
5. **Permissions:** 
   - Pode deixar sem políticas adicionais (ou adicionar conforme necessário)
6. **Next**
7. **Role name:** `ecsTaskRole`
8. **Create role**

---

## 🚀 Depois de Criar as Roles

Depois de criar as roles, posso continuar criando as task definitions e services!

**Me avise quando criar as roles e eu continuo!** 🚀

