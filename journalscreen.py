from functools import partial

from gamestrings import GameStrings
from menuinterface import BasicScreen
from menuinterface import CustomLabel
from menuinterface import MenuButton
from menuinterface import ScreenChanging
from menuinterface import ScrollableLabel
from dataaccessapi import DataAccessAPI

class JournalScreen(BasicScreen):

    def on_enter(self):

        journalEntries = DataAccessAPI.getJournalContent()
        journalContent = ('\n\n'.join(journalEntries))
        journalContentField = JournalContentField
        journalContentField.text = journalContent
        closeButton = MenuButton(text=GameStrings.closetext)
        closeButton.size_hint_y=0.2
        closeButton.bind(on_press=partial(ScreenChanging.goToScreen,'gamescreen'))
        self.journalScreenLayout.add_widget(CustomLabel(text=GameStrings.journaltext,halign='center',valign='center',size_hint_y=0.2 ))
        self.journalScreenLayout.add_widget(ScrollableLabel(text=journalContent))
        self.journalScreenLayout.add_widget(closeButton)

    def on_leave(self, *args):
        self.journalScreenLayout.clear_widgets()
        pass

class JournalContentField(ScrollableLabel):
    pass