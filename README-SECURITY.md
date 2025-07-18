# 🔒 Security System Documentation

Este documento descreve o sistema completo de segurança pré-commit implementado neste projeto.

## 📋 Visão Geral

O sistema de segurança pré-commit detecta automaticamente vulnerabilidades e problemas de segurança antes que o código seja commitado. Ele inclui várias ferramentas e verificações customizadas para Python e JavaScript.

## 🚀 Instalação Rápida

Execute um único comando para instalar e configurar todo o sistema:

```bash
chmod +x setup-security.sh
./setup-security.sh
```

## 🛡️ Ferramentas Incluídas

### Python Security Tools
- **Bandit**: Análise estática de segurança para Python
- **Safety**: Verificação de dependências vulneráveis
- **Semgrep**: Análise de padrões de segurança
- **detect-secrets**: Detecção de segredos hardcoded
- **pip-audit**: Auditoria de pacotes Python

### JavaScript Security Tools
- **ESLint Security Plugin**: Detecção de vulnerabilidades JavaScript
- **npm audit**: Auditoria de dependências Node.js
- **Custom patterns**: Verificações customizadas para XSS e injection

### Verificações Customizadas
- **security-check.py**: Script personalizado com regras específicas
- **Command injection detection**: Detecção de execução de comandos inseguros
- **Hardcoded secrets**: Busca por tokens, senhas e chaves
- **SQL injection patterns**: Detecção de vulnerabilidades SQL
- **XSS vulnerability detection**: Identificação de potenciais XSS
- **Insecure configurations**: Configurações inseguras (debug mode, SSL, etc.)

## 📁 Arquivos de Configuração

### `.pre-commit-config.yaml`
Configuração principal dos hooks de segurança:
```yaml
repos:
  - repo: https://github.com/PyCQA/bandit
    rev: '1.7.5'
    hooks:
      - id: bandit
        args: ['-r', '-x', '*/test_*', '-f', 'json']
  # ... outros hooks
```

### `.bandit`
Configuração do Bandit para análise Python:
```ini
[bandit]
exclude_dirs = tests,test
tests = B101,B102,B103...
confidence = low
severity = low
```

### `requirements-security.txt`
Dependências das ferramentas de segurança:
```txt
pre-commit==3.5.0
bandit==1.7.5
safety==2.3.5
semgrep==1.45.0
detect-secrets==1.4.0
```

### `security-check.py`
Script customizado para verificações específicas.

## 🔍 Vulnerabilidades Detectadas

### 🚨 Críticas (Bloqueiam commit)
- **Command Injection**: `subprocess.call(shell=True)`, `os.system()`
- **Code Injection**: `eval()`, `exec()`
- **Hardcoded Secrets**: Senhas, tokens, chaves API
- **JWT Insecure**: Verificação de assinatura desabilitada
- **SQL Injection**: Formatação insegura de strings SQL
- **Deserialization**: `pickle.load()` inseguro

### ⚠️ Altas (Geram warning)
- **SSL/TLS Issues**: Verificação SSL desabilitada
- **XSS Vulnerabilities**: `innerHTML`, `document.write`
- **Debug Mode**: Modo debug habilitado em produção
- **Open Redirect**: Redirecionamentos inseguros

### ⚡ Médias (Informativas)
- **Weak Cryptography**: `Math.random()` para segurança
- **Information Disclosure**: Logging de dados sensíveis
- **Storage Issues**: Dados sensíveis em localStorage

## 🔧 Uso

### Verificação Automática
Os hooks são executados automaticamente a cada commit:
```bash
git add .
git commit -m "Sua mensagem"
# Hooks de segurança são executados automaticamente
```

### Verificação Manual
Execute todas as verificações:
```bash
pre-commit run --all-files
```

Execute ferramentas específicas:
```bash
# Bandit (Python)
bandit -r . -f json

# Safety (dependências Python)
safety check

# Semgrep (análise de padrões)
semgrep --config=auto .

# detect-secrets (segredos hardcoded)
detect-secrets scan --all-files

# Script customizado
python security-check.py *.py *.js
```

### Verificação de Dependências
```bash
# Python
pip-audit
safety check

# JavaScript
npm audit --audit-level=high
```

## 🛠️ Configuração Avançada

### Personalizando Verificações
Edite `security-check.py` para adicionar novos padrões:

```python
'pattern': r'sua_regex_aqui',
'message': 'Sua mensagem de segurança',
'severity': 'CRITICAL'
```

### Excluindo Arquivos
Adicione exclusões no `.pre-commit-config.yaml`:
```yaml
exclude: ^(tests/|docs/|migrations/)
```

