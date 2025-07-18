# 🔒 Segurança Pré-Commit - DemoAI

## 🚨 Por que você não recebeu alerta de vulnerabilidade?

**Resposta**: As ferramentas de segurança pré-commit não estavam configuradas ainda!

## ⚡ Solução Rápida - Instalar Agora

### 1. Para Windows PowerShell (Recomendado)
```powershell
# Execute no PowerShell
.\setup-security.ps1
```

### 2. Para Linux/Mac/WSL
```bash
# Execute no Terminal
bash setup-security.sh
```

### 3. Instalação Manual (Alternativa)
```bash
# Instalar pre-commit
pip install pre-commit

# Instalar ferramentas de segurança
pip install bandit safety gitguardian black flake8

# Ativar hooks
pre-commit install
```

## 🛡️ O que será detectado automaticamente:

### ✅ Suas vulnerabilidades atuais serão BLOQUEADAS:
- 🚨 **Command Injection** (linha 17): `subprocess.check_output(f"ping -c 1 {host}", shell=True)`
- 🚨 **Hardcoded Secret** (linha 11): `SECRET_KEY = "1234-super-secret-key"`
- 🚨 **JWT sem validação** (linha 23): `verify_signature": False`

### 🔍 Ferramentas ativas:
- **Bandit**: Vulnerabilidades Python
- **GitGuardian**: Secrets e credenciais
- **Safety**: Dependências vulneráveis
- **Custom hooks**: Validações específicas

## 🎯 Teste Imediato

Depois de instalar, tente fazer um commit:

```bash
git add .
git commit -m "test"
```

**Resultado esperado**:
```
🚨 Command Injection detectado!
🚨 Hardcoded secret detectado!
🚨 JWT sem verificação detectado!
❌ Commit BLOQUEADO!
```

## 📊 Exemplo de Saída

```
🔒 Bandit Security Scanner........................Failed
🔐 Secret Scanner.................................Failed
🛡️ Dependency Security Check.....................Passed
🎯 Custom Security Validation....................Failed

🚨 HIGH: B602[subprocess_popen_with_shell_equals_true] 
   vunerable_app.py:17 - subprocess call with shell=True
   
🚨 Hardcoded secret detectado!
🚨 JWT sem verificação detectado!
```

## 🚀 Benefícios

✅ **Detecção instantânea** de vulnerabilidades
✅ **Bloqueio automático** de commits inseguros  
✅ **Zero configuração** adicional necessária
✅ **Funciona offline** - não depende de internet
✅ **Integração VS Code** - alertas em tempo real

---

**⚡ Após instalar, você NUNCA mais conseguirá commitar código vulnerável!**