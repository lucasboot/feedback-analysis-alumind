from app.utils.database import get_db_connection
import uuid



def add_sentiment(sentiment):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sentiments (feedback_id, sentiment) VALUES (%s, %s)",
            (sentiment.feedback_id, sentiment.sentiment)
        )
        conn.commit()
        
    except Exception as e:
        raise(e)
    finally:
        cursor.close()
        conn.close()

def add_features_reasons(requested_features, feedback_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for feature in requested_features:
            code = feature["code"]
            reason = feature["reason"]
            
            # Verificar se o código já existe na tabela "codes"
            cursor.execute("SELECT code_id FROM codes WHERE code = %s", (code,))
            result = cursor.fetchone()
            
            if result is None:
                code_id = str(uuid.uuid4())
                cursor.execute(
                    "INSERT INTO codes (code_id, code) VALUES (%s, %s)",
                    (code_id, code)
                )
            else:
                code_id = result[0]
            
            # Adicionar na tabela "sentiments_codes"
            cursor.execute(
                "INSERT INTO sentiments_codes (feedback_id, code_id) VALUES (%s, %s)",
                (feedback_id, code_id)
            )
            
            # Adicionar reason na tabela "reasons"
            reason_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO reasons (reason_id, reason) VALUES (%s, %s)",
                (reason_id, reason)
            )
            
            # Adicionar na tabela "codes_reasons"
            cursor.execute(
                "INSERT INTO codes_reasons (code_id, reason_id) VALUES (%s, %s)",
                (code_id, reason_id)
            )
        
        conn.commit()
        
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()
