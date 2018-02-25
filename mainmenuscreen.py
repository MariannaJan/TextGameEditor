"""Starting screen of the game."""

from kivy.core.audio import SoundLoader
from menuinterface import BasicScreen
from menuinterface import SoundSettings
from menuinterface import ActionPopup
from dataaccessapi import DataAccessAPI


class MainMenuScreen(BasicScreen):
	"""Create main menu for the game. The complete setup in kv file."""

	def __init__(self, **kwargs):
		"""Setup the main screen with the name and proper background sound."""

		super(MainMenuScreen,self).__init__(**kwargs)
		self.screenName = 'mainmenu'
		self.backgroundSound = SoundLoader.load(filename=SoundSettings.getAudioFilePath(requestedSound=self.screenName))
		try:
			SoundSettings.playMusic(self.backgroundSound)
		except:
			print("no audio file to load on this path!")

	def on_enter(self, *args):
		"""Start playing appropriate background sound on entering the screen."""

		if self.backgroundSound is None:
			self.backgroundSound = SoundLoader.load(filename=SoundSettings.getAudioFilePath(requestedSound=self.screenName))
		try:
			SoundSettings.playMusic(self.backgroundSound)
		except:
			print("no audio file to load on this path!")

	def on_leave(self, *args):
		"""Stop playing the background sound on leaving the screen."""

		try:
			self.backgroundSound.stop()
		except:
			print("no audio file to be stopped")

	def newGameConfirmationPopupOpen(self):
		confirmPop = NewGameConfirmationPopup()
		confirmPop.open()

class NewGameConfirmationPopup(ActionPopup):

	@classmethod
	def startNewGame(cls):
		DataAccessAPI.clearAvailablePlaces()
		pageNo = DataAccessAPI.getNewGamePageNo()
		DataAccessAPI.resetEmpathy()
		DataAccessAPI.resetSanity()
		DataAccessAPI.clearInventory()
		DataAccessAPI.clearTakenReferences()
		DataAccessAPI.clearJournal()
		DataAccessAPI.setCurrentPageNo(pageNo)

