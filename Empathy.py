import kivy
kivy.require("1.10.0")

from gc import collect

from kivy.app import App
from kivy.core.window import Window, WindowBase
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader

from screenchanger import ScreenChanger
from menuinterface import SoundSettings
from menuinterface import FontSettings

class Empathy(App):
	"""Create and run main game loop"""

	Window.size = (600, 800)
	Window.minimum_width = 600
	Window.minimum_height = 800
	# Window.fullscreen = 'auto'

	startingPage=''
	FontSettings.registerFonts()

	def build(self):
		self.title = 'Empathy'
		masterWidget = BoxLayout()
		screenChanger = ScreenChanger()
		masterWidget.add_widget(screenChanger)
		return masterWidget

	def restartApp(self):
		ap = App.get_running_app()
		rootWidget = ap.root
		rootWidget.clear_widgets()
		collect()
		rootWidget.add_widget(ScreenChanger())

	def on_start(self):
		audio_open_sound = SoundLoader.load(filename=SoundSettings.getAudioFilePath(requestedSound='opening_sound'))
		try:
			audio_open_sound.volume = SoundSettings.soundVolume
			audio_open_sound.play()
		except:
			print("no audio file to load on this path!")



if __name__=="__main__":
	Empathy().run()