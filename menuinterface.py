from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from dataaccess import DataAccess

class ThemeSetter:

    @classmethod
    def setupTheme(self):
        da = DataAccess()
        themeSettings = da.getTheme(da.getThemeName())
        return themeSettings

class MenuButton(Button):

    custom_text_c = (ThemeSetter.setupTheme())['customButtonTextColor']
    custom_back = (ThemeSetter.setupTheme())['customButtonBackgrondColor']

class MainMenuButton(MenuButton):
    pass

class MenuBoxLayout(BoxLayout):

    custom_canvas = (ThemeSetter.setupTheme())['customLayoutCanvasColor']

class StorylineLabel(Label):

    custom_canvas = (ThemeSetter.setupTheme())['customLayoutCanvasColor']

class ActionPopup(Popup):

    def closePopupButton(self, popup):
        closeButton = MenuButton(text='Close')
        closeButton.bind(on_press=popup.dismiss)
        return closeButton
