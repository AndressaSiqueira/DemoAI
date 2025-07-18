#!/bin/bash

# 🔒 Setup de Segurança Pré-Commit - DemoAI
# Executa uma única vez para configurar todas as ferramentas

echo "🚀 Configurando ambiente de segurança..."

# Instalar pre-commit
echo "📦 Instalando pre-commit..."
pip install pre-commit

# Instalar ferramentas de segurança
echo "🔧 Instalando ferramentas de segurança..."
pip install bandit safety gitguardian black flake8

# Instalar hooks
echo "🔗 Instalando hooks de segurança..."
pre-commit install

# Testar configuração
echo "🧪 Testando configuração..."
pre-commit run --all-files

echo "✅ Configuração completa!"
echo ""
echo "🎯 Agora todas as vulnerabilidades serão detectadas ANTES do commit!"
echo "🚨 Teste fazendo um commit - você verá os alertas de segurança!"