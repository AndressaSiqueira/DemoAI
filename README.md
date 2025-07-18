# DemoAI - Security Workflow Demo

Este repositório demonstra a implementação de um **workflow de segurança obrigatório** que protege o código contra vulnerabilidades, secrets e problemas de qualidade.

## 🔒 Segurança Implementada

### ✅ Verificações Automáticas
- **Bandit**: Detecta vulnerabilidades em código Python
- **Safety/pip-audit**: Verifica dependências vulneráveis
- **TruffleHog**: Detecta secrets e credenciais
- **Detect-secrets**: Proteção adicional contra vazamentos
- **Black/isort/flake8**: Qualidade e formatação de código

### ✅ Proteções Ativas
- **GitHub Actions**: Executa automaticamente em todos os pushes/PRs
- **Branch Protection**: Bloqueia merges sem aprovação de segurança
- **Pre-commit Hooks**: Verificações locais antes do commit
- **Status Checks**: Impossibilita bypass das verificações

## 🚀 Configuração

### 1. Desenvolvimento Local

```bash
# Clonar o repositório
git clone https://github.com/AndressaSiqueira/DemoAI.git
cd DemoAI

# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt

# Configurar pre-commit hooks
pre-commit install

# Executar verificações locais
pre-commit run --all-files
```

### 2. Branch Protection (Administrador)

Para ativar completamente a segurança, configure no GitHub:

1. Vá para **Settings > Branches > Add rule**
2. Configure:
   - **Branch name pattern**: `main`
   - ✅ **Require status checks to pass before merging**
   - ✅ **Require branches to be up to date before merging**
   - **Required status checks**:
     - `🔍 Security Scanning`
     - `📝 Code Quality`
     - `✅ Security Status Check`
   - ✅ **Require pull request reviews before merging**
   - ✅ **Dismiss stale PR approvals when new commits are pushed**
   - ✅ **Do not allow bypassing the above settings**

## 🔍 Vulnerabilidades Detectadas

Este repositório contém **vulnerabilidades intencionais** para demonstrar a eficácia do workflow:

### `vunerable_app.py`
- **Hardcoded Secret**: `SECRET_KEY = "1234-super-secret-key"`
- **RCE Vulnerability**: `subprocess.check_output(f"ping -c 1 {host}", shell=True)`
- **JWT sem validação**: `jwt.decode(token, options={"verify_signature": False})`
- **Dependências vulneráveis**: PyJWT 1.7.1, urllib3 1.26.18

## 🛡️ Como Funciona

### Workflow de Segurança
1. **Developer** faz push → **GitHub Actions** executam
2. **Bandit** escaneia código → Encontra vulnerabilidades
3. **Safety/pip-audit** verifica dependências → Encontra CVEs
4. **TruffleHog** procura secrets → Detecta hardcoded keys
5. **Status Check** falha → **Branch Protection** bloqueia merge

### Processo de Correção
1. **Fix** vulnerabilidades encontradas
2. **Commit** correções
3. **Push** novamente
4. **Verificações** passam → **Merge** liberado

## 📊 Arquivos de Configuração

- `.github/workflows/security.yml`: Workflow principal
- `.pre-commit-config.yaml`: Hooks locais
- `requirements-dev.txt`: Dependências de desenvolvimento
- `pyproject.toml`: Configuração do Bandit
- `SECURITY.md`: Documentação detalhada

## 🔧 Resolução de Problemas

### ❌ Security scan failed
```bash
# Verificar vulnerabilidades
bandit -r . -f txt
pip-audit

# Corrigir e fazer commit
git add .
git commit -m "fix: resolve security vulnerabilities"
```

### ❌ Code quality checks failed
```bash
# Aplicar formatação
black .
isort .

# Corrigir linting
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

### ❌ Pre-commit hooks failed
```bash
# Reinstalar hooks
pre-commit clean
pre-commit install
pre-commit run --all-files
```

## 🎯 Objetivo

**Demonstrar que é possível implementar um workflow de segurança rigoroso que:**
- ✅ Detecta vulnerabilidades automaticamente
- ✅ Bloqueia código inseguro
- ✅ Não pode ser contornado
- ✅ Facilita correção de problemas
- ✅ Mantém alta qualidade de código

---

*"Security is not a product, but a process."* - Bruce Schneier