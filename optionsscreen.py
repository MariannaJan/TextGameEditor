from functools import partial
from kivy.app import App
from kivy.core.audio import SoundLoader

from dataaccess import DataAccess
from menuinterface import ActionPopup
from menuinterface import MenuButton
from menuinterface import SoundSettings
from menuinterface import BasicScreen
from menuinterface import CustomSlider

class OptionsScreen(BasicScreen):


	def changeTheme(self):
		th=Themes()
		th.chooseTheme()

	def adjustSound(self):
		soundPop = SoundPopup(title = 'Adjust sound')
		soundToggleButton = MuteButton()
		soundToggleButton.text = soundToggleButton.createMuteButtonText(float(SoundSettings.soundVolume))
		soundPop.soundPopupLayout.add_widget(SoundVolumeSlider())
		soundPop.soundPopupLayout.add_widget(soundToggleButton)
		soundPop.soundPopupLayout.add_widget(ActionPopup.closePopupButton(self,soundPop))
		soundPop.open()

class MuteButton(MenuButton):

	def muteSound(self):
		soundVolume = float(SoundSettings.soundVolume)
		soundVolumeSlider = self.parent.children[2]
		if soundVolume >= 0.1:
			SoundSettings.soundVolume = 0
			DataAccess.setSoundVolume(0)
			soundVolumeSlider.value = 0
			self.text = 'Turn the sound ON'
		elif soundVolume < 0.1:
			SoundSettings.soundVolume = 1
			DataAccess.setSoundVolume(1)
			soundVolumeSlider.value = 1
			self.text = 'Turn the sound OFF'


	def createMuteButtonText(self,vol):
		if vol >=0.1:
			text = 'Turn the sound OFF'
		elif vol < 0.1:
			text = 'Turn the sound ON'
		return text

	def on_press(self):
		self.muteSound()

class SoundVolumeSlider(CustomSlider):

	def __init__(self):
		super(SoundVolumeSlider,self).__init__()
		soundVolume = float(SoundSettings.soundVolume)
		self.value = soundVolume

	def adjustSoundVolume(self):
		newSoundVolume = self.value_normalized
		print(newSoundVolume)
		SoundSettings.soundVolume = newSoundVolume
		DataAccess.setSoundVolume(newSoundVolume)

		try:
			muteButtonReference = self.parent.children[1]
		except:
			print('no parent on init')
		else:
			muteButtonReference.text = muteButtonReference.createMuteButtonText(newSoundVolume)


	def on_value(self,*args):
		self.adjustSoundVolume()
		bip = SoundLoader.load(SoundSettings.getAudioFilePath('button_sound'))
		bip.volume = SoundSettings.soundVolume
		bip.play()


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
		DataAccess.setThemeName(themeName)
		ap=App.get_running_app()
		ap._restartApp()


class ThemesPopup(ActionPopup):
	pass

class SoundPopup(ActionPopup):

	pass

#TODO: User defined Themes
#TODO: choosing of different fonts
#TODO: allow user for own music instead of the one provided with the app
