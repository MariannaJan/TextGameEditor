from functools import partial

from menuinterface import BasicScreen
from menuinterface import StorylineLabel
from menuinterface import MenuButton
from dataaccessapi import DataAccessAPI
from menuinterface import ActionPopup



class InventoryScreen(BasicScreen):
    """Setup the screen for inventory."""

    def on_enter(self, *args):
        """
        Dinamically generates the inventory screen.

        Makes a list of buttons with nemes of items in the inventory.
        """

        inventoryTitle = InventoryTitle(text='Inventory')
        inventoryClose = InventoryCloseButton()
        self.inventoryLayout.add_widget(inventoryTitle)
        self.inventoryButtonGeneration(buttonNames=DataAccessAPI.getInventoryItems(),layout=self.inventoryLayout)
        self.inventoryLayout.add_widget(inventoryClose)

    def on_leave(self, *args):
        self.inventoryLayout.clear_widgets()


    def inventoryButtonGeneration(self,buttonNames, layout):
        if buttonNames == {}:
            noButtonsInfo = StorylineLabel()
            noButtonsInfo.text = "There is nothing in your inventory!"
            layout.add_widget(noButtonsInfo)
        for buttonName in buttonNames:
            buttonTitle = buttonName
            button = MenuButton()
            button.text = buttonTitle
            button.bind(on_press=partial(InventoryScreen.openInventoryItemPopup,buttonName,buttonNames[buttonName]))
            layout.add_widget(button)

    def openInventoryItemPopup(popupTitle,itemDescription,*args):
        inventoryPop = InventoryItemPopup()
        inventoryPop.title = popupTitle
        closeButton = ActionPopup.closePopupButton(inventoryPop)
        closeButton.size_hint_y = 0.3
        inventoryPop.inventoryItemLayout.add_widget(StorylineLabel(text=itemDescription))
        inventoryPop.inventoryItemLayout.add_widget(closeButton)
        inventoryPop.open()


class InventoryTitle(StorylineLabel):
    pass

class InventoryCloseButton(MenuButton):
    pass

class InventoryItemPopup(ActionPopup):
    pass