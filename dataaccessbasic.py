from dataaccessinterface import DataAccessInterface
from referencesdictionary import references
from storyline import storyline

class DataAccess(DataAccessInterface):

    def getActiveObjectName(self, refName):
        try:
            activeObjectName = (references[refName])[0]
        except:
            print('Unable to find such reference name.')
        return activeObjectName

    def getActiveObjectDescription(self, refName):
        activeObjectDescription = (references[refName])[1]
        return activeObjectDescription

    def getActiveObjectInteractions(self, refName):
        activeObjectInteractions = (references[refName])[2]
        return activeObjectInteractions

    def getStorylinePageText(self, pageNo):
        storylinePageText = (storyline[pageNo])[0]
        return storylinePageText

    def getStorylineMilestonJournal(self, pageNo):
        storylineMilestonJournal = (storyline[pageNo])[1]
        return storylineMilestonJournal