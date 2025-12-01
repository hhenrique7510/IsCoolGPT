# ⚠️ Resolver Permissions Boundary - Problema de Permissões

## 🔍 O Problema

O erro menciona **"permissions boundary"** - isso significa que há um limite de permissões configurado no usuário que está bloqueando as ações, mesmo com a política anexada.

---

## ✅ Solução: Remover Permissions Boundary

### Passo 1: Acessar o Usuário

1. **AWS Console:** https://console.aws.amazon.com/iam/
2. **Users** → `github-actions-iscoolgpt`
3. Clique no usuário

### Passo 2: Verificar Permissions Boundary

1. Na página do usuário, procure por **"Permissions boundary"** (Limite de permissões)
2. Se houver algo configurado, você verá algo como:
   ```
   Permissions boundary: arn:aws:iam::...:policy/...
   ```

### Passo 3: Remover Permissions Boundary

1. Clique em **"Edit"** (Editar) ao lado de Permissions boundary
2. Selecione **"No permissions boundary"** (Sem limite de permissões)
3. Clique em **"Save changes"** (Salvar alterações)

⚠️ **Nota:** Você precisa estar logado como **administrador** ou ter permissões IAM para fazer isso.

---

## 🔄 Alternativa: Se Não Puder Remover

Se você não tem permissão para remover o boundary, você tem duas opções:

### Opção A: Criar o Cluster Manualmente no Console

1. **AWS Console:** https://console.aws.amazon.com/ecs/
2. **Clusters** → **Create Cluster**
3. **Nome:** `iscoolgpt-cluster`
4. **Infrastructure:** AWS Fargate
5. **Create**

Depois disso, o GitHub Actions poderá usar o cluster mesmo sem permissão para criar.

### Opção B: Usar uma Conta/Usuário Admin

Se você tem acesso a uma conta admin, use essas credenciais para:
1. Criar o cluster ECS
2. Configurar os recursos necessários

Depois, o usuário `github-actions-iscoolgpt` pode usar os recursos criados.

---

## 🎯 Verificar se Funcionou

Depois de remover o permissions boundary, aguarde 1-2 minutos e teste:

```powershell
aws ecs create-cluster --cluster-name iscoolgpt-cluster --region us-east-1
```

**Ou se criou manualmente:**

```powershell
aws ecs describe-clusters --clusters iscoolgpt-cluster --region us-east-1
```

---

## 📋 Checklist

- [ ] Acessei Users → github-actions-iscoolgpt
- [ ] Verifiquei se há Permissions boundary configurado
- [ ] Removi o Permissions boundary (ou criei cluster manualmente)
- [ ] Testei criar/descrever cluster (funcionou!)

---

## 💡 Dica

**Para entrega acadêmica:** Se não conseguir remover o boundary, você pode:
- ✅ Criar o cluster manualmente no console
- ✅ Mostrar que o pipeline funciona (testes + build)
- ✅ Explicar que o deploy AWS requer permissões admin

**Isso já demonstra conhecimento de DevOps!**

---

**Tente remover o permissions boundary e me avise se funcionou! 🚀**

