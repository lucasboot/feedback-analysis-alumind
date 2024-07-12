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

def add_features(requested_features):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        for feature in requested_features:
            code = feature["code"]
            cursor.execute("SELECT COUNT(*) FROM codes WHERE code = %s", (code,))
            result = cursor.fetchone()
        
            if result[0] == 0:
                code_id = str(uuid.uuid4())
                cursor.execute(
                    "INSERT INTO codes (code_id, code) VALUES (%s, %s)",
                    (code_id, code)
                )
        conn.commit()
        
    except Exception as e:
        raise(e)
    finally:
        cursor.close()
        conn.close()