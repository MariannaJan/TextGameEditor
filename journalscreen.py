from functools import partial
from menuinterface import BasicScreen
from menuinterface import CustomLabel
from menuinterface import MenuButton
from menuinterface import ScreenChanging

class JournalScreen(BasicScreen):

    def on_enter(self):
        self.journalScreenLayout.add_widget(CustomLabel(text='Journal',halign='center',valign='center'))
        self.journalScreenLayout.add_widget(MenuButton(text = 'lol'))
        self.journalScreenLayout.add_widget(MenuButton(text='Close',on_press = partial(ScreenChanging.goToScreen,'gamescreen')))



    def on_leave(self, *args):
        self.journalScreenLayout.clear_widgets()
