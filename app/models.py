import uuid

class Feedback:
    def __init__(self, feedback_id: str, feedback: str):
        self.feedback_id = feedback_id
        self.feedback = feedback

class Sentiment:
    def __init__(self, sentiment_id: str, sentiment: str):
        self.sentiment_id = sentiment_id
        self.sentiment = sentiment

class Reason:
    def __init__(self, reason_id: str, reason: str):
        self.reason_id = reason_id
        self.reason = reason

class Code:
    def __init__(self, code_id: str, code: str):
        self.code_id = code_id
        self.code = code

class FeedbackSentiment:
    def __init__(self, feedback_id: str, sentiment_id: str):
        self.feedback_id = feedback_id
        self.sentiment_id = sentiment_id

class SentimentCode:
    def __init__(self, sentiment_id: str, code_id: str):
        self.sentiment_id = sentiment_id
        self.code_id = code_id

class CodeReason:
    def __init__(self, code_id: str, reason_id: str):
        self.code_id = code_id
        self.reason_id = reason_id
