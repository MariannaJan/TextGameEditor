from functools import partial
from menuinterface import MenuButton
from menuinterface import StorylineLabel
from menuinterface import ActionPopup
from dataaccess import DataAccess


class ActiveReference:

	def __init__(self,refName):
		self.activeObjectName = DataAccess.getActiveObjectName(self,refName)
		self.activeObjectDescription = DataAccess.getActiveObjectDescription(self,refName)
		self.activeObjectInteractions = DataAccess.getActiveObjectInteractions(self,refName)
		
	def inspectReference(self):
		self.open_inspect_popup()
		
	def open_inspect_popup(self):
		inspectTitle='Inspecting '+self.activeObjectName
		insPop=InspectPopup(title=inspectTitle)
		insPop.referenceDescription.text = self.activeObjectDescription
		insPop.open()	

	def interactWithReference(self):
		self.open_interact_popup()

	def open_interact_popup(self):
		interactTitle='Interacting with '+self.activeObjectName
		intPop=InteractPopup(title=interactTitle)
		self.interactButtonsGeneration(intPop)
		closeButton = ActionPopup.closePopupButton(self,intPop)
		closeButton.size_hint_y = 0.3
		intPop.interactPopupLayout.add_widget(closeButton)
		intPop.open()

	def interactButtonsGeneration(self,intPop):
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
		self.open_interact_result_popup(interaction,interactee)

	def open_interact_result_popup(self, interaction, interactee):
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
	pass

class InteractPopup(ActionPopup):
	pass

class InteractResultPopup(ActionPopup):
	pass
	
