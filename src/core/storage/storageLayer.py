import uuid

import lmdb
import msgpack
from pydantic import BaseModel

from src.core.storage.serializationLayer import deserialize, serialize
from src.utils.objectUtils import generateID


class PydanticStorage:
    
    def __init__(self,path:str="./Data.lmdb") -> None:
        self.database=lmdb.open(path,map_size=10*1024*1024)    

    def save(self, obj: BaseModel, obj_id: str | None = None) -> str:
        if obj_id is None:
            obj_id = getattr(obj, "_id", None)

        if obj_id is None:
            obj_id = generateID()

        data = serialize(obj)

        with self.database.begin(write=True) as txn:
            key:bytes=obj_id.encode("utf-8")
            value:bytes=msgpack.packb(data) # type: ignore
            txn.put(key, value) 

        return obj_id
    
    def get(self, obj_id: str) -> BaseModel | None:
        with self.database.begin() as txn:
            raw = txn.get(obj_id.encode())
            if raw is None:
                return None

            data = msgpack.unpackb(raw)
            return deserialize(data)
    
    def delete(self, obj_id: str) -> None:
        with self.database.begin(write=True) as txn:
            txn.delete(obj_id.encode())
            
    def list_all(self):
        with self.database.begin() as txn:
            return [
                deserialize(msgpack.unpackb(value))
                for _, value in txn.cursor()
            ]