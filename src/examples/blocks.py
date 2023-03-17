from typing import Union

from prefect.blocks.core import Block
from pydantic import AnyUrl, BaseModel, Field, SecretStr


class BrokenModel(BaseModel):
    name: str = Field(..., description="The name of the user")
    password: SecretStr = Field(..., description="The password of the user")
    happiness_rating: int = Field(..., description="The happiness rating of the user, where 0 is existential dread and 10 is bliss")


class BrokenBlock(Block):
    _block_type_name = "Broken UI"
    name: str = Field(..., description="The name of the block")
    broken: Union[BrokenModel, str] = Field(..., description="The broken field")