from prefect import task, Flow
from datetime import timedelta
from prefect.schedules import IntervalSchedule
# Pushbullet API
from pushbullet import Pushbullet
import yaml

with open('credentials.yaml') as f:
    credentials = yaml.safe_load(f)

@task
def push_hello(user_id):
    pb = Pushbullet(credentials[user_id]["pushbullet_key"])
    push = pb.push_note("Hey " + user_id + "!", "This is a message for you.")

schedule = IntervalSchedule(interval=timedelta(seconds=60))

with Flow("Hello", schedule) as flow:
    push_hello("Dan")

flow.run()

