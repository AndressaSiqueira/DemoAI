# 🔒 Security Workflow Setup

Este repositório implementa um workflow de segurança obrigatório que deve ser executado por **TODOS** os desenvolvedores antes de qualquer push ser aceito.

## 🚀 Configuração Automática

### 1. GitHub Actions
- **Workflow**: `.github/workflows/security.yml`
- **Execução**: Automática em todos os pushes e PRs
- **Verificações**:
  - 🔐 Detecção de Secrets (TruffleHog)
  - 🛡️ Análise de Segurança (Bandit)
  - 🩺 Vulnerabilidades de Dependências (Safety)
  - 📝 Qualidade de Código (Black, isort, flake8, mypy)

### 2. Branch Protection Rules (Configuração Manual Necessária)

**⚠️ ATENÇÃO**: As regras de proteção de branch devem ser configuradas manualmente no GitHub:

1. Vá para: `Settings > Branches > Add rule`
2. Configure:
   - **Branch name pattern**: `main` (ou branch padrão)
   - ✅ **Require status checks to pass before merging**
   - ✅ **Require branches to be up to date before merging**
   - **Status checks required**:
     - `🔍 Security Scanning`
     - `📝 Code Quality`
     - `✅ Security Status Check`
   - ✅ **Require pull request reviews before merging**
   - ✅ **Dismiss stale PR approvals when new commits are pushed**
   - ✅ **Require review from CODEOWNERS**
   - ✅ **Restrict pushes that create files**
   - ✅ **Do not allow bypassing the above settings**

### 3. Configuração Local (Pre-commit)

```bash
# Instalar dependências
pip install -r requirements-dev.txt

# Configurar pre-commit
pre-commit install

# Executar manualmente (opcional)
pre-commit run --all-files
```

## 🔍 Ferramentas de Segurança

### Bandit
- **Função**: Detecta vulnerabilidades de segurança em código Python
- **Configuração**: `pyproject.toml`
- **Execução**: Automática no CI/CD e pre-commit

### Safety
- **Função**: Verifica vulnerabilidades conhecidas nas dependências
- **Execução**: Automática no CI/CD e pre-commit

### TruffleHog
- **Função**: Detecta secrets e credenciais no código
- **Execução**: Automática no CI/CD

### Detect Secrets
- **Função**: Detecta secrets localmente
- **Execução**: Pre-commit hook

## 🚫 Política de Segurança

### Vulnerabilidades Detectadas
O workflow atual detecta e bloqueia:

1. **Hardcoded Secrets**: Chaves API, senhas, tokens
2. **Vulnerabilidades de Código**: SQL injection, XSS, RCE
3. **Dependências Vulneráveis**: Bibliotecas com CVEs conhecidos
4. **Má Qualidade de Código**: Formatação, imports, tipos

### Consequências
- ❌ **Push Rejeitado**: Se vulnerabilidades forem detectadas
- ❌ **PR Bloqueado**: Merge impedido até correção
- ❌ **Sem Bypass**: Administradores não podem ignorar

## 📊 Relatórios

Os relatórios de segurança são gerados automaticamente:
- `bandit-report.json`: Vulnerabilidades de código
- `safety-report.json`: Vulnerabilidades de dependências

## 🔧 Solução de Problemas

### Erro: "Security scan failed"
1. Verifique os logs do GitHub Actions
2. Corrija as vulnerabilidades detectadas
3. Faça commit das correções

### Erro: "Code quality checks failed"
1. Execute localmente: `black . && isort .`
2. Corrija erros de linting
3. Faça commit das correções

### Pre-commit não funciona
```bash
# Reinstalar pre-commit
pre-commit clean
pre-commit install
```

## 🎯 Objetivo

**Garantir que nenhum código vulnerável seja aceito no repositório, independente de quem faça o push.**

---

*Este workflow foi configurado para máxima segurança e não pode ser contornado por nenhum usuário, incluindo administradores.*