import asyncio
from fastapi import APIRouter, WebSocket
from fastapi.encoders import jsonable_encoder
from src.core.dockerManager import listAllContainers,convertContainersToPydanticContainers,extractRunningContainers
from src.typed.docker.container import Container
router = APIRouter(prefix="/docker",tags=["docker"])

@router.get("/containers")
def get_Containers() ->list[Container]:    
    containers = listAllContainers()
    return convertContainersToPydanticContainers(containers)

@router.websocket("/containers/stream")
async def get_Containers_Stream(websocket:WebSocket) ->list[Container]:
    await websocket.accept()
    while True:
        
        containers= listAllContainers()
        convertedOnes:list[Container]=convertContainersToPydanticContainers(containers)
        
        await websocket.send_json(jsonable_encoder(convertedOnes))
        await asyncio.sleep(1)


@router.get("/containers/running")
async def get_Running_Containers()->list[Container]:
    containers = listAllContainers()
    runningOnes=extractRunningContainers(containers)
    return convertContainersToPydanticContainers(runningOnes)

@router.websocket("/containers/running/stream")
async def get_Running_Containers_Stream(websocket:WebSocket)->list[Container]:
    await websocket.accept()
    while True:
        
        containers = listAllContainers()
        runningOnes=extractRunningContainers(containers)
        convertedOnes:list[Container]=convertContainersToPydanticContainers(runningOnes)
        
        await websocket.send_json(jsonable_encoder(convertedOnes))
        await asyncio.sleep(1)
