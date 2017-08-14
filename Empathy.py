#kivy.require("1.10.0")
from kivy.app import App
from kivy.core.window import Window, WindowBase
from kivy.uix.boxlayout import BoxLayout
from screenchanger import ScreenChanger
from kivy.core.text import LabelBase
from kivy.core.audio import SoundLoader


LabelBase.register(name="Playfair",
				   fn_regular="Fonts/PlayfairDisplay-Regular.ttf",
				   fn_bold="Fonts/PlayfairDisplay-Bold.ttf",
				   fn_italic="Fonts/PlayfairDisplay-Italic.ttf",
				   fn_bolditalic="Fonts/PlayfairDisplay-BoldItalic.ttf")


Window.size = (600,800)
Window.minimum_width = 600
Window.minimum_height = 800
#Window.fullscreen = 'auto'

class Empathy(App):
	audio_close_sound = SoundLoader.load("Audio/opensound.wav")
	startingPage=''

	def build(self):
		self.title = 'Empathy'
		masterWidget = BoxLayout()
		screenChanger = ScreenChanger()
		masterWidget.add_widget(screenChanger)
		return masterWidget

	def _restartApp(self):
		ap = App.get_running_app()
		lol = ap.root
		lol.clear_widgets()
		lol.add_widget(ScreenChanger())

	def on_start(self):
		self.audio_close_sound.play()



if __name__=="__main__":
	Empathy().run()