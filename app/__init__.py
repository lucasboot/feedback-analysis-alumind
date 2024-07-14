from flask import Flask
from flask_cors import CORS
from .config import Config
from .celery_config import make_celery
from celery.schedules import crontab

# schedule semanal 'schedule': crontab(hour=17, minute=0, day_of_week='fri'),
# schedule a cada 1 minuto para testes 'schedule': crontab(minute='*')
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["CELERY_CONFIG"] = {"imports": "app.utils.send_weekly_report", "broker_url": "redis://:STOwRijujbtHO0jnftiuaGcQKxYBwEcq@redis-10690.c251.east-us-mz.azure.redns.redis-cloud.com:10690/0", "result_backend": "redis://:STOwRijujbtHO0jnftiuaGcQKxYBwEcq@redis-10690.c251.east-us-mz.azure.redns.redis-cloud.com:10690/0", "beat_schedule": {
        'send-weekly-report-every-friday-5pm': {
            'task': 'app.utils.send_weekly_report.send_weekly_report_email',
            'schedule': crontab(hour=17, minute=0, day_of_week='fri')
        },
    }}

    CORS(app)

    celery = make_celery(app)
    celery.set_default()

    from .routes.feedback_routes import feedback_routes
    from .routes.pages_routes import pages_routes
    
    app.register_blueprint(feedback_routes)
    app.register_blueprint(pages_routes)

    return app, celery
