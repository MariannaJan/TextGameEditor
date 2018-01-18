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
from gamescreen import GameScreen



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
        useInInventoryButton.bind(on_press = partial(InventoryScreen.useInInventory,itemID = itemDescription[1],popupToClose = inventoryPop))
        closeButton = ActionPopup.closePopupButton(inventoryPop)
        closeButton.size_hint_y = 0.2
        inventoryPop.inventoryItemLayout.add_widget(StorylineLabel(text=itemDescription[0]))
        inventoryPop.inventoryItemLayout.add_widget(useInWorldButton)
        inventoryPop.inventoryItemLayout.add_widget(useInInventoryButton)
        inventoryPop.inventoryItemLayout.add_widget(closeButton)
        inventoryPop.open()

    def useInWorld(self,itemID,popupToClose):
        ActiveReference.objectFromInventory = itemID
        print('useInWEorld',itemID)
        App.get_running_app().root.children[0].current = 'gamescreen'
        currentPopup = popupToClose
        currentPopup.dismiss()

    def useInInventory(self,itemID,popupToClose):
        currentPopup = popupToClose
        currentPopup.dismiss()
        useItemOnItemPopup = UseItemOnItemPopup(title = itemID)

        usableItems = {k:v for (k,v) in DataAccessAPI.getInventoryItems().items() if v[1]!= itemID}
        if not usableItems:
            useItemOnItemPopup.useItemOnItemLayout.add_widget(EmptyInventoryLabel(text='No other object in the inventory.'))
        else:
            for usableItem in usableItems:
                itemButton = MenuButton()
                itemButton.text = usableItem
                itemButton.bind(on_press=partial(InventoryScreen.useItemOnItem,itemID = itemID,targetItemID=usableItems[usableItem][1],popupToClose=useItemOnItemPopup))
                useItemOnItemPopup.useItemOnItemLayout.add_widget(itemButton)
        closeButton = ActionPopup.closePopupButton(useItemOnItemPopup)
        closeButton.size_hint_y = 0.2
        useItemOnItemPopup.useItemOnItemLayout.add_widget(closeButton)
        useItemOnItemPopup.open()

    def useItemOnItem(self,itemID,targetItemID,popupToClose):
        currentPopup = popupToClose
        currentPopup.dismiss()
        try:
            infoOnItemUse = DataAccessAPI.getInfoOnItemUseOnItem(itemID,targetItemID)
            resultDescription = infoOnItemUse[3]
        except Exception as e:
            print(e)
            ActiveReference.open_no_interactions_popup()
        else:

            useItemOnItemResultPopup = UseItemOnItemResultPopup()
            useItemOnItemResultPopup.title = ' '.join(['Use', itemID, 'on', targetItemID])
            closeButton = ActionPopup.closePopupButton(useItemOnItemResultPopup)
            closeButton.size_hint_y = 0.2
            useItemOnItemResultPopup.useItemOnItemResultLayout.add_widget(StorylineLabel(text=resultDescription))
            useItemOnItemResultPopup.useItemOnItemResultLayout.add_widget(closeButton)
            useItemOnItemResultPopup.open()
            createdItem = infoOnItemUse[2]
            InventoryScreen.inventoryItemsUpdate(createdItem,itemID,targetItemID)

    @classmethod
    def inventoryItemsUpdate(cls,createdItem,itemID,targetItemID):
        DataAccessAPI.putItemInInventory(createdItem)
        DataAccessAPI.removeUsedItemFromInventory(itemID)
        DataAccessAPI.removeUsedItemFromInventory(targetItemID)
        App.get_running_app().root.children[0].current_screen.on_leave()
        App.get_running_app().root.children[0].current_screen.on_enter()

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

class UseItemOnItemPopup(ActionPopup):
    pass

class UseItemOnItemResultPopup(ActionPopup):
    pass


