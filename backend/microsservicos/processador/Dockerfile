FROM python:3.10.1-alpine

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk update

RUN apk add ffmpeg
RUN apk add zip

# Copia as dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do microsserviço
COPY . .

# Copia um vídeo de teste para dentro do container
COPY video123.mp4 /app/video123.mp4

ENV PYTHONPATH=/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
