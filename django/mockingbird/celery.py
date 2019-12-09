from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mockingbird.settings')
redis = 'redis://h:ped0612c2ab8f1af2281848fbdce999d9e4c5f420ebf81c6c028a1cc85602b55a@ec2-54-164-134-74.compute-1.amazonaws.com:22949'
app = Celery('mockingbird', broker='redis') #broker='amqp://agixgbiz:rz5IW-...@shark.rmq.cloudamqp.com/agixgbiz')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
