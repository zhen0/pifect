from prefect import task, Flow
from datetime import timedelta
from prefect.schedules import IntervalSchedule
# Pushbullet API
from pushbullet import Pushbullet
import yaml
import datetime

with open('credentials.yaml') as f:
    credentials = yaml.safe_load(f)

@task
def push_hello(user_id, message):
    pb = Pushbullet(credentials[user_id]["pushbullet_key"])
    push = pb.push_note("Hey " + user_id + "!", message)

schedule = IntervalSchedule(interval=timedelta(seconds=60))

with Flow("Hello", schedule) as flow:
    push_hello("Dan", "The time here is " + datetime.datetime.now())

flow.run()

