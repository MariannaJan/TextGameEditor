"""Classes for dealing with the active references from the markup text in game."""

from functools import partial
from menuinterface import MenuButton
from menuinterface import StorylineLabel
from menuinterface import ActionPopup
from dataaccess import DataAccess


class ActiveReference:
	"""Provide methods for interacting with active references from the markup text in game."""

	def __init__(self,refName):
		"""Retreive data from database according to the name of chosen reference."""

		self.activeObjectName = DataAccess.getActiveObjectName(self,refName)
		self.activeObjectDescription = DataAccess.getActiveObjectDescription(self,refName)
		self.activeObjectInteractions = DataAccess.getActiveObjectInteractions(self,refName)
		
	def inspectReference(self):
		"""Open inspect popup for the chosen reference."""

		self.open_inspect_popup()
		
	def open_inspect_popup(self):
		"""Create inspect popup for the chosen reference."""

		inspectTitle='Inspecting '+self.activeObjectName
		insPop=InspectPopup(title=inspectTitle)
		insPop.referenceDescription.text = self.activeObjectDescription
		insPop.open()	

	def interactWithReference(self):
		"""Open interact popup for the chosen reference."""

		self.open_interact_popup()

	def open_interact_popup(self):
		"""Create interact popup for the chosen reference with buttons according to the available interactions for the reference."""

		interactTitle='Interacting with '+self.activeObjectName
		intPop=InteractPopup(title=interactTitle)
		self.interactButtonsGeneration(intPop)
		closeButton = ActionPopup.closePopupButton(self,intPop)
		closeButton.size_hint_y = 0.3
		intPop.interactPopupLayout.add_widget(closeButton)
		intPop.open()

	def interactButtonsGeneration(self,intPop):
		"""Generate interaction buttons according to interactions available for the chosen reference.
		Display info if no onteractions are available.
		"""

		interactions=self.activeObjectInteractions.keys()
		if self.activeObjectInteractions == {}:
			noInteractionInfo = StorylineLabel()
			noInteractionInfo.text="I can't do anything with that"
			intPop.interactPopupLayout.add_widget(noInteractionInfo)
		for interaction in interactions:
			interactButtonTitle = interaction
			interactButton = MenuButton()
			interactButton.text=interactButtonTitle
			interactButton.bind(on_press=partial(self.interactButtonFunction,interaction,self.activeObjectName))
			intPop.interactPopupLayout.add_widget(interactButton)

	def interactButtonFunction(self,interaction,interactee,*args):
		"""Open popup for the chosen interaction with the info on the interaction's result."""

		self.open_interact_result_popup(interaction,interactee)

	def open_interact_result_popup(self, interaction, interactee):
		"""Create popup with the info on the chosen interaction's result."""
		interactResultTitle= interaction + ' ' + interactee
		interactionResultDescription=(self.activeObjectInteractions[interaction])[4]
		intResPop=InteractResultPopup()
		intResPop.title =interactResultTitle
		interactionResultLabel=StorylineLabel()
		interactionResultLabel.text=interactionResultDescription
		intResPop.interactResultPopupLayout.add_widget(interactionResultLabel)
		closeButton=ActionPopup.closePopupButton(self, intResPop)
		closeButton.size_hint = (1,0.3)
		intResPop.interactResultPopupLayout.add_widget(closeButton)
		intResPop.open()


class InspectPopup(ActionPopup):
	"""Setup popup for inspecting a reference. Details in gamescreen.kv file."""

	pass

class InteractPopup(ActionPopup):
	"""Setup popup for interacting with a reference. Details in gamescreen.kv file."""

	pass

class InteractResultPopup(ActionPopup):
	"""Setup popup for displaying result of interacting with a reference. Details in gamescreen.kv file."""

	pass
	
