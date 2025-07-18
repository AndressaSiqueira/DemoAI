# 🔒 Setup de Segurança Pré-Commit - DemoAI (Windows PowerShell)
# Executa uma única vez para configurar todas as ferramentas

Write-Host "🚀 Configurando ambiente de segurança no Windows..." -ForegroundColor Green

# Verificar se Python está instalado
try {
    $pythonVersion = python --version 2>$null
    if ($pythonVersion) {
        Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python não encontrado"
    }
} catch {
    Write-Host "❌ Python não encontrado! Instale Python primeiro." -ForegroundColor Red
    Write-Host "Download: https://python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Instalar pre-commit
Write-Host "📦 Instalando pre-commit..." -ForegroundColor Yellow
pip install pre-commit

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro ao instalar pre-commit!" -ForegroundColor Red
    exit 1
}

# Instalar ferramentas de segurança
Write-Host "🔧 Instalando ferramentas de segurança..." -ForegroundColor Yellow
pip install bandit safety gitguardian black flake8

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro ao instalar ferramentas de segurança!" -ForegroundColor Red
    exit 1
}

# Instalar hooks
Write-Host "🔗 Instalando hooks de segurança..." -ForegroundColor Yellow
pre-commit install

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Erro ao instalar hooks!" -ForegroundColor Red
    exit 1
}

# Testar configuração
Write-Host "🧪 Testando configuração..." -ForegroundColor Yellow
pre-commit run --all-files

Write-Host ""
Write-Host "✅ Configuração completa!" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 Agora todas as vulnerabilidades serão detectadas ANTES do commit!" -ForegroundColor Cyan
Write-Host "🚨 Teste fazendo um commit - você verá os alertas de segurança!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Para testar:" -ForegroundColor White
Write-Host "  git add ." -ForegroundColor Gray
Write-Host "  git commit -m `"test security`"" -ForegroundColor Gray