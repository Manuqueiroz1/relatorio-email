#!/bin/bash
echo "📦 Empacotando aplicação para distribuição..."

# Criar diretório de distribuição
mkdir -p dist

# Copiar arquivos necessários
cp -r email_dashboard_app dist/

# Criar arquivo zip
cd dist
zip -r email_dashboard_$(date +%Y%m%d_%H%M%S).zip email_dashboard_app/

echo "✅ Aplicação empacotada em dist/"
ls -la dist/
