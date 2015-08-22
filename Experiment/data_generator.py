from sound_data_object import SoundDataObject
from sound_syns import SoundSyns
from sound_decomp import SoundDecomposer
from sample import Sample
from random import shuffle
#Generate an SDO that has an array of training sample object
#each traning sample contains its data in .data, and labels in .labels

class Generator:
	
	def __init__(self, duration = 2):
		self.duration = duration
		
	def generate(self, name, max_samples):
		labelCombos = Generator._getLabelCombinations()
		sdo = self._getSdo(max_samples, labelCombos)
		sdo.save()
		return sdo
		
	def _getSdo(self, name, max_samples, labelCombos):
		sdo = SoundDataObject(name)
		for i in range(min(max_samples, len(labelCombos))):
			#use sound syns to get label and signal
			labels = [label for label in labelCombos[i]]
			syns = SoundSyns()
			for key in labels:
				syns.add_key(key)
			#get buckets
			decomp = SoundDecomposer(name)
			decomp.readSignal(SoundSyns.rate, syns.signal)
			#add buckets to sdo
			sdo.addDataSingle(Sample(decomp.freqBuckets, labels))
		return sdo
		
	def generateSet(self, name, max_samples, training_percent, cv_percent, test_percent):
		if abs(training_percent + test_percent + cv_percent - 1) > 1e-5:
			raise ValueError("The input percents must add up to 1!")
		
		labelCombos = Generator._getLabelCombinations()
		shuffle(labelCombos)
		
		lastTrainingIndex = int(training_percent * len(labelCombos))
		lastCvIndex = int((training_percent + cv_percent) * len(labelCombos))
		
		labelsTraining = labelCombos[: lastTrainingIndex]
		labelsCv = labelCombos[lastTrainingIndex : lastCvIndex]
		labelsTest = labelCombos[lastCvIndex:]
		
		sdoTraining = self._getSdo(name + "_Training", int(max_samples * training_percent), labelsTraining)
		sdoCv = self._getSdo(name + "_CV", int(max_samples * cv_percent), labelsCv)
		sdoTest = self._getSdo(name + "_Test", int(max_samples * test_percent), labelsTest)
		
		sdoTraining.save()
		sdoCv.save()
		sdoTest.save()
		
		return sdoTraining, sdoCv, sdoTest
		
	@staticmethod
	def _getLabelCombinations():
		return Generator._getCombos(SoundSyns.key_mappings.keys())
		
	@staticmethod
	def _getCombos(items):
		items = [e for e in items]
		if len(items) <= 1:
			return [items]
		first, rest = items[0], items[1:]
		restCombos = Generator._getCombos(rest)
		return [[first]] + restCombos + [[first] + combo for combo in restCombos]
		
	@staticmethod
	def _getPerms(items):
		items = [e for e in items]
		if len(items) <= 1:
			return items
		first, rest = items[0], items[1:]
		restPerms = Generator._getPerms(rest)
		perms = []
		for i in range(len(restPerms)):
			cur_perm = restPerms[i]
			for j in range(len(cur_perm)):
				perms.append(cur_perm[:j] + first + cur_perm[j:])
		return perms
		
result = Generator().generateSet("keys", 20, 0.7, 0.15, 0.15)