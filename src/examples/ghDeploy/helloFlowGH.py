from prefect import task, flow

import time


@task(tags=['blue'], persist_result=True)
def say_hi(user_name: str):
    time.sleep(20)
    return user_name


@flow
def hello(user: str = "world", persist_result=True):
    say_hi(user)
    return 'blue'




