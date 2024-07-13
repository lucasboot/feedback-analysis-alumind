from flask import Blueprint, jsonify, render_template
from app.utils.database import get_db_connection
from app.services.database_service import get_sentiment_distribution, get_top_features
pages_routes = Blueprint('pages_routes', __name__)


@pages_routes.route('/report')
def report():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT feedback_id, feedback FROM feedbacks")
    db_response_list = cursor.fetchall()
    feedbacks = transform_feedbacks(db_response_list, cursor)
    cursor.close()
    conn.close() 
    return render_template('report.html', feedbacks=feedbacks)

@pages_routes.route('/simulation')
def simulation():
    return render_template('simulation.html')

@pages_routes.route('/feedback/<feedback_id>')
def feedback_detail(feedback_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Encontrar o feedback_id na tabela feedbacks e sentiment na tabela sentiments
    cursor.execute("""
        SELECT f.feedback_id, f.feedback, s.sentiment
        FROM feedbacks f
        LEFT JOIN sentiments s ON f.feedback_id = s.feedback_id
        WHERE f.feedback_id = %s
    """, (feedback_id,))
    feedback = cursor.fetchone()
    
    if not feedback:
        cursor.close()
        conn.close()
        return jsonify({"error": "Feedback não encontrado"}), 404
    
    feedback_id, feedback_text, sentiment = feedback
    
    # 2. Buscar todos os codes relacionados ao feedback_id
    cursor.execute("""
        SELECT c.code_id, c.code
        FROM codes c
        JOIN sentiments_codes sc ON c.code_id = sc.code_id
        WHERE sc.feedback_id = %s
    """, (feedback_id,))
    codes = cursor.fetchall()
    
    # 3. Para cada code, encontrar suas reasons
    codes_with_reasons = []
    for code_id, code in codes:
        cursor.execute("""
            SELECT r.reason
            FROM reasons r
            JOIN codes_reasons cr ON r.reason_id = cr.reason_id
            WHERE cr.code_id = %s
        """, (code_id,))
        reasons = [row[0] for row in cursor.fetchall()]
        codes_with_reasons.append({"code": code, "reasons": reasons})
    
    cursor.close()
    conn.close()
    
    # 4. Preparar e retornar a resposta JSON
    feedback_details = {
        "feedback_id": feedback_id,
        "feedback": feedback_text,
        "sentiment": sentiment,
        "requested_features": codes_with_reasons
    }
    return jsonify(feedback_details)


@pages_routes.route('/sentiment_distribution')
def sentiment_distribution():
    # Supondo que get_sentiment_distribution retorne um dicionário com a contagem de sentimentos
    sentiment_data = get_sentiment_distribution()  # {'POSITIVO': 30, 'NEGATIVO': 15, 'INCONCLUSIVO': 5}
    return jsonify(sentiment_data)

@pages_routes.route('/top-features', methods=['GET'])
def top_features():
    try:
        features = get_top_features()
        print(jsonify(features))
        return jsonify(features)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def transform_feedbacks(feedbacks, cursor):
    transformed_feedbacks = []
    for feedback in feedbacks:
        feedback_id, feedback_text = feedback

        cursor.execute("SELECT COUNT(*) FROM sentiments WHERE feedback_id = %s", (feedback_id,))
        exists = cursor.fetchone()[0]

        transformed_feedback = {
            "feedback_id": feedback_id,
            "feedback": feedback_text,
            "status": "green" if exists else "red"
        }
        transformed_feedbacks.append(transformed_feedback)
    return transformed_feedbacks