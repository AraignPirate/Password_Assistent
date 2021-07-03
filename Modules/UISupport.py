from typing import DefaultDict
from kivy.uix.screenmanager import Screen,ScreenManager,SlideTransition, RiseInTransition,FallOutTransition,SwapTransition,FadeTransition,WipeTransition

from Modules.CustomWidget import *
from Modules.DBSupport import *
from Modules.Features import *
from settings.MainImports import *
from settings.AppSettings import *
from Modules.LogoSupport import *

from threading import Thread, active_count
import time
import sys , re, os
logger = Logging("UISUPPORT")
class MyScreenManager(ScreenManager):
    def on_enter(self):
        logger.info("Root Widget Initiated")

class SplashScreen(Screen,MyWidgits):
    def on_enter(self):
        logger.info("Screen : Splash Screen")
        logger.info("Checking Required Files")
        Clock.schedule_once(lambda x : Thread(target=self.install_setup).start())
    def install_setup(self,*data):
        time.sleep(1)
        self.barval = 0
        self.update_bar(0,"Initiating..")
        self.update_bar(10,"Checking OS")
        self.get_os()
    def get_os(self):
        osname = sys.platform
        self.update_bar(10,osname + " Platform")
        self.fileslist = {
            "Font data " : os.path.join(ROOT_APP_PATH,APP_FILES,ALL_REQUIRED_FILES[0]) ,
            "Text Engine": os.path.join(ROOT_APP_PATH,APP_FILES,ALL_REQUIRED_FILES[1]) , 
            "Database": os.path.join(ROOT_APP_PATH,APP_FILES,DB_NAME),
            "GUI Data":os.path.join(ROOT_APP_PATH,APP_FILES,APP_UI_FILE),
            "Log Dir": os.path.join(ROOT_APP_PATH,LOG_DIR),
            "Logo Dir": os.path.join(ROOT_APP_PATH,LOGO_DIR)}
        leftbardata = 100-self.barval
        notfound = []
        for keys in self.fileslist.keys():
            if  os.path.exists(self.fileslist[keys]):
                self.update_bar(leftbardata//len(self.fileslist),keys)
            else : 
                if keys == "Database":
                    self.initDb()
                    continue
                elif keys == "Log Dir":
                    try:
                        os.mkdir(self.fileslist[keys])
                        continue
                    except:
                        logger.warning("Unable To Create 'Logs' Directory")
                        logger.error("Create 'Logs' directory in app's Root dir.")
                elif keys == "Logo Dir":
                    try:
                        os.mkdir(self.fileslist[keys])
                        continue
                    except:
                        logger.warning("Unable To Create 'Logo' Directory")
                        logger.error("Create 'Logo' directory in app's Root dir.")
                notfound.append(keys)
        if notfound: 
            self.showErrorDialog("Files Not Found..","\n".join(notfound),1)
            logger.error("Files Not Found :" +" ".join(notfound))
        else:
            if self.manager.current == "splash":
                self.manager.current = "login"
    def update_bar(self,val,data,timee = 0.2):
        self.ids.progress.value = self.barval + val
        self.ids.installtext.text = data
        self.barval += val
        time.sleep(timee)
    def initDb(self):
        logger.info("Creating Database")
        self.barval = 0
        self.update_bar(5,"Database Not Found")
        with DbOpenlocal() as conn:
            try:
                self.update_bar(5,"Creating New Database")
                DbInit(conn,self) 
                logger.info("Database Created Successfully")
            except Exception as e:
                logger.info("Unable to Create Database")

class LoginScreen(Screen,MyWidgits):
    
    def on_enter(self):
        logger.info("Screen : Login Screen")
        Clock.schedule_once(self.bind_data)
    def on_leave(self):
        logger.info("Leaving Login Screen")
        self.ids.userfield.text = ""
        self.ids.passfield.text = ""
        self.ids.uservalid.icon ="checkbox-blank-circle-outline"
    def bind_data(self,val):
        self.manager.transition = SlideTransition(direction="left")
        self.ids.passfield.bind(
            on_text_validate = self.validate_password,
        )
        self.ids.userfield.bind(
            on_text_validate = self.validate_user
        )
    def validate_password(self,inst):
        widget = MyWidgits()
        if self.validate_user(self.ids.userfield):
            passhash = Encryption(password=inst.text.strip()).hash
            with DbOpenlocal() as conn:
                if DBHelper().get_password(conn=conn,passs=passhash,user=self.ids.userfield.text.strip()):
                    self.manager.user = self.ids.userfield.text.strip()
                    self.manager.email, self.manager.userid  = DBHelper().getemail(conn=conn,user=self.ids.userfield.text.strip(),passs=passhash)
                    self.manager.get_screen("userscreen").ids.user.text = self.manager.user[0].upper()+ self.manager.user[1:].lower()
                    self.manager.get_screen("userscreen").ids.email.text = self.manager.email
                    self.manager.get_screen("userscreen").ids.userscreenmanager.get_screen("dashboard").userid = self.manager.userid 
                    self.manager.transition = FadeTransition()
                    self.manager.current="userscreen"
                    self.manager.get_screen("userscreen").ids.navdrawer.set_state("close")
                    self.manager.get_screen("userscreen").ids.userscreenmanager.current = "dashboard"
                else:
                    widget.snack_bar("Password Not Matched")
    
    def validate_user(self,inst):
        inst.text = inst.text.strip()
        if "'" in inst.text:
            self.toast_raise("Only Alphanumeric is allowed in Username",2)
            return False
        if inst.text:
            with DbOpenlocal() as conn:
                if DBHelper().check_user(conn=conn,user=inst.text):
                    self.user = inst.text
                    self.ids.uservalid.icon = "check-circle"
                    return True
                else:
                    self.ids.uservalid.icon = "checkbox-blank-circle-outline"
                    self.toast_raise("User Not Found")
                    return False
        else:       
            self.ids.uservalid.icon = "checkbox-blank-circle-outline"
            self.toast_raise("Enter a username")
            return False 

class RegisterScreen(Screen,MyWidgits):
    def on_enter(self):
        logger.info("Screen : Register Screen")
        Clock.schedule_once(self.bind_data)
    def on_leave(self):
        logger.info("Leaving Register Screen")
        self.ids.userfield.text = ""
        self.ids.passwordfield1.text =""
        self.ids.passwordfield2.text = ""
        self.ids.emailfield.text = ""
        self.ids.emailvalid.icon = "checkbox-blank-circle-outline"
        self.ids.uservalid.icon = "checkbox-blank-circle-outline"
    def bind_data(self,val):
        self.ids.userfield.bind(
            on_text_validate = self.validate_user
        )
        self.ids.passwordfield2.bind(
            on_text_validate = self.validate_password
        )
        self.ids.emailfield.bind(
            on_text_validate = self.validate_Email
        )
    def validate_user(self,inst):
        inst.text = inst.text.strip()
        if "'" in inst.text:
            self.toast_raise("Only Alphanumeric is allowed in Username",2)
            return False
        if inst.text and len(inst.text) >= 4:
            with DbOpenlocal() as conn:
                if DBHelper().check_user(conn=conn,user=inst.text):
                    self.showErrorDialog("Username already exists..","Try another username or just try login with this one.",0)
                    return False
                else:
                    self.ids.uservalid.icon = "check-circle"
                    self.username = inst.text
                    return True
        else:
            if inst.text:
                self.ids.userfield.helper_text = "It's less than 4 letters"
            else:
                self.ids.userfield.helper_text = "Username empty"
            self.ids.userfield.error = True
            self.ids.uservalid.icon = "checkbox-blank-circle-outline"
            Clock.schedule_once(self.remove_username_error,2)
            return False
    def remove_username_error(self,dt):
        self.ids.userfield.error = False
        self.ids.uservalid.icon = "checkbox-blank-circle-outline"
        self.ids.userfield.helper_text = "Username Invalid"
    def validate_password(self,inst):
        error = 1
        if self.validate_user(self.ids.userfield):
            error = 0
        else:
            error = 1
            self.toast_raise("Username Invalid !!")
            return
        if self.validate_Email(self.ids.emailfield):
            error = 0
        else:
            error = 1
            self.toast_raise("Email_unvalid")
            return
        if inst.text.strip() and self.ids.passwordfield1.text.strip():
            if len(inst.text) >= 8:
                if inst.text.strip() == self.ids.passwordfield1.text.strip():
                    error = 0
                else:
                    self.toast_raise("Password Didn't Match")
                    error = 1
                    return
            else:
                error = 1
                self.toast_raise("Password must have 8 characters.")
                return
        else:
            if not inst.text.strip():
                self.ids.passwordfield2.error = True
                self.ids.passwordfield2.helper_text = "Empty Password"
            if not self.ids.passwordfield1.text.strip():
                self.ids.passwordfield1.error = True
                self.ids.passwordfield1.helper_text = "Empty Password"
            Clock.schedule_once(self.remove_conf_password_error)
            Clock.schedule_once(self.remove_password_error)
            error = 1
            return
        if error != 1:
            self.username = self.ids.userfield.text.strip()
            self.email = self.ids.emailfield.text.strip()
            self.password = Encryption(password=inst.text.strip()).hash
            self.manager.current = "question"
    def remove_conf_password_error(self,dt):
        self.ids.passwordfield2.error = False
        self.ids.passwordfield2.helper_text = "Password Invalid"
    def remove_password_error(self,dt):
        self.ids.passwordfield1.error = False
        self.ids.passwordfield1.helper_text = "Password Invalid"
    def validate_Email(self,inst):
        email = inst.text.strip()
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if email:
            if(re.search(regex, email)):
                self.ids.emailvalid.icon = "check-circle"
                self.email = email
                return True
            else:
                self.ids.emailfield.error = True
                self.ids.emailvalid.icon = "checkbox-blank-circle-outline"
                Clock.schedule_once(self.remover_email_error)
                return False
        else:
            self.ids.emailfield.error = True
            self.ids.emailvalid.icon = "checkbox-blank-circle-outline"
            Clock.schedule_once(self.remover_email_error)
    def remover_email_error(self,dt):
        self.ids.emailfield.error = False
        self.ids.emailvalid.icon = "checkbox-blank-circle-outline"

class UserScreen(Screen):
    def on_enter(self):
        logger.info("Screen : User Dashboard")
        self.ids.userscreenmanager.get_screen("dashboard").ids.mdlist.clear_widgets()
        self.ids.userscreenmanager.get_screen("dashboard").get_data()
    def on_leave(self):
        self.ids.userscreenmanager.get_screen("dashboard").ids.mdlist.clear_widgets()
        logger.info("Leaving User Dashboard")

class SettingsScreen(Screen):
    def on_enter(self):
        self.manager.transition.direction = "left"
        logger.info("Screen : Settings Screen")
    def on_leave(self):
        self.manager.transition.direction = "right"
        logger.info("Leaving Settings Screen")
    def set_custom_info(self,inst):
        SETTINGS["CUSTOM_INFO"] = inst.active
        if SETTINGS["CUSTOM_INFO"]:
            SETTINGS["LOGS_TO_FILE"] = False
        else:    
            SETTINGS["LOGS_TO_FILE"] = True
        with open(os.path.join(ROOT_APP_PATH,APP_FILES,SETTINGS_JSON),"w") as discriptor:
            json.dump(SETTINGS,discriptor)
    def set_logfile_info(self,inst):
        SETTINGS["LOGS_TO_FILE"] = inst.active
        if SETTINGS["LOGS_TO_FILE"]:
            SETTINGS["CUSTOM_INFO"] = False
        else:
            SETTINGS["CUSTOM_INFO"] = True
        with open(os.path.join(ROOT_APP_PATH,APP_FILES,SETTINGS_JSON),"w") as discriptor:
            json.dump(SETTINGS,discriptor)
    def set_ui_info(self,inst):
        SETTINGS["UI_INFO"] = inst.active
        with open(os.path.join(ROOT_APP_PATH,APP_FILES,SETTINGS_JSON),"w") as discriptor:
            json.dump(SETTINGS,discriptor)

class AboutScreen(Screen):
    def on_enter(self):
        self.manager.transition = SlideTransition(direction="left")
        logger.info("Screen : About Screen")
    def on_leave(self):
        self.manager.transition = SlideTransition(direction="right")
        logger.info("Leaving About Screen")

class PassCreatorScreen(Screen,MyWidgits):
    def on_enter(self):
        self.passwordlength = 8
        self.specialsw = False
        self.smallsw = False
        self.largesw = False
        self.numsw = False
        self.ids.num.active = False
        self.ids.small.active = False
        self.ids.large.active = False
        self.ids.special.active = False
        self.manager.transition = SlideTransition(direction="left")
        logger.info("Screen : Password Creation Screen")
    def on_leave(self):
        self.manager.transition = SlideTransition(direction="right")
        logger.info("Leaving Password Creation Screen")
    def set_num(self,inst):
        self.numsw = inst.active
    def set_small(self,inst):
        self.smallsw = inst.active
    def set_large(self,inst):
        self.largesw = inst.active
    def set_special(self,inst):
        self.specialsw = inst.active
    def createpass(self):
        listpass = Password_Creator().create_pass(self.passwordlength,self.smallsw,self.largesw,self.numsw,self.specialsw)
        if listpass:
            dialog = ShowGenPass.open(listpass)
        else:
            self.toast_raise("No Characters Included")

class ForgotUserScreen(Screen,MyWidgits):
    def on_enter(self):
        logger.info("Screen : Reset Screen")
        self.ids.userfield.bind(
            on_text_validate = self.search_user
        )
    def on_leave(self):
        logger.info("Leaving Reset Screen")
        self.ids.userfield.text = ""
        self.ids.uservalid.icon ="checkbox-blank-circle-outline"
    def search_user(self,inst):
        Widget = MyWidgits()
        uname = inst.text.strip()
        if "'" in uname:
            self.toast_raise("Only Alphanumeric is allowed in Username",2)
            return False
        if uname:
            with DbOpenlocal() as conn:
                if DBHelper().check_user(conn=conn,user=uname):
                    self.manager.recovuser = uname
                    self.ids.uservalid.icon = "check-circle"
                    self.manager.transition.direction = "down"
                    with DbOpenlocal() as conn:
                        self.manager.get_screen("recovery").ids.question.text , self.manager.checkans = DBHelper().getQuestion(conn=conn,user=self.manager.recovuser)
                    time.sleep(0.7)
                    self.manager.current = "recovery"
                else:
                    Widget.toast_raise("User Not Found")
        else:
            Widget.toast_raise("Enter username")

class ForgotScreen(Screen):
    def on_enter(self):
        logger.info("Screen : Forgot Screen")
    def on_leave(self):
        logger.info("Leaving Forgot Screen")
        self.ids.passfield.text = ""
    def submit_answer(self,inst):
        widget = MyWidgits()
        ans = inst.text.strip()
        if ans == self.manager.checkans:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = "passreset"
        else:
            widget.snack_bar("Answer did'nt match its case sensitive !!!")

class PassResetScreen(Screen):
    def on_leave(self):
        self.ids.passwordfield1.text =""
        self.ids.passwordfield2.text =""
    def reset_password(self,inst):
        widget = MyWidgits()
        pass1 = inst.text.strip()
        pass2 = self.ids.passwordfield1.text.strip()
        if pass1 and pass2:
            if pass1 == pass2:
                if len(pass1) >= 8:
                    passs = Encryption(password=pass1).hash
                    with DbOpenlocal() as conn:
                        DBHelper().update_pass(conn=conn,user=self.manager.recovuser,passs=passs)
                    self.manager.transition.direction = "right"
                    self.manager.current = "login"
                    widget.snack_bar("Now login with updated password")
                else:
                    widget.snack_bar("need atleast 8 characters")
            else:
                widget.toast_raise("Password disnt match")
        else:
            widget.toast_raise("Fill both fields")



class ChoiceScreen(Screen):
    def getdata(self,text):
        self.manager.get_screen("question").ids.questionfield.text = text
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = "question"
        self.manager.transition = SlideTransition(direction='left')

class QuestionScreen(Screen):
    def on_enter(self):
        logger.info("Screen : Backup Question Screen")
    def on_leave(self):
        logger.info("Leaving Backup Question Screen")
        self.ids.questionfield.text = ""
        self.ids.answerfields.text = ""
    def show_questions(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = "choice"
    def submit(self,inst):
        widget = MyWidgits()
        if self.manager.get_screen("question").ids.questionfield.text.strip():
            if self.manager.get_screen("question").ids.answerfields.text.strip():
                with DbOpenlocal() as conn:
                    inst.disable = True
                    obj = DBHelper()
                    obj.create_user(
                        conn=conn,
                        user=self.manager.get_screen("register").username,
                        passs=self.manager.get_screen("register").password,
                        email=self.manager.get_screen("register").email,
                        que=self.manager.get_screen("question").ids.questionfield.text.strip(),
                        ans=self.manager.get_screen("question").ids.answerfields.text.strip()
                        )
                self.manager.transition = SlideTransition(direction="right")
                self.manager.current = "login"
                widget.toast_raise("login in your account",2.5)
            else:
                widget.toast_raise("Please provide answer")
        else:
            widget.toast_raise("Choose or write a question")



class WifiScreen(Screen,MyWidgits):
    
    def on_enter(self):
        logger.info("Screen : Wifi Credentials")
        self.ids.mdlist.clear_widgets()
        Clock.schedule_once(lambda x : Thread(target=self.check_root).start())
    def on_leave(self):
        logger.info("Leaving wifi Credentials screen")
    def check_root(self,*dt):
        time.sleep(0.1)
        if ROOT is not None and ROOT:
            if SYSTEM == "Linux":
                pass_list = Linux_wifi(self)
                total = len(pass_list.dictt)
                if total > 0:
                    val = 0
                    add = 100//total
                    Clock.schedule_once(self.show_bar)
                    time.sleep(0.2)
                    for dictt in pass_list.dictt:
                        self.driver.label.text = "Checking.."
                        if dictt["ssid"] == "None" or dictt["psk"] == "None": continue
                        vidget =TwoLineAvatarIconListItem(text=dictt["ssid"],secondary_text="*"*len(dictt["psk"]),theme_text_color="Custom",text_color=[0.0, 0.7843137254901961, 0.3254901960784314, 1.0],secondary_theme_text_color="Custom",secondary_text_color=[1,1,1,1])
                        button = IconRightWidget(icon="content-copy",theme_text_color="Custom",text_color=[0.0, 0.7843137254901961, 0.3254901960784314, 1.0],on_release= self.copy)
                        button.password = dictt["psk"]
                        self.driver.label.text = "Creating.."
                        vidget.add_widget(button)
                        button2 = IconLeftWidget(icon="wifi-strength-4-lock",theme_text_color="Custom",text_color=[0.0, 0.7843137254901961, 0.3254901960784314, 1.0],on_press=self.press,on_release=self.release)
                        button2.up = vidget
                        button2.password = dictt["psk"]
                        vidget.add_widget(button2)
                        self.ids.mdlist.add_widget(vidget)
                        self.driver.label.text = "Success"
                        self.driver.bar.value = val + add
                        val += add
                    self.driver.dismiss()
                    del self.driver
                    logger.info("Got all data Successfully")
            elif SYSTEM == "Windows":
                self.create_fr_win()
        else:
            if SYSTEM == "Windows":
                self.create_fr_win()   
            else:
                logger.error("Need Root Privilages")
                self.wifi_unroot("Need To be Root","To get all wifi passwords I need Admin Rights..!!!",self)
    def copy(self,inst):
        Clipboard.copy(inst.password)
        logger.info("Coppied to clipboard")
        self.toast_raise("Password cliped")
    def show_bar(self,*dt):
        self.driver = MDDialog(
            auto_dismiss = False,
            size_hint = (None,None),
            size = (250,200)
        )
        box = BoxLayout(padding="16dp",orientation="vertical", size_hint_y=None)
        label = MDLabel(text="Initializing..",theme_text_color="Custom",text_color=(1,1,1,1))
        box.add_widget(label)
        bar = MDProgressBar(value = 0,color=[0.0, 0.7843137254901961, 0.3254901960784314, 1.0])
        box.add_widget(bar)
        self.driver.bar = bar
        self.driver.label = label
        self.driver.add_widget(box)
        self.driver.open()

    def create_fr_win(self):
        wifi_list = Win_wifi(self).maindic
        total = len(wifi_list)
        if total > 0:
            val = 0
            add = 100//total
            Clock.schedule_once(self.show_bar)
            time.sleep(0.2)
            for dictt in wifi_list:
                self.driver.label.text = "checking.."
                if dictt["ssid"] == None or dictt["psk"] == None: continue
                self.driver.label.text = "Extracting.."
                vidget =TwoLineAvatarIconListItem(text=dictt["ssid"],secondary_text="*"*len(dictt["psk"]),theme_text_color="Custom",text_color=[0.0, 0.7843137254901961, 0.3254901960784314, 1.0],secondary_theme_text_color="Custom",secondary_text_color=[1,1,1,1])
                button = IconRightWidget(icon="content-copy",theme_text_color="Custom",text_color=[0.0, 0.7843137254901961, 0.3254901960784314, 1.0],on_release= self.copy)
                button.password = dictt["psk"]
                vidget.add_widget(button)
                button2 = IconLeftWidget(icon="wifi-strength-4-lock",theme_text_color="Custom",text_color=[0.0, 0.7843137254901961, 0.3254901960784314, 1.0],on_press=self.press,on_release=self.release)
                button2.up = vidget
                button2.password = dictt["psk"]
                vidget.add_widget(button2)
                self.driver.label.text = "Creating.."
                self.ids.mdlist.add_widget(vidget)
                self.driver.label.text = "Success"
                self.driver.bar.value = val + add
                val += add
            self.driver.dismiss()
            del self.driver
        else:
            logger.error("Need Administrator Privilager To get wifi data")
            self.wifi_unroot("Start as Administrator","To get all wifi passwords I need Admin Rights..!!!",self)     
    def press(self,inst):
        inst.up.secondary_text = inst.password
        inst.icon = "wifi-strength-4"
    def release(self,inst):
        inst.up.secondary_text = "*" * len(inst.password)
        inst.icon = "wifi-strength-4-lock"
class CoverScreen(Screen):
    def on_enter(self):
        logger.info("Screen : Cover")
    def on_leave(self):
        logger.info("Leaving Cover")
class DashBoardScreen(Screen,MyWidgits):
    def on_enter(self):
        self.ids.mdlist.clear_widgets()
        super(DashBoardScreen,self).__init__()
        logger.info("Screen : Dashboard")
        self.ids.actionbut.close_stack()
        Clock.schedule_once(self.bind_data)
        Clock.schedule_once(self.get_data)
    def on_leave(self):
        logger.info("Leaving Dashboard")
        self.ids.actionbut.close_stack()
    def bind_data(self,*dt):
        self.manager.transition.direction = "left"
    def call(self,button):
        if button.icon == 'biohazard':
            self.generate_password()
        elif button.icon == 'lastpass':
            self.add_password()
    def generate_password(self):
        self.manager.current = "passcreator"
    def add_password(self):
        logger.info("Password getter initiated")
        dialog = Password_Adder_card.open(self)
    def validate_data(self,addobj):
        sitename = addobj.ids.site.text.strip()
        username = addobj.ids.creduser.text.strip()
        password = addobj.ids.credpassfield.text.strip()
        if sitename and username and password:
            if addobj.imagename == None:
                addobj.get_image(addobj.ids.site)
            with DbOpenlocal() as conn:
                sitename = Add_Password().create_password_encrypted(sitename)
                username = Add_Password().create_password_encrypted(username)
                password = Add_Password().create_password_encrypted(password)
                icon = Add_Password().create_password_encrypted(addobj.imagename)
                userid = self.userid
                DBHelper().add_credentials(conn=conn,userid=userid,site=sitename,username=username,credentials=password,icon=icon)
            Password_Adder_card.close(addobj)
            logger.info("Credentials Added Successfully")
            self.ids.actionbut.close_stack()
            Clock.schedule_once(self.get_data)
            self.toast_raise("Credentials Added",2)    
        else:
            self.toast_raise("All Fields are required")
    def get_data(self,*p):
        self.ids.mdlist.clear_widgets()
        logger.info("Getting Credentials For Current User")
        with DbOpenlocal() as conn:
            self.credentials = DBHelper().get_all_credentials(conn=conn,userid=self.userid)
        for cred in self.credentials:
            logger.info("Decrypting Passwords")
            site = Add_Password().extract_encrypted_password(cred[2])
            username = Add_Password().extract_encrypted_password(cred[3])
            password = Add_Password().extract_encrypted_password(cred[4])
            icon = Add_Password().extract_encrypted_password(cred[5])
            logger.info("Creating List")
            self.listitem = ThreeLineAvatarListItem(
                text=site,
                secondary_text=username,
                tertiary_text= "*" * len(password),
                on_press = self.opencreds

            )

            logger.info("Adding Password")
            self.listitem.id = cred[0]
            self.listitem.userid = cred[1]
            self.listitem.password = password
            self.listitem.username = username
            self.listitem.site = site
            logger.info("Checking Logo")
            if icon == "DEFAULT":
                path = os.path.join(ROOT_APP_PATH,APP_FILES,DEFAUTL_LOGO)
            elif os.path.exists(os.path.join(ROOT_APP_PATH,LOGO_DIR,icon)):
                path = os.path.join(ROOT_APP_PATH,LOGO_DIR,icon)
            else:
                path = os.path.join(ROOT_APP_PATH,APP_FILES,DEFAUTL_LOGO)
            logger.info("Setting Logo")
            self.iconimage = ImageLeftWidget(source=path)
            self.listitem.add_widget(self.iconimage)
            logger.info("Adding Object To List")
            self.ids.mdlist.add_widget(self.listitem)
    def opencreds(self,object):
        Password_Show_card.open(object,self.ids.mdlist)
