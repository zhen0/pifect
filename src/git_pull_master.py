from prefect import task, Flow
from datetime import timedelta
from prefect.schedules import IntervalSchedule
import os

@task
def update_local_branch():
    os.system("git pull origin master")

schedule = IntervalSchedule(interval=timedelta(seconds=60))

with Flow("Pull git master", schedule) as flow:
    update_local_branch()

flow.run()
