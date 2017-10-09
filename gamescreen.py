"""Create screen for the core gamplay."""
from functools import partial

from kivy.properties import ObjectProperty
from activereference import ActiveReference
from dataaccessapi import DataAccessAPI

from menuinterface import BasicScreen

class GameScreen(BasicScreen):
	"""Setup core gameplay screen. Details in kv file."""

	referenceTextLabel = ObjectProperty(None)

	def setStoryline(self,pageNo):
		"""Set the text displayed in gamescreen according to the current page ID.

		:param str pageNo: ID of the current page to be displayed on the core gamescreen
		"""

		self.referenceTextLabel.text = DataAccessAPI.getReferenceStorylineText(self,pageNo)

	def useReference(self, refName, **kwargs):
		"""Enable choosing of action for the chosen reference. Recognise clicked reference.

		Name of the clicked reference is passed from the on_ref_press callback: refName = args[1], set in kv file

		:param refName: name of the clicked reference from the markup text
		:type refName: string
		"""

		try:
			clickedReference = ActiveReference(refName)
		except:
			print('No reference in references dictionary.')
		else:
			useFlag = self.referenceTextLabel.flag
			print(refName, useFlag)
			possibleUses = {
				'ins': clickedReference.inspectReference,
				'int': clickedReference.interactWithReference,
				'inv': self.clickInventory,
				'inf': self.clickInterface
			}

			try:
				possibleUses.get(useFlag,partial(print,'No action selected'))()
			except:
				print("Lack of data for the chosen reference in references dictionary")
			finally:
				self.referenceTextLabel.flag= ""


	def clickInspect(self):
		"""Set the chosen action for reference to inspect."""

		self.referenceTextLabel.flag = 'ins'

	def clickInteract(self):
		"""Set the chosen action for reference to interact."""

		self.referenceTextLabel.flag = 'int'

	def clickInventory(self):
		"""Set the chosen action for reference to use inventory."""

		self.referenceTextLabel.flag = 'inv'

		print (self.referenceTextLabel.flag)
		
	def clickInterface(self):
		"""On button click open additional game interface with map, journal, etc..."""

		self.referenceTextLabel.flag = 'inf'
		print (self.referenceTextLabel.flag)
		print('Opening interface screen')	
		
		