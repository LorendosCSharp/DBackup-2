from typing import Literal

from src.core.backupGenerator import generateForFile
from src.typed.backupTargets.baseTarget import BaseBT, BaseBTPub
from src.core.storage.classRegistry import registry
from src.utils.objectUtils import generateID

@registry.add
class FileBT(BaseBT):
    type: Literal["file"] = "file"
    path: str
    
    @classmethod
    def from_pub(cls, pubInstance: "FileBTPub") -> "FileBT":
        return cls(**pubInstance.model_dump(), id=generateID())
    
    def package(self,BPSId:str)-> str:
        path=generateForFile(self.path,BPSId,forContainer=False)
        return path

@registry.add
class FileBTPub(BaseBTPub):
    type: Literal["file"] = "file"
    path: str
    
    
    