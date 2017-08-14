from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color
from kivy.core.audio import SoundLoader
from kivy.uix.togglebutton import ToggleButton

from dataaccess import DataAccess

class MenuButton(Button):

    def __init__(self,**kwargs):
        super(MenuButton,self).__init__()
        self.audio_button_click = SoundLoader.load("Audio/buttonclick.wav")
        self.background_color = (DataAccess.setupTheme())['customButtonBackgrondColor']
        self.color = (DataAccess.setupTheme())['customButtonTextColor']

    def on_press(self):
        self.audio_button_click.play()

class MainMenuButton(MenuButton):
    pass

class CustomToggleButton(ToggleButton):
    def __init__(self,text_normal,text_down,**kwargs):
        super(CustomToggleButton,self).__init__()
        self.audio_button_click = SoundLoader.load("Audio/buttonclick.wav")
        self.background_color = (DataAccess.setupTheme())['customButtonBackgrondColor']
        self.color = (DataAccess.setupTheme())['customButtonTextColor']
        self.text_normal = text_normal
        self.text_down = text_down
        self.text = self.text_normal

    def on_press(self):
        self.audio_button_click.play()

    def toggleText(self):
        if self.state == 'normal':
            self.text = self.text_normal

        elif self.state == 'down':
            self.text = self.text_down



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
