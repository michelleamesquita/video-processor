# 🎬 Projeto de Processamento de Vídeos 🚀

## 📌 Como Rodar a Aplicação

### 1️⃣ **Subir os Containers Docker**
```sh
docker-compose up --build
```

### 2️⃣ **Acessar a API**
- **Processar vídeo**: `POST http://localhost:8000/process-video/`
- **Cancelar processamento**: `POST http://localhost:8000/cancelar/{video_id}`
- **Obter status de um vídeo**: `GET http://localhost:8000/processar/status/{video_id}`
- **Listar status dos vídeos**: `GET http://localhost:8000/videos/status/`
- **Baixar vídeo processado**: `GET http://localhost:8000/download/?video_id={video_id}`
- **Criar usuário**: `POST http://localhost:8001/register/`
- **Fazer login**: `POST http://localhost:8001/login/`
- **Criar filme**: `POST http://localhost:8003/filmes/`
- **Notificar usuário**: `POST http://localhost:8004/notify/`
- **Verificar saúde do sistema**: `GET http://localhost:8000/health`

### 3️⃣ **Rodar os Testes**
```sh
pytest backend/tests/
```
--- 

### 📌 **Documentação da API (Swagger UI)**
A API conta com documentação automática via Swagger UI e Redoc:
```
Swagger UI: http://localhost:8000/docs
Redoc: http://localhost:8000/redoc
```
Isso permite visualizar e testar endpoints de forma interativa. 🚀

---

## 🔹 **Arquitetura MVC**
Este projeto segue uma estrutura baseada em **MVC (Model-View-Controller)** adaptada para microsserviços:

- **Model**: Representa os dados no banco de dados. Exemplo: `User`, `Filme`.
- **View**: As respostas da API servem como "view", entregando JSON como saída.
- **Controller**: Cada serviço (`processador`, `usuario`, `filmes`, `notificacoes`) atua como um controlador específico para sua funcionalidade.

Essa arquitetura garante modularidade, escalabilidade e separação de responsabilidades. 🎯

---

## 📁 **Estrutura das Pastas**
```
backend/
│
├── microsservicos/
│   ├── filmes/
│   │   ├── models/
│   │   ├── controllers/
│   │   ├── routes.py
│   │   └── main.py
│   ├── notificacoes/
│   │   ├── controllers/
│   │   ├── routes.py
│   │   └── main.py
│   ├── processador/
│   │   ├── controllers/
│   │   ├── routes.py
│   │   └── main.py
│   ├── usuario/
│   │   ├── models/
│   │   ├── controllers/
│   │   ├── routes.py
│   │   └── main.py
└── tests/
```

---

## 📡 **Exemplos de Rotas**

### 🏗️ **Processador**
#### **Processar Vídeo**
`POST /process-video/`
- **Descrição**: Envia um vídeo para processamento.
- **Exemplo de Requisição**:
  ```json
  {
    "video_id": "123",
    "video_path": "/path/to/video.mp4"
  }
  ```
- **Resposta Esperada**:
  ```json
  {
    "message": "Processamento iniciado",
    "video_id": "123",
    "user_id": "user01",
    "user_email": "email@example.com"
  }
  ```

#### **Cancelar Processamento**
`POST /cancelar/{video_id}`
- **Descrição**: Interrompe o processamento de um vídeo.

---

### 👤 **Usuário**
#### **Registrar Usuário**
`POST /register/`
- **Descrição**: Registra um novo usuário.
- **Exemplo de Requisição**:
  ```json
  {
    "username": "user1",
    "password": "password123"
  }
  ```

#### **Login**
`POST /login/`
- **Descrição**: Autentica um usuário e retorna um token JWT.
- **Exemplo de Requisição**:
  ```json
  {
    "username": "user1",
    "password": "password123"
  }
  ```
- **Resposta Esperada**:
  ```json
  {
    "message": "Login bem-sucedido!",
    "token": "jwt-token-aqui"
  }
  ```

---

### 🎥 **Filmes**
#### **Criar Filme**
`POST /filmes/`
- **Descrição**: Adiciona um novo filme ao banco de dados.
- **Exemplo de Requisição**:
  ```json
  {
    "titulo": "Inception",
    "status": "available"
  }
  ```

---

### 📩 **Notificações**
#### **Enviar Notificação**
`POST /notify/`
- **Descrição**: Envia uma notificação por e-mail.
- **Exemplo de Requisição**:
  ```json
  {
    "email": "user@example.com",
    "message": "Seu vídeo está pronto para download."
  }
  ```

---

### 📊 **Obter Status do Vídeo**
#### **Obter Status do Vídeo**
`GET /processar/status/{video_id}`
- **Descrição**: Retorna o status atual de um vídeo específico.

---

## ✅ **Justificativa Técnica do Sistema**
O sistema foi projetado para atender a **requisitos funcionais e técnicos**, garantindo eficiência, segurança e escalabilidade.

### 📌 **Requisitos do Sistema**
1️⃣ **Processamento paralelo de vídeos**  
✔️ Uso do RabbitMQ para filas de mensagens permite múltiplos processadores simultâneos.  

2️⃣ **Garantia de processamento em caso de pico**  
✔️ O RabbitMQ enfileira requisições, garantindo que nenhuma seja perdida.  

3️⃣ **Autenticação segura**  
✔️ JWT é utilizado para proteger endpoints e validar usuários.  

4️⃣ **Listagem do status dos vídeos de um usuário**  
✔️ Endpoint `/videos/status/` lista o status atualizado dos vídeos processados.  

5️⃣ **Notificação de erro para usuários**  
✔️ O serviço de notificações avisa o usuário sobre falhas via e-mail.  

---

### 📌 **Requisitos Técnicos**
1️⃣ **Persistência dos dados**  
✔️ MySQL armazena usuários, vídeos e status do processamento.  

2️⃣ **Escalabilidade**  
✔️ Arquitetura de microsserviços permite adicionar novos processadores facilmente.  

3️⃣ **Testes automatizados**  
✔️ Testes unitários e de integração garantem a qualidade do código.  

---

## ⚡ **Separação de Responsabilidades**
🔹 **Models (models/)**  
- Define as estruturas de dados e interage com o banco.  
- Exemplo: `video.py` gerencia informações de vídeos e `rabbitmq.py` lida com a fila.  

🔹 **Controllers (controllers/)**  
- Gerencia a lógica de negócios e coordena os fluxos da aplicação.  
- Exemplo: `processador_controller.py` processa vídeos e publica status no RabbitMQ.  

🔹 **Services (services/)**  
- Contém funcionalidades auxiliares, como notificações.  
- Exemplo: `notification_service.py` envia e-mails quando um vídeo é processado.  

---

