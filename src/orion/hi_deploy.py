from prefect import flow
from prefect.deployments import Deployment


@flow(log_prints=True)
def hi():
    print("Hi from Prefect! 🤗")

deployment = Deployment.build_from_flow(
    flow=hi,
    name="prefect-example-deployment",
)

deployment.apply()