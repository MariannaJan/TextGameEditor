from menuinterface import BasicScreen
from kivy.properties import ListProperty
from menuinterface import CustomListItemButton
from dataaccessapi import DataAccessAPI

class AvailableLocationsScreen(BasicScreen):

    locations = ListProperty([])

    def on_pre_enter(self, *args):
        places = DataAccessAPI.getPlaces()
        self.locations = places.keys()




