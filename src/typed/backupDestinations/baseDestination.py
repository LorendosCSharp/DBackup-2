from typing import Literal

from pydantic import BaseModel, PrivateAttr

from src.core.storage.classRegistry import registry
from src.utils.objectUtils import generateID

@registry.add
class BaseBD(BaseModel):
    type: Literal["base"] = "base"
    id: str
    
    @classmethod
    def from_pub(cls, pubInstance: "BaseBDPub") -> "BaseBD":
        return cls(**pubInstance.model_dump(), id=generateID())
    
    def testDestination(self):
        return "basic BD"
    
    def sendTo(self,path:str):
        pass

@registry.add
class BaseBDPub(BaseModel):
    type: Literal["base"] = "base"

    