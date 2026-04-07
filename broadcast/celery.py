import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'broadcast.settings')

app = Celery('broadcast')

# Load config from Django settings (CELERY_ prefix)
app.config_from_object('django.conf:settings', namespace='CELERY')

# THIS IS THE IMPORTANT LINE THAT WAS MISSING
app.autodiscover_tasks()

# Debug task so you can see it's working
@app.task(bind=True)
def debug_task(self):
    print(f'Debug task request: {self.request!r}')