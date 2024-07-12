from flask import Blueprint, request, jsonify
from app.models import Feedback
from app.utils.database import get_db_connection
from app.services.feedback_service import analyze_sentiment
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
