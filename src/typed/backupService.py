from datetime import datetime

from pydantic import BaseModel

from src.typed.backupDestinations.BDTypes import BDTypes, BDTypesPub
from src.typed.backupTargets.BTTypes import BTTypes, BTTypesPub
from src.core.storage.classRegistry import registry
from src.utils.objectUtils import generateID

@registry.add
class BPS(BaseModel):
    name: str
    destinations: list[BDTypes]
    targets: list[BTTypes]
    cronTime: str = "*_*_*_1_*_*_"
    lastExecution:float=0
    include: bool = True
    id: str
    
    # Convertion Abomination
    @classmethod
    def from_pub(cls, pubInstance: "BPSPub") -> "BPS":
        from src.typed.backupDestinations.baseDestination import BaseBD
        from src.typed.backupDestinations.sshDestination import SshBD
        from src.typed.backupDestinations.telegramDestination import TelegramBD

        from src.typed.backupTargets.baseTarget import BaseBT
        from src.typed.backupTargets.container.containerBT import ContainerBT
        from src.typed.backupTargets.container.containerFileTarget import ContainerFileBT
        from src.typed.backupTargets.container.containerPostgresqlTarget import ContainerPostgresqlBT
        from src.typed.backupTargets.fileTarget import FileBT
        from src.typed.backupTargets.postgresqlTarget import PostgresqlBT

        converters = {
            "BaseBDPub": BaseBD,
            "SshBDPub": SshBD,
            "TelegramBDPub": TelegramBD,
            "BaseBTPub": BaseBT,
            "ContainerBTPub": ContainerBT,
            "FileBTPub": FileBT,
            "ContainerFileBTPub": ContainerFileBT,
            "PostgresqlBTPub": PostgresqlBT,
            "ContainerPostgresqlBTPub": ContainerPostgresqlBT,
        }

        def convert(items):
            return [
                converters[item.__class__.__name__].from_pub(item)
                for item in items
                if item.__class__.__name__ in converters
            ]

        return cls(
            name=pubInstance.name,
            destinations=convert(pubInstance.destinations),
            targets=convert(pubInstance.targets),
            cronTime=pubInstance.cronTime,
            include=pubInstance.include,
            id=generateID(),
        )
    

    
@registry.add
class BPSPub(BaseModel):
    name: str
    destinations: list[BDTypesPub]
    targets: list[BTTypesPub]
    cronTime: str = "*_*_*_1_*_*_"
    include: bool = True
