from pydantic import BaseModel
from src.typed.docker.mount import Mount

class Container(BaseModel):
    # the list is hre because for some reason docker saves the name of a container as a list
    Names:list[str]
    State:str
    Id:str
    Mounts:list[Mount]