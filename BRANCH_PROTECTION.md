# 🔒 Branch Protection Rules Setup

Para garantir que o workflow de segurança seja **obrigatório** e **não possa ser contornado**, configure as seguintes regras de proteção no GitHub:

## 📋 Configuração Passo a Passo

### 1. Acessar Configurações
1. Vá para o repositório no GitHub
2. Clique em **Settings** (Configurações)
3. No menu lateral, clique em **Branches**

### 2. Criar Regra de Proteção
1. Clique em **Add rule** (Adicionar regra)
2. Configure os seguintes campos:

#### Branch name pattern
```
main
```

#### Protect matching branches
- ✅ **Require a pull request before merging**
  - ✅ Require approvals: `1`
  - ✅ Dismiss stale PR approvals when new commits are pushed
  - ✅ Require review from CODEOWNERS

- ✅ **Require status checks to pass before merging**
  - ✅ Require branches to be up to date before merging
  - **Required status checks** (adicione estes):
    - `🔍 Security Scanning`
    - `📝 Code Quality`
    - `✅ Security Status Check`

- ✅ **Require conversation resolution before merging**

- ✅ **Require linear history**

- ✅ **Restrict pushes that create files**

- ✅ **Do not allow bypassing the above settings**
  - ✅ Include administrators

### 3. Salvar Configuração
1. Clique em **Create** (Criar)
2. A regra será aplicada imediatamente

## 🚫 Resultado Final

Com essas configurações:
- ❌ **Pushes diretos** para main são **bloqueados**
- ❌ **Merge sem PR** é **impossível**
- ❌ **Bypass por administradores** é **bloqueado**
- ❌ **Status checks falhando** **impedem merge**
- ❌ **Código vulnerável** **não entra** no repositório

## ✅ Fluxo de Trabalho Obrigatório

1. Developer cria **branch** → faz **commits** → abre **PR**
2. **GitHub Actions** executam **automaticamente**
3. Se **vulnerabilidades** encontradas → **Status Check FALHA**
4. **Branch Protection** **bloqueia merge** até correção
5. Developer **corrige** vulnerabilidades → **nova verificação**
6. **Status Check PASSA** → **Merge liberado**

## 🔧 Validação

Para testar se está funcionando:

1. Tente fazer push direto para main (deve falhar)
2. Abra PR com código vulnerável (deve ser bloqueado)
3. Corrija vulnerabilidades (deve ser liberado)

---

**⚠️ IMPORTANTE**: Essas regras garantem que **NENHUM** código vulnerável seja aceito no repositório, **independente** de quem faça o push.