import os

from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

key:str=os.getenv("ENCRYPTION_KEY") # type: ignore
backupPath:str=os.getenv("BACKUP_FILES_PATH") # type: ignore

def encrypt_backup(backup_path:str) -> str:
    global key
    global backupPath
    if key is None:
        raise RuntimeError("ENCRYPTION_KEY not configured")
    
    if not os.path.exists(backup_path):
        raise FileNotFoundError(backup_path)
    
    _,filename=os.path.split(backup_path)
    
    with open(backup_path,"rb") as file:
            data=file.read()        
    fernet=Fernet(key.encode())
    encryptedData=fernet.encrypt(data)
    encryptedFolder=os.path.join(backupPath,"encrypted")
    if not os.path.exists(encryptedFolder):
        os.mkdir(encryptedFolder)
        
    encryptedPath=os.path.join(encryptedFolder,filename+".enc")
    with open(encryptedPath,"wb") as file:
        file.write(encryptedData)
    return encryptedPath

def decrypt_backup(backup_path:str) -> str:
    global key
    global backupPath
    
    if key is None:
        raise RuntimeError("ENCRYPTION_KEY not configured")
    
    if not os.path.exists(backup_path):
        raise FileNotFoundError(backup_path)
    
    _,filename=os.path.split(backup_path)
    if not filename.endswith(".enc"):
        raise ValueError("Provided file is not encrypted")
    
    with open(backup_path,"rb") as file:
            data=file.read()        
    fernet=Fernet(key.encode())
    decryptedData=fernet.decrypt(data)
    decryptedPath=os.path.join(backupPath,filename[:-4])
    with open(decryptedPath,"wb") as file:
        file.write(decryptedData)
    return decryptedPath