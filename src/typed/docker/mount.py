from pydantic import BaseModel
from typing import Optional

class Mount(BaseModel):
    Type:str
    Name:Optional[str]=None
    Source:str
    Destination:str
    Driver:Optional[str]=None
    Mode:str
    RW:bool
    Propagation:Optional[str]=None
