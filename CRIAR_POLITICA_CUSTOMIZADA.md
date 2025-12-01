# 🚀 Criar Política Customizada AWS - Guia Rápido

## 📋 Passo a Passo Visual

### 1️⃣ Abrir o Arquivo JSON

Abra o arquivo: `aws/iscoolgpt-policy.json`

Você verá:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:*",
                "ecs:*",
                "logs:*",
                "iam:PassRole"
            ],
            "Resource": "*"
        }
    ]
}
```

**Copie TODO esse conteúdo!** (Ctrl+A, Ctrl+C)

---

### 2️⃣ Criar Política no AWS Console

1. **Acesse:** https://console.aws.amazon.com/iam/
2. **Menu lateral:** Clique em **Policies** (Políticas)
3. **Botão:** Clique em **Create policy** (Criar política)

---

### 3️⃣ Colar o JSON

1. **Aba JSON:** Clique na aba **JSON** (no topo)
2. **Selecionar tudo:** Delete o conteúdo padrão (Ctrl+A, Delete)
3. **Colar:** Cole o conteúdo que você copiou (Ctrl+V)

**Deve ficar assim:**
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:*",
                "ecs:*",
                "logs:*",
                "iam:PassRole"
            ],
            "Resource": "*"
        }
    ]
}
```

4. **Validar:** Clique em **Next** (Próximo)

---

### 4️⃣ Configurar Nome

1. **Policy name:** Digite: `IsCoolGPT-FullAccess`
2. **Description (opcional):** 
   ```
   Full access to ECR, ECS, and CloudWatch Logs for IsCoolGPT project
   ```
3. **Clique em:** **Create policy** (Criar política)

✅ **Política criada!**

---

### 5️⃣ Anexar ao Usuário

1. **Volte para Users:**
   - Menu lateral → **Users**
   - Clique em: **github-actions-iscoolgpt**

2. **Adicionar Permissões:**
   - Aba **Permissions** (Permissões)
   - Botão **Add permissions** (Adicionar permissões)
   - Selecione: **Attach policies directly**

3. **Buscar e Selecionar:**
   - Na busca, digite: `IsCoolGPT`
   - Marque a checkbox: ✅ `IsCoolGPT-FullAccess`
   - Clique em **Next: Review**

4. **Confirmar:**
   - Clique em **Add permissions**

✅ **Pronto! Permissões adicionadas!**

---

### 6️⃣ Testar

Agora teste se funcionou:

```powershell
# Testar criar cluster ECS
aws ecs create-cluster --cluster-name iscoolgpt-cluster --region us-east-1
```

**Se funcionar, você verá:**
```json
{
    "cluster": {
        "clusterName": "iscoolgpt-cluster",
        ...
    }
}
```

---

## ✅ Checklist

- [ ] Arquivo `aws/iscoolgpt-policy.json` aberto
- [ ] Conteúdo copiado
- [ ] IAM → Policies → Create policy
- [ ] JSON colado no console
- [ ] Política criada com nome `IsCoolGPT-FullAccess`
- [ ] Política anexada ao usuário `github-actions-iscoolgpt`
- [ ] Teste de criar cluster funcionou

---

## 🎯 O que essa Política Permite?

- ✅ **ECR:** Push/pull de imagens Docker
- ✅ **ECS:** Criar e gerenciar clusters e serviços
- ✅ **CloudWatch Logs:** Ver logs da aplicação
- ✅ **IAM PassRole:** Passar roles para recursos ECS

**Isso é tudo que você precisa para o projeto IsCoolGPT!**

---

## 🆘 Problemas?

### Erro: "Invalid JSON"
- Verifique se copiou TODO o conteúdo
- Verifique se não há espaços extras
- Use um validador JSON online se necessário

### Erro: "Policy name already exists"
- Use outro nome: `IsCoolGPT-FullAccess-v2`
- Ou delete a política antiga primeiro

### Ainda não funciona?
- Verifique se a política está realmente anexada ao usuário
- Aguarde alguns segundos (AWS pode demorar para propagar)
- Tente fazer logout/login do AWS CLI

---

**Pronto! Agora você tem todas as permissões! 🚀**

