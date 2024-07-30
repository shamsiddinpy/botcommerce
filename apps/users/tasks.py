# Create your tasks here
import time

from celery import shared_task


@shared_task
def add(y):
    print("boshlandi..")
    time.sleep(2)
    print("tugadi..")
    return f'ishladi,{y}'
