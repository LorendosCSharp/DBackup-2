#import docker

import logging
import os

import docker
from docker.errors import NotFound
from docker.models.containers import Container as DockerContainer
from src.typed.docker.container import Container
from src.typed.docker.mount import Mount


dockerClient = docker.from_env()


def listAllContainers():
    containers: list[DockerContainer] = dockerClient.containers.list(all=True)
    return containers


def extractMounts(containers: list[DockerContainer]):
    containerMounts = {}

    for container in containers:
        mountsRaw = container.attrs.get("Mounts", [])
        mountsObjects = []

        for mount in mountsRaw:
            mountObject = Mount(**mount)
            mountsObjects.append(mountObject)

        containerMounts[container.id] = mountsObjects

    return containerMounts


def extractNames(containers: list[DockerContainer]):

    names: list[str] = []

    for container in containers:
        name = container.attrs.get("Name", "")
        names.append(name)

    return names


def extractRunningContainers(containers: list[DockerContainer]):
    runningContainers: list[DockerContainer] = []

    for container in containers:
        if container.attrs.get("State", {}).get("Status") == "running":
            runningContainers.append(container)

    return runningContainers


# This is for FastAPI
def convertContainersToPydanticContainers(
    containers: list[DockerContainer],
):
    convertedContainers = []

    for container in containers:
        attrs = container.attrs
        convertedContainer = Container(
            Id=attrs.get("Id", ""),
            Names=[attrs.get("Name", "")],
            State=attrs.get("State", {}).get("Status", ""),
            Mounts=[
                Mount(**mount)
                for mount in attrs.get("Mounts", [])
            ],
        )
        convertedContainers.append(convertedContainer)

    return convertedContainers


def startTempContainer(name:str,command:str,voulems)->tuple[dict[str,int],str]:
    container=dockerClient.containers.run(
        name=name,
        image="alpine",
        command=command,
        detach=True,
        volumes=voulems,
        user=f"{os.getuid()}:{os.getgid()}"
    )
    result,logs=container.wait(),container.logs().decode()
    container.remove()
    return result,logs
    
def pauseContainer(containerID:str):
    if not checkContainerID(containerID):
        return
    
    container=dockerClient.containers.get(containerID)
    
    if container.status =="paused":
        logging.warning(f"Container {containerID} is already paused")
        return
    
    container.pause()
    logging.info(f"Paused a container {containerID}")

def unpauseContainer(containerID:str):
    if not checkContainerID(containerID):
        return
    
    container=dockerClient.containers.get(containerID)
    
    if container.status != "paused":
        logging.warning(f"Container {containerID} is already unpaused")
        return
    
    container.unpause()
    logging.info(f"Unpaused a container {containerID}")



def checkContainerID(containerID:str):
    if containerID=="" or containerID is None:
        return False
    
    try:
        dockerClient.containers.get(containerID)
        return True
    except NotFound:
        logging.error(f"Container with id {containerID} does not exist")
        return False
    
def getContainerNameFromID(containerID:str) -> str | None:
    
    if not checkContainerID(containerID):
        return
    
    container= dockerClient.containers.get(containerID)
    return container.name
    
    
    
    pass