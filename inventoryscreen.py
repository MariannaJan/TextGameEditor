from functools import partial

from menuinterface import BasicScreen
from menuinterface import StorylineLabel
from menuinterface import CustomLabel
from menuinterface import MenuButton
from dataaccessapi import DataAccessAPI
from menuinterface import ActionPopup

from kivy.uix.label import Label
from kivy.core.window import Window

class InventoryScreen(BasicScreen):
    """Setup the screen for inventory."""

    def on_enter(self, *args):
        """Dinamically generates the inventory screen."""

        inventoryTitle = InventoryTitle(text='Inventory')
        inventoryClose = InventoryCloseButton()
        self.inventoryLayout.add_widget(inventoryTitle)
        buttonNames = DataAccessAPI.getInventoryItems()
        if not buttonNames:
            noItemInfo = EmptyInventoryLabel()
            self.inventoryLayout.add_widget(noItemInfo)
        else:
            self.inventoryButtonGeneration(buttonNames,layout=self.inventoryLayout)
        self.inventoryLayout.add_widget(inventoryClose)

    def on_leave(self, *args):
        """Removes all widgets from yhe screen on leave."""

        self.inventoryLayout.clear_widgets()


    def inventoryButtonGeneration(self,buttonNames, layout):
        """Makes buttons with names of items in the inventory.

        :param buttonNames: Dictionary of inventory item names : their descriptions.
        :type buttonNames: dict [str,str]
        :param layout: Kivy layout to which the buttons are to be added.
        """
        for buttonName in buttonNames:
            print(buttonNames)
            buttonTitle = buttonName
            button = MenuButton()
            button.text = buttonTitle
            button.bind(on_press=partial(InventoryScreen.openInventoryItemPopup, buttonName, buttonNames[buttonName]))
            layout.add_widget(button)


    def openInventoryItemPopup(popupTitle,itemDescription,*args):
        """Generate and open the popup with info on the selected item from inventory

        :param popupTitle: The name of the item from inventory, for which the popup  is opened.
        :param itemDescription: The description of the item from inventory, for which the popup  is opened.
        """
        inventoryPop = InventoryItemPopup()
        inventoryPop.title = popupTitle
        closeButton = ActionPopup.closePopupButton(inventoryPop)
        closeButton.size_hint_y = 0.3
        inventoryPop.inventoryItemLayout.add_widget(StorylineLabel(text=itemDescription))
        inventoryPop.inventoryItemLayout.add_widget(closeButton)
        inventoryPop.open()


class InventoryTitle(CustomLabel):
    """Setup title label for the Inventory screen. Details in inventoryscreen.kv file"""
    pass

class EmptyInventoryLabel(CustomLabel):
    def __init__(self,**kwargs):
        """Set Colors, font and layout for the label (rest in kv file)."""
        super(EmptyInventoryLabel,self).__init__(**kwargs)
        self.font_size = Window.height *.06

    pass

class InventoryCloseButton(MenuButton):
    """Setup close button for the Inventory screen. Details in inventoryscreen.kv file"""
    pass

class InventoryItemPopup(ActionPopup):
    """Setup popup for individual item from inventory Details in inventoryscreen.kv file"""
    pass