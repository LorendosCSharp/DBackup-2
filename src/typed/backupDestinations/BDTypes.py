from typing import Union, Annotated
from pydantic import Discriminator, Field

from src.typed.backupDestinations.baseDestination import BaseBD, BaseBDPub
from src.typed.backupDestinations.sshDestination import SshBD, SshBDPub
from src.typed.backupDestinations.telegramDestination import TelegramBD, TelegramBDPub


def get_type(v):
    if isinstance(v, dict):
        return v.get("type")
    return v.type


BDTypes = Annotated[Union[BaseBD, SshBD, TelegramBD],  Field(discriminator="type"),]
BDTypesPub = Annotated[Union[BaseBDPub, SshBDPub, TelegramBDPub],  Field(discriminator="type"),]