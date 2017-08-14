#kivy.require("1.10.0")
from kivy.app import App
from kivy.core.window import Window, WindowBase
from kivy.uix.boxlayout import BoxLayout
from screenchanger import ScreenChanger
from kivy.core.text import LabelBase

LabelBase.register(name="Playfair",
				   fn_regular="PlayfairDisplay-Regular.ttf",
				   fn_bold="PlayfairDisplay-Bold.ttf",
				   fn_italic="PlayfairDisplay-Italic.ttf",
				   fn_bolditalic="PlayfairDisplay-BoldItalic.ttf")


Window.size = (600,800)
Window.minimum_width = 600
Window.minimum_height = 800
#Window.fullscreen = 'auto'

class Empathy(App):

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

if __name__=="__main__":
	Empathy().run()