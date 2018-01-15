"""Create screen for the core gamplay."""
from functools import partial

from activereference import ActiveReference
from dataaccessapi import DataAccessAPI
from menuinterface import BasicScreen



class GameScreen(BasicScreen):
	"""Setup core gameplay screen. Details in kv file."""

	def useReference(self, refName, **kwargs):
		"""Enable choosing of action for the chosen reference. Recognise clicked reference.

		Name of the clicked reference is passed from the on_ref_press callback: refName = args[1], set in kv file

		:param refName: name of the clicked reference from the markup text
		:type refName: string
		"""
		print('useReference',self,type(self))
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
				'inv': partial(clickedReference.useInventoryItemOnReference,refName),
				'inf': self.clickInterface
			}

			possibleUses.get(useFlag, partial(print, 'No action selected'))()
			self.referenceTextLabel.flag = ""
			'''
						try:
							possibleUses.get(useFlag,partial(print,'No action selected'))()
						except:
							print("Lack of data for the chosen reference in references dictionary",useFlag)
						finally:
							self.referenceTextLabel.flag= ""
			'''

	def clickInspect(self):
		"""Set the chosen action for reference to inspect."""

		self.referenceTextLabel.flag = 'ins'

	def clickInteract(self):
		"""Set the chosen action for reference to interact."""

		self.referenceTextLabel.flag = 'int'

	def clickInventory(self):
		"""Set the chosen action for reference to use inventory."""

		self.referenceTextLabel.flag = 'inv'


		
	def clickInterface(self):
		"""On button click open additional game interface with map, journal, etc..."""

		self.referenceTextLabel.flag = 'inf'
		print (self.referenceTextLabel.flag)
		print('Opening interface screen',type(self))
		




#	currentEmpathyValue = NumericProperty(0)
#	currentEmpathyValue = DataAccessAPI.getCurrentEmpathyValue()

