from kivy.core.audio import SoundLoader
from menuinterface import BasicScreen
from menuinterface import SoundSettings


class MainMenuScreen(BasicScreen):

	def __init__(self, **kwargs):
		super(MainMenuScreen,self).__init__(**kwargs)
		self.screenName = 'mainmenu'
		self.backgroundSound = SoundLoader.load(filename=SoundSettings.getAudioFilePath(requestedSound=self.screenName))
		try:
			SoundSettings.playMusic(self.backgroundSound)
		except:
			print("no audio file to load on this path!")

	def on_enter(self, *args):

		if self.backgroundSound is None:
			self.backgroundSound = SoundLoader.load(filename=SoundSettings.getAudioFilePath(requestedSound=self.screenName))
		try:
			SoundSettings.playMusic(self.backgroundSound)
		except:
			print("no audio file to load on this path!")

	def on_leave(self, *args):
		try:
			self.backgroundSound.stop()
		except:
			print("no audio file to be stopped")


