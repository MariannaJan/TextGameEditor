from dataaccess import DataAccess

class DataAccessAPI:
    """API for getting the necessary data, separating the mechanism of data base access from providing necessary data."""

    def getReferenceName(self, refName):
        """Get the display name of the clicked reference.

        :param refName: name of the clicked reference from markup
        :type refName: string
        :return: full name of the chosen reference
        :rtype: string
        """

        referenceName = DataAccess.getActiveObjectName(self,refName)
        return referenceName

    def getReferenceDescription(self,refName):
        """Get the display description of the clicked reference.

        :param refName: name of the clicked reference from markup
        :type refName: string
        :return: description of the chosen reference
        :rtype: string
        """

        referenceDescription = DataAccess.getActiveObjectDescription(self,refName)
        return referenceDescription

    def getReferenceInteractions(self,refName):
        """Get possible interactions for the clicked reference and their details.

        :param refName: name of ther clicked reference from markup
        :type refName: string
        :return: {string interaction name : tuple(string page ID,string map ID, int empathy, int sanity,string description,optional string journal entry)}
        :rtype: dict [str,tuple(string,string,int,int,string,string)]
        """

        referenceInteractions = DataAccess.getActiveObjectInteractions(self,refName)
        return referenceInteractions

    def getReferenceStorylineText(self,pageNo):
        """Get the text with active references for the current gamplay page.

        :param pageNo:
        :return:
        """

        referenceStorylineText = DataAccess.getStorylinePageText(self,pageNo)
        return referenceStorylineText

    @classmethod
    def getColorFromTheme(cls, colorCategory):
        """Get different colors from a theme.

        :param str colorCategory: name of function of color from the theme
        :return: color from theme (float R, float G, float B, float A)
        :rtype: tuple(float,float,float,float)
        """

        color = (DataAccess.setupTheme())[colorCategory]
        return color

    @classmethod
    def getThemeChooser(cls):
        """Get available color themes.

        :return: {string theme name: string theme full name, as for button text generation}
        :rtype: dict [str,str]
        """
        return DataAccess.getAvailableThemes()

    @classmethod
    def setThemeName(cls, themeName):
        """Set the name of the chosen color theme for the current game.

        :param str themeName: name of theme to be set
        """
        DataAccess.setSavedThemeName(themeName)

    @classmethod
    def getFontName(cls):
        """Get the name of the current font used by game.

        :return: name of font
        :rtype: str
        """
        return DataAccess.getSavedFontName()

    @classmethod
    def getFontFilePath(cls,fontName,fontStyle):
        """Get the path to the file for the specified font in specified style.
        :param str fontName: name of the font
        :param str fontStyle: style of font, eg. bold
        :return: path to the file
        :rtype: str
        """
        fontFileName = DataAccess.getFonts(fontName,fontStyle)
        fontFilePath = "".join(['Fonts/',fontFileName])
        return fontFilePath

    @staticmethod
    def getAudioFilePath(requestedSound):
        """Get the path to the requested sound file.

        :param str requestedSound: name of the requested sound
        :return: path to file
        :rtype: str
        """
        audioFilePaths = DataAccess.getSoundFilesNames()
        filePath = ''.join(('Audio/',audioFilePaths.get(requestedSound,'')))
        return filePath

    @classmethod
    def getSoundVolume(cls):
        """Get the current volume of sound in game.

        :return: current volume of sound
        :rtype: float
        """
        return DataAccess.getSavedSoundVolume()

    @classmethod
    def setSoundVolume(cls,soundVolume):
        """Set the current volume of the sound in  game.

        :param soundVolume: volume of sound to be set
        :type: float
        """
        DataAccess.setSavedSoundVolume(soundVolume)

    @classmethod
    def getInventoryItems(cls):
        """Get the dictionary of items currently in inventory with their descriptions.

        :return: gictionary of items currently in inventory with their descriptions
        :rtype: dict [str,str]
        """
        inventoryItems = DataAccess.getItemFeatures(itemIDs=DataAccess.getInventoryContentIds())
        return inventoryItems

    @classmethod
    def getCurrentPageNo(cls):
        """Get the ID of the current page to be displayed on the gamescreen.

        :return: ID of the current page to be displayed on the gamescreen
        :rtype: str
        """
        currenPageNo = DataAccess.getSavedPageNo()
        return currenPageNo

    @classmethod
    def setCurrentPageNo(cls,pageNo):
        DataAccess.setSavedPageNo(pageNo)

    @classmethod
    def getCurrentEmpathyValue(cls):
        """Get the current value of Empathy.

        :return: current value of Empathy
        :rtype: int """

        currentEmpathyValue = DataAccess.getSavedEmpathyValue()
        return currentEmpathyValue

    @classmethod
    def setCurrentEmpathyValue(cls,empathyValue):
        DataAccess.setSavedEmpathyValue(empathyValue)

    @classmethod
    def getCurrentSanityValue(cls):
        """Get the current value of Sanity.

        :return: current value of Sanity
        :rtype: int """

        currentSanityValue = DataAccess.getSavedSanityValue()
        return currentSanityValue

    @classmethod
    def setCurrentSanityValue(cls,sanityValue):
        DataAccess.setSavedSanityValue(sanityValue)

    @classmethod
    def getNewGamePageNo(cls):
        newGamePageNo = DataAccess.getStoryFirstPageNo()
        return newGamePageNo

    @classmethod
    def getNewGameEmpathyValue(cls):
        newGameEmpathyValue = DataAccess.getStartingEmpathyValue()
        return newGameEmpathyValue

    @classmethod
    def getNewGameSanityValue(cls):
        newGameSanityValue = DataAccess.getStartingSanityValue()
        return newGameSanityValue