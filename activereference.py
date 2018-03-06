"""Classes for dealing with the active references from the markup text in game."""

from functools import partial
from random import *

from gamestrings import GameStrings
from menuinterface import MenuButton
from menuinterface import StorylineLabel
from menuinterface import ActionPopup
from dataaccessapi import DataAccessAPI
from menuinterface import ScreenChanging
from kivy.app import App

from kivy.properties import StringProperty


class ActiveReference:
    """Provide methods for interacting with active references from the markup text in game."""
    objectFromInventory = ''

    def __init__(self, refName):
        """Setup basic variables according to the name of chosen reference."""

        self.refName = refName
        self.activeReferenceName = DataAccessAPI.getReferenceName(self, refName)
        self.activeReferenceInteractions = DataAccessAPI.getAvailableInteractions(refName=self.refName,interactions=DataAccessAPI.getReferenceInteractions(self, refName))

    def inspectReference(self):
        """Open inspect popup for the chosen reference."""

        if DataAccessAPI.checkIfReferenceTaken(self.refName):
            referenceTakenPop = RefernceTakenPopup()
            referenceTakenPop.open()
        else:
            self.open_inspect_popup()

    def open_inspect_popup(self):
        """Create inspect popup for the chosen reference."""
        try:
            inspectTitle = ''.join((GameStrings.inspectingtext, self.activeReferenceName))

        except Exception as e:
            print(e)
        else:
            insPop = InspectPopup(title=inspectTitle)
            try:
                insPop.referenceDescription.text = DataAccessAPI.getReferenceDescription(self, self.refName)
                insPop.open()
            except Exception as e:
                print(e)

    def interactWithReference(self):
        """Open interact popup for the chosen reference."""
        if DataAccessAPI.checkIfReferenceTaken(self.refName):
            referenceTakenPop = RefernceTakenPopup()
            referenceTakenPop.open()
        else:
            self.open_interact_popup()


    def open_interact_popup(self):
        """Create interact popup for the chosen reference with buttons according to the available interactions for the reference."""

        try:
            interactTitle = ''.join((GameStrings.interactingwithtext,self.activeReferenceName))
        except Exception as e:
            print(e)
            ActiveReference.open_no_interactions_popup()
        else:
            try:
                #if DataAccessAPI.getAvailableInteractions(refName=self.refName,interactions=self.activeReferenceInteractions) == {}:
                if self.activeReferenceInteractions == {}:
                    ActiveReference.open_no_interactions_popup(title=interactTitle)

                else:
                    intPop = InteractPopup(title=interactTitle)
                    self.interactButtonsGeneration(intPop)
                    closeButton = ActionPopup.closePopupButton(intPop)
                    closeButton.size_hint_y = 0.3
                    intPop.interactPopupLayout.add_widget(closeButton)
                    intPop.open()
            except Exception as e:
                print(str(e))

    def interactButtonsGeneration(self, intPop):
        """Generate interaction buttons according to interactions available for the chosen reference.
                Display info if no interactions are available.
                """

        interactions = self.activeReferenceInteractions
        for interaction in interactions.keys():
            interactButtonTitle = interaction
            interactButton = MenuButton()
            interactButton.text = interactButtonTitle
            interactButton.bind(on_press=partial(self.interactButtonFunction, interaction, self.activeReferenceName, intPop))
            if DataAccessAPI.checkIfDisabled(empathyTreshold=interactions[interaction]['empathyTreshold'],sanityTreshold=interactions[interaction]['sanityTreshold']):
                interactButton.disabled = True
            intPop.interactPopupLayout.add_widget(interactButton)

    def interactButtonFunction(self,interaction,interactee,intPop,*args):
        """Open popup for the chosen interaction with the info on the interaction's result.

        :param str interaction: interaction on the button
        :param str interactee: display name of the clicked reference, to be interacted with
        """
        intPop = intPop
        self.open_interact_result_popup(interaction, interactee)
        takenItem = self.activeReferenceInteractions[interaction]['takeItemID']
        if takenItem !=[]:
            self.takeItem(takenItemIDs=takenItem)
        intPop.dismiss()


    def open_interact_result_popup(self, interaction, interactee):
        """Create popup with the info on the chosen interaction's result.

        :param str interaction: chosen interaction to perform
        :param str interactee: display name of the clicked reference, to be interacted with
        """

        interactResultTitle = ' '.join((interaction,interactee))
        interactionResultDescription=(self.activeReferenceInteractions[interaction])['interactionDescription']
        intResPop=InteractResultPopup()
        intResPop.title =interactResultTitle
        interactionResultLabel=StorylineLabel()
        interactionResultLabel.text=interactionResultDescription
        intResPop.interactResultPopupLayout.add_widget(interactionResultLabel)
        closeButton=ActionPopup.closePopupButton(intResPop)
        closeButton.size_hint = (1,0.3)
        intResPop.interactResultPopupLayout.add_widget(closeButton)
        intResPop.open()
        ActiveReference.activateInteractionEffects(interactionInfo=self.activeReferenceInteractions[interaction],refName=self.refName,interactionName=interaction)

    @classmethod
    def removeLockedPages(cls,lockedPages):
        if lockedPages is not None:
            lockedPages = lockedPages.split(',')
            for page in lockedPages:
                DataAccessAPI.removePlace(page)

    def takeItem(self,takenItemIDs):
        for takenItemID in takenItemIDs:
            DataAccessAPI.putItemInInventory(takenItemID)
        DataAccessAPI.markReferenceAsTaken(self.refName)

    @classmethod
    def receiveItem(cls,takenItemIDs):
        if takenItemIDs !=[]:
            for takenItemID in takenItemIDs:
                DataAccessAPI.putItemInInventory(takenItemID)

    @classmethod
    def switchCurrentPage(cls,pageName):
        DataAccessAPI.setCurrentPageNo(pageName)
        refTextLabel = App.get_running_app().root.children[0].children[0].ids['reference_text_label']
        refTextLabel.changeCurrentPage()

    def useInventoryItemOnReference(self,refName):
        itemID = self.objectFromInventory
        try:
            itemFeatures = DataAccessAPI.getInfoOnItemUseInWorld(refName,itemID)[itemID]
            useEffectDescriptionText = itemFeatures['effectDescription']
        except Exception as e:
            print(str(e))
            ActiveReference.open_no_interactions_popup()
        else:
            if DataAccessAPI.checkIfDisabled(empathyTreshold=itemFeatures['empathyTreshold'],sanityTreshold=itemFeatures['sanityTreshold']):
                ActiveReference.open_no_interactions_popup()
            else:
                useIntOnRefPopup = UseItemInWorldPopup()
                useIntOnRefPopupTitle = GameStrings.useontext.format(itemID, refName)
                useIntOnRefPopup.title = useIntOnRefPopupTitle
                useEffectDescription = StorylineLabel()
                useEffectDescription.text = useEffectDescriptionText
                closeButton = ActionPopup.closePopupButton(useIntOnRefPopup)
                closeButton.size_hint = (1, 0.3)
                useIntOnRefPopup.useInWorldLayout.add_widget(useEffectDescription)
                useIntOnRefPopup.useInWorldLayout.add_widget(closeButton)
                useIntOnRefPopup.open()
                ActiveReference.activateInteractionEffects(interactionInfo=itemFeatures)
                ActiveReference.receiveItem(takenItemIDs=itemFeatures['takeItemID'])

    @classmethod
    def open_no_interactions_popup(cls,title=''):
        noInterPop = NoInteractionsPopup(title = title)
        noInterPop.open()

    @classmethod
    def adjustBars(cls,refName='',interaction='',interactionName=''):
        if DataAccessAPI.checkIfFirstUse(refName=refName,interaction=interaction):
            ActiveReference.adjustEmpathy(interaction['empathyValue'])
            ActiveReference.adjustSanity(interaction['sanityValue'])
            DataAccessAPI.markInteractionAsUsed(refName, interactionName)

    @classmethod
    def adjustEmpathy(cls,emapthyValue):
        DataAccessAPI.setCurrentEmpathyValue(emapthyValue)
        app = App.get_running_app()
        empathyBar = app.root.children[0].current_screen.empathyBar
        empathyBar.empathyValue = DataAccessAPI.getCurrentEmpathyValue()

    @classmethod
    def adjustSanity(cls,sanityValue):
        DataAccessAPI.setCurrentSanityValue(sanityValue)
        app = App.get_running_app()
        sanityBar = app.root.children[0].current_screen.sanityBar
        sanityBar.sanityValue = DataAccessAPI.getCurrentSanityValue()

    @classmethod
    def activateInteractionEffects(cls,interactionInfo,refName='',interactionName=''):
        ActiveReference.switchCurrentPage(pageName=interactionInfo['pageNo'])
        ActiveReference.adjustBars(refName=refName, interaction=interactionInfo, interactionName=interactionName)
        if interactionInfo['optionalJournalEntry'] is not None:
            DataAccessAPI.addJournalEntry(interactionInfo['optionalJournalEntry'])
        lockedPages = interactionInfo['pagesLocked']
        ActiveReference.removeLockedPages(lockedPages)
        if interactionInfo['RemoveItemId'] != []:
            for itemID in interactionInfo['RemoveItemId']:
                DataAccessAPI.removeUsedItemFromInventory(itemID)
                print(itemID)
        if interactionInfo['PurgeInventoryFlag']:
            DataAccessAPI.clearInventory()
        try:
            if interactionInfo['OneTimeInteractionFlag']:
                DataAccessAPI.removeFromAvailableInteractions(refName, interactionName)
        except Exception as e:
            print(e)

