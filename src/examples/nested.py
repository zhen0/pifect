from prefect import flow
from prefect.deployments import Deployment
from pydantic import BaseModel


class SubModel(BaseModel):
    param1: str
    param2: int


class RootModel(BaseModel):
    param1: int
    sub_model: SubModel


@flow(log_prints=True)
def flow_with_pydantic_nested_parameters(root_parameters: RootModel):
    print(root_parameters)
    pass


if __name__ == "__main__":
    deployment = Deployment.build_from_flow(
        flow_with_pydantic_nested_parameters,
        name="flow_with_pydantic_nested_parameter",
    )
    deployment.apply()