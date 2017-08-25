import sqlite3

class DataAccess:

    def __init__(self):
        self.conn = sqlite3.connect('Empathy.db')
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def _query(self, queryText, *args):
        self.cur.execute(queryText,*args)
        self.conn.commit()
        return self.cur

    def _getSingleString(self, queryText, *args):
        base=DataAccess()
        singleString = str(((base._query(queryText, *args)).fetchone())[0])
        return singleString

    def __del__(self):
        self.conn.close()

    @classmethod
    def _getSavedSetting(cls,requestedSetting):
        queryText = ''.join(['select ',requestedSetting,' from SavedSettings'])
        savedSetting = cls._getSingleString(cls,queryText)
        return savedSetting

    @classmethod
    def _setSavedSetting(cls,changedSettingName,changedSettingValue):
        base = DataAccess()
        queryText = ''.join(['update SavedSettings set ',changedSettingName,'=(?)'])
        base._query(queryText, (changedSettingValue,))


    def getActiveObjectName(self, refName):
        try:
            activeObjectName = DataAccess._getSingleString(self, "select Name from ReferenceDictionary where Reference = (?)", (refName,))
        except:
            print('Unable to find such reference name.')
        return activeObjectName

    def getActiveObjectDescription(self, refName):
        activeObjectDescription = DataAccess._getSingleString(self, "select Description from ReferenceDictionary where Reference = (?)", (refName,))
        return activeObjectDescription

    def getActiveObjectInteractions(self, refName):
        activeObjectInteractions = {}
        base = DataAccess()
        c=base._query("select Name,Storyline_PageNo,MapNo,EmpathyValue,SanityValue,Description,OptionalJournalEntry from Interactions where ReferenceDictionary_Reference =(?)", (refName,))
        for Name,Storyline_PageNo,MapNo,EmpathyValue,SanityValue,Description,OptionalJournalEntry in c.fetchall():
            activeObjectInteractions[Name]=(Storyline_PageNo,MapNo,EmpathyValue,SanityValue,Description,OptionalJournalEntry)
        return activeObjectInteractions

    def getStorylinePageText(self, pageNo):
        storylinePageText = DataAccess._getSingleString(self, "select PageText from Storyline where pageNo = (?)", (pageNo,))
        return storylinePageText

    def getStorylineMilestonJournal(self, pageNo):
        storylineMilestonJournal=DataAccess._getSingleString(self, "select MilestoneJournalEntry from Storyline where pageNo = (?)", (pageNo,))
        return storylineMilestonJournal

    @classmethod
    def getThemeName(cls):
        themeName = cls._getSavedSetting('themes_themeName')
        return themeName

    @classmethod
    def setThemeName(cls, themeName):
        cls._setSavedSetting('themes_themeName',themeName)

    def getColor(self,colorName):
        color = []
        c = DataAccess._query(self, "select R,G,B,A from Colors where Name=(?)", (colorName,))
        result=c.fetchall()
        for R,G,B,A in result:
            color = [R,G,B,A]
        return color

    def getTheme(self, themeName):
        base = DataAccess()
        c = base._query("select customButtonTextColor,customButtonBackgroundColor,customLayoutCanvasColor from Themes where themeName=(?)", (themeName,))
        result = c.fetchone()
        themeColors = {}
        startingColumn = 0
        for coloredObject in result.keys():
            colorName = ((tuple(result))[startingColumn])
            themeColors[coloredObject] = base.getColor(colorName)
            startingColumn += 1
        return themeColors

    @classmethod
    def getThemeChooser(cls):
        themeChooser={}
        base=DataAccess()
        themes = base._query("select themeName,themeDescription from Themes")
        for theme in themes.fetchall():
            themeChooser[theme[0]] = (theme[1])
        return themeChooser

    @classmethod
    def setupTheme(cls):
        base = DataAccess()
        themeSettings = base.getTheme(base.getThemeName())
        return themeSettings

    @classmethod
    def getSoundVolume(cls):
        soundVolume = cls._getSavedSetting('soundVolume')
        return soundVolume

    @classmethod
    def setSoundVolume(cls, soundVolume):
        cls._setSavedSetting('soundVolume',soundVolume)

    @classmethod
    def getSoundFilesNames(cls):
        base = DataAccess()
        c = base._query('select * from Sounds')
        soundFilesNames = {}
        for soundName, fileName in c.fetchall():
            soundFilesNames[soundName]=fileName
        return soundFilesNames

    @classmethod
    def getFontName(cls):
        fontName = cls._getSavedSetting('fonts_name')
        return fontName

    @classmethod
    def getFonts(cls,fontName,fontStyle):
        fontQueryText = ''.join(['select ',fontStyle,' from Fonts where name=(?)'])
        fontFile = DataAccess._getSingleString(cls, fontQueryText, (fontName,))
        fontFilePath = "".join(['Fonts/',fontFile])
        return fontFilePath



if __name__=="__main__":
	DataAccess().__init__()



