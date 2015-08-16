import pickle
class SoundDataObject:
	
	def __init__(self, name):
		self.name = name
		self.data = []
		
	def save(self):
		file = open(self.name + ".sdo", 'w')
		pickle.dump(self, file)
		file.close()
		
	#static method
	def loadSdo(name):
		file = open(self.name + ".sdo", 'r')
		obj = pickle.load(file)
		file.close()
		return obj
		
	def addDataSingle(self, one_data):
		self.data.append(one_data)
		
	def addDataBulk(self, many_data):
		self.data.extend(many_data)