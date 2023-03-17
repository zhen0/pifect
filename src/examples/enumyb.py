from prefect import flow
from enum import Enum
from prefect.deployments import Deployment
from pydantic import BaseModel,Field

class ModeSelect(str, Enum):
    create = "create",
    resign = "resign"
   
class Param(BaseModel):
    mode: ModeSelect=Field(default = ModeSelect.create, required = True)
   
@flow
def enumy(param: Param):
    print("running")

deployment = Deployment.build_from_flow(
    flow=enumy,
    name="enumy-deployment",
)

deployment.apply()