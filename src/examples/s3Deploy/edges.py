from prefect import task, flow, allow_failure
import random
from prefect.filesystems import GitHub, S3

gh_block = GitHub.load("jen-gh")
s3_block = S3.load("jen-s3")

@task
def task_1():
    print("task 1 succeeded")


@task
def task_2():
    print("task 2 succeeded")


@task(persist_result=True)
def task_3():
    print("task 3 succeeded")
    return 'task 3 succeeded'


@task
def task_4():
    print("This task often fails")
    if random.random() > 0.5:
        raise ValueError("Non-deterministic error has occured.")
    else:
        print("task 4 succeeded")


@task(persist_result=True)
def task_5():
    print("task 5 succeeded")
    return 'task 5 succeeded'


@task
def clean_up_task():
    print("Cleaning up new 🧹")


@flow(log_prints=True, name="Some edges", persist_result=True, result_storage=s3_block, result_serializer='json')
def edges():
    # 1, 2, 3 can run concurrently
    one = task_1.submit()
    two = task_2.submit()
    three = task_3.submit()
    four = task_4.submit(wait_for=[one, two, three])
    five = task_5.submit()
    clean_up_task.submit(wait_for=[allow_failure(four), allow_failure(five)])
    return 'boo'

