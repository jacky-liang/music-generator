import pickle
class SoundDataObject:
	
	def __init__(self, name):
		self.name = name
		self.data = []
		
	def save(self):
		file = open(SoundDataObject._getFileName(self.name), 'w')
		pickle.dump(self, file)
		file.close()
		
	@staticmethod
	def _getFileName(name):
		return name + ".sdo" if not name.endswith(".sdo") else name
		
	@staticmethod
	def loadSdo(name):
		file = open(SoundDataObject._getFileName(name), 'r')
		obj = pickle.load(file)
		file.close()
		return obj
		
	def addDataSingle(self, one_data):
		self.data.append(one_data)
		
	def addDataBulk(self, many_data):
		self.data.extend(many_data)