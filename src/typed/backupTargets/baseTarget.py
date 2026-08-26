from typing import Literal

from pydantic import BaseModel


from src.core.storage.classRegistry import registry
from src.utils.objectUtils import generateID

@registry.add
class BaseBT(BaseModel):
    type: Literal["base"] = "base"
    id: str
    
    # returns path to the compressed backup file
    def package(self)-> str:
        return ""
        
    
    @classmethod
    def from_pub(cls, pubInstance: "BaseBTPub") -> "BaseBT":
        return cls(**pubInstance.model_dump(), id=generateID())

@registry.add
class BaseBTPub(BaseModel):
    type: Literal["base"] = "base"


