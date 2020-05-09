from prefect import task, Flow, Parameter
import requests
from prefect.engine.state import Failed
from prefect.utilities.notifications import gmail_notifier

handler = gmail_notifier(only_states=[Failed])

@task (name= 'fail', state_handlers = [handler])
def getNothing(nothing):
    empty = requests.post(nothing)
    return empty

with Flow("FailingFlow", state_handlers=[handler]) as flow:
    getNothing('42')
    
flow.run()
