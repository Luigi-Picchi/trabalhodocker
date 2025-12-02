FROM python:3.10-slim

WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar script
COPY gera_relatorio.py .

# Definir entrypoint
ENTRYPOINT ["python", "gera_relatorio.py"]