from prefect import task, Flow

with Flow ('empty') as flow:
    

    flow.deploy(project_name="Jenny")