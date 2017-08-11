#kivy.require("1.10.0")
from kivy.app import App
from kivy.core.window import Window, WindowBase
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from screenchanger import ScreenChanger
from mainmenuscreen import MainMenuScreen
from optionsscreen import OptionsScreen
from gamescreen import GameScreen

Window.size = (600,800)
Window.minimum_width = 600
Window.minimum_height = 800
#Window.fullscreen = 'auto'
#Window.clearcolor = (0.03,0.07,0.01,1)


class Empathy(App):

	startingPage=''

	def build(self):
		self.title = 'Empathy'
		masterWidget = BoxLayout()
		screenChanger = ScreenChanger()
		screenChanger.add_widget(MainMenuScreen(name='mainmenu'))
		screenChanger.add_widget(GameScreen(name='gamescreen'))
		screenChanger.add_widget(OptionsScreen(name='options'))
		masterWidget.add_widget(screenChanger)
		masterWidget.size = Window.size
		return masterWidget

	def _restartApp(self):
		ap = App.get_running_app()
		lol = ap.root
		lol.clear_widgets()
		#lol.add_widget(Label(text = 'zoo'))
		# screenChanger = ScreenChanger()
		# screenChanger.add_widget(MainMenuScreen(name='mainmenu'))
		# screenChanger.add_widget(GameScreen(name='gamescreen'))
		# screenChanger.add_widget(OptionsScreen(name='options'))
		# lol.add_widget(screenChanger)

if __name__=="__main__":
	Empathy().run()