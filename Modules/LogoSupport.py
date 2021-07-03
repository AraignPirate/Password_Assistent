
import urllib.request , json ,os
import numpy as np
from PIL import Image, ImageDraw
from settings.AppSettings import LOGO_API , ROOT_APP_PATH , LOGO_DIR
import traceback
from Modules.AppLogging import Logging

logger = Logging("LOGODRIVER")

class GetImage():
    Error = None
    def __init__(self):
        self.api = LOGO_API
        logger.info("Logo Api Loaded")
    def request(self):
        try:
            logger.info("Requesting Logo for site")
            response = urllib.request.urlopen(self.api+self.site).read()
            response = json.loads(response)
            logger.info("Got Logo for site.")
            return None , response
        except:
            logger.error(f"Unable to get Logo for site '{self.site}'")
            return True , None
    def get_logo(self,site):
        self.site = site
        GetImage.Error , data = self.request()
        if data != None:
            logger.info("Extracting Logo Data")
            icons = sorted(data["icons"], key = lambda i: i['width'])
            if len(icons) == 1:
                self.url = icons[0]["url"]
                self.imagename = site.replace(".","_")+"."+icons[0]["format"]
                if os.path.exists(os.path.join(ROOT_APP_PATH,LOGO_DIR,self.imagename)):
                    logger.info("Logo Already Exists.")
                    return None , self.imagename
                logger.info("Downloading Logo for site.")
                GetImage.Error, imagepath = self.download()
                if GetImage.Error==None:
                    logger.info("Sending Logo to crop Workshop")
                    GetImage.Error, imagepath = self.crop_and_save(imagepath)
                    return GetImage.Error , self.imagename
                else:
                    logger.warning("Using DEFAULT as logo")
                    return GetImage.Error , "DEFAULT"
            for dict in icons:
                if dict["width"] > 100:
                    self.url = dict["url"]
                    self.imagename = site.replace(".","_")+"."+dict["format"]
                    if os.path.exists(os.path.join(ROOT_APP_PATH,LOGO_DIR,self.imagename)):
                        logger.info("Logo Already Exists.")
                        return None , self.imagename
                    logger.info("Downloading Logo for site.")
                    GetImage.Error, imagepath = self.download()
                    if GetImage.Error==None:
                        logger.info("Sending Logo to crop Workshop")
                        GetImage.Error, imagepath = self.crop_and_save(imagepath)
                        logger.info("Logo Saved Successfully")
                        return GetImage.Error , self.imagename
                    else:
                        logger.warning("Using DEFAULT as logo")
                        return GetImage.Error , "DEFAULT"
            logger.warning("Logo Not Available")
            return GetImage.Error , "DEFAULT"
        else:
            logger.warning("Using DEFAULT as logo")
            return GetImage.Error , "DEFAULT"
    def download(self):
        try:
            logger.info("Started Downloading Logo.")
            image = urllib.request.urlopen(self.url).read()
            with open(os.path.join(ROOT_APP_PATH,LOGO_DIR,self.imagename),"wb") as imagefile:
                imagefile.write(image)
            logger.info("Raw Logo Saved")
            return None , os.path.join(ROOT_APP_PATH,LOGO_DIR,self.imagename)
        except:
            logger.error("Unable to Download raw logo.")
            logger.traceback(traceback.format_exc())
            return True , "DEFAULT"
    def crop_and_save(self,imagepath):
        try:
            logger.info("Logo in Workshop To Croped.")
            img=Image.open(imagepath).convert("RGB")
            npImage=np.array(img)
            h,w=img.size
            alpha = Image.new('L', img.size,0)
            draw = ImageDraw.Draw(alpha)
            draw.pieslice([0,0,h,w],0,360,fill=255)
            npAlpha=np.array(alpha)
            npImage=np.dstack((npImage,npAlpha))
            Image.fromarray(npImage).save(imagepath)
            return None , imagepath
        except:
            logger.error(f"Unable To Crop Logo from site '{self.site}'")
            logger.traceback(traceback.format_exc())
            return True, "DEFAULT" 