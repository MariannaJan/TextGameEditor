from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader

from dataaccess import DataAccess

class MainMenuScreen(Screen):

	audio_mainmenu_sound = SoundLoader.load("Audio/mainmenu.wav")
	audio_mainmenu_sound.loop = True



