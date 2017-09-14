"""**Module grouping all the templates for the interface elements and initialization of sound and graphic settings.**"""

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color
from kivy.core.audio import SoundLoader
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.slider import Slider
from kivy.core.text import LabelBase

from dataaccessapi import DataAccessAPI

class FontSettings():
    """Setting the fonts for the current game.

    :var fontName: name of the current font from the saved settings
    :vartype fontName: string
    """

    fontName = DataAccessAPI.getFontName()

    @classmethod
    def registerFonts(cls):
        """Register the current font from the saved settings for the use with the current game.

        In case of lack of font sets Roboto as the default font for the game.
        """

        try:
            LabelBase.register(name=cls.fontName,
                               fn_regular=DataAccessAPI.getFontFilePath(cls.fontName,"fn_regular"),
                               fn_bold=DataAccessAPI.getFontFilePath(cls.fontName,"fn_bold"),
                               fn_italic=DataAccessAPI.getFontFilePath(cls.fontName,"fn_italic"),
                               fn_bolditalic=DataAccessAPI.getFontFilePath(cls.fontName,"fn_bolditalic"))
        except:
            print('No font to register')
            cls.fontName = 'Roboto'

class SoundSettings():
    """Setting and playing the sounds for the current game.

    :var soundVolume:  numeric proprty, in the reange 0-1
    :vartype soundVolume: float
    """

    soundVolume= NumericProperty(0)
    soundVolume = DataAccessAPI.getSoundVolume()

    @staticmethod
    def getAudioFilePath(requestedSound):
        """Provide path to the specified sound file.

        :param str requestedSound: name of the requested sound
        :return: path to the requested sound file
        :rtype: string
        """

        # audioFilePaths = DataAccess.getSoundFilesNames()
        # filePath = ''.join(('Audio/',audioFilePaths.get(requestedSound,'')))
        return DataAccessAPI.getAudioFilePath(requestedSound)


    @staticmethod
    def playMusic(sound):
        """Play the specified sound in a loop with the sound volume from saved settings.

        :param str sound: name of the sound to be played
        """

        sound.loop = True
        sound.volume = SoundSettings.soundVolume
        sound.play()

class ThemeSettings():

    @classmethod
    def getCustomButtonBackgroundColor(cls):
        """:return: customButtonBackgroundColor from current theme (float R, float G, float B, float A)
        :rtype: tuple(float,float,float,float)
        """

        return DataAccessAPI.getColorFromTheme('customButtonBackgroundColor')

    @classmethod
    def getCustomButtonTextColor(cls):
        """:return: customButtonTextColor from current theme (float R, float G, float B, float A)
        :rtype: tuple(float,float,float,float)
        """

        return DataAccessAPI.getColorFromTheme('customButtonTextColor')


    @classmethod
    def getCustomLayoutCanvasColor(cls):
        """:return: customLayoutCanvasColor from current theme (float R, float G, float B, float A)
        :rtype: tuple(float,float,float,float)
        """

        return DataAccessAPI.getColorFromTheme('customLayoutCanvasColor')

class BasicScreen(Screen):
    """Template for basic screen, providing mechanism of playing background sound."""

    def on_enter(self, *args):
        """
        Start looping appropriate background sound on entering the screen."""

        screenName = self.manager.current

        self.backgroundSound = SoundLoader.load(filename=SoundSettings.getAudioFilePath(requestedSound=screenName))
        try:
            SoundSettings.playMusic(self.backgroundSound)
        except:
            print("no audio file to load on this path!")


    def on_leave(self, *args):
        """Stop looping background sound on leaving the current screen."""

        try:
            self.backgroundSound.stop()
        except:
            print("no audio file to be stopped")


class MenuButton(Button):
    """Template for basic menu button, setting the look and sounds of a button."""

    def __init__(self,**kwargs):
        """Set up click sound, colors and font for the basic menu button. Sizes and text alignment in kv file."""
        super(MenuButton,self).__init__(**kwargs)
        self.audio_button_click =SoundLoader.load(filename=SoundSettings.getAudioFilePath(requestedSound='button_sound'))
        self.background_color = ThemeSettings.getCustomButtonBackgroundColor()
        self.color = ThemeSettings.getCustomButtonTextColor()
        self.font_name = FontSettings.fontName

    def on_press(self):
        """Play the click sound with sound volume from the saved settings on clicking the button."""
        try:
            self.audio_button_click.volume = SoundSettings.soundVolume
            self.audio_button_click.play()
        except:
            print("no audio file to load on this path!")

class MainMenuButton(MenuButton):
    """Extends MenuButton. Provide a link back to main menu."""
    pass

class MenuBoxLayout(BoxLayout):
    """Basic box layout template for all the gameplay."""

    def __init__(self,**kwargs):
        """Set colors and alignment for the layout (rest in kv file)."""
        super(MenuBoxLayout,self).__init__(**kwargs)
        with self.canvas.before:
            Color(rgba=ThemeSettings.getCustomLayoutCanvasColor())

class StorylineLabel(Label):
    """Basic temple for ingame label - text widget."""

    def __init__(self,**kwargs):
        """Set Colors, font and layout for the label (rest in kv file)."""
        super(StorylineLabel,self).__init__(**kwargs)
        self.color = ThemeSettings.getCustomButtonTextColor()
        self.font_name = FontSettings.fontName
        with self.canvas.before:
            Color(rgba=ThemeSettings.getCustomLayoutCanvasColor())

class ActionPopup(Popup):
    """Basic template for a popup."""

    def __init__(self,**kwargs):
        """Set colors and font for a popup (rest in kv file)."""
        super(ActionPopup,self).__init__(**kwargs)
        self.title_font = FontSettings.fontName

    def closePopupButton(self, popup):
        """Extends MenuButton. Provide a button generation for closing a popup."""
        closeButton = MenuButton()
        closeButton.text='Close'
        closeButton.bind(on_press=popup.dismiss)
        return closeButton

class CustomSlider(Slider):
    """Basic template for horizontal slider."""

    def __init__(self,**kwargs):
        """Set colors and sizes for a basic slider (rest in kv file)."""
        super(CustomSlider,self).__init__()
        self.value_track_color = ThemeSettings.getCustomButtonTextColor()
