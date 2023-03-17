from helloFlowGH import hello
from prefect.deployments import Deployment
from prefect.filesystems import GitHub

gh_block = GitHub.load("jen-gh")

deployment = Deployment.build_from_flow(
    flow=hello,
    name="gh-hello",
    work_queue_name="jj",
    storage=gh_block,
    description="Jenny's test deployment for github"
)

deployment.apply()