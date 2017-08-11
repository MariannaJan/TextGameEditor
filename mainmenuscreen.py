from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.label import Label


class MainMenuScreen(Screen):

	def restartApp(self):
		ap = App.get_running_app()
		lol = ap.root
		lol.clear_widgets()
		#lol.add_widget(Label(text = 'zoo'))
		#lol.add_widget(ScreenChanger())

	pass