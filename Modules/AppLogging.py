from colorama import init, Fore
from datetime import datetime as dt

from settings.StaticVars import LOG_DIR, ROOT_APP_PATH, APP_FILES, LOG_FILE

import os

init(autoreset=True)

class Logging():
    File = None
    def __init__(self,logername):
        if os.environ["PASSWORD_ASSISTENT_LOG"] == "STDOUT":
            self.switch = True
        elif os.environ["PASSWORD_ASSISTENT_LOG"] == "FILE":
            self.switch = False
            if Logging.File == None:
                    try:
                        os.mkdir(os.path.join(ROOT_APP_PATH,LOG_DIR))
                    except:
                        pass
                    Logging.File = open(os.path.join(ROOT_APP_PATH,LOG_DIR,LOG_FILE),"a")
        self.logername = logername
    def info(self,msg):
        if self.switch:
            print(Fore.WHITE+f'{dt.now().strftime("[%Y-%m-%d %H:%M:%S %p]")}' + Fore.GREEN +" INFO " +Fore.YELLOW+ self.logername +Fore.RESET+" "+Fore.WHITE+msg+Fore.RESET)
            return
        Logging.File.write(f'{dt.now().strftime("[%Y-%m-%d %H:%M:%S %p]")}'+" INFO "+ self.logername +" "+msg+"\n")
    def error(self,msg):
        if self.switch:
            print(Fore.WHITE+f'{dt.now().strftime("[%Y-%m-%d %H:%M:%S %p]")}' + Fore.RED +" ERROR " +Fore.YELLOW+ self.logername +Fore.RESET+" "+Fore.WHITE+msg+Fore.RESET)
            return
        Logging.File.write(f'{dt.now().strftime("[%Y-%m-%d %H:%M:%S %p]")}'+" ERROR " + self.logername +" "+msg+"\n")
    def warning(self,msg):
        if self.switch:
            print(Fore.WHITE+f'{dt.now().strftime("[%Y-%m-%d %H:%M:%S %p]")}' + Fore.BLUE +" WARNING " +Fore.YELLOW+ self.logername +Fore.RESET+" "+Fore.WHITE+msg+Fore.RESET)
            return
        Logging.File.write(f'{dt.now().strftime("[%Y-%m-%d %H:%M:%S %p]")}'+" WARNING " + self.logername +" "+msg+"\n")
    def traceback(self,data):
        if self.switch:
            print(Fore.YELLOW+"="*20)
            print(Fore.WHITE+data)
            print(Fore.YELLOW+"="*20)
            return
        Logging.File.write("="*20)
        Logging.File.write(data)
        Logging.File.write("="*20)
    def start(self):
        if self.switch:
            print(f"{Fore.WHITE}{dt.now().strftime('[%Y-%m-%d %H:%M:%S %p]')}==[{Fore.YELLOW}PASSWORD ASSISTENT{Fore.WHITE}]==[{Fore.GREEN}START{Fore.WHITE}]============>")
            return
        Logging.File.write(f"{dt.now().strftime('[%Y-%m-%d %H:%M:%S %p]')}==[PASSWORD ASSISTENT]==[START]============>\n")
    def __del__(self):
        if Logging.File:
            Logging.File.close()
            Logging.File = None
