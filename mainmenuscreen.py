"""Starting screen of the game."""
from gc import collect

from kivy.core.audio import SoundLoader
from kivy.app import App
from menuinterface import BasicScreen
from menuinterface import SoundSettings
from menuinterface import ActionPopup
from dataaccessapi import DataAccessAPI
from dataaccess import DataAccess

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

	@classmethod
	def newGameConfirmationPopupOpen(cls):
		if DataAccess.checkIfStoryExists():
			confirmPop = NewGameConfirmationPopup()
			confirmPop.open()
		else:
			mustChoosePop = MustChooseStoryPopup()
			mustChoosePop.open()

	@classmethod
	def continueGame(cls):
		if DataAccess.checkIfStoryExists():
			App.get_running_app().root.children[0].current = "gamescreen"
		else:
			mustChoosePop = MustChooseStoryPopup()
			mustChoosePop.open()

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
		DataAccessAPI.clearUsedInteractions()
		DataAccessAPI.setCurrentPageNo(pageNo)
		DataAccessAPI.clearOneTimeInteractions()
		collect()

class MustChooseStoryPopup(ActionPopup):
	pass
