-- Criar o banco de dados se ele ainda não existir
CREATE DATABASE IF NOT EXISTS alumind_db;
USE alumind_db;

-- Tabela feedbacks
CREATE TABLE feedbacks (
    feedback_id CHAR(36) NOT NULL,
    feedback VARCHAR(800) NOT NULL,
    PRIMARY KEY (feedback_id)
);

-- Tabela sentiments
CREATE TABLE sentiments (
    feedback_id CHAR(36) NOT NULL,
    sentiment VARCHAR(20) NOT NULL,
    PRIMARY KEY (feedback_id)
);

-- Tabela reasons
CREATE TABLE reasons (
    reason_id CHAR(36) NOT NULL,
    reason VARCHAR(400) NOT NULL,
    PRIMARY KEY (reason_id)
);

-- Tabela codes
CREATE TABLE codes (
    code_id CHAR(36) NOT NULL,
    code VARCHAR(40) NOT NULL UNIQUE,
    PRIMARY KEY (code_id)
);


-- Tabela sentiments_codes (relacionamento 1:N)
CREATE TABLE sentiments_codes (
    feedback_id CHAR(36) NOT NULL,
    code_id CHAR(36) NOT NULL,
    PRIMARY KEY (feedback_id, code_id),
    FOREIGN KEY (feedback_id) REFERENCES sentiments(feedback_id),
    FOREIGN KEY (code_id) REFERENCES codes(code_id)
);

-- Tabela codes_reasons (relacionamento 1:1)
CREATE TABLE codes_reasons (
    code_id CHAR(36) NOT NULL,
    reason_id CHAR(36) NOT NULL,
    PRIMARY KEY (code_id, reason_id),
    FOREIGN KEY (code_id) REFERENCES codes(code_id),
    FOREIGN KEY (reason_id) REFERENCES reasons(reason_id)
);

