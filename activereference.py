"""Classes for dealing with the active references from the markup text in game."""

from functools import partial
from random import *
from menuinterface import MenuButton
from menuinterface import StorylineLabel
from menuinterface import ActionPopup
from dataaccessapi import DataAccessAPI
from menuinterface import ScreenChanging
from kivy.app import App

from kivy.properties import StringProperty


class ActiveReference:
	"""Provide methods for interacting with active references from the markup text in game."""
	objectFormInventory = ''

	def __init__(self,refName):
		"""Setup basic variables according to the name of chosen reference."""

		self.refName = refName
		self.activeReferenceName = DataAccessAPI.getReferenceName(self, refName)
		self.activeReferenceInteractions = DataAccessAPI.getReferenceInteractions(self, refName)

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
			inspectTitle = ''.join(('Inspecting ',self.activeReferenceName))

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
			interactTitle = ''.join(('Interacting with ',self.activeReferenceName))
		except Exception as e:
			print(e)
			ActiveReference.open_no_interactions_popup(self)
		else:
			try:
				if self.activeReferenceInteractions == {}:
					ActiveReference.open_no_interactions_popup(self,title=interactTitle)
					print('no interactions')

				else:
					print(self.activeReferenceInteractions)
					intPop = InteractPopup(title=interactTitle)
					self.interactButtonsGeneration(intPop)
					closeButton = ActionPopup.closePopupButton(intPop)
					closeButton.size_hint_y = 0.3
					intPop.interactPopupLayout.add_widget(closeButton)
					intPop.open()
			except Exception as e:
				print(str(e))


	def interactButtonsGeneration(self,intPop):
		"""Generate interaction buttons according to interactions available for the chosen reference.
		Display info if no interactions are available.
		"""

		interactions=self.activeReferenceInteractions.keys()

		for interaction in interactions:
			interactButtonTitle = interaction
			interactButton = MenuButton()
			interactButton.text=interactButtonTitle
			interactButton.bind(on_press=partial(self.interactButtonFunction, interaction, self.activeReferenceName,intPop))
			intPop.interactPopupLayout.add_widget(interactButton)

	def interactButtonFunction(self,interaction,interactee,intPop,*args):
		"""Open popup for the chosen interaction with the info on the interaction's result.

		:param str interaction: interaction on the button
		:param str interactee: display name of the clicked reference, to be interacted with
		"""
		intPop = intPop
		self.open_interact_result_popup(interaction, interactee)
		if interaction == 'Take':
			self.takeItem()
		intPop.dismiss()


	def open_interact_result_popup(self, interaction, interactee):
		"""Create popup with the info on the chosen interaction's result.

		:param str interaction: chosen interaction to perform
		:param str interactee: display name of the clicked reference, to be interacted with
		"""

		interactResultTitle = ' '.join((interaction,interactee))
		interactionResultDescription=(self.activeReferenceInteractions[interaction])[4]
		intResPop=InteractResultPopup()
		intResPop.title =interactResultTitle
		interactionResultLabel=StorylineLabel()
		interactionResultLabel.text=interactionResultDescription
		intResPop.interactResultPopupLayout.add_widget(interactionResultLabel)
		closeButton=ActionPopup.closePopupButton(intResPop)
		closeButton.size_hint = (1,0.3)
		intResPop.interactResultPopupLayout.add_widget(closeButton)
		intResPop.open()
		self.switchCurrentPage(pageName=self.activeReferenceInteractions[interaction][0])

	def takeItem(self):

		DataAccessAPI.addItemToInventoryByReference(self.refName)
		DataAccessAPI.markReferenceAsTaken(self.refName)

	def switchCurrentPage(self,pageName):
		DataAccessAPI.setCurrentPageNo(pageName)
		refTextLabel = App.get_running_app().root.children[0].children[0].ids['reference_text_label']
		refTextLabel.changeCurrentPage()

	def useInventoryItemOnReference(self,refName):
		itemID = self.objectFormInventory
		itemFeatures = DataAccessAPI.getInfoOnItemUseInWorld(refName,itemID)[refName]
		useIntOnRefPopup = UseItemInWorldPopup()
		useIntOnRefPopupTitle = ' '.join(['Use',itemID,'on',refName])
		useIntOnRefPopup.title = useIntOnRefPopupTitle
		useEffectDescription = StorylineLabel()
		try:
			useEffectDescriptionText = itemFeatures[1]
		except Exception as e:
			print(e)
			ActiveReference.open_no_interactions_popup(self)
		else:
			useEffectDescription.text = useEffectDescriptionText
			closeButton = ActionPopup.closePopupButton(useIntOnRefPopup)
			closeButton.size_hint = (1, 0.3)
			useIntOnRefPopup.useInWorldLayout.add_widget(useEffectDescription)
			useIntOnRefPopup.useInWorldLayout.add_widget(closeButton)
			useIntOnRefPopup.open()
			self.switchCurrentPage(pageName=itemFeatures[6])
			removeFromInvenoryFlag = itemFeatures[10]
			if removeFromInvenoryFlag.lower() == 'true':
				DataAccessAPI.removeUsedItemFromInventory(self,itemID)




	def open_no_interactions_popup(self,title=''):
		noInterPop = NoInteractionsPopup(title = title)
		noInterPop.open()

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
		noInteractionsTexts = (['Nothing to do!',
								'I cannot do anything with that.',
								'I have no idea what to do with that...',
								'Really..?'])
		noInteractionsText = choice(noInteractionsTexts)
		return noInteractionsText


class ReferenceTextLabel(StorylineLabel):

	currentPage = StringProperty('')

	def changeCurrentPage(self):
		pageNo = DataAccessAPI.getCurrentPageNo()
		self.currentPage = DataAccessAPI.getReferenceStorylineText(self,pageNo)

	def on_currentPage(self,*args):
		print('page change')