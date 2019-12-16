import os
os.environ['PREFECT__LOGGING__LEVEL'] = "INFO"
from prefect import Flow, task


@task 
def hw():
    print('Hello ...')
    print()

with Flow('hello') as flow:
    hw()

flow.run()

