from prefect import task, flow

import time


@task(tags=['blue'])
def say_hi(user_name: str):
    logger = get_run_logger()
    time.sleep(20)
    logger.info("Hello %s!", user_name)


@flow
def hello(user: str = "world"):
    say_hi(user)




if __name__ == "__main__":
    hello()