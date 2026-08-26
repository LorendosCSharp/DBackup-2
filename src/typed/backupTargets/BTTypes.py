from typing import Union, Annotated
from pydantic import Discriminator, Field

from src.typed.backupTargets.baseTarget import BaseBT, BaseBTPub
from src.typed.backupTargets.container.containerBT import ContainerBT, ContainerBTPub
from src.typed.backupTargets.container.containerFileTarget import ContainerFileBT, ContainerFileBTPub
from src.typed.backupTargets.container.containerPostgresqlTarget import ContainerPostgresqlBT, ContainerPostgresqlBTPub
from src.typed.backupTargets.fileTarget import FileBT, FileBTPub
from src.typed.backupTargets.postgresqlTarget import PostgresqlBT, PostgresqlBTPub


def get_type(v):
    if isinstance(v, dict):
        return v.get("type")
    return v.type


BTTypes = Annotated[Union[BaseBT,ContainerBT, FileBT, ContainerFileBT, PostgresqlBT, ContainerPostgresqlBT], Field(discriminator="type"),]
BTTypesPub = Annotated[Union[BaseBTPub,ContainerBTPub, FileBTPub, ContainerFileBTPub, PostgresqlBTPub, ContainerPostgresqlBTPub],  Field(discriminator="type"),]