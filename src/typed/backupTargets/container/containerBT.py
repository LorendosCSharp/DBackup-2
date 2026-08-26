from typing import Literal

from src.typed.backupTargets.baseTarget import BaseBT, BaseBTPub
from src.typed.docker.container import Container
from src.core.storage.classRegistry import registry
from src.utils.objectUtils import generateID

@registry.add
class ContainerBT(BaseBT):
    type: Literal["container"] = "container"
    container: Container
        
    @classmethod
    def from_pub(cls, pubInstance: "ContainerBTPub") -> "ContainerBT":
        return cls(**pubInstance.model_dump(), id=generateID())

@registry.add
class ContainerBTPub(BaseBTPub):
    type: Literal["container"] = "container"
    container: Container

