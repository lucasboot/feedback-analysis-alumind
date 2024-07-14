import pytest
from unittest.mock import patch, MagicMock
from app.services.database_service import (
    feedback_exists, add_sentiment, add_features_reasons,
    get_top_features, get_top_weekly_features, get_sentiment_distribution, 
    get_weekly_feedback_summary
)
from app.models import Sentiment

# Fixture para criar um objeto Sentiment
@pytest.fixture
def sentiment():
    return Sentiment(feedback_id='feedback1', sentiment='POSITIVE')

# Testa a função feedback_exists
@patch('app.services.database_service.get_db_connection')
def test_feedback_exists(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Simula o caso onde o feedback existe
    mock_cursor.fetchone.return_value = [1]
    assert feedback_exists('feedback1') is True

    # Simula o caso onde o feedback não existe
    mock_cursor.fetchone.return_value = [0]
    assert feedback_exists('feedback1') is False

# Testa a função add_sentiment
@patch('app.services.database_service.get_db_connection')
def test_add_sentiment(mock_get_db_connection, sentiment):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    add_sentiment(sentiment)

    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO sentiments (feedback_id, sentiment) VALUES (%s, %s)",
        (sentiment.feedback_id, sentiment.sentiment)
    )
    mock_conn.commit.assert_called_once()

# Testa a função add_features_reasons
@patch('app.services.database_service.get_db_connection')
def test_add_features_reasons(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    requested_features = [
        {"code": "CODE1", "reason": "Reason 1"},
        {"code": "CODE2", "reason": "Reason 2"}
    ]

    mock_cursor.fetchone.side_effect = [None, None]  # Nenhum código existente

    add_features_reasons(requested_features, 'feedback1')

    assert mock_cursor.execute.call_count == 8
    mock_conn.commit.assert_called_once()

# Testa a função get_top_features
@patch('app.services.database_service.get_db_connection')
def test_get_top_features(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        ('code1', 'Code 1', 10),
        ('code2', 'Code 2', 8)
    ]

    result = get_top_features()

    assert len(result) == 2
    assert result[0]['code_id'] == 'code1'
    assert result[0]['count'] == 10

# Testa a função get_top_weekly_features
@patch('app.services.database_service.get_db_connection')
def test_get_top_weekly_features(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        ('Code 1', 5, 'Reason 1'),
        ('Code 2', 3, 'Reason 2')
    ]

    result = get_top_weekly_features()

    assert len(result) == 2
    assert result[0]['code'] == 'Code 1'
    assert result[0]['count'] == 5

# Testa a função get_sentiment_distribution
@patch('app.services.database_service.get_db_connection')
def test_get_sentiment_distribution(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        ('POSITIVE', 10),
        ('NEGATIVE', 5)
    ]

    result = get_sentiment_distribution()

    assert result['POSITIVE'] == 10
    assert result['NEGATIVE'] == 5

# Testa a função get_weekly_feedback_summary
@patch('app.services.database_service.get_db_connection')
def test_get_weekly_feedback_summary(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.side_effect = [[20], [('POSITIVO', 10), ('NEGATIVO', 5)]]
    mock_cursor.fetchall.return_value = [
        ('Code 1', 5, 'Reason 1'),
        ('Code 2', 3, 'Reason 2')
    ]

    result = get_weekly_feedback_summary()

    assert result['positive_percentage'] == 50.0
    assert result['negative_percentage'] == 25.0
    assert len(result['top_features']) == 2
