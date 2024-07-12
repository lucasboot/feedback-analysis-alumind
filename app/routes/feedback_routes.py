from flask import Blueprint, request, jsonify
from app.models import Feedback
from app.utils.database import get_db_connection
from app.services.feedback_service import analyze_sentiment
import uuid
import json


feedback_routes = Blueprint('feedback_routes', __name__)

@feedback_routes.route('/feedbacks', methods=['POST'])
def create_feedback():
    data = request.json
    feedback = Feedback(feedback_id=data['id'], feedback=data['feedback'])
    
   
    conn = get_db_connection()
    cursor = conn.cursor()
    
    analysis = analyze_sentiment(feedback.feedback)
    response_json = json.loads(analysis)
    response_json = {
        "id": feedback.feedback_id,
        "sentiment": response_json["sentiment"],
        "requested_features": response_json["requested_features"]
    }

    cursor.close()
    conn.close()
    
    return json.dumps(response_json, indent=2), 201


# No intuito de simular a ingestão de dados no banco, uma rota auxiliar, que não faz parte dos requisitos da aplicação, foi criada
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
