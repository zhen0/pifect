from hedges import edges
from prefect.deployments import Deployment
from prefect.filesystems import GitHub

gh_block = GitHub.load("jen-gh")

deployment = Deployment.build_from_flow(
    flow=edges,
    name="gh-edges",
    work_pool_name="prefect-managed-execution-pool",
    storage=gh_block,
    description="Jenny's edges deployment for github"
)

deployment.apply()