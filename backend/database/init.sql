-- Criando o banco de dados USERS
CREATE DATABASE IF NOT EXISTS users;
USE users;

-- Criando a tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- Criando o banco de dados FILMES
CREATE DATABASE IF NOT EXISTS filmes;
USE filmes;

-- Criando a tabela de filmes
CREATE TABLE IF NOT EXISTS filmes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS video_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    video_id VARCHAR(255) NOT NULL UNIQUE,
    user_id VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Criando o usuário admin se não existir
CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY 'password';

-- Garantindo acesso total ao banco USERS e FILMES
GRANT ALL PRIVILEGES ON users.* TO 'admin'@'%';
GRANT ALL PRIVILEGES ON filmes.* TO 'admin'@'%';

-- Aplicando as mudanças
FLUSH PRIVILEGES;

