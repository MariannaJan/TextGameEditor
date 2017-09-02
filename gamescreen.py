"""Create screen for the core gamplay."""

from kivy.properties import ObjectProperty
from activereference import ActiveReference
from dataaccess import DataAccess

from menuinterface import BasicScreen

class GameScreen(BasicScreen):
	"""Setup core gameplay screen. Details in kv file.

	:var storylinePageText: ID of the page from database for the creation of the current game screen.
	:vartype storylinePageText: string
	"""

	storylinePageText = ObjectProperty(None)

	def setStoryline(self,pageNo):
		"""Set the thext displayed in gamescreen according to the current page ID.

		:param str pageNo: ID of the current page to be displayed on the core gamescreen
		"""

		self.storylinePageText.text = DataAccess.getStorylinePageText(self,pageNo)
	
	def useReference(self, args):
		"""Enable choosing of action for the chosen reference. Recognise clicked reference.

		:param args: name of the clicked reference from the markup text
		:type args: string
		"""
		useFlag=self.storylinePageText.flag
		referenceName= args[1]
		print(referenceName,useFlag)

		try:
			try:
				clickedReference = ActiveReference(referenceName)
			finally:

				if useFlag=='ins':
					clickedReference.inspectReference()

				elif useFlag=='int':
					clickedReference.interactWithReference()

				elif useFlag=='inv':
					print('Opening inventory for: ', referenceName)

				#elif useFlag=='inf':
					#print('Opening interface screen')

				else:
					print('No action selected')

				self.storylinePageText.flag= ""
		except:
			print('No reference in reference dictionary.')
	
	
	
	def clickInspect(self):
		"""Set the chosen action for reference to inspect."""

		self.storylinePageText.flag = 'ins'
		print (self.storylinePageText.flag)
		
		
	def clickInteract(self):
		"""Set the chosen action for reference to interact."""

		self.storylinePageText.flag = 'int'
		print (self.storylinePageText.flag)
		
	def clickInventory(self):
		"""Set the chosen action for reference to use inventory."""

		self.storylinePageText.flag = 'inv'
		print (self.storylinePageText.flag)
		
	def clickInterface(self):
		"""On button click open additional game interface with map, journal, etc..."""

		self.storylinePageText.flag = 'inf'
		print (self.storylinePageText.flag)
		print('Opening interface screen')	
		
		