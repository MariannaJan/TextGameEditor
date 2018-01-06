"""User interface for checking and changing game settings, like colors, sounds etc."""

from functools import partial
from kivy.app import App
from kivy.core.audio import SoundLoader

from dataaccessapi import DataAccessAPI
from menuinterface import ActionPopup
from menuinterface import MenuButton
from menuinterface import SoundSettings
from menuinterface import BasicScreen
from menuinterface import CustomSlider

class OptionsScreen(BasicScreen):
	"""Extends BasicScreen. Provides user interface for changing game settings."""

	def changeTheme(self):
		"""On button press generate theme selection popup."""

		th=Themes()
		th.chooseTheme()

	def adjustSound(self):
		"""On button press generate sound adjustment popup."""

		soundPop = SoundPopup(title = 'Adjust sound')
		soundToggleButton = MuteButton()
		soundToggleButton.text = soundToggleButton.createMuteButtonText(float(SoundSettings.soundVolume))
		soundPop.soundPopupLayout.add_widget(SoundVolumeSlider())
		soundPop.soundPopupLayout.add_widget(soundToggleButton)
		soundPop.soundPopupLayout.add_widget(ActionPopup.closePopupButton(soundPop))
		soundPop.open()

class MuteButton(MenuButton):
	"""Extends MenuButton. Provides auto-adjusting button for setting sound volume to 0 or 1."""

	def muteSound(self):
		"""Check for current sound volume and adjust button text and function, to allow turning the sound on or off."""

		soundVolume = float(SoundSettings.soundVolume)
		soundVolumeSlider = self.parent.children[2]
		if soundVolume >= 0.1:
			SoundSettings.soundVolume = 0
			DataAccessAPI.setSoundVolume(0)
			soundVolumeSlider.value = 0
			self.text = 'Turn the sound ON'
		elif soundVolume < 0.1:
			SoundSettings.soundVolume = 1
			DataAccessAPI.setSoundVolume(1)
			soundVolumeSlider.value = 1
			self.text = 'Turn the sound OFF'

	def createMuteButtonText(self,vol):
		"""Set the mute button text according to the current sound volume."""

		if vol >=0.1:
			text = 'Turn the sound OFF'
		elif vol < 0.1:
			text = 'Turn the sound ON'
		return text

	def on_press(self):
		"""On button press toggle text and function of MuteButton."""
		self.muteSound()

class SoundVolumeSlider(CustomSlider):
	"""Extends CustomSlider. Slider to adjust sound volume from 0 to 1, step 0.1."""

	def __init__(self):
		"""Create sound volume slider according to current sound volume from saved settings."""

		super(SoundVolumeSlider,self).__init__()
		soundVolume = float(SoundSettings.soundVolume)
		self.value = soundVolume

	def adjustSoundVolume(self):
		"""Set sound volume on slider change amd adjust mute button accordingly."""

		newSoundVolume = self.value_normalized
		SoundSettings.soundVolume = newSoundVolume
		DataAccessAPI.setSoundVolume(newSoundVolume)
		try:
			muteButtonReference = self.parent.children[1]
		except:
			print('no parent on init')
		else:
			muteButtonReference.text = muteButtonReference.createMuteButtonText(newSoundVolume)

	def on_value(self,*args):
		"""Set sound slider sound."""

		self.adjustSoundVolume()
		bip = SoundLoader.load(SoundSettings.getAudioFilePath('button_sound'))
		bip.volume = SoundSettings.soundVolume
		bip.play()

class SoundPopup(ActionPopup):
	"""Create popup for sound settings. All specs in kv file."""

	pass

class Themes:
	"""Provide methods for creation od theme selection popup."""

	def chooseTheme(self):
		"""Dynamically create choose theme popup according to the data in database."""

		themePop = ThemesPopup(title = 'Choose theme')
		themes = DataAccessAPI.getThemeChooser()

		for theme in themes:
			themeButtonTitle = themes[theme]
			themeButton = MenuButton()
			themeButton.text = themeButtonTitle
			themeButton.bind(on_press=partial(self.updateTheme,theme))
			themePop.themesPopupLayout.add_widget(themeButton)

		themePop.themesPopupLayout.add_widget(ActionPopup.closePopupButton(themePop))
		themePop.open()

	def updateTheme(self,themeName,*args):
		"""Change the current theme in saved settings and restart app to enable changes."""

		DataAccessAPI.setThemeName(themeName)
		ap=App.get_running_app()
		ap.restartApp()

class ThemesPopup(ActionPopup):
	"""Set the popup template for changing themes."""

	pass

#TODO: User defined Themes
#TODO: choosing of different fonts
#TODO: allow user for own music instead of the one provided with the app
