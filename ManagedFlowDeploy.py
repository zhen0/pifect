from managedFlow import hello
from prefect.deployments import Deployment
from prefect.filesystems import GitHub

gh_block = GitHub.load("jen-gh")

deployment = Deployment.build_from_flow(
    flow=hello,
    name="managed-execution-hello",
    work_pool_name="prefect-managed-execution-pool",
    storage=gh_block,
    description="Jenny's test deployment for managed execution"
)

deployment.apply()