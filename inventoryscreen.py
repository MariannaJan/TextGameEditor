from functools import partial

from kivy.core.window import Window
from kivy.app import App

from menuinterface import BasicScreen
from menuinterface import StorylineLabel
from menuinterface import CustomLabel
from menuinterface import MenuButton
from dataaccessapi import DataAccessAPI
from menuinterface import ActionPopup
from menuinterface import ScreenChanging
from activereference import ActiveReference



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
            button = InventoryItemButton(font_size=10)
            button.text = buttonTitle
            button.bind(on_press=partial(InventoryScreen.openInventoryItemPopup, popupTitle=buttonName, itemDescription=buttonNames[buttonName]))
            layout.add_widget(button)



    def openInventoryItemPopup(self,popupTitle,itemDescription,*args):
        """Generate and open the popup with info on the selected item from inventory

        :param popupTitle: The name of the item from inventory, for which the popup  is opened.
        :param itemDescription: The description of the item from inventory, for which the popup  is opened.
        """
        inventoryPop = InventoryItemPopup()
        inventoryPop.title = popupTitle
        useInWorldButton = InventoryItemPopupButton()
        useInWorldButton.text='Use on item in world'
        useInWorldButton.bind(on_press = partial(InventoryScreen.useInWorld,itemID=itemDescription[1],popupToClose = inventoryPop))
        useInInventoryButton = InventoryItemPopupButton()
        useInInventoryButton.text = 'Use on item in inventory'
        closeButton = ActionPopup.closePopupButton(inventoryPop)
        closeButton.size_hint_y = 0.2
        inventoryPop.inventoryItemLayout.add_widget(StorylineLabel(text=itemDescription[0]))
        inventoryPop.inventoryItemLayout.add_widget(useInWorldButton)
        inventoryPop.inventoryItemLayout.add_widget(useInInventoryButton)
        inventoryPop.inventoryItemLayout.add_widget(closeButton)
        inventoryPop.open()

    def useInWorld(self,itemID,popupToClose):
        ActiveReference.objectFormInventory = itemID
        App.get_running_app().root.children[0].current = 'gamescreen'
        currentPopup = popupToClose
        currentPopup.dismiss()


class InventoryTitle(CustomLabel):
    """Setup title label for the Inventory screen. Details in inventoryscreen.kv file"""
    pass

class EmptyInventoryLabel(CustomLabel):
    def __init__(self,**kwargs):
        """Set Colors, font and layout for the label (rest in kv file)."""
        super(EmptyInventoryLabel,self).__init__(**kwargs)
        self.font_size = Window.height *.06


class InventoryCloseButton(MenuButton):
    """Setup close button for the Inventory screen. Details in inventoryscreen.kv file"""
    pass

class InventoryItemButton(MenuButton):

    def __init__(self,**kwargs):

        super(InventoryItemButton,self).__init__()
        self.font_size = 0.9*self.font_size



class InventoryItemPopup(ActionPopup):
    """Setup popup for individual item from inventory Details in inventoryscreen.kv file"""
    pass

class InventoryItemPopupButton(MenuButton):
    def __init__(self,**kwargs):
        super(InventoryItemPopupButton,self).__init__()
        self.font_size = self.font_size*0.5




