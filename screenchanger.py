from kivy.uix.screenmanager import ScreenManager

# noinspection PyUnresolvedReferences
from mainmenuscreen import MainMenuScreen
# noinspection PyUnresolvedReferences
from gamescreen import GameScreen
# noinspection PyUnresolvedReferences
from optionsscreen import OptionsScreen


class ScreenChanger(ScreenManager):
	"""Main widget for the creation of all the game screens.

	Added as a child to the master widget in Empathy.
	Screens
	* MainMenuScreen
	* GameScreen
	* OptionsScreen
	"""

	pass