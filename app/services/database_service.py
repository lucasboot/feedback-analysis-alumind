from app.utils.database import get_db_connection
import uuid



def feedback_exists(feedback_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM sentiments WHERE feedback_id = %s", (feedback_id,))
        count = cursor.fetchone()[0]
        print('Ocorrencias:', count)
        
        return count > 0
    except Exception as e:
        raise(e)
    finally:
        cursor.close()
        conn.close()

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



def get_top_features():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Consulta para contar o número de ocorrências de cada code_id
        query = """
        SELECT code.code_id, code.code, COUNT(*) AS count
        FROM codes AS code
        JOIN sentiments_codes AS sc ON code.code_id = sc.code_id
        GROUP BY code.code_id, code.code
        ORDER BY count DESC
        LIMIT 10
        """
        cursor.execute(query)

        # Coletar os resultados
        results = cursor.fetchall()

        # Formatar os resultados no formato desejado
        top_features = []
        for row in results:
            code_id, code_name, count = row
            top_features.append({
                'code_id': code_id,
                'code_name': code_name,
                'count': count
            })

        return top_features
        
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    finally:
        cursor.close()
        conn.close()



def get_sentiment_distribution():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT sentiment, COUNT(*) AS count
        FROM sentiments
        GROUP BY sentiment
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Formatar os resultados no formato desejado
        sentiment_counts = {}
        for row in results:
            sentiment, count = row
            sentiment_counts[sentiment] = count
        
        return sentiment_counts
        
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
