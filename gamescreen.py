"""Create screen for the core gamplay."""
from functools import partial

from kivy.properties import ObjectProperty
from activereference import ActiveReference
from dataaccess import DataAccess

from menuinterface import BasicScreen

class GameScreen(BasicScreen):
	"""Setup core gameplay screen. Details in kv file.

	:var storylinePageText: ID of the page from database for the creation of the current game screen.
	:vartype storylinePageText: string
	"""

	referenceTextLabel = ObjectProperty(None)

	def setStoryline(self,pageNo):
		"""Set the text displayed in gamescreen according to the current page ID.

		:param str pageNo: ID of the current page to be displayed on the core gamescreen
		"""

		self.referenceTextLabel.text = DataAccess.getStorylinePageText(self, pageNo)

	def useReference(self, referenceName, **kwargs):
		"""Enable choosing of action for the chosen reference. Recognise clicked reference.

		Name of the clicked reference is passed from the on_ref_press callback: referenceName = args[1], set in kv file

		:param referenceName: name of the clicked reference from the markup text
		:type referenceName: string
		"""

		try:
			try:
				clickedReference = ActiveReference(referenceName)
			finally:

				useFlag = self.referenceTextLabel.flag
				print(referenceName, useFlag)
				possibleUses = {
					'ins': clickedReference.inspectReference,
					'int': clickedReference.interactWithReference,
					'inv': self.clickInterface,
					'inf': self.clickInterface
				}

				possibleUses.get(useFlag,partial(print,'No action selected'))()

				self.referenceTextLabel.flag= ""
		except:
			print('No reference in reference dictionary.')

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
		
		