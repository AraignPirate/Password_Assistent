#Gui Imports
from Modules.AppLogging import Logging
Logging("MAINIMPORTS").info("Loading Dependencies")
from kivy.core.clipboard import Clipboard
from kivymd.toast import toast
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivymd.uix.button import MDFlatButton
from kivymd.theming import ThemeManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.progressbar import MDProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineIconListItem,IconLeftWidget,IconRightWidget,TwoLineAvatarIconListItem,ThreeLineAvatarListItem,ImageLeftWidget,OneLineIconListItem

