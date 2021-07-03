from Modules.CustomWidget import *

import hashlib
import platform
import os
from cryptography.fernet import Fernet
import subprocess
import string , random

class Encryption():
  def __init__(self,*,password):
    Hash = self._checkPass(password)
    if Hash[0] == "DONE":
      self.hash = Hash[1]
  def _getSalt(self) -> str:
    _salt = "$" + platform.system() +  "$"
    return _salt
  def _salted(self, passwd:str) -> str: 
    _salt = self._getSalt()
    _saltedPassword = ""
    letter_count = 0
    for letter in passwd:
      if letter_count == 3:
        _saltedPassword += _salt
        letter_count = 0
      _saltedPassword += letter
      letter_count += 1
    return self._hashCreate(_saltedPassword)
  def _checkPass(self,passwd:str) -> str:
    hashedPasswd = self._salted(passwd)
    return "DONE",hashedPasswd
  def _hashCreate(self,_saltedPasswd:str) -> str:
    _hashedPassword = hashlib.sha256(_saltedPasswd.encode("utf-8")).hexdigest()
    return _hashedPassword

class Linux_wifi(MyWidgits):
    def __init__(self,obj):
        self.get_dixt_pass()
        self.obj = obj
    def get_dixt_pass(self):
        path = LINUX_WIFI_DIR_PATH
        try :
            files = os.listdir(path)
        except:
            self.wifi_unroot("Wifi Data Not Found","Unable to find wifi passwords..",self.obj)
            return
        self.dictt = []
        if len(files) > 0:
            temp = {}
            for filee in files:
                with open(os.path.join(path,filee)) as f:
                    data = f.read().split("\n")
                    for i in data:
                        if i.startswith("ssid"):
                            temp["ssid"] = i[5:]
                        elif i.startswith("psk"):
                            temp["psk"] = i[4:]
                        else:
                            continue
                    if "ssid" not in temp.keys(): temp["ssid"] ="None"
                    if "psk" not in temp.keys(): temp["psk"] = "None"
                self.dictt.append(temp)
                temp = {}
        else:
            self.wifi_unroot("Wifi Data Not Found","Unable to find wifi passwords..",self.obj)
        self.dictt

class Win_wifi(MyWidgits):
    def __init__(self,obj):
        self.obj = obj
        self.get_wifi()
    def get_wifi(self):
        data = subprocess.check_output(["netsh","wlan","show","profile"])
        data = data.decode("utf-8",errors="backslashreplace")
        data = data.split("\n")
        wifi = []
        for i in data:
            if "All User Profile" in i:
                w = i.split(":")[1].strip()
                if w: wifi.append(w)
        self.get_pass(wifi)
    def get_pass(self,wifis):
        if wifis:
            self.maindic = []
            for wifi in wifis:
                ssid , auth , security , pwd = None ,None,None,None
                data = subprocess.check_output(["netsh","wlan","show","profile",wifi,"key=clear"])
                data = data.decode("utf-8",errors="backslashreplace")
                data = [i.strip() for i in data.split("\n") if i != "\r"]
                dictt = {}
                dictt["ssid"] = wifi
                for i in data:
                    if i.startswith("Authentication"):
                        dictt["Authentication"] = i.split(":")[1].strip()
                    elif "Security Key" in i:
                        dictt["Security Key"] = i.split(":")[1].strip()
                    elif "Key Content" in i:
                        dictt["psk"] = i.split(":")[1].strip()
                self.maindic.append(dictt)
                dictt = {}
            self.maindic
        else:
            self.wifi_unroot("No Saved Wifi..","No saved wifi found on your device..",self.obj)

class Add_Password():
    def __init__(self):
        self.key = Fernet.generate_key()
    def create_password_encrypted(self,password):
        fernet = Fernet(self.key)
        enc_pwd = fernet.encrypt(password.encode())
        return enc_pwd.decode()[:-1]+self.key.decode()[:-1]
    def extract_encrypted_password(self,encpass):
        fernet = Fernet((encpass[-43:]+"=").encode())
        return fernet.decrypt((encpass[:-43]+"=").encode()).decode()


class Password_Creator():
    def __init__(self):
        self.mixin = ""
    def create_pass(self,passlength,small,large,num,special):
        if small or large or num or special:
            if small:
                self.mixin += string.ascii_lowercase
            if large:
                self.mixin += string.ascii_uppercase
            if num:
                self.mixin += string.digits
                if not large and not small and not special:
                    if not passlength <= 10:
                        passlength = 10
            if special:
                self.mixin += string.punctuation
        else:
            return None
        return ["".join(random.sample(self.mixin,passlength)) for x in range(0,TOTAL_PASSWORD_GENERATION)]
   

