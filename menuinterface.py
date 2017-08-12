from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color

from dataaccess import DataAccess

class ThemeSetter:

    @classmethod
    def setupTheme(self):
        da = DataAccess()
        themeSettings = da.getTheme(da.getThemeName())
        return themeSettings

class MenuButton(Button):

    def __init__(self,**kwargs):
        super(MenuButton,self).__init__()
        self.background_color = (ThemeSetter.setupTheme())['customButtonBackgrondColor']
        self.color = (ThemeSetter.setupTheme())['customButtonTextColor']

class MainMenuButton(MenuButton):
    pass

class MenuBoxLayout(BoxLayout):

    def __init__(self,**kwargs):
        super(MenuBoxLayout,self).__init__()
        with self.canvas.before:
            Color(rgba=((ThemeSetter.setupTheme())['customLayoutCanvasColor']))

class StorylineLabel(Label):

    def __init__(self,**kwargs):
        super(StorylineLabel,self).__init__()
        with self.canvas.before:
            Color(rgba=((ThemeSetter.setupTheme())['customLayoutCanvasColor']))

class ActionPopup(Popup):

    def closePopupButton(self, popup):
        closeButton = MenuButton()
        closeButton.text='Close'
        closeButton.bind(on_press=popup.dismiss)
        return closeButton
