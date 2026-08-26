import logging
import os
from typing import Any

from dotenv import load_dotenv

from src.core.storage.storageLayer import PydanticStorage
from src.typed.backupDestinations.BDTypes import BDTypes
from src.typed.backupService import BPS
from src.typed.backupTargets.BTTypes import BTTypes

load_dotenv()

outputPath = os.getenv("BACKUP_FILES_PATH")

BPSList: list[BPS] = []
storage: PydanticStorage | None = None


def findBPS(id: str) -> BPS | None:
    for bps in BPSList:
        if getattr(bps, "id", None) == id:
            return bps
    return None


def loadBPSList() -> None:
    global BPSList
    global storage

    storage = PydanticStorage(path="./BPSData.lmdb")
    BPSList = storage.list_all()


def _ensureStorage() -> PydanticStorage:
    global storage

    if storage is None:
        loadBPSList()

    return storage  # type: ignore[return-value]


def addBPS(bps: BPS):
    storage_instance = _ensureStorage()
    storage_instance.save(bps, bps.id)
    BPSList.append(bps)


def deleteBPS(id: str):
    bps = findBPS(id)
    if bps is None:
        print(f"Error while deleting BPS: There is no BPS with id: {id}")
        return None

    BPSList.remove(bps)
    _ensureStorage().delete(bps.id)
    return bps

def updateBPS(bps: BPS, id: str):
    current = findBPS(id)
    if current is None:
        print(f"Error while updating BPS: There is no BPS with id: {id}")
        return None

    incoming_state = bps.__dict__.copy()
    incoming_state.pop("id", None)
    current.__dict__.update(incoming_state)
    current.id = id
    _ensureStorage().save(current, current.id)
    return current


def generateFiles(bps: BPS):
    generated_paths: list[str] = []
    for backupTarget in bps.targets:
        try:
            result = backupTarget.package(bps.id)
            if result:
                generated_paths.append(result)
        except Exception as exc:
            logging.error(f"Error while generating backup for BPS {bps.id}: {exc}")
            raise
    return generated_paths


def sendFilesToDestination(bps: BPS):
    if not outputPath:
        raise RuntimeError("BACKUP_FILES_PATH not configured")

    backupPathForThisBPS = os.path.join(outputPath, bps.id)
    os.makedirs(backupPathForThisBPS, exist_ok=True)

    allBackupFiles: list[str] = os.listdir(backupPathForThisBPS)
    sortedBackupFiles: list[str] = []
    for file in allBackupFiles:
        filepath = os.path.join(backupPathForThisBPS, file)
        if os.path.isfile(filepath):
            sortedBackupFiles.append(filepath)

    for filepath in sortedBackupFiles:
        destinations: list[BDTypes] = bps.destinations
        for backupDestination in destinations:
            try:
                backupDestination.sendTo(filepath)
            except Exception as exc:
                logging.error(f"Error while sending backup {filepath} to destination: {exc}")

    return sortedBackupFiles


def triggerBackup(id: str):
    bps = findBPS(id)

    if bps is None:
        raise ValueError(f"Couldn't find BPS with id {id} while backuping")

    generated_paths = generateFiles(bps)
    sent_paths = sendFilesToDestination(bps)
    return {"generated": generated_paths, "sent": sent_paths}


def triggerBackupForAll():
    results = []
    for bps in BPSList:
        if getattr(bps, "include", True) is False:
            continue
        results.append(triggerBackup(bps.id))
    return results


def returnBPSList():
    return BPSList.copy()



def findDestination(id: str, destid: str) -> tuple[BDTypes, int] | None:
    for bps in BPSList:
        if getattr(bps, "id", None) == id:
            for i, destination in enumerate(bps.destinations):
                if getattr(destination, "id", None) == destid:
                    return destination, i
    return None


def updateDestination(id: str, destid: str, value: BDTypes):
    bps = findBPS(id)
    if bps is None:
        print(f"Couldn't find BPS with this id {id} while updating a destination")
        return None

    destination = findDestination(id, destid)
    if destination is None:
        print(f"Couldn't find destination with this id {destid} while updating a destination")
        return None

    bps.destinations[destination[1]] = value
    _ensureStorage().save(bps, bps.id)
    return destination[0]


def deleteDestination(id: str, destid: str):
    bps = findBPS(id)
    if bps is None:
        print(f"Couldn't find BPS with this id {id} while deleting a destination")
        return None

    destination = findDestination(id, destid)
    if destination is None:
        print(f"Couldn't find destination with this id {destid} while deleting a destination")
        return None

    bps.destinations.remove(bps.destinations[destination[1]])
    _ensureStorage().save(bps, bps.id)
    return "sigma"


def findTarget(id: str, targid: str) -> tuple[BTTypes, int] | None:
    for bps in BPSList:
        if getattr(bps, "id", None) == id:
            for i, target in enumerate(bps.targets):
                if getattr(target, "id", None) == targid:
                    return target, i
    return None


def updateTarget(id: str, targid: str, value: BTTypes):
    bps = findBPS(id)
    if bps is None:
        print(f"Couldn't find BPS with this id {id} while updating a target")
        return None

    target = findTarget(id, targid)
    if target is None:
        print(f"Couldn't find target with this id {targid} while updating a target")
        return None

    bps.targets[target[1]] = value
    _ensureStorage().save(bps, bps.id)
    return target[0]


def deleteTarget(id: str, targid: str):
    bps = findBPS(id)
    if bps is None:
        print(f"Couldn't find BPS with this id {id} while deleting a destination")
        return None

    target = findTarget(id, targid)
    if target is None:
        print(f"Couldn't find destination with this id {targid} while deleting a destination")
        return None

    bps.targets.remove(bps.targets[target[1]])
    _ensureStorage().save(bps, bps.id)
    return "sigma"


