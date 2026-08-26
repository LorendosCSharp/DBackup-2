from fastapi import APIRouter, HTTPException, Response

from src.core.bpsManager import *
from src.typed.backupService import *

router = APIRouter(prefix="/bps",tags=["bps"])


# BPS
@router.post("/")
def create_One(value:BPSPub)-> BPS:
    
    convertedBPS=BPS.from_pub(value)
    addBPS(convertedBPS)
    
    bpsList=returnBPSList()
    
    bps=bpsList[-1]
    #Kinda Validation
    #IDK if I will check the return object here or in the frontend
    if bps != None:
        return bps
    else:
        raise HTTPException(status_code=404,detail=f"Couldn't find BPS with id {id} while creating")
    

@router.put("/{id}")
def update_One(id:str,value:BPSPub)-> BPS:
    updateBPS(BPS.from_pub(value),id)
    #Kinda Validation
    #IDK if I will check the return object here or in the frontend
    bps=findBPS(id)
    
    if bps != None:
        return bps
    else:
        raise HTTPException(status_code=404,detail=f"Couldn't find BPS with id {id} while updating")

@router.get("/")
def get_All()-> list[BPS]:
    return returnBPSList()

@router.get("/{id}")
def get_One(id:str) -> BPS:
    bps=findBPS(id)
    
    if bps != None:
        return bps
    else:
        raise HTTPException(status_code=404,detail=f"Couldn't find BPS with id {id}")

@router.delete("/{id}")
def delete_One(id:str):
    if findBPS(id) == None:
        return HTTPException(status_code=500,detail=f"Couldn't delete BPS with id {id}")
    else:
        deleteBPS(id)
        return Response(status_code=200,content=f"Could delete BPS with id {id}")
        
    

@router.post("/backup/{id}")
def start_Backup_For(id:str):
    triggerBackup(id)
    return Response(status_code=200,content="Backup was succeeded")

@router.post("/backup")
def start_Backup_For_All():
    triggerBackupForAll()
    return Response(status_code=200,content="Backup was succeeded for all BPS")

