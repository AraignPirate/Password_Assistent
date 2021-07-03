# Root App Path Support import
from pathlib import Path
import json,os
# App Settings Global
APP_FILES = "Appfiles"
DB_NAME = "Assist.db"
APP_UI_FILE = "App.UI"
ROOT_APP_PATH = Path().resolve()
ALL_REQUIRED_FILES = ["Gruppo-Regular.ttf","Righteous-Regular.ttf"]
REQUIRED_MODULES = []
IMAGE_LOGO = "Icon.png"
LOGO_API = "https://besticon-demo.herokuapp.com/allicons.json?url="
LOGO_DIR = "Logo"
LOG_FILE = "App_Logs.log"
APP_NAME = "Password Assistent"
DEFAUTL_LOGO = "DEFAULT.png"
SETTINGS_JSON = "settings.json"
LINUX_WIFI_DIR_PATH ="/etc/NetworkManager/system-connections/"
TOTAL_PASSWORD_GENERATION = 15
LOG_DIR = "Logs"
with open(os.path.join(ROOT_APP_PATH,APP_FILES,SETTINGS_JSON),"r") as settingsfile:
    SETTINGS = json.load(settingsfile)


