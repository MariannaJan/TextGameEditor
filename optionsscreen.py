from functools import partial
from kivy.uix.screenmanager import Screen
from kivy.app import App

from dataaccess import DataAccess
from menuinterface import ActionPopup
from menuinterface import MenuButton



class OptionsScreen(Screen):

	def changeTheme(self):
		th=Themes()
		th.chooseTheme()


class Themes:

	def chooseTheme(self):
		themePop = ThemesPopup(title = 'Choose theme')
		themes = DataAccess.getThemeChooser()

		for theme in themes:
			themeButtonTitle = themes[theme]
			themeButton = MenuButton()
			themeButton.text = themeButtonTitle
			themeButton.bind(on_press=partial(self.updateTheme,theme))
			themePop.themesPopupLayout.add_widget(themeButton)

		themePop.themesPopupLayout.add_widget(ActionPopup.closePopupButton(self,themePop))
		themePop.open()

	def updateTheme(self,themeName,*args):
		DataAccess.setTheme(self,themeName)
		ap=App.get_running_app()
		ap._restartApp()


class ThemesPopup(ActionPopup):
	pass

#TODO: User defined Themes
