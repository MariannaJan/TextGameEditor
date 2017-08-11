from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from dataaccess import DataAccess

class ThemeSetter:


    def setupTheme(self):
        da = DataAccess()
        themeSettings = da.getTheme(da.getThemeName())
        return themeSettings

class MenuButton(Button):

    themeSettings=ThemeSetter()
    custom_text_c = (themeSettings.setupTheme())['customButtonTextColor']
    custom_back = (themeSettings.setupTheme())['customButtonBackgrondColor']

class MainMenuButton(MenuButton):
    pass

class MenuBoxLayout(BoxLayout):
    themeSettings = ThemeSetter()
    custom_canvas = (themeSettings.setupTheme())['customLayoutCanvasColor']

class StorylineLabel(Label):
    themeSettings = ThemeSetter()
    custom_canvas = (themeSettings.setupTheme())['customLayoutCanvasColor']

class ActionPopup(Popup):

    def closePopupButton(self, popup):
        closeButton = MenuButton(text='Close')
        closeButton.bind(on_press=popup.dismiss)
        return closeButton
