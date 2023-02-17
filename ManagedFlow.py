from prefect import task, flow

import time


@task(tags=['jen'])
def say_hi(user_name: str):
    time.sleep(20)
    print("Hello", user_name)


@flow(log_prints=True)
def hello(user: str = "world"):
    say_hi(user)


