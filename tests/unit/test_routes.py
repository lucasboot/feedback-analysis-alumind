import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, json, jsonify
from app.routes.feedback_routes import feedback_routes

# Configura o aplicativo Flask para testes
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(feedback_routes)
    app.testing = True
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

# Testa a rota /feedbacks
@patch('app.routes.feedback_routes.feedback_exists')
@patch('app.routes.feedback_routes.classify_spam')
@patch('app.routes.feedback_routes.analyze_sentiment')
@patch('app.routes.feedback_routes.add_sentiment')
@patch('app.routes.feedback_routes.add_features_reasons')
def test_create_feedback(mock_add_features_reasons, mock_add_sentiment, mock_analyze_sentiment, mock_classify_spam, mock_feedback_exists, client):
    mock_feedback_exists.return_value = False
    mock_classify_spam.return_value = 'NOT_SPAM'
    mock_analyze_sentiment.return_value = json.dumps({
        "sentiment": "POSITIVE",
        "requested_features": ["feature1", "feature2"]
    })

    response = client.post('/feedbacks', json={
        "feedback": "This is a feedback",
        "id": "feedback123"
    })

    assert response.status_code == 201
    assert response.json['sentiment'] == "POSITIVE"
    assert "requested_features" in response.json

# Testa a rota /feedbacks_ingestion
@patch('app.routes.feedback_routes.get_db_connection')
def test_data_ingestion(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post('/feedbacks_ingestion', json=[
        {"feedback": "Feedback 1"},
        {"feedback": "Feedback 2"}
    ])

    assert response.status_code == 201
    assert response.json['message'] == "Feedbacks inserted successfully"
    mock_cursor.execute.assert_called()

# Testa a rota /run_script
@patch('app.routes.feedback_routes.send_feedbacks_to_route')
def test_run_script(mock_send_feedbacks_to_route, client):
    mock_send_feedbacks_to_route.return_value = "Script executed successfully"

    response = client.post('/run_script')

    assert response.status_code == 200
    assert response.json['message'] == "Script executed successfully"

# Testa a rota /generate_weekly_report
@patch('app.routes.feedback_routes.get_sentiment_distribution')
@patch('app.routes.feedback_routes.get_top_weekly_features')
def test_generate_weekly_report(mock_get_top_weekly_features, mock_get_sentiment_distribution, client):
    mock_get_sentiment_distribution.return_value = {'POSITIVE': 10, 'NEGATIVE': 5, 'INCONCLUSIVO': 2}
    mock_get_top_weekly_features.return_value = ['feature1', 'feature2']

    response = client.get('/generate_weekly_report')

    assert response.status_code == 200
    assert 'sentiment_distribution' in response.json
    assert 'top_features' in response.json
    assert 'INCONCLUSIVO' not in response.json['sentiment_distribution']


### Pages Routes, ainda em desenvolvimento e correção


# Testa a rota /report
@patch('app.routes.pages_routes.get_db_connection')
@patch('app.routes.pages_routes.transform_feedbacks')
def test_report(mock_transform_feedbacks, mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Testa o caso com feedbacks
    mock_cursor.fetchall.return_value = [('feedback1', 'Feedback 1')]
    mock_transform_feedbacks.return_value = [{'feedback_id': 'feedback1', 'feedback': 'Feedback 1', 'status': 'green'}]

    response = client.get('/report')
    assert response.status_code == 200
    assert b'Feedback 1' in response.data  

    # Testa o caso com banco de dados vazio
    mock_cursor.fetchall.return_value = []
    response = client.get('/report')
    assert response.status_code == 200
    assert b'Database Empty' in response.data  

# Testa a rota /simulation
def test_simulation(client):
    response = client.get('/simulation')
    assert response.status_code == 200
    assert b'Simulation Page' in response.data  # Adapte a verificação para o conteúdo esperado da página


# Testa a rota /sentiment_distribution
@patch('app.routes.pages_routes.get_sentiment_distribution')
def test_sentiment_distribution(mock_get_sentiment_distribution, client):
    mock_get_sentiment_distribution.return_value = {'POSITIVE': 10, 'NEGATIVE': 5, 'INCONCLUSIVO': 1}

    response = client.get('/sentiment_distribution')
    assert response.status_code == 200
    assert response.json == {'POSITIVE': 10, 'NEGATIVE': 5, 'INCONCLUSIVO': 1}

# Testa a rota /top-features
@patch('app.routes.pages_routes.get_top_features')
def test_top_features(mock_get_top_features, client):
    mock_get_top_features.return_value = [{'code_id': "1a",
                'code_name': "EDITAR_PERFIL",
                'count': 2}]

    response = client.get('/top-features')
    assert response.status_code == 200
    assert response.json == [{'code_id': "1a",
                'code_name': "EDITAR_PERFIL",
                'count': 2}]

    # Testa o caso de exceção
    mock_get_top_features.side_effect = Exception('Database error')
    response = client.get('/top-features')
    assert response.status_code == 500
    assert response.json['error'] == 'Database error'