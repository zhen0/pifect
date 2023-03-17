import time
from datetime import datetime

from prefect import flow, task, get_run_logger


@task(name="Test Task")
def test_task(my_range):
    logger = get_run_logger()
    logger.info(my_range)
    time.sleep(2)
    logger.info(datetime.today())

@flow(name="Test Flow")
def test_flow():
    iterate_list = [x for x in range(2888)]
    blah = test_task.map(iterate_list)
    print(blah)


if __name__ == "__main__":
    test_flow()