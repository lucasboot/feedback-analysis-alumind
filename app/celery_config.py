from celery import Celery
from celery.schedules import crontab

def make_celery(app):
    celery = Celery(
        app.import_name
    )
    celery.conf.update(app.config["CELERY_CONFIG"])
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    celery.conf.timezone = 'UTC'
    return celery
