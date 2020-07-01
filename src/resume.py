from prefect import task, Flow
from prefect.triggers import manual_only


@task
def return_data():
    return [1, 2, 3]

@task(trigger=manual_only)
def process_data(xs):
    return [i + 1 for i in xs]

@task(trigger=manual_only)
def process_data_again(xs):
    return [i + 2 for i in xs]

with Flow("Pause:Resume") as flow:
    process_data(return_data)
    process_data_again(return_data)

flow.register(project_name="Jenny")