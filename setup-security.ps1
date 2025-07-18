# Setup de Segurança Pré-Commit - DemoAI (Windows PowerShell)
# Executa uma única vez para configurar todas as ferramentas

Write-Host "Configurando ambiente de segurança no Windows..."

# Verificar se Python está instalado
try {
    $pythonVersion = python --version 2>$null
    if ($pythonVersion) {
        Write-Host "Python encontrado: $pythonVersion"
    } else {
        throw "Python não encontrado"
    }
} catch {
    Write-Host "ERRO: Python não encontrado! Instale Python primeiro."
    Write-Host "Download: https://python.org/downloads/"
    exit 1
}

# Instalar pre-commit
Write-Host "Instalando pre-commit..."
pip install pre-commit

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO: Falha ao instalar pre-commit!"
    exit 1
}

# Instalar ferramentas de segurança essenciais
Write-Host "Instalando ferramentas de segurança..."
pip install bandit safety black flake8

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO: Falha ao instalar ferramentas de segurança!"
    exit 1
}

# Instalar hooks
Write-Host "Instalando hooks de segurança..."
pre-commit install

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERRO: Falha ao instalar hooks!"
    exit 1
}

# Testar configuração
Write-Host "Testando configuração..."
pre-commit run --all-files

Write-Host ""
Write-Host "SUCESSO: Configuração completa!"
Write-Host ""
Write-Host "Ferramentas instaladas:"
Write-Host "- Bandit: Scanner de vulnerabilidades Python"
Write-Host "- Safety: Verificador de dependências"
Write-Host "- Black: Formatador de código"
Write-Host "- Flake8: Linter de código"
Write-Host "- Custom hooks: Validações específicas"
Write-Host ""
Write-Host "Agora todas as vulnerabilidades serão detectadas ANTES do commit!"
Write-Host "Teste fazendo um commit - você verá os alertas de segurança!"
Write-Host ""
Write-Host "Para testar:"
Write-Host "  git add ."
Write-Host "  git commit -m test"