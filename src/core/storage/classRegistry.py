from pydantic import BaseModel


class ClassRegistry():
    def __init__(self) -> None:
        self.classes:dict[str,type[BaseModel]]={}
        
    def add(self, classType:type[BaseModel]):
        self.classes[classType.__name__]=classType
        return classType
    
    def get(self,classStr:str):
        if classStr not in self.classes:
            raise ValueError(f"Couldn't parse! The class {classStr} is not included")
        return self.classes[classStr]
    
registry=ClassRegistry()