class InspectPopup(ActionPopup):
    """Setup popup for inspecting a reference. Details in gamescreen.kv file."""

    pass

class InteractPopup(ActionPopup):
    """Setup popup for interacting with a reference. Details in gamescreen.kv file."""

    pass

class InteractResultPopup(ActionPopup):
    """Setup popup for displaying result of interacting with a reference. Details in gamescreen.kv file."""

    pass

class RefernceTakenPopup(ActionPopup):

    @staticmethod
    def goToInventory():
        App.get_running_app().root.children[0].current_screen.clickInventory()
        ScreenChanging.goToScreen('inventoryscreen')


class UseItemInWorldPopup(ActionPopup):
    pass

class NoInteractionsPopup(ActionPopup):

    def randomNoInteractionsInfo(self):
        noInteractionsTexts = GameStrings.nointeractionstext
        noInteractionsText = choice(noInteractionsTexts)
        return noInteractionsText


class ReferenceTextLabel(StorylineLabel):

    currentPage = StringProperty('')

    def changeCurrentPage(self):
        pageNo = DataAccessAPI.getCurrentPageNo()
        self.currentPage = DataAccessAPI.getReferenceStorylineText(self,pageNo)

    def on_currentPage(self,*args):

        pageNo = DataAccessAPI.getCurrentPageNo()
        journalEntry = DataAccessAPI.getPageJournalEntry(pageNo)
        if journalEntry is not None:
            DataAccessAPI.addJournalEntry(journalEntry)

        DataAccessAPI.addPlace(pageNo)

