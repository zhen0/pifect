from edges import edges
from prefect.deployments import Deployment
from prefect.filesystems import GitHub, S3

gh_block = GitHub.load("jen-gh")
s3_block = S3.load("jen-s3")

deployment = Deployment.build_from_flow(
    flow=edges,
    name="s3-edges",
    storage=s3_block,
    description="Jenny's edges deployment for s3"
)

deployment.apply()