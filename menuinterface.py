from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color
from kivy.core.audio import SoundLoader
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider
from kivy.core.text import LabelBase

from dataaccess import DataAccess

class FontSettings():

    fontName = StringProperty(None)
    fontName = DataAccess.getFontName()

    @classmethod
    def registerFonts(cls):

        LabelBase.register(name=cls.fontName,
                           fn_regular=DataAccess.getFonts(cls.fontName,"fn_regular"),
                           fn_bold=DataAccess.getFonts(cls.fontName,"fn_bold"),
                           fn_italic=DataAccess.getFonts(cls.fontName,"fn_italic"),
                           fn_bolditalic=DataAccess.getFonts(cls.fontName,"fn_bolditalic"))

class SoundSettings():
    soundVolume= NumericProperty(0)
    soundVolume=DataAccess.getSoundVolume()

    @staticmethod
    def getAudioFilePath(requestedSound):
        audioFilePaths = DataAccess.getSoundFilesNames()
        filePath = ''.join(('Audio/',audioFilePaths.get(requestedSound,'')))
        return filePath


    @staticmethod
    def playMusic(sound):
        sound.loop = True
        sound.volume = SoundSettings.soundVolume
        sound.play()

class ThemeSettings():

    @classmethod
    def _getColor(cls,colorCategory):
        color = (DataAccess.setupTheme())[colorCategory]
        return color

    @classmethod
    def getCustomButtonBackgroundColor(cls):
        return cls._getColor('customButtonBackgroundColor')

    @classmethod
    def getCustomButtonTextColor(cls):
        return cls._getColor('customButtonTextColor')

    @classmethod
    def getCustomLayoutCanvasColor(cls):
        return cls._getColor('customLayoutCanvasColor')

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
        super(MenuButton,self).__init__(**kwargs)
        self.audio_button_click =SoundLoader.load(filename=SoundSettings.getAudioFilePath(requestedSound='button_sound'))
        self.background_color = ThemeSettings.getCustomButtonBackgroundColor()
        self.color = ThemeSettings.getCustomButtonTextColor()
        self.font_name = FontSettings.fontName

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
        super(MenuBoxLayout,self).__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=ThemeSettings.getCustomLayoutCanvasColor())

class StorylineLabel(Label):

    def __init__(self,**kwargs):
        super(StorylineLabel,self).__init__(**kwargs)
        self.color = ThemeSettings.getCustomButtonTextColor()
        self.font_name = FontSettings.fontName
        with self.canvas.before:
            Color(rgba=ThemeSettings.getCustomLayoutCanvasColor())

class ActionPopup(Popup):

    def __init__(self,**kwargs):
        super(ActionPopup,self).__init__(**kwargs)
        self.title_font = FontSettings.fontName

    def closePopupButton(self, popup):
        closeButton = MenuButton()
        closeButton.text='Close'
        closeButton.bind(on_press=popup.dismiss)
        return closeButton

class CustomSlider(Slider):

    def __init__(self,**kwargs):
        super(CustomSlider,self).__init__()
        self.value_track_color = ThemeSettings.getCustomButtonTextColor()
