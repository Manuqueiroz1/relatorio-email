#!/bin/bash
echo "🚀 Iniciando o Dashboard de Email Marketing..."

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não está instalado. Por favor, instale o Python 3.7+"
    exit 1
fi

# Verificar se o pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não está instalado. Por favor, instale o pip3"
    exit 1
fi

# Instalar dependências
echo "📦 Instalando dependências..."
pip3 install -r requirements.txt

# Executar testes
echo "🧪 Executando testes..."
python3 test_app.py

if [ $? -eq 0 ]; then
    echo "✅ Testes passaram com sucesso!"
    echo "🌐 Iniciando aplicação Streamlit..."
    streamlit run app.py
else
    echo "❌ Testes falharam. Verifique os erros acima."
    exit 1
fi
