from prefect import flow
from prefect.deployments import Deployment


@flow(log_prints=True)
def hi():
    print("Hi from Prefect! 🤗")

deployment = Deployment.build_from_flow(
    flow=hi,
    name="prefect-markdown-deployment",
    description="# My Depoyment with a markdown header ```some code``` some text and a link [link](https://www.google.com)"
)

deployment.apply()