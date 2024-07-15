from flask import Blueprint, request, jsonify
from app.models import Feedback, Sentiment
from app.utils.database import get_db_connection
from app.services.feedback_service import analyze_sentiment, classify_spam
from app.services.database_service import add_sentiment, add_features_reasons, feedback_exists, get_sentiment_distribution, get_top_features, get_top_weekly_features, get_weekly_feedback_summary
from app.utils.sending_simulation import send_feedbacks_to_route

import uuid
import json


feedback_routes = Blueprint('feedback_routes', __name__)

@feedback_routes.route('/feedbacks', methods=['POST'])
def create_feedback():

    feedback_text = request.json['feedback']
    feedback_id = request.json['id']
    
   
    if (feedback_exists(feedback_id)):
        return jsonify({
        "message": "Este feedback já tem uma análise de sentimento feita"
        }), 304
    if(str(classify_spam(feedback_text)) == 'SPAM'):
        return jsonify({
        "message": "Este feedback foi considero um SPAM, logo não pode ser analisado"
        })
    
    # Análise do sentimento
    analysis = analyze_sentiment(feedback_text)
    response_json = json.loads(analysis)
    
    sentiment = Sentiment(feedback_id, response_json["sentiment"])
    requested_features = response_json['requested_features']

   # Operações no banco de dados
    add_sentiment(sentiment)
    add_features_reasons(requested_features, sentiment.feedback_id)

    
    response_json = {
        "id": feedback_id,
        "sentiment": sentiment.sentiment,
        "requested_features": requested_features
    }
    return jsonify(response_json), 201


'''
No intuito de simular a ingestão de dados no banco, uma rota auxiliar, que não 
faz parte dos requisitos da aplicação, foi criada.
'''
@feedback_routes.route('/feedbacks_ingestion', methods=['POST'])
def data_ingestion():
    data = request.json
    if not isinstance(data, list):
        return jsonify({"error": "Invalid data format, expected a list of objects"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    for feedback in data:
        feedback_id = str(uuid.uuid4())
        feedback_text = feedback.get('feedback')
        
        if feedback_id and feedback_text:
            sql = "INSERT INTO feedbacks (feedback_id, feedback) VALUES (%s, %s)"
            cursor.execute(sql, (feedback_id, feedback_text))
        else:
            return jsonify({"error": "Missing 'id' or 'feedback' in the request data"}), 400
        
    conn.commit()    
    cursor.close()
    conn.close()
    return jsonify({"message": "Feedbacks inserted successfully"}), 201

'''
Rota criada para interagir com o template de simulação de envio dos feedbacks por outra equipe de dev
'''
@feedback_routes.route('/run_script', methods=['POST'])
def run_script():
    result = send_feedbacks_to_route()
    if "Error" in result:
        return jsonify({"message": result}), 500
    return jsonify({"message": result}), 200
    
@feedback_routes.route('/generate_weekly_report', methods=['GET'])
def generate_weekly_report():
    sentiment_count = get_sentiment_distribution()
    top_features = get_top_weekly_features()
    total_feedbacks = sum(sentiment_count.values())
    
    # Transformação de Dados
    sentiment_percentage = {
        sentiment: round((count / total_feedbacks) * 100, 2)
        for sentiment, count in sentiment_count.items()
    } 
    if 'INCONCLUSIVO' in sentiment_percentage:
        del sentiment_percentage['INCONCLUSIVO']
        
    report = {
        'sentiment_distribution': sentiment_percentage,
        'top_features': top_features
    }
    return jsonify(report)