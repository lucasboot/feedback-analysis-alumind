import uuid
import pytest

from app.models import Feedback, Sentiment, Reason, Code, FeedbackSentiment, SentimentCode, CodeReason

def test_feedback_creation():
    feedback_id = str(uuid.uuid4())
    feedback_text = "Encontrei dificuldades em encontrar um tutorial claro sobre como utilizar as ferramentas de autoajuda disponíveis."
    feedback = Feedback(feedback_id, feedback_text)
    
    assert feedback.feedback_id == feedback_id
    assert feedback.feedback == feedback_text

def test_sentiment_creation():
    feedback_id = str(uuid.uuid4())
    sentiment_value = "POSITIVE"
    sentiment = Sentiment(feedback_id, sentiment_value)
    
    assert sentiment.feedback_id == feedback_id
    assert sentiment.sentiment == sentiment_value

def test_reason_creation():
    reason_id = str(uuid.uuid4())
    reason_text = "O usuário gostaria de realizar a edição do próprio perfil"
    reason = Reason(reason_id, reason_text)
    
    assert reason.reason_id == reason_id
    assert reason.reason == reason_text

def test_code_creation():
    code_id = str(uuid.uuid4())
    code_value = "EDITAR_PERFIL"
    code = Code(code_id, code_value)
    
    assert code.code_id == code_id
    assert code.code == code_value

def test_feedback_sentiment_creation():
    feedback_id = str(uuid.uuid4())
    sentiment_id = str(uuid.uuid4())
    feedback_sentiment = FeedbackSentiment(feedback_id, sentiment_id)
    
    assert feedback_sentiment.feedback_id == feedback_id
    assert feedback_sentiment.sentiment_id == sentiment_id

def test_sentiment_code_creation():
    sentiment_id = str(uuid.uuid4())
    code_id = str(uuid.uuid4())
    sentiment_code = SentimentCode(sentiment_id, code_id)
    
    assert sentiment_code.sentiment_id == sentiment_id
    assert sentiment_code.code_id == code_id

def test_code_reason_creation():
    code_id = str(uuid.uuid4())
    reason_id = str(uuid.uuid4())
    code_reason = CodeReason(code_id, reason_id)
    
    assert code_reason.code_id == code_id
    assert code_reason.reason_id == reason_id

