import time
from celery import Celery 


@celery.task()
def get_nics():
    time.sleep(2)
    return "hola"