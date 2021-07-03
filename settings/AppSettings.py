from ctypes import string_at
from sqlite3.dbapi2 import PARSE_COLNAMES

import os
import platform
import ctypes
import subprocess
from cryptography.fernet import Fernet as Encoder

from Modules.AppLogging import Logging
from settings.StaticVars import *
if not SETTINGS["UI_INFO"]:
    os.environ["KIVY_NO_CONSOLELOG"] = "1"
if SETTINGS["LOGS_TO_FILE"]:
    os.environ["PASSWORD_ASSISTENT_LOG"] = "FILE"
else:
    os.environ["PASSWORD_ASSISTENT_LOG"] = "STDOUT"
if SETTINGS["CUSTOM_INFO"]:
    os.environ["PASSWORD_ASSISTENT_LOG"] = "STDOUT"
logger = Logging("SETTINGS")
logger.start()
logger.info("Setting Environment")
logger.info("Loading Main App Configurations")
logger.info("Checking Platform")
# Platform specfic settings
SYSTEM = platform.system()
logger.info("Platform : "+SYSTEM)
if SYSTEM == "Windows":
    os.environ["KIVY_GL_BACKEND"]="angle_sdl2"


# Init Settings import
from kivy.config import Config

# Fixing window size
logger.info("Getting Window Size")
Config.set("graphics","resizable",False)
Config.set('kivy', 'log_dir', os.path.join(ROOT_APP_PATH,LOG_DIR))
logger.info("Setting Icon")
Config.set('kivy','window_icon',os.path.join(ROOT_APP_PATH,APP_FILES,IMAGE_LOGO))

from kivy.core.window import Window

logger.info("Platform Specific Settings done.")
# Platform Specific settings
logger.info("Setting Window Size")
if SYSTEM == "Windows": 
    width = int(ctypes.windll.user32.GetSystemMetrics(0))
    height = int(ctypes.windll.user32.GetSystemMetrics(1))
    if width > 1750:
        logger.info(f"Window : ('Height':{height*0.7},'Width':{width*0.22})")
        Window.size = (width*0.22,height*0.7)
    else:
        logger.info(f"Window : ('Height': 600,'Width':350)")
        Window.size = (350,600)
    try:
        ROOT = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if ROOT:
            logger.info(f"GOT ADMIN ACCESS")
        else:
            logger.warning("NO ADMINISTRATOR ACCESS")
    except Exception as e:
        ROOT = None
        
if SYSTEM == "Linux": 
    data = subprocess.Popen(["xrandr"],stderr=subprocess.PIPE,stdout=subprocess.PIPE).stdout
    data = subprocess.Popen(["grep","*"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=data).stdout.read().decode("utf-8")
    width = int(data.split()[0].split("x")[0]) 
    height = int(data.split()[0].split("x")[1])
    if width > 1750:
        logger.info(f"Window : ('Height':{height*0.7},'Width':{width*0.22})")
        Window.size = (width*0.22,height*0.7)
    else:
        logger.info(f"Window : ('Height': 600,'Width':300)")
        Window.size = (300,600)
    try:
        ROOT = os.getuid() == 0
        if ROOT:
            logger.info(f"GOT ROOT ACCESS")
        else:
            logger.warning("NO ROOT ACCESS")    
    except Exception as e:
        ROOT = None

# Font Styles and theme setting imports
from kivy.core.text import LabelBase
from kivymd.font_definitions import theme_font_styles


def get_app_ui():
    with open(os.path.join(ROOT_APP_PATH,APP_FILES,APP_UI_FILE),"rb") as discripter:
        logger.info("Decrypting UI")
        enui = discripter.read()
    decryptor = Encoder(enui[-44:])
    ui = decryptor.decrypt(enui[:-44]+b"==")
    return ui.decode("utf-8")

def set_style_and_theme(self):
    # Theme settings
    logger.info("Init Theme")
    self.theme_cls.primary_palette = "Green"
    self.theme_cls.primary_hue = "A700"
    self.theme_cls.theme_style = "Dark"
    # Font Settings
    logger.info("Init Fonts")
    LabelBase.register(name="Gruppo", fn_regular=os.path.join(ROOT_APP_PATH,APP_FILES,ALL_REQUIRED_FILES[0]))
    LabelBase.register(name="Right", fn_regular=os.path.join(ROOT_APP_PATH,APP_FILES,ALL_REQUIRED_FILES[1]))
    theme_font_styles.append("Gruppo")
    theme_font_styles.append("Right")
    self.theme_cls.font_styles["Gruppo"] = ["Gruppo",20,True,0.15]
    self.theme_cls.font_styles["Right"] = ["Right",18,True,0.15]
def load_settings(root):
    logger.info("Init Settings")
    obj = root.get_screen("userscreen").ids.userscreenmanager.get_screen("settings").ids
    obj.uilog.active = SETTINGS["UI_INFO"]
    obj.applog.active = SETTINGS["CUSTOM_INFO"]
    obj.logfile.active = SETTINGS["LOGS_TO_FILE"]

