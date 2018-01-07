"""Classes for dealing with the active references from the markup text in game."""

from functools import partial
from menuinterface import MenuButton
from menuinterface import StorylineLabel
from menuinterface import ActionPopup
from dataaccessapi import DataAccessAPI




class ActiveReference:
	"""Provide methods for interacting with active references from the markup text in game."""

	def __init__(self,refName):
		"""Setup basic variables according to the name of chosen reference."""

		self.refName = refName
		self.activeReferenceName = DataAccessAPI.getReferenceName(self, refName)
		self.activeReferenceInteractions = DataAccessAPI.getReferenceInteractions(self, refName)

	def inspectReference(self):
		"""Open inspect popup for the chosen reference."""

		self.open_inspect_popup()
		
	def open_inspect_popup(self):
		"""Create inspect popup for the chosen reference."""

		inspectTitle = ''.join(('Inspecting ',self.activeReferenceName))
		insPop=InspectPopup(title=inspectTitle)
		insPop.referenceDescription.text = DataAccessAPI.getReferenceDescription(self, self.refName)
		insPop.open()	

	def interactWithReference(self):
		"""Open interact popup for the chosen reference."""

		self.open_interact_popup()

	def open_interact_popup(self):
		"""Create interact popup for the chosen reference with buttons according to the available interactions for the reference."""

		interactTitle = ''.join(('Interacting with ',self.activeReferenceName))
		intPop=InteractPopup(title=interactTitle)
		self.interactButtonsGeneration(intPop)
		closeButton = ActionPopup.closePopupButton(intPop)
		closeButton.size_hint_y = 0.3
		intPop.interactPopupLayout.add_widget(closeButton)
		intPop.open()

	def interactButtonsGeneration(self,intPop):
		"""Generate interaction buttons according to interactions available for the chosen reference.
		Display info if no interactions are available.
		"""

		interactions=self.activeReferenceInteractions.keys()
		if self.activeReferenceInteractions == {}:
			noInteractionInfo = StorylineLabel()
			noInteractionInfo.text="I can't do anything with that"
			intPop.interactPopupLayout.add_widget(noInteractionInfo)
		for interaction in interactions:
			interactButtonTitle = interaction
			interactButton = MenuButton()
			interactButton.text=interactButtonTitle
			interactButton.bind(on_press=partial(self.interactButtonFunction, interaction, self.activeReferenceName))
			intPop.interactPopupLayout.add_widget(interactButton)

	def interactButtonFunction(self,interaction,interactee,*args):
		"""Open popup for the chosen interaction with the info on the interaction's result.

		:param str interaction: interaction on the button
		:param str interactee: display name of the clicked reference, to be interacted with
		"""

		self.open_interact_result_popup(interaction,interactee)

	def open_interact_result_popup(self, interaction, interactee):
		"""Create popup with the info on the chosen interaction's result.

		:param str interaction: chosen interaction to perform
		:param str interactee: display name of the clicked reference, to be interacted with
		"""

		interactResultTitle = ' '.join((interaction,interactee))
		print(interaction)
		if interaction == 'Take':
			self.takeItem()
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

	def takeItem(self):
		DataAccessAPI.addItemToInventoryByReference(self.refName)



class InspectPopup(ActionPopup):
	"""Setup popup for inspecting a reference. Details in gamescreen.kv file."""

	pass

class InteractPopup(ActionPopup):
	"""Setup popup for interacting with a reference. Details in gamescreen.kv file."""

	pass

class InteractResultPopup(ActionPopup):
	"""Setup popup for displaying result of interacting with a reference. Details in gamescreen.kv file."""

	pass
	
