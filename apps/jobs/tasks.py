from __future__ import absolute_import

from celery import Celery

app = Celery('tasks',
             broker='amqp://guest@192.168.186.192',
             backend='amqp://guest@192.168.186.192',
             include=['tasks'])

@app.task(name="tasks.add")
def add(x,y):
	pass

@app.task(name="tasks.calculate")
def calculate(function, bucket_list, dataset_id, table, output_column, *input_columns):
	pass

