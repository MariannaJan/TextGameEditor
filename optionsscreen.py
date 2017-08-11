from functools import partial
from kivy.uix.screenmanager import Screen
from dataaccess import DataAccess
from menuinterface import ActionPopup
from menuinterface import MenuButton
from menuinterface import ThemeSetter

class OptionsScreen(Screen):

	def changeTheme(self):
		th=Themes()
		th.chooseTheme()


class Themes:

	def chooseTheme(self):
		themePop = ThemesPopup(title = 'Choose theme')
		themes = DataAccess.getThemeChooser(self)

		for theme in themes:
			themeButtonTitle = themes[theme]
			themeButton = MenuButton(text=themeButtonTitle)
			themeButton.bind(on_press=partial(self.updateTheme,theme))
			themePop.themesPopupLayout.add_widget(themeButton)

		themePop.themesPopupLayout.add_widget(ActionPopup.closePopupButton(self,themePop))
		themePop.open()

	def updateTheme(self,themeName,*args):
		DataAccess.setTheme(self,themeName)
		#ThemeSetter.setupTheme()
		print(themeName)

class ThemesPopup(ActionPopup):
	pass


