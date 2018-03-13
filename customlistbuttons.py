from menuinterface import CustomListItemButton
from menuinterface import ScreenChanging
from dataaccessapi import DataAccessAPI
from mainmenuscreen import NewGameConfirmationPopup
from gamestrings import GameStrings
from menuinterface import ActionPopup

class LocationsButton(CustomListItemButton):

    def on_press(self):
        pageNo = DataAccessAPI.getPlaces()[self.text]
        DataAccessAPI.setCurrentPageNo(pageNo)
        ScreenChanging.goToScreen('gamescreen')

class StoriesButton(CustomListItemButton):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.storyDatabase = ''

    def on_press(self):
        storyTitle = self.text.capitalize()
        storyDescPop = StoryDescriptionPopup(title=storyTitle, storyDatabase=self.storyDatabase)
        storyDescPop.open()

    def setStoryDatabase(self,storyDatabase):
        self.storyDatabase = storyDatabase

class StoryDescriptionPopup(ActionPopup):

    def __init__(self, storyDatabase, **kwargs):
        super().__init__(**kwargs)
        self.story = storyDatabase
        storyDescription = DataAccessAPI.getStoryDesc(self.story)
        self.popupText.text = '\n\n'.join([GameStrings.newgameconfirmtext, storyDescription])

    def startStory(self):
        DataAccessAPI.setChosenStory(self.story)
        NewGameConfirmationPopup.startNewGame()

