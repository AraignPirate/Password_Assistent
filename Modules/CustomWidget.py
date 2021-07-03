from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton
from kivymd.toast import toast
from kivymd.uix.textfield import MDTextField
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineListItem

from functools import partial

from kivy.core.clipboard import Clipboard

from Modules.LogoSupport import GetImage
from Modules.DBSupport import *
from Modules.AppLogging import Logging

logger = Logging("CUSTOMUI")

class MyWidgits():    
    def wifi_unroot(self,title,text,obj):
        self.dialog = MDDialog(
            title=title,
            text=text,
            type="alert",
            buttons=[MDFlatButton(text="Ok",text_color=[0.0, 0.7843137254901961, 0.3254901960784314, 1.0],on_release=partial(self.mycallback2,"Ok",obj))],
            size_hint = (None,None),
            size = (250,200),
            auto_dismiss = False,
            )
        self.dialog.open()
    def mycallback2(self,data,obj,*p):
        self.dialog.dismiss()
        obj.manager.transition.direction = "right"
        obj.manager.current = "dashboard"
    def showErrorDialog(self,title,text,switch):
        self.dialog = MDDialog(
            title=title,
            text=text,
            type="alert",
            buttons=[MDFlatButton(text="Ok",text_color=[0.0, 0.7843137254901961, 0.3254901960784314, 1.0],on_release=partial(self.mycallback,"Ok",switch))],
            size_hint = (None,None),
            size = (250,200),
            auto_dismiss = False,
            )
        self.dialog.open()
    def mycallback(self,data,switch,*p):
        self.dialog.dismiss()
        if switch == 1:
            exit(-1)
    def snack_bar(self,data):
        Snackbar(
            text=data,
                 ).open()
    def toast_raise(self,data,dur = 1):
        toast(
            data,
            duration=dur,
        )
class ShowGeneratedPass(BoxLayout,MyWidgits):
    def __init__(self,listpass):
        logger.info("Init Pass List")
        self.listpass = listpass
        super().__init__()
        self.create()
    def create(self):
        for data in self.listpass:
            self.item = OneLineListItem(
                text=fr"{data}",
                on_release=self.copydata,
                theme_text_color="Custom",
                text_color=[0.0, 0.7843137254901961, 0.3254901960784314, 1.0]
            )
            self.item.data = data
            self.ids.mdlist.add_widget(self.item)
    def copydata(self,inst):
        Clipboard.copy(inst.data)
        self.toast_raise("Copied")
class AddPassword(BoxLayout):
    def __init__(self):
        super().__init__()
        self.imagename = None
        self.ids.site.bind(
            on_text_validate = self.get_image
        )
        self.ids.credpassfield.bind(
            on_text_validate = Password_Adder_card.validate_data
        )
    def get_image(self,inst):
        sitename = inst.text.strip()
        Error , imagename = GetImage().get_logo(sitename)
        self.ids.credico.icon = "check-circle"
        if Error == None:
            self.ids.sitevalid.icon = "check-circle"
            self.imagename = imagename
        else:
            self.ids.sitevalid.icon = "check-circle"
            self.imagename = "DEFAULT"
    

class ShowCredentials(BoxLayout,MyWidgits):
    def __init__(self,listobj) -> None:
        super().__init__()
        self.listobj = listobj
        self.ids.site.text = self.listobj.site
        self.ids.username.text = self.listobj.username
        self.ids.credpassfield.text = "*" * len(self.listobj.password)
    def show_pass(self,*p):
        self.ids.credpassfield.text = self.listobj.password
        self.ids.credpassiconeye.icon = "eye"
    def hide_pass(self,*p):
        self.ids.credpassfield.text = "*" * len(self.listobj.password)
        self.ids.credpassiconeye.icon = "eye-off"
    def copy_password(self,inst):
        Clipboard.copy(self.listobj.password)
        self.toast_raise("Password cliped")
        logger.info("Coppied to clipboard")
    def copy_username(self,inst):
        Clipboard.copy(self.listobj.username)
        self.toast_raise("Username cliped")
        logger.info("Coppied to clipboard")
    def delete(self,obj,mdlist):
        with DbOpenlocal() as conn:
            DBHelper().delete_credentials(conn=conn,id=self.listobj.id,userid=self.listobj.userid)
        obj.dismiss(force=True)
        mdlist.remove_widget(self.listobj)
        logger.info("Credential Deleted")
        

