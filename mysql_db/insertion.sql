-- Inserções de exemplo para demonstração
INSERT INTO feedbacks (feedback_id, feedback)
VALUES
    (UUID_SHORT(), 'Feedback positivo'),
    (UUID_SHORT(), 'Feedback negativo'),
    (UUID_SHORT(), 'Feedback neutro');

INSERT INTO sentiments (sentiment_id, sentiment)
VALUES
    (UUID_SHORT(), 'POSITIVO'),
    (UUID_SHORT(), 'NEGATIVO'),
    (UUID_SHORT(), 'INCONCLUSIVO');

INSERT INTO reasons (reason_id, reason)
VALUES
    (UUID_SHORT(), 'Razão 1'),
    (UUID_SHORT(), 'Razão 2'),
    (UUID_SHORT(), 'Razão 3');

INSERT INTO codes (code_id, code)
VALUES
    (UUID_SHORT(), 'Code A'),
    (UUID_SHORT(), 'Code B'),
    (UUID_SHORT(), 'Code C');

INSERT INTO feedbacks_sentiments (feedback_id, sentiment_id)
VALUES
    (UUID_SHORT(), UUID_SHORT()),
    (UUID_SHORT(), UUID_SHORT()),
    (UUID_SHORT(), UUID_SHORT());

INSERT INTO sentiments_codes (sentiment_id, code_id)
VALUES
    (UUID_SHORT(), UUID_SHORT()),
    (UUID_SHORT(), UUID_SHORT()),
    (UUID_SHORT(), UUID_SHORT());

INSERT INTO codes_reasons (code_id, reason_id)
VALUES
    (UUID_SHORT(), UUID_SHORT()),
    (UUID_SHORT(), UUID_SHORT()),
    (UUID_SHORT(), UUID_SHORT());
