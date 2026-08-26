import os
import shutil
from typing import Literal

from dotenv import dotenv_values
from pydantic import PrivateAttr

from src.core.backupGenerator import generateSplitBackups
from src.typed.backupDestinations.baseDestination import BaseBD, BaseBDPub
from src.core.storage.classRegistry import registry
from src.utils.objectUtils import generateID
from telebot import TeleBot
from telebot.apihelper import ApiException
@registry.add


class TelegramBD(BaseBD):
    type: Literal["tg"] = "tg"
    # To get this use @userinfobot in telegram itseld
    chatId: int
    botKeyPath:str
    
    @classmethod
    def from_pub(cls, pubInstance: "TelegramBDPub") -> "TelegramBD":
        
        # this is to deal with PrivateAttr
        instance = cls(**pubInstance.model_dump(), id=generateID())
        #instance.botKey=botKey
        return instance
    
    def sendTo(self,path:str):
        try:  
            botKey=dotenv_values(self.botKeyPath).get("BOT_KEY")
            if not botKey:
                raise ValueError(f"BOT_KEY not found in {self.botKeyPath}")
            print(path)
            print("Sending to telegram")
            bot=TeleBot(botKey)
            returnedSplitPath=generateSplitBackups(path,13)
            splitPaths=os.listdir(returnedSplitPath)
            
            bot.send_message(self.chatId,f"Sending {path}")
            for filePath in splitPaths:
                splitPath=os.path.join(returnedSplitPath,filePath)
                print(splitPath)
                with open(splitPath,"rb") as splitFile:
                    bot.send_document(self.chatId,splitFile)
            bot.send_message(self.chatId,f"Finished for {path}")
            shutil.rmtree(returnedSplitPath, ignore_errors=True)
                

            
        except ApiException as e:
            print(f"Error while communicating with Telegram: {e}")
            pass
        except FileNotFoundError as e:
            print(f"Error, file not found: {e}")
            pass
        except PermissionError as e:
            print(f"Permission denied: {e}")
            pass
        except Exception as e:
            print(f"Error while sending packages to TelegramBD: {e}")
            pass
        

@registry.add
class TelegramBDPub(BaseBDPub):
    type: Literal["tg"] = "tg"
    chatId: int
    botKeyPath:str