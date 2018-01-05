from functools import partial

from menuinterface import BasicScreen
from menuinterface import StorylineLabel
from menuinterface import MenuButton
from dataaccessapi import DataAccessAPI



class InventoryScreen(BasicScreen):
    """Setup the screen for inventory."""

    def on_enter(self, *args):
        inventoryTitle = InventoryTitle(text='Inventory')
        inventoryClose = InventoryCloseButton(text = 'Close')
        self.inventoryLayout.add_widget(inventoryTitle)
        self.inventoryButtonGeneration(buttonNames=DataAccessAPI.getInventoryItems(),layout=self.inventoryLayout)
        self.inventoryLayout.add_widget(inventoryClose)


    def inventoryButtonGeneration(self,buttonNames, layout):
        if buttonNames == {}:
            noButtonsInfo = StorylineLabel()
            noButtonsInfo.text = "There is nothing in your inventory!"
            layout.add_widget(noButtonsInfo)
        for buttonName in buttonNames:
            buttonTitle = buttonName
            button = MenuButton()
            button.text = buttonTitle
            button.bind(on_press=partial(self.openInventoryItemPopup,))
            layout.add_widget(button)

    def openInventoryItemPopup(self):
        pass


class InventoryTitle(StorylineLabel):
    pass

class InventoryCloseButton(MenuButton):
    pass
