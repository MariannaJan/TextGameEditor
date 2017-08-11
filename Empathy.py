#kivy.require("1.10.0")
from kivy.app import App
from kivy.core.window import Window, WindowBase
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
# noinspection PyUnresolvedReferences
from screenchanger import ScreenChanger

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
		screenChanger = Builder.load_file("screenchanger.kv")
		masterWidget.add_widget(screenChanger)
		masterWidget.size = Window.size
		return masterWidget

if __name__=="__main__":
	Empathy().run()