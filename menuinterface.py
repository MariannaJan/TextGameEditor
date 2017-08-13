from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color

from dataaccess import DataAccess

class MenuButton(Button):

    def __init__(self,**kwargs):
        super(MenuButton,self).__init__()
        self.background_color = (DataAccess.setupTheme())['customButtonBackgrondColor']
        self.color = (DataAccess.setupTheme())['customButtonTextColor']

class MainMenuButton(MenuButton):
    pass

class MenuBoxLayout(BoxLayout):

    def __init__(self,**kwargs):
        super(MenuBoxLayout,self).__init__()
        with self.canvas.before:
            Color(rgba=((DataAccess.setupTheme())['customLayoutCanvasColor']))

class StorylineLabel(Label):

    def __init__(self,**kwargs):
        super(StorylineLabel,self).__init__()
        self.color = (DataAccess.setupTheme())['customButtonTextColor']
        with self.canvas.before:
            Color(rgba=((DataAccess.setupTheme())['customLayoutCanvasColor']))

class ActionPopup(Popup):

    def closePopupButton(self, popup):
        closeButton = MenuButton()
        closeButton.text='Close'
        closeButton.bind(on_press=popup.dismiss)
        return closeButton
