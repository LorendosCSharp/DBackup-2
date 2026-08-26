from typing import Literal

from src.core.storage.classRegistry import registry
from src.typed.backupTargets.container.containerBT import ContainerBT, ContainerBTPub
from src.utils.objectUtils import generateID

@registry.add
class ContainerPostgresqlBT(ContainerBT):
    type: Literal["c_postgres"] = "c_postgres"
    path: str
    
    @classmethod
    def from_pub(cls, pubInstance: "ContainerPostgresqlBTPub") -> "ContainerPostgresqlBT":
        return cls(**pubInstance.model_dump(), id=generateID())
    
    
    def package(self)->str:
        return ""

@registry.add
class ContainerPostgresqlBTPub(ContainerBTPub):
    type: Literal["c_postgres"] = "c_postgres"
    path: str