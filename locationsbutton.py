from menuinterface import CustomListItemButton
from menuinterface import ScreenChanging
from dataaccessapi import DataAccessAPI

class LocationsButton(CustomListItemButton):

    def on_press(self):
        pageNo = DataAccessAPI.getPlaces()[self.text]
        DataAccessAPI.setCurrentPageNo(pageNo)
        ScreenChanging.goToScreen('gamescreen')
