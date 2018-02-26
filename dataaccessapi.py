from dataaccess import DataAccess as DA
from functools import partial

class DataAccessAPI:
    """API for getting the necessary data, separating the mechanism of data base access from providing necessary data."""

    def getReferenceName(self, refName):
        """Get the display name of the clicked reference.

        :param refName: name of the clicked reference from markup
        :type refName: string
        :return: full name of the chosen reference
        :rtype: string
        """

        referenceName = DA.getActiveObjectName(self,refName)
        return referenceName

    def getReferenceDescription(self,refName):
        """Get the display description of the clicked reference.

        :param refName: name of the clicked reference from markup
        :type refName: string
        :return: description of the chosen reference
        :rtype: string
        """

        referenceDescription = DA.getActiveObjectDescription(self,refName)
        return referenceDescription

    def getReferenceInteractions(self,refName):
        """Get possible interactions for the clicked reference and their details.

        :param refName: name of ther clicked reference from markup
        :type refName: string
        :return: {string interaction name : tuple(string page ID,string map ID, int empathy, int sanity,string description,optional string journal entry)}
        :rtype: dict [str,tuple(string,string,int,int,string,string)]
        """

        referenceInteractions  = {}
        interactions = DA.getActiveObjectInteractions(self,refName)
        for interaction, description in interactions.items():
            referenceInteractions[interaction] = {'pageNo'                  :description[0],
                                                  'mapNo'                   :description[1],
                                                  'empathyValue'            :description[2],
                                                  'sanityValue'             :description[3],
                                                  'interactionDescription'  :description[4],
                                                  'optionalJournalEntry'    :description[5],
                                                  'empathyTreshold'         :description[6],
                                                  'sanityTreshold'          :description[7],
                                                  'pagesLocked'             :description[8],
                                                  'takeItemID'              :description[9]}
        return referenceInteractions

    def getReferenceStorylineText(self,pageNo):
        """Get the text with active references for the current gamplay page.

        :param pageNo:
        :return:
        """

        referenceStorylineText = DA.getStorylinePageText(self,pageNo)
        return referenceStorylineText

    @classmethod
    def getColorFromTheme(cls, colorCategory):
        """Get different colors from a theme.

        :param str colorCategory: name of function of color from the theme
        :return: color from theme (float R, float G, float B, float A)
        :rtype: tuple(float,float,float,float)
        """

        color = (DA.setupTheme())[colorCategory]
        return color

    @classmethod
    def getThemeChooser(cls):
        """Get available color themes.

        :return: {string theme name: string theme full name, as for button text generation}
        :rtype: dict [str,str]
        """
        return DA.getAvailableThemes()

    @classmethod
    def setThemeName(cls, themeName):
        """Set the name of the chosen color theme for the current game.

        :param str themeName: name of theme to be set
        """
        DA.setSavedThemeName(themeName)

    @classmethod
    def getFontName(cls):
        """Get the name of the current font used by game.

        :return: name of font
        :rtype: str
        """
        return DA.getSavedFontName()

    @classmethod
    def getFontFilePath(cls,fontName,fontStyle):
        """Get the path to the file for the specified font in specified style.
        :param str fontName: name of the font
        :param str fontStyle: style of font, eg. bold
        :return: path to the file
        :rtype: str
        """
        fontFileName = DA.getFonts(fontName,fontStyle)
        fontFilePath = "".join(['Fonts/',fontFileName])
        return fontFilePath

    @staticmethod
    def getAudioFilePath(requestedSound):
        """Get the path to the requested sound file.

        :param str requestedSound: name of the requested sound
        :return: path to file
        :rtype: str
        """
        audioFilePaths = DA.getSoundFilesNames()
        filePath = ''.join(('Audio/',audioFilePaths.get(requestedSound,'')))
        return filePath

    @classmethod
    def getSoundVolume(cls):
        """Get the current volume of sound in game.

        :return: current volume of sound
        :rtype: float
        """
        return DA.getSavedSoundVolume()

    @classmethod
    def setSoundVolume(cls,soundVolume):
        """Set the current volume of the sound in  game.

        :param soundVolume: volume of sound to be set
        :type: float
        """
        DA.setSavedSoundVolume(soundVolume)

    @classmethod
    def getInventoryItems(cls):
        """Get the dictionary of items currently in inventory with their descriptions.

        :return: gictionary of items currently in inventory with their descriptions
        :rtype: dict [str,tuple(str,str)]
        """
        inventoryItems = DA.getItemFeatures(itemIDs=DA.getInventoryContentIds())
        return inventoryItems

    @classmethod
    def getCurrentPageNo(cls):
        """Get the ID of the current page to be displayed on the gamescreen.

        :return: ID of the current page to be displayed on the gamescreen
        :rtype: str
        """
        currenPageNo = DA.getSavedPageNo()
        return currenPageNo

    @classmethod
    def setCurrentPageNo(cls,pageNo):
        DA.setSavedPageNo(pageNo)

    @classmethod
    def getCurrentEmpathyValue(cls):
        """Get the current value of Empathy.

        :return: current value of Empathy
        :rtype: int """

        currentEmpathyValue = DA.getSavedEmpathyValue()
        return int(currentEmpathyValue)

    @classmethod
    def setCurrentEmpathyValue(cls,empathyValue):
        resultingEmpathyValue = empathyValue + int(DA.getSavedEmpathyValue())
        if (DataAccessAPI.getMinimumEmpathy() < resultingEmpathyValue < DataAccessAPI.getMaximumEmpathy()) or empathyValue == 0:
            newEmpathyValue = resultingEmpathyValue
        elif empathyValue < 0:
            newEmpathyValue = DataAccessAPI.getMinimumEmpathy()
        elif empathyValue > 0:
            newEmpathyValue = DataAccessAPI.getMaximumEmpathy()
        DA.setSavedEmpathyValue(newEmpathyValue)

    @classmethod
    def getCurrentSanityValue(cls):
        """Get the current value of Sanity.

        :return: current value of Sanity
        :rtype: int """

        currentSanityValue = DA.getSavedSanityValue()
        return int(currentSanityValue)

    @classmethod
    def setCurrentSanityValue(cls,sanityValue):
        resultingSanityValue = sanityValue + int(DA.getSavedSanityValue())
        if DataAccessAPI.getMinimumSanity() < resultingSanityValue < DataAccessAPI.getMaximumSanity():
            newSanityValue = resultingSanityValue
        elif resultingSanityValue < 0:
            newSanityValue = DataAccessAPI.getMinimumSanity()
        elif resultingSanityValue > 0:
            newSanityValue = DataAccessAPI.getMaximumSanity()
        DA.setSavedSanityValue(newSanityValue)

    @classmethod
    def getNewGamePageNo(cls):
        newGamePageNo = DA.getStoryFirstPageNo()
        return newGamePageNo

    @classmethod
    def resetEmpathy(cls):
        newGameEmpathyValue = int(DA.getStartingEmpathyValue())
        DA.setSavedEmpathyValue(newGameEmpathyValue)

    @classmethod
    def resetSanity(cls):
        newGameSanityValue = int(DA.getStartingSanityValue())
        DA.setSavedSanityValue(newGameSanityValue)

    @classmethod
    def clearInventory(cls):
        DA.deleteItemsFromInventory()

    @classmethod
    def putItemInInventory(cls,itemID):
        DA.addItemToInventory(itemID)

    @classmethod
    def removeUsedItemFromInventory(cls,ItemID):
        DA.deleteUsedItemFromInventory(ItemID)

    @classmethod
    def checkIfReferenceTaken(cls,refName):
        takenReferences = DA.getTakenReferences()
        if refName in takenReferences:
            return True
        else:
            return False

    @classmethod
    def markReferenceAsTaken(cls,refName):
        DA.addTakenReference(refName)

    @classmethod
    def clearTakenReferences(cls):
        DA.deleteRefsFromTakenReferences()

    @classmethod
    def getInfoOnItemUseInWorld(cls,refName,itemID):

        infoOnItemUseInWorld = {}
        itemUseInWorld = DA.getDataOnItemUseInWorld(refName,itemID)
        for id,description in itemUseInWorld.items():
            infoOnItemUseInWorld[id] = {'refName'                   :description[0],
                                        'effectDescription'         :description[1],
                                        'sanityValue'               :description[2],
                                        'empathyValue'              :description[3],
                                        'sanityTreshold'            :description[4],
                                        'empathyTreshold'           :description[5],
                                        'pageNo'                    :description[6],
                                        'mapNo'                     :description[7],
                                        'optionalJpurnalEntry'      :description[8],
                                        'pagesLocked'               :description[9],
                                        'removeFromInventoryFlag'   :description[10]}
        return infoOnItemUseInWorld

    @classmethod
    def getInfoOnItemUseOnItem(cls,itemID_1,itemID_2):

        itemUseOnItem = DA.getDataOnItemUseOnItem(itemID_1,itemID_2)
        infoOnItemUseOnItem = {'itemID_1'               :itemUseOnItem[0],
                               'itemID_2'               :itemUseOnItem[1],
                               'createdObjectID'        :itemUseOnItem[2],
                               'effectDescription'      :itemUseOnItem[3],
                               'sanityValue'            :itemUseOnItem[4],
                               'empathyValue'           :itemUseOnItem[5],
                               'sanityTreshold'         :itemUseOnItem[6],
                               'empathyTreshold'        :itemUseOnItem[7],
                               'pageNo'                 :itemUseOnItem[8],
                               'mapNo'                  :itemUseOnItem[9],
                               'optionalJournalEntry'   :itemUseOnItem[10],
                               'pagesLocked'            :itemUseOnItem[11]}
        return infoOnItemUseOnItem

    @classmethod
    def getJournalContent(cls):
        journalContent = DA.getJournalEntries()
        return journalContent

    @classmethod
    def addJournalEntry(cls,journalEntry):
        currentEntries=DA.getJournalEntries()
        if journalEntry != '' and journalEntry not in currentEntries:
            DA.setJournalEntry(journalEntry)

    @classmethod
    def clearJournal(cls):
        DA.removeEntriesFromJournal()

    @classmethod
    def getPageJournalEntry(cls,pageNo):
        pageJournalEntry = DA.getStorylineMilestonJournal(pageNo)
        return pageJournalEntry

    @classmethod
    def getPlaces(cls):
        places = DA.getAvailableLocations()
        return places

    @classmethod
    def addPlace(cls,pageNo):
        currentPlaces = DA.getAvailableLocations().values()
        if pageNo not in currentPlaces:
            DA.addAvailableLocation(pageNo=pageNo, locationName=DA.getLocationName(pageNo))

    @classmethod
    def removePlace(cls,pageNo):
        DA.removeLocation(pageNo)

    @classmethod
    def clearAvailablePlaces(cls):
        DA.removeAvailableLocations()

    @classmethod
    def getMinimumEmpathy(cls):
        minimumEmpathy = DA.getMinimumEmpathyValue()
        return int(minimumEmpathy)

    @classmethod
    def getMaximumEmpathy(cls):
        maximumEmpathy = DA.getMaximumEmpathyValue()
        return int(maximumEmpathy)

    @classmethod
    def getEmpathyRange(cls):
        empathyRange = (int(DA.getMinimumEmpathyValue()),int(DA.getMaximumEmpathyValue()))
        return empathyRange

    @classmethod
    def getMinimumSanity(cls):
        minimumSanity = DA.getMinimumSanityValue()
        return int(minimumSanity)

    @classmethod
    def getMaximumSanity(cls):
        maximumSanity = DA.getMaximumSanityValue()
        return int(maximumSanity)

    @classmethod
    def getSanityRange(cls):
        sanityRange = (int(DA.getMinimumSanityValue()),int(DA.getMaximumSanityValue()))
        return sanityRange

    @classmethod
    def getEmpathyNameReplacement(cls):
        empathyNameReplacement = DA.getEmpathyName()
        return empathyNameReplacement

    @classmethod
    def getEmpathyDescriptionReplacement(cls):
        empathyDescriptionReplacemet = DA.getEmpathyDescription()
        return empathyDescriptionReplacemet

    @classmethod
    def getSanityNameReplacement(cls):
        sanityNameReplacement = DA.getSanityName()
        return sanityNameReplacement

    @classmethod
    def getSanityDescriptionReplacement(cls):
        sanityNameReplacement = DA.getSanityDescription()
        return sanityNameReplacement

    @classmethod
    def _checkTreshold(cls, emp_san_switch, value, treshold):
        switch = emp_san_switch.lower()
        switches = {
            'e': DA.getEmpathyDirection(),
            's': DA.getSanityDirection()}
        direction = (switches.get(switch,partial(print, 'emp_san_switch must be either e or s'))).lower()
        directions = {
            'above': lambda: True if value >= treshold else False,
            'below': lambda: True if value <= treshold else False}
        ifTresholdMet = directions.get(direction, partial(print, 'emp_san_switch must be either e or s'))()
        return ifTresholdMet

    @classmethod
    def checkIfDisabled(cls,empathyTreshold,sanityTreshold):
        empathyCondition = DataAccessAPI._checkTreshold('e', value=DataAccessAPI.getCurrentEmpathyValue(), treshold=empathyTreshold)
        sanityCondition = DataAccessAPI._checkTreshold('s', value=DataAccessAPI.getCurrentSanityValue(), treshold=sanityTreshold)
        if (empathyCondition and sanityCondition)==False:
            return True

