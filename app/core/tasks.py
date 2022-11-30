from celery import shared_task

@shared_task
def add(x,y):
    sum = 0
    for i in range(100000):
        for j in range(10000):
            sum += i+j
    print(sum)