import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_DB = os.getenv('MYSQL_DB')
    CELERY_BROKER_URL = 'redis://:STOwRijujbtHO0jnftiuaGcQKxYBwEcq@redis-10690.c251.east-us-mz.azure.redns.redis-cloud.com:10690/0'
    CELERY_RESULT_BACKEND = 'redis://:STOwRijujbtHO0jnftiuaGcQKxYBwEcq@redis-10690.c251.east-us-mz.azure.redns.redis-cloud.com:10690/0'
    CELERY_IMPORTS = ('app.utils.tasks',)
    
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
