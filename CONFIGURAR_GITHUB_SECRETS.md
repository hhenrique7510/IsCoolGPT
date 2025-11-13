# 🔐 Como Configurar GitHub Secrets para AWS

## ❌ Problema Atual

O pipeline do GitHub Actions está falhando com o erro:
```
Error: Credentials could not be loaded, please check your action inputs: 
Could not load credentials from any providers
```

Isso acontece porque os **GitHub Secrets** não estão configurados.

---

## ✅ Solução: Configurar GitHub Secrets

### Passo 1: Obter Credenciais AWS

Se você ainda não tem credenciais AWS, você tem **duas opções**:

#### Opção A: Usar AWS (Recomendado para deploy completo)

1. **Criar conta AWS** (se não tiver): https://aws.amazon.com/
2. **Criar usuário IAM:**
   - Acesse: AWS Console → IAM → Users → Add users
   - Nome: `github-actions-iscoolgpt`
   - Permissões: Anexar políticas:
     - `AmazonEC2ContainerRegistryFullAccess`
     - `AmazonECS_FullAccess`
     - `AmazonEC2ContainerServiceFullAccess`
   - Criar e **salvar as credenciais**:
     - Access Key ID
     - Secret Access Key

#### Opção B: Pular AWS (Para entrega sem deploy)

O workflow foi ajustado para **funcionar sem AWS**! Ele vai:
- ✅ Rodar os testes
- ✅ Buildar a imagem Docker
- ⚠️ Pular o push para ECR (se não tiver credenciais)
- ⚠️ Pular o deploy para ECS (se não tiver credenciais)

**Isso é suficiente para demonstrar o CI/CD funcionando!**

---

### Passo 2: Adicionar Secrets no GitHub

1. **Acesse seu repositório no GitHub**

2. **Vá em Settings:**
   - Clique em **Settings** (no topo do repositório)
   - No menu lateral, clique em **Secrets and variables** → **Actions**

3. **Adicione os Secrets:**
   
   Clique em **"New repository secret"** e adicione:

   **Secret 1:**
   - **Name:** `AWS_ACCESS_KEY_ID`
   - **Value:** Sua Access Key ID da AWS
   - Clique em **"Add secret"**

   **Secret 2:**
   - **Name:** `AWS_SECRET_ACCESS_KEY`
   - **Value:** Sua Secret Access Key da AWS
   - Clique em **"Add secret"**

4. **Verificar:**
   - Você deve ver os dois secrets listados
   - ⚠️ **Importante:** Os valores são mascarados por segurança

---

## 🔄 Testar o Pipeline

Após configurar os secrets:

1. **Faça um novo commit e push:**
   ```powershell
   git commit --allow-empty -m "test: trigger CI/CD pipeline"
   git push origin main
   ```

2. **Verifique o GitHub Actions:**
   - Vá em **Actions** (aba no topo do repositório)
   - Clique no workflow mais recente
   - Agora deve passar em todos os steps:
     - ✅ Run Tests
     - ✅ Build Docker Image
     - ✅ Deploy to ECS (se AWS configurado)

---

## 📊 O que o Pipeline Faz Agora

### Sem AWS Configurado:
- ✅ **Test:** Roda testes (sempre funciona)
- ✅ **Build:** Builda imagem Docker (sempre funciona)
- ⚠️ **Push ECR:** Pula com aviso (secrets não configurados)
- ⚠️ **Deploy ECS:** Pula com aviso (secrets não configurados)

### Com AWS Configurado:
- ✅ **Test:** Roda testes
- ✅ **Build:** Builda imagem Docker
- ✅ **Push ECR:** Envia imagem para ECR
- ✅ **Deploy ECS:** Faz deploy no ECS

---

## 🎓 Para Entrega Acadêmica

### Se NÃO configurar AWS:
- ✅ O pipeline **vai funcionar** (testes + build)
- ✅ Você pode mostrar que o CI/CD está configurado
- ✅ Pode explicar que o deploy AWS é opcional
- ✅ **Isso é suficiente para demonstrar DevOps!**

### Se configurar AWS:
- ✅ Pipeline completo funcionando
- ✅ Deploy automatizado na AWS
- ✅ Mais pontos na avaliação (provavelmente)

---

## 🆘 Problemas Comuns

### Erro: "Invalid credentials"
- Verifique se copiou as credenciais corretamente
- Verifique se não há espaços extras
- Crie novas credenciais se necessário

### Erro: "Access denied"
- Verifique as permissões IAM do usuário
- Certifique-se de que tem permissões para ECR e ECS

### Pipeline ainda falha
- Verifique se os nomes dos secrets estão corretos:
  - `AWS_ACCESS_KEY_ID` (exatamente assim)
  - `AWS_SECRET_ACCESS_KEY` (exatamente assim)
- Verifique se fez push após adicionar os secrets

---

## ✅ Checklist

- [ ] Credenciais AWS obtidas (ou decidiu pular AWS)
- [ ] Secrets adicionados no GitHub
- [ ] Novo push feito
- [ ] Pipeline rodando com sucesso
- [ ] Screenshot do pipeline funcionando (para evidências)

---

**Dica:** Mesmo sem AWS, o pipeline demonstra CI/CD funcionando! 🚀

