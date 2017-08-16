from functools import partial
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.slider import Slider

from dataaccess import DataAccess
from menuinterface import ActionPopup
from menuinterface import MenuButton
from menuinterface import SoundSettings
from menuinterface import BasicScreen

class OptionsScreen(BasicScreen):


	def changeTheme(self):
		th=Themes()
		th.chooseTheme()

	def adjustSound(self):
		soundPop = SoundPopup(title = 'Adjust sound')
		soundToggleButton = MuteButton()
		soundToggleButton.text = soundToggleButton.createMuteButtonText(int(SoundSettings.soundVolume))
		soundPop.soundPopupLayout.add_widget(Slider())
		soundPop.soundPopupLayout.add_widget(soundToggleButton)
		soundPop.soundPopupLayout.add_widget(ActionPopup.closePopupButton(self,soundPop))
		soundPop.open()


class MuteButton(MenuButton):

	def muteSound(self):
		print(SoundSettings.soundVolume)
		ss = int(SoundSettings.soundVolume)
		if ss == 1:
			SoundSettings.soundVolume = 0
			DataAccess.setToggleSound(0)
			print(ss)
			self.text = 'Turn the sound ON'
		elif ss == 0:
			SoundSettings.soundVolume = 1
			DataAccess.setToggleSound(1)
			self.text = 'Turn the sound OFF'
			print(ss)

	def createMuteButtonText(self,vol):
		if vol == 1:
			text = 'Turn the sound OFF'
		elif vol == 0:
			text = 'Turn the sound ON'
		return text


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

class SoundPopup(ActionPopup):
	pass

#TODO: User defined Themes