class Password_Adder_card():
    dialog = None
    screenobj = None
    def open(obj):
        Password_Adder_card.screenobj = obj
        Password_Adder_card.cancilbut = MDFlatButton(text="CANCEL",  md_bg_color=[0.0, 0.7843137254901961, 0.3254901960784314, 1.0],on_release=Password_Adder_card.close)
        Password_Adder_card.Adddata=MDFlatButton(text="ADD",  md_bg_color=[0.0, 0.7843137254901961, 0.3254901960784314, 1.0], on_release=Password_Adder_card.validate_data)
        Password_Adder_card.mainobj = AddPassword()
        Password_Adder_card.dialog = MDDialog(
                auto_dismiss=False,
                title="Add Password",
                type="custom",
                content_cls=Password_Adder_card.mainobj,
                buttons=[
                    Password_Adder_card.cancilbut,
                    Password_Adder_card.Adddata
                ],
            )
        Password_Adder_card.dialog.open()
        return Password_Adder_card.dialog
    def close(object):
        Password_Adder_card.cancilbut.disabled = True
        Password_Adder_card.dialog.dismiss(force=True)
    def validate_data(obj):
        Password_Adder_card.Adddata.disabled = True
        Password_Adder_card.screenobj.validate_data(Password_Adder_card.mainobj)
class ShowGenPass():
    dialog = None
    screenobj = None
    def open(listpass):
        ShowGenPass.cancilbut = MDFlatButton(text="CLOSE",  md_bg_color=[0.0, 0.7843137254901961, 0.3254901960784314, 1.0],on_release=ShowGenPass.close)
        ShowGenPass.mainobj = ShowGeneratedPass(listpass)
        ShowGenPass.dialog = MDDialog(
                auto_dismiss=False,
                title="Copy Passwd",
                type="custom",
                content_cls=ShowGenPass.mainobj,
                buttons=[
                    ShowGenPass.cancilbut
                ],
            )
        ShowGenPass.dialog.open()
        return ShowGenPass.dialog
    def close(object):
        ShowGenPass.cancilbut.disabled = True
        ShowGenPass.dialog.dismiss(force=True)

class Password_Show_card():
    dialog = None
    screenobj = None
    def open(obj,mdlist):
        Password_Show_card.screenobj = obj
        Password_Show_card.mdlist = mdlist
        Password_Show_card.cancilbut = MDFlatButton(text="CLOSE",  md_bg_color=[0.0, 0.7843137254901961, 0.3254901960784314, 1.0],on_release=Password_Show_card.close)
        Password_Show_card.mainobj = ShowCredentials(Password_Show_card.screenobj)
        Password_Show_card.Delete=MDFlatButton(text="DELETE",  md_bg_color=[0.0, 0.7843137254901961, 0.3254901960784314, 1.0], on_release=Password_Show_card.delete)
        Password_Show_card.dialog = MDDialog(
                auto_dismiss=False,
                title="Credentials",
                type="custom",
                content_cls=Password_Show_card.mainobj,
                buttons=[
                    Password_Show_card.Delete,
                    Password_Show_card.cancilbut,
                ],
            )
        Password_Show_card.dialog.open()
        return Password_Show_card.dialog
    def close(object):
        Password_Show_card.cancilbut.disabled = True
        Password_Show_card.dialog.dismiss(force=True)
    def delete(object):
        Password_Show_card.mainobj.delete(Password_Show_card.dialog,Password_Show_card.mdlist)