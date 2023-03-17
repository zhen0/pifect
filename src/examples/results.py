from prefect import flow, task
from prefect.deployments import Deployment

@task
def hello():
    print('hello from task')
    return {'description': "hello"}

@flow(log_prints=True, persist_result=True)
def hi():
    hello()
    print("Hi from flow")
    return {'description': "hello"}

# deployment = Deployment.build_from_flow(
#     flow=hi,
#     name="prefect-example-result-deployment",
# )

# deployment.apply()

result = hi()
print(result)