from kivy.properties import ListProperty
from menuinterface import BasicScreen
from dataaccessapi import DataAccessAPI
from kivy.app import App
from customlistbuttons import StoriesButton



class ChooseStoryScreen(BasicScreen):

    stories = ListProperty([])

    def on_pre_enter(self,*args):
        self.stories = DataAccessAPI.getAvailableStoriesNames()

    def on_enter(self, *args):
        storyChooserView = App.get_running_app().root.children[0].children[0].ids['story_chooser_view'].adapter

        for i in range(storyChooserView.get_count()):
            storyChooserView.get_view(i).setStoryDatabase(DataAccessAPI.getStories()[i])


