from prefect import task, Flow, Parameter
from prefect.storage import GitHub
# from prefect.engine.signals import FAIL
import time
# from prefect.run_configs import ECSRun
# from prefect.run_configs import LocalRun
from prefect.run_configs import KubernetesRun
import prefect
from prefect.tasks.prefect.flow_run import StartFlowRun

new_flow = StartFlowRun(flow_name="Skip Flow", project_name="Jenny")

@task(name="")
def sleep_for_x(x):
    time.sleep(x)
    prefect.artifacts.create_link("ftp://ftp-server/my-file.csv")
    





with Flow(name="Start Flow") as flow:
    x = Parameter('x', default = 22, required= True)
    sleep_for_x(x)
    new_flow()

flow.run_config = KubernetesRun(cpu_request=2, memory_request="2Gi")
# flow.run_config = LocalRun(
    
#     labels=['runConfig']
# )

flow.storage = GitHub(
    repo="bestdan/pifect",                            # name of repo
    path="src/childFlow.py",                    # location of flow file in repo
    access_token_secret="Jen_Github_token"   # name of personal access token secret
)

flow.register('Jenny')

