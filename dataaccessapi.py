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