import abc

class DataAccessInterface(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def getActiveObjectName(self,refName):
        raise NotImplementedError('need to implement getActiveObjectName')

    @abc.abstractmethod
    def getActiveObjectDescription(self, refName):
        raise NotImplementedError('need to implement getActiveObjectDescription')

    @abc.abstractmethod
    def getActiveObjectInteractions(self,refName):
        raise NotImplementedError('need to implement getActiveObjectInteractions')

    @abc.abstractmethod
    def getStorylinePageText(self,pageNo):
        raise  NotImplementedError('need to implement getStorylinePageText')

    def getStorylineMilestonJournal(self,pageNo):
        raise NotImplementedError('need to implement getStorylineMilestonJournal')

    @abc.abstractmethod
    def getThemeName(self):
        raise NotImplementedError('need to implement getThemeName')

    @abc.abstractmethod
    def setTheme(self, themeName):
        raise NotImplementedError('need to implement setTheme')

    @abc.abstractmethod
    def getColor(self, colorName):
        raise NotImplementedError('need to implement getColor')

    @abc.abstractmethod
    def getTheme(self,themeNo):
        raise ModuleNotFoundError('need to implement getTheme')