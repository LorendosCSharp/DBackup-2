from datetime import datetime
import gzip
import logging
import os
import tarfile
import tempfile

from dotenv import load_dotenv
from src.core.dockerManager import getContainerNameFromID, pauseContainer, startTempContainer, unpauseContainer
from src.core.encryption import encrypt_backup
load_dotenv()
outputPath=os.getenv("BACKUP_FILES_PATH")
if not outputPath:
    raise RuntimeError("BACKUP_FILES_PATH not configured")
def generateForFile(path:str,BPSId:str,containerID:str="", forContainer:bool=True)-> str:
    
    try:
        outputPathWithBPSId=os.path.join(outputPath,BPSId)  # type: ignore
        containerName=""
        if forContainer:
            containerName=getContainerNameFromID(containerID)
        else:
            containerName=os.path.basename(path)
        
        currentTime = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        filename = f"{currentTime}_{containerName}.tar.gz"
        target= os.path.join("/temp",filename)
        
        os.makedirs(outputPathWithBPSId, exist_ok=True)
        os.chmod(outputPathWithBPSId, 0o1777)
        
        if forContainer:
            pauseContainer(containerID)
        
        command=f"tar czf {target} /data"
        result,logs=startTempContainer("test",command,{
            path:{"bind":"/data","mode":"ro"},
            outputPathWithBPSId:{"bind":"/temp","mode":"rw"}
        })
        
        logging.info(f"logs from running temp container {logs}")
        if result.get("StatusCode") !=0:
            logging.error(f"Error while executing temp container for generateForFile, path: {path}")  
            raise RuntimeError(f"Error while executing temp container for generateForFile, path: {path}")
        

        if forContainer:
            unpauseContainer(containerID)
        
        archivePath = os.path.join(outputPathWithBPSId, filename)
        encryptedFilePath = encrypt_backup(archivePath)
        
        return outputPathWithBPSId
    except Exception as e:
        logging.error(f"Couldn't generate backup for {path}. Error: {e}")
        return path

# returns path to a folder containing all chunks

def generateSplitBackups(path: str, maxSize: int) -> str:
    try:
        print("Path from spliter(before with)",path)
        with tempfile.TemporaryDirectory() as extracted_dir:
            print("Path from spliter(in with)",path)
            # Extract original archive
            with tarfile.open(path, "r:gz") as tar:
                print("Path from spliter(in second with)",path)
                tar.extractall(extracted_dir)


            archive_name = os.path.splitext(os.path.splitext(os.path.basename(path))[0])[0]
            
            extendedOutputPath=os.path.join(outputPath,archive_name) #type:ignore
            
            # this is to fix permission error
            os.makedirs(extendedOutputPath, exist_ok=True)
            os.chmod(extendedOutputPath, 0o1777)
            
            
            # Re-create tar.gz and split into chunks
            command = (
                f"sh -c 'tar -czf - -C /data . | "
                f"split -b {maxSize}m - /temp/{archive_name}.tar.gz.'"
            )

            result, logs = startTempContainer("test",command,{
                    extracted_dir: {"bind": "/data", "mode": "ro"},
                    extendedOutputPath: {"bind": "/temp", "mode": "rw"}
            })

            logging.info(f"(split)logs from running temp container {logs}")
            if result.get("StatusCode") != 0:
                print("skibidi")
                raise RuntimeError(f"Container failed while generating chunks for {path}")

            return extendedOutputPath

    except Exception as e:
        logging.error(f"Couldn't generate chunks for {path}. Error: {e}")
        return path
    

def generateForDatabase(path:str):
    
    
    
    pass