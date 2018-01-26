from menuinterface import BasicScreen
from mainmenuscreen import NewGameConfirmationPopup

class ChooseStoryScreen(BasicScreen):

    @classmethod
    def startStory(cls):
        warningPop = NewGameConfirmationPopup()
        warningPop.open()


