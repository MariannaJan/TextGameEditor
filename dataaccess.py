import sqlite3

class DataAccess:
    """Main class for accessing the database.

    Allows for default values if database connection is impossible and offers rudimentary error handling.
    """

    def __init__(self):
        """Creates the database connection.

        Checks if the database file exists. If it exists creates a connection and returns cursor.
        If the datatbase file doesn't exist raises IO Error.
        """
        try:
            with open('Empathy.db'):
                with sqlite3.connect('Empathy.db') as self.conn:
                    self.conn.row_factory = sqlite3.Row
                    self.cur = self.conn.cursor()
        except IOError:
            print('No database to open!')

    def _query(self, queryText, *args):
        """Internal method for simplifying making queries to database.

        :param queryText: query for the database
        :type queryText: string
        :param args: optional - allows for adding arguments for query
        :type args: tuple
        :return: cursor after the query
        :raises: database error if cur.execute fails
        """
        try:
            self.cur.execute(queryText,*args)
        except:
            print('database error - cannot execute query')
        else:
            self.conn.commit()
            return self.cur

    def _getSingleString(self, queryText, *args):
        """Internal method to get single string as a respons from database query.

        :param queryText: query for the database
        :type queryText: string
        :param args: optional - allows for adding arguments for query
        :type args: tuple
        :return: response from database query
        :rtype: string
        :raises: error if query fails
        """
        base=DataAccess()
        try:
            singleString = str(((base._query(queryText, *args)).fetchone())[0])
        except:
            print('database error - cannot get single string')
        else:
            return singleString

    @classmethod
    def _getSavedSetting(cls,requestedSetting):
        """Internal method for retreiving data from Saved Settings table

        :param requestedSetting: name of the column containing the setting to retreive
        :type requestedSetting: string
        :return: the value of requested setting from the saved settings
        """
        queryText = ''.join(['select ',requestedSetting,' from SavedSettings'])
        savedSetting = cls._getSingleString(cls,queryText)
        return savedSetting

    @classmethod
    def _setSavedSetting(cls,changedSettingName,changedSettingValue):
        """Internal method for changing data in Saved Settings table

        :param changedSettingName: name of the column containing the setting to change
        :type changedSettingName: string
        :param changedSettingValue: new value of the setting to be changed
        """
        base = DataAccess()
        queryText = ''.join(['update SavedSettings set ',changedSettingName,'=(?)'])
        base._query(queryText, (changedSettingValue,))

    def getActiveObjectName(self, refName):
        """Matches the name from data base with the markup reference that has been chosen by the player.

        :param refName: name of the clicked reference from markup
        :type refName: string
        :return: full name of the chosen object, retreived from database
        :rtype: string
        """
        try:
            activeObjectName = DataAccess._getSingleString(self, "select Name from ReferenceDictionary where Reference = (?)", (refName,))
        except:
            print('Unable to find such reference name.')
        return activeObjectName

    def getActiveObjectDescription(self, refName):
        """Retreive from database the description of the markup reference that has been chosen by the player.

        :param refName: name of ther clicked reference from markup
        :type refName: string
        :return: description of the chosen object, retreived from database
        :rtype: string
        """
        activeObjectDescription = DataAccess._getSingleString(self, "select Description from ReferenceDictionary where Reference = (?)", (refName,))
        return activeObjectDescription

    def getActiveObjectInteractions(self, refName):
        """Retreive from database details of interactions available for the markup reference that has been chosen by the player.

        :param refName: name of ther clicked reference from markup
        :type refName: string
        :return: {string interaction name : tuple(string page ID,string map ID, int empathy, int sanity,string description,optional string journal entry)}
        :rtype: dict [str,tuple(string,string,int,int,string,string)]
        """
        activeObjectInteractions = {}
        base = DataAccess()
        c=base._query("select Name,Storyline_PageNo,MapNo,EmpathyValue,SanityValue,Description,OptionalJournalEntry from Interactions where ReferenceDictionary_Reference =(?)", (refName,))
        for Name,Storyline_PageNo,MapNo,EmpathyValue,SanityValue,Description,OptionalJournalEntry in c.fetchall():
            activeObjectInteractions[Name]=(Storyline_PageNo,MapNo,EmpathyValue,SanityValue,Description,OptionalJournalEntry)
        return activeObjectInteractions

    def getStorylinePageText(self, pageNo):
        """Retreive from database the text of the given page.

        :param pageNo: ID of the page
        :type pageNo: string
        :return: ext (with markup) of the chosen plot page (according to the ID)
        :rtype: string
        """
        storylinePageText = DataAccess._getSingleString(self, "select PageText from Storyline where pageNo = (?)", (pageNo,))
        return storylinePageText

    def getStorylineMilestonJournal(self, pageNo):
        """Retreive from database the text of the milestone juournal entry associated with the given page ID.

        :param pageNo: ID of the page
        :type pageNo: string
        :return: the text of the milestone juournal entry associated with the given page ID
        :rtype: string
        """
        storylineMilestonJournal=DataAccess._getSingleString(self, "select MilestoneJournalEntry from Storyline where pageNo = (?)", (pageNo,))
        return storylineMilestonJournal

    @classmethod
    def getThemeName(cls):
        """Get the name of the theme from the saved settings.

        :return: name of the theme from the saved settings
        :rtype: string
        """
        themeName = cls._getSavedSetting('themes_themeName')
        return themeName

    @classmethod
    def setThemeName(cls, themeName):
        """Set the name of the theme in the saved settings.

        :param themeName: name of the theme to be written in the saved settings table
        :type themeName: string
        """
        cls._setSavedSetting('themes_themeName',themeName)

    def getColor(self,colorName):
        """Retreive from database the list for RGBA values for the given color name.

        :param colorName: name of the color to be retreived as RGBA list
        :type colorName: string
        :return: color specified as [float R, float G, float B, float A]
        :rtype: list
        """
        color = []
        c = DataAccess._query(self, "select R,G,B,A from Colors where Name=(?)", (colorName,))
        result=c.fetchall()
        for R,G,B,A in result:
            color = [R,G,B,A]
        return color

    def getTheme(self, themeName):
        """Retreive from database colors for the given theme.

        :param themeName: name of the theme being checked
        :type themeName: string
        :return: {string name of function of color from the theme: tuple color(float R, float G, float B, float A)}
        :rtype: dict [str,tuple(float,float,float,float)]
        """
        base = DataAccess()
        c = base._query("select customButtonTextColor,customButtonBackgroundColor,customLayoutCanvasColor from Themes where themeName=(?)", (themeName,))
        try:
            result = c.fetchone()
        except:
            print('no theme colors to fetch')
            return {'customButtonTextColor':(0,0,0,1),'customButtonBackgroundColor':(1,1,1,1),'customLayoutCanvasColor':(1,1,1,1)}
        else:
            themeColors = {}
            startingColumn = 0
            for coloredObject in result.keys():
                colorName = ((tuple(result))[startingColumn])
                themeColors[coloredObject] = base.getColor(colorName)
                startingColumn += 1
            return themeColors

    @classmethod
    def getThemeChooser(cls):
        """Retreive available themes from datatbase.

        :return: {string theme name: string theme full name, as for button text generation}
        :rtype: dict [str,str]
        """
        themeChooser={}
        base=DataAccess()
        themes = base._query("select themeName,themeDescription from Themes")
        for theme in themes.fetchall():
            themeChooser[theme[0]] = (theme[1])
        return themeChooser

    @classmethod
    def setupTheme(cls):
        """Choose the color theme for the current gameplay according to the saved settings.

        :return: {string name of function of color from the theme: tuple color(float R, float G, float B, float A)}
        :rtype: dict{str,tuple(float,float,float,float)}
        """
        base = DataAccess()
        themeSettings = base.getTheme(base.getThemeName())
        return themeSettings

    @classmethod
    def getSavedSoundVolume(cls):
        """Retreive the sound volume from the database saved settings.

        :return: sound volume from the database saved settings
        :rtype: float
        """
        soundVolume = cls._getSavedSetting('soundVolume')
        return soundVolume

    @classmethod
    def setSoundVolume(cls, soundVolume):
        """Set chosen sound volume in the saved settings in database.

        :param soundVolume: sound volume
        :type soundVolume: float
        """
        cls._setSavedSetting('soundVolume',soundVolume)

    @classmethod
    def getSoundFilesNames(cls):
        """Retreive from database the names of the files for the sounds in game.

        :return: string name of sound : string name of the sound file}
        :rtype: dict [str,str]
        """
        base = DataAccess()
        c = base._query('select * from Sounds')
        soundFilesNames = {}
        try:
            for soundName, fileName in c.fetchall():
                soundFilesNames[soundName]=fileName
        except:
            print('database error')
            return {}
        else:
            return soundFilesNames

    @classmethod
    def getSavedFontName(cls):
        """Get the name of the font for the current gameplay from the saved settings in database.

        :return: name of font from the saved settings in database
        :rtype: string
        """
        fontName = cls._getSavedSetting('fonts_name')
        return fontName

    @classmethod
    def getFonts(cls,fontName,fontStyle):
        """Retreive from database the name of the font file in a specified style.

        :param fontName: name of the font
        :type fontName: string
        :param fontStyle: style of the font
        :type fontStyle: string
        :return: name of the font file in a specified style from the database
        :rtype: string
        """
        fontQueryText = ''.join(['select ',fontStyle,' from Fonts where name=(?)'])
        fontFileName = DataAccess._getSingleString(cls, fontQueryText, (fontName,))
        return fontFileName




if __name__=="__main__":
	DataAccess.__init__()



