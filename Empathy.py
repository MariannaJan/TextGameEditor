#kivy.require("1.10.0")
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window, WindowBase
from kivy.uix.boxlayout import BoxLayout

# noinspection PyUnresolvedReferences
from gamescreen import GameScreen
# noinspection PyUnresolvedReferences
from mainmenuscreen import MainMenuScreen
# noinspection PyUnresolvedReferences
from optionsscreen import OptionsScreen

Window.size = (600,800)
Window.minimum_width = 600
Window.minimum_height = 800
#Window.fullscreen = 'auto'
#Window.clearcolor = (0.03,0.07,0.01,1)


class ScreenChanger(ScreenManager):
	pass

class Empathy(App):

	startingPage=''

	def build(self):
		self.title = 'Empathy'
		masterWidget = BoxLayout()
		masterWidget.add_widget(ScreenChanger())
		masterWidget.size = Window.size
		return masterWidget

if __name__=="__main__":
	Empathy().run() 