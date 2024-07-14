import subprocess

def start_flask():
    return subprocess.Popen(['flask', 'run'])

def start_celery_worker():
    return subprocess.Popen(['celery', '-A', 'run.celery', 'worker','--pool=solo', '--loglevel=info'])

def start_celery_beat():
    return subprocess.Popen(['celery', '-A', 'run.celery', 'beat', '--loglevel=info'])

if __name__ == '__main__':
    print("Inicializando Flask server...")
    flask_process = start_flask()

    print("Inicializando Celery worker...")
    worker_process = start_celery_worker()

    print("Inicializando Celery beat...")
    beat_process = start_celery_beat()

    flask_process.wait()
    worker_process.wait()
    beat_process.wait()
