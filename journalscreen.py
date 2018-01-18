from functools import partial
from menuinterface import BasicScreen
from menuinterface import CustomLabel
from menuinterface import MenuButton
from menuinterface import ScreenChanging

class JournalScreen(BasicScreen):

    def on_enter(self):
        journalTitle=CustomLabel(text='Journal',halign='center',valign='center')
        journalTitle.size_hint_y=0.2
        self.journalScreenLayout.add_widget(journalTitle)
        journalEntries = ['first','second','third']
        journalContent = ('\n'.join(journalEntries))
        self.journalScreenLayout.add_widget(MenuButton(text = journalContent))
        closeButton = MenuButton(text='Close',on_press = partial(ScreenChanging.goToScreen,'gamescreen'))
        closeButton.size_hint_y=0.2
        self.journalScreenLayout.add_widget(closeButton)



    def on_leave(self, *args):
        self.journalScreenLayout.clear_widgets()
