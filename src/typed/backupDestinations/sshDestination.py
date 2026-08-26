
import logging
from typing import Literal

from src.core.storage.classRegistry import registry
from src.typed.backupDestinations.baseDestination import BaseBD, BaseBDPub
from src.utils.objectUtils import generateID

from paramiko import AuthenticationException, SSHClient, SSHException
from scp import SCPClient


@registry.add
class SshBD(BaseBD):
    type: Literal["ssh"] = "ssh"
    user: str
    ip: str
    port:int=22
    keyPath: str
    remoteDirectory:str="home/backups"
    
    @classmethod
    def from_pub(cls, pubInstance: "SshBDPub") -> "SshBD":
        return cls(**pubInstance.model_dump(), id=generateID())
    
    def sendTo(self,path:str):
        try:
            ssh = SSHClient()
            ssh.load_system_host_keys()

            ssh.connect(
                username=self.user,
                hostname=self.ip,
                key_filename=self.keyPath,
                port=self.port
            )
            transport=ssh.get_transport()
            if transport is None:
                raise RuntimeError("SSH transport is unavaliable!")
            scp=SCPClient(transport)
            scp.put(path, remote_path=self.remoteDirectory)
            scp.close()
            
        except AuthenticationException as e:
            logging.error(f"Error while authenticating to ssh destination: {e}")
        except SSHException as e:
            logging.error(f"Error in ssh destination: {e}")
        except Exception as e:
            logging.error(f"General error in ssh destination: {e}")

@registry.add
class SshBDPub(BaseBDPub):
    type: Literal["ssh"] = "ssh"
    user: str
    ip: str
    port:int=22
    keyPath: str
    remoteDirectory:str