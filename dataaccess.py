import sqlite3


class DataAccess:

    def __init__(self):
        self.conn = sqlite3.connect('Empathy.db')
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def query(self,queryText,*args):
        self.cur.execute(queryText,*args)
        self.conn.commit()
        return self.cur

    def getSingleString(self,queryText,*args):
        base=DataAccess()
        singleString = str(((base.query(queryText,*args)).fetchone())[0])
        return singleString

    def __del__(self):
        self.conn.close()

    def getActiveObjectName(self, refName):
        try:
            activeObjectName = DataAccess.getSingleString(self,"select Name from ReferenceDictionary where Reference = (?)",(refName,))
        except:
            print('Unable to find such reference name.')
        return activeObjectName

    def getActiveObjectDescription(self, refName):
        activeObjectDescription = DataAccess.getSingleString(self,"select Description from ReferenceDictionary where Reference = (?)",(refName,))
        return activeObjectDescription

    def getActiveObjectInteractions(self, refName):
        activeObjectInteractions = {}
        base = DataAccess()
        c=base.query("select Name,Storyline_PageNo,MapNo,EmpathyValue,SanityValue,Description,OptionalJournalEntry from Interactions where ReferenceDictionary_Reference =(?)",(refName,))
        for Name,Storyline_PageNo,MapNo,EmpathyValue,SanityValue,Description,OptionalJournalEntry in c.fetchall():
            activeObjectInteractions[Name]=(Storyline_PageNo,MapNo,EmpathyValue,SanityValue,Description,OptionalJournalEntry)
        return activeObjectInteractions

    def getStorylinePageText(self, pageNo):
        storylinePageText = DataAccess.getSingleString(self,"select PageText from Storyline where pageNo = (?)",(pageNo,))
        return storylinePageText

    def getStorylineMilestonJournal(self, pageNo):
        storylineMilestonJournal=DataAccess.getSingleString(self,"select MilestoneJournalEntry from Storyline where pageNo = (?)",(pageNo,))
        return storylineMilestonJournal

    @classmethod
    def getThemeName(cls):
        themeName=DataAccess.getSingleString(cls,'select themes_themeName from SavedSettings')
        return themeName

    def getColor(self,colorName):
        color = []
        c = DataAccess.query(self,"select R,G,B,A from Colors where Name=(?)",(colorName,))
        result=c.fetchall()
        for R,G,B,A in result:
            color = [R,G,B,A]
        return color

    def getTheme(self, themeName):
        base = DataAccess()
        c = base.query("select customButtonTextColor,customButtonBackgrondColor,customLayoutCanvasColor from Themes where themeName=(?)",(themeName,))
        result = c.fetchone()
        themeColors = {}
        startingColumn = 0
        for coloredObject in result.keys():
            colorName = ((tuple(result))[startingColumn])
            themeColors[coloredObject] = base.getColor(colorName)
            startingColumn += 1
        return themeColors

    def setTheme(self,themeName):
        base = DataAccess()
        base.query("update SavedSettings set themes_themeName=(?)",(themeName,))
        print(themeName)

    @classmethod
    def getThemeChooser(cls):
        themeChooser={}
        base=DataAccess()
        themes = base.query("select themeName,themeDescription from Themes")
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
        soundVolume = DataAccess.getSingleString(cls, 'select soundVolume from SavedSettings')
        return soundVolume

    @classmethod
    def setSoundVolume(cls, soundVolume):
        base = DataAccess()
        base.query('update SavedSettings set soundVolume=(?)', (soundVolume,))

