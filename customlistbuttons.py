from menuinterface import CustomListItemButton
from menuinterface import ScreenChanging
from dataaccessapi import DataAccessAPI
from mainmenuscreen import NewGameConfirmationPopup
from menuinterface import ActionPopup

class LocationsButton(CustomListItemButton):

    def on_press(self):
        pageNo = DataAccessAPI.getPlaces()[self.text]
        DataAccessAPI.setCurrentPageNo(pageNo)
        ScreenChanging.goToScreen('gamescreen')

class StoriesButton(CustomListItemButton):\

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.storyDatabase = ''

    @classmethod
    def startStory(cls):
        warningPop = NewGameConfirmationPopup()
        warningPop.open()

    def on_press(self):
        storyTitle = self.text.capitalize()
        storyDescription = DataAccessAPI.getStoryDesc(self.storyDatabase)
        storyDescPop = StoryDescriptionPopup(title=storyTitle)
        storyDescPop.popupText.text = storyDescription
        storyDescPop.open()

    def setStoryDatabase(self,storyDatabase):
        self.storyDatabase = storyDatabase

class StoryDescriptionPopup(NewGameConfirmationPopup):
    pass
