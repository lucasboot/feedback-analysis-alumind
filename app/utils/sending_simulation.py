from flask import current_app as app
from app.utils.database import get_db_connection

def send_feedbacks_to_route():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT feedback_id, feedback FROM feedbacks")
        feedbacks = cursor.fetchall()
        cursor.close()
        conn.close()
        with app.test_request_context():
            for feedback in feedbacks:
                feedback_id, feedback_text = feedback
                #print('id: ', feedback_id)
                #print('feedback:', feedback_text)
                response = app.test_client().post('/feedbacks', json={
                    'id': feedback_id,
                    'feedback': feedback_text
                })
                if response.status_code != 201 and response.status_code != 304: 
                    return f"Error sending feedbacks: {response.data.decode()}"
        return "Feedbacks sent successfully"
    except Exception as e:
        return str(e)
