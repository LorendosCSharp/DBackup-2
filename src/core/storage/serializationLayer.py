import json
from pydantic import BaseModel

from src.core.storage.classRegistry import registry

def serialize(obj:BaseModel):
    output:bytearray= bytearray(b"")
    
    className=obj.__class__.__name__
    objectDict=obj.model_dump()
    
    classNameBytes=len(className).to_bytes(4, "big")+className.encode("utf-8")
    dataRaw=json.dumps(objectDict, separators=(",", ":")).encode("utf-8")
    data=len(dataRaw).to_bytes(4,"big")+dataRaw
    output+=classNameBytes
    output+=data
    
    return output

def deserialize(byteInp:bytearray) -> Any:
    
    classNameLength=int.from_bytes(byteInp[:4],byteorder="big",signed=True)
    className=byteInp[4:4+classNameLength].decode("utf-8")
    dataLength=int.from_bytes(byteInp[4+classNameLength:8+classNameLength],byteorder="big",signed=True)
    data=byteInp[8+classNameLength:8+classNameLength+dataLength].decode("utf-8")

    obj=registry.get(className).model_validate_json(data)
    
    return obj