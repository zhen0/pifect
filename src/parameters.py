from prefect import task, Flow, Parameter, prefect
import time
from prefect.storage import Github

@task
def sleep(x):
    time.sleep(x)

@task
def sleepagain(y):
    time.sleep(y)



with Flow(name='Params') as flow:
    x = Parameter('x', default = 8)
    y = Parameter('y', default = 8)
    sleep(x=x)
    sleepagain(y=y)
    


# flow.run()
flow.register('Jenny')
flow.storage = GitHub(repo="pifect", path="/src/parameters.py")