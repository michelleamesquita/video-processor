FROM python:3.10

WORKDIR /app

# Copia as dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do microsserviço
COPY . .

ENV PYTHONPATH=/app


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
