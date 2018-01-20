from functools import partial

from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty

from menuinterface import BasicScreen
from menuinterface import CustomLabel
from menuinterface import StorylineLabel
from menuinterface import MenuButton
from menuinterface import ScreenChanging

from menuinterface import ScrollableLabel

class JournalScreen(BasicScreen):
    #journalContent =StringProperty

    def on_enter(self):


        journalEntries = ['first','second','third','dagdgadfgad','first','second','third','dagdgadfgad','first','second','third','dagdgadfgad','first','second','third','dagdgadfgad','first','second','third','dagdgadfgad','first','second','third','dagdgadfgad','first','second','third','dagdgadfgad','first','second','third','dagdgadfgad','end']
        journalContent = ('\n'.join(journalEntries))
        journalContentField = JournalContentField
        journalContentField.text = journalContent
        closeButton = MenuButton(text='Close')
        closeButton.size_hint_y=0.2
        closeButton.bind(on_press=partial(ScreenChanging.goToScreen,'gamescreen'))
        self.journalScreenLayout.add_widget(CustomLabel(text='Journal',halign='center',valign='center',size_hint_y=0.2 ))
        self.journalScreenLayout.add_widget(ScrollableLabel(text=journalContent))
        self.journalScreenLayout.add_widget(closeButton)

    def on_leave(self, *args):
        self.journalScreenLayout.clear_widgets()
        pass

class JournalContentField(ScrollableLabel):
    pass