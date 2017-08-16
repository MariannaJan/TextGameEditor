from kivy.properties import ObjectProperty
from activereference import ActiveReference
from dataaccess import DataAccess

from menuinterface import BasicScreen

class GameScreen(BasicScreen):

	storylinePageText = ObjectProperty(None)

	def setStoryline(self,pageNo):
		self.storylinePageText.text = DataAccess.getStorylinePageText(self,pageNo)
	
	def useReference(self, args):
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
		self.storylinePageText.flag = 'ins'
		print (self.storylinePageText.flag)
		
		
	def clickInteract(self):
		self.storylinePageText.flag = 'int'
		print (self.storylinePageText.flag)
		
	def clickInventory(self):
		self.storylinePageText.flag = 'inv'
		print (self.storylinePageText.flag)
		
	def clickInterface(self):
		self.storylinePageText.flag = 'inf'
		print (self.storylinePageText.flag)
		print('Opening interface screen')	
		
		