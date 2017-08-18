from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color
from kivy.core.audio import SoundLoader
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider

from dataaccess import DataAccess

class SoundSettings():
    soundVolume= NumericProperty(0)
    soundVolume=DataAccess.getSoundVolume()

    @staticmethod
    def getAudioFilePath(requestedSound):
        audioFilePaths = {'mainmenu': "mainmenu.wav", 'gamescreen': "game.wav", '': "mainmenu.wav",
                          'opening_sound': "opensound.wav", 'button_sound': "buttonclick.wav"}
        filePath = ''.join(('Audio/',audioFilePaths.get(requestedSound,'')))
        return filePath


    @staticmethod
    def playMusic(sound):
        sound.loop = True
        sound.volume = SoundSettings.soundVolume
        sound.play()

class BasicScreen(Screen):

    def on_enter(self, *args):
        screenName = self.manager.current
        self.backgroundSound = SoundLoader.load(filename=SoundSettings.getAudioFilePath(requestedSound=screenName))
        try:
            SoundSettings.playMusic(self.backgroundSound)
        except:
            print("no audio file to load on this path!")


    def on_leave(self, *args):
        try:
            self.backgroundSound.stop()
        except:
            print("no audio file to be stopped")


class MenuButton(Button):

    def __init__(self,**kwargs):
        super(MenuButton,self).__init__()
        self.audio_button_click =SoundLoader.load(filename=SoundSettings.getAudioFilePath(requestedSound='button_sound'))
        self.background_color = (DataAccess.setupTheme())['customButtonBackgrondColor']
        self.color = (DataAccess.setupTheme())['customButtonTextColor']

    def on_press(self):
        try:
            self.audio_button_click.volume = SoundSettings.soundVolume
            self.audio_button_click.play()
        except:
            print("no audio file to load on this path!")

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

class CustomSlider(Slider):

    def __init__(self,**kwargs):
        super(CustomSlider,self).__init__()
        self.value_track_color = (DataAccess.setupTheme())['customButtonTextColor']

    pass
