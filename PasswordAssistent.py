from settings import AppSettings
from settings.MainImports import *

from Modules.AppLogging import Logging
from Modules.UISupport import *

logger = Logging("PWDASSIST")

## Password Asistent App
class Password_AssistentApp(MDApp):
    def __init__(self,**kawrg):
        logger.info("Iniciating Super Class")
        super(Password_AssistentApp,self).__init__(**kawrg)
        logger.info("Settings UI Theme and Fonts")
        AppSettings.set_style_and_theme(self)
        logger.info("Loading UI")
        self.root = Builder.load_string(AppSettings.get_app_ui())
        logger.info("Loading Settings")
        AppSettings.load_settings(self.root)
    def build(self):
        logger.info("Creating UI")
        self.title = APP_NAME
        return self.root
    def __del__(Self):
        logger.info("Good Byee !!")


## Main ##
if __name__ == "__main__":
    try:
        logger.info("Starting App")
        Password_AssistentApp().run()
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt Exiting App bye !!")
        
