from typing import Literal

from src.core.backupGenerator import generateForFile
from src.core.storage.classRegistry import registry
from src.typed.backupTargets.container.containerBT import ContainerBT, ContainerBTPub
from src.utils.objectUtils import generateID

@registry.add
class ContainerFileBT(ContainerBT):
    type: Literal["c_file"] = "c_file"
    path: str
    
    @classmethod
    def from_pub(cls, pubInstance: "ContainerFileBTPub") -> "ContainerFileBT":
        return cls(**pubInstance.model_dump(), id=generateID())
    
    def package(self,BPSId:str)-> str:
        path=generateForFile(self.path,BPSId,containerID=self.container.Id)
        return path

@registry.add
class ContainerFileBTPub(ContainerBTPub):
    type: Literal["c_file"] = "c_file"
    path: str
    
    
    