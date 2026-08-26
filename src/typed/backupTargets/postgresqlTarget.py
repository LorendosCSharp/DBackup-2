from typing import Literal

from src.typed.backupTargets.baseTarget import BaseBT, BaseBTPub
from src.core.storage.classRegistry import registry
from src.utils.objectUtils import generateID

@registry.add
class PostgresqlBT(BaseBT):
    type: Literal["postgres"] = "postgres"
    path: str
    
    @classmethod
    def from_pub(cls, pubInstance: "PostgresqlBTPub") -> "PostgresqlBT":
        return cls(**pubInstance.model_dump(), id=generateID())
    
    
    def package(self)->str:
        return ""

@registry.add
class PostgresqlBTPub(BaseBTPub):
    type: Literal["postgres"] = "postgres"
    path: str