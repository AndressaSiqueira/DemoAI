# 🔒 Setup de Segurança Pré-Commit - DemoAI (Windows PowerShell)
# Executa uma única vez para configurar todas as ferramentas

Write-Host "🚀 Configurando ambiente de segurança no Windows..." -ForegroundColor Green

# Verificar se Python está instalado
try {
    $pythonVersion = python --version
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python não encontrado! Instale Python primeiro." -ForegroundColor Red
    exit 1
}

# Instalar pre-commit
Write-Host "📦 Instalando pre-commit..." -ForegroundColor Yellow
pip install pre-commit

# Instalar ferramentas de segurança
Write-Host "🔧 Instalando ferramentas de segurança..." -ForegroundColor Yellow
pip install bandit safety gitguardian black flake8

# Instalar hooks
Write-Host "🔗 Instalando hooks de segurança..." -ForegroundColor Yellow
pre-commit install

# Testar configuração
Write-Host "🧪 Testando configuração..." -ForegroundColor Yellow
pre-commit run --all-files

Write-Host ""
Write-Host "✅ Configuração completa!" -ForegroundColor Green
Write-Host "🎯 Agora todas as vulnerabilidades serão detectadas ANTES do commit!" -ForegroundColor Cyan
Write-Host "🚨 Teste fazendo um commit - você verá os alertas de segurança!" -ForegroundColor Yellow