### Configurando Bandit
Modifique `.bandit` para ajustar:
- Testes executados
- Nível de confiança
- Diretórios excluídos
- Formato de saída

### Baseline de Segredos
Atualize a baseline quando necessário:
```bash
detect-secrets scan --all-files --baseline .secrets.baseline
```

## 📊 Interpretando Resultados

### Níveis de Severidade
- 🚨 **CRITICAL**: Bloqueia commit, deve ser corrigido
- ⚠️ **HIGH**: Problema sério, recomenda correção
- ⚡ **MEDIUM**: Problema moderado, revisar
- 💡 **LOW**: Melhoria sugerida
- ℹ️ **INFO**: Informativo

### Exemplo de Saída
```
🔒 Security Issues Found:
==================================================

🚨 CRITICAL (2 issues)
------------------------------
  📁 vunerable_app.py:17
  💬 Command injection vulnerability: shell=True with subprocess
  🔍 Code: subprocess.check_output(f"ping -c 1 {host}", shell=True)

  📁 vunerable_app.py:11
  💬 Hardcoded secret detected
  🔍 Code: SECRET_KEY = "1234-super-secret-key"

📊 Summary: 2 total issues found
   🚨 Critical: 2
   ⚠️ High: 0
   ⚡ Medium: 0
   💡 Low: 0
   ℹ️ Info: 0

🛑 COMMIT BLOCKED: Critical security issues must be fixed!
```

## 🔧 Resolução de Problemas

### Hook Falha na Instalação
```bash
# Reinstalar hooks
pre-commit uninstall
pre-commit install
pre-commit install --install-hooks
```

### Dependências Não Encontradas
```bash
# Reativar ambiente virtual
source venv-security/bin/activate
pip install -r requirements-security.txt
```

### Falsos Positivos
Para ignorar temporariamente:
```python
# nosec: B101 - Bandit ignore
# noqa: E501 - Flake8 ignore
```

Para baseline de segredos:
```bash
detect-secrets scan --all-files --baseline .secrets.baseline
```

### Performance Lenta
Para acelerar verificações:
```bash
# Executar apenas em arquivos modificados
pre-commit run

# Pular verificações específicas
SKIP=bandit,semgrep git commit -m "message"
```

## 📝 Workflow Recomendado

1. **Desenvolvedor faz alterações**
2. **Executa verificações locais** (opcional)
   ```bash
   pre-commit run --all-files
   ```
3. **Faz commit**
   ```bash
   git add .
   git commit -m "Sua mensagem"
   ```
4. **Hooks executam automaticamente**
5. **Se crítico encontrado**: Commit bloqueado
6. **Se apenas warnings**: Commit permitido com aviso
7. **Se sem problemas**: Commit normal

## 🔄 Atualização

Para atualizar as ferramentas:
```bash
# Atualizar hooks
pre-commit autoupdate

# Atualizar dependências Python
pip install --upgrade -r requirements-security.txt

# Atualizar dependências JavaScript
npm update
```

## 🏷️ Integração CI/CD

Adicione ao seu pipeline CI/CD:
```yaml
# GitHub Actions exemplo
- name: Security Check
  run: |
    pip install -r requirements-security.txt
    pre-commit run --all-files
```

## 📚 Recursos Adicionais

### Documentação das Ferramentas
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Safety Documentation](https://pyup.io/safety/)
- [Semgrep Documentation](https://semgrep.dev/docs/)
- [detect-secrets Documentation](https://github.com/Yelp/detect-secrets)
- [ESLint Security Plugin](https://github.com/nodesecurity/eslint-plugin-security)

### Padrões de Segurança
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE (Common Weakness Enumeration)](https://cwe.mitre.org/)
- [SANS Top 25](https://www.sans.org/top25-software-errors/)

### Treinamento
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
- [Secure Code Warrior](https://www.securecodewarrior.com/)
- [Python Security Best Practices](https://python-security.readthedocs.io/)

## 💡 Dicas de Boas Práticas

1. **Nunca ignore problemas críticos**
2. **Mantenha dependências atualizadas**
3. **Use variáveis de ambiente para segredos**
4. **Valide todas as entradas do usuário**
5. **Use HTTPS sempre que possível**
6. **Implemente logs de segurança**
7. **Faça revisões de código regulares**
8. **Mantenha backups seguros**

## 🆘 Suporte

Para problemas ou dúvidas:
1. Verifique este documento
2. Consulte logs de erro
3. Verifique issues no repositório
4. Contacte a equipe de segurança

---

**🔒 Lembre-se: A segurança é responsabilidade de todos!**