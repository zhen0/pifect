from prefect import flow, task
from prefect.deployments import Deployment
import requests

@flow
def surf():
    """
    This flow surfs.

    :return: `None` if the job was submitted succesfully
    """
    response = requests.post(
        url='bob'
    )

    if not response.ok:
        return response.raise_for_status()

    return None


deployment = Deployment.build_from_flow(
    flow=surf,
    name="surf",
    work_queue_name="test",
    description="am i being used?"
)

if __name__ == "__main__":
    deployment.apply()