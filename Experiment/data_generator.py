from sound_data_object import SoundDataObject
from sound_syns import SoundSyns
from sound_decomp import SoundDecomposer
from sample import Sample
#Generate an SDO that has an array of training sample object
#each traning sample contains its data in .data, and labels in .labels

class Generator:
	
	def __init__(self, duration = 2):
		self.duration = duration
		
	def generate(self, name, max_samples):
		sdo = SoundDataObject(name)
		permLabels = Generator._getLabelPermutations()
		for i in range(min(max_samples, len(permLabels))):
			#use sound syns to get label and signal
			label = permLabels[i]
			syns = SoundSyns()
			for key in label:
				syns.add_key(key)
			#get buckets
			decomp = SoundDecomposer(name)
			decomp.readSignal(syns.signal)
			#add buckets to sdo
			sdo.addDataSingle(Sample(decomp.freqBuckets, label))
		sdo.save()
		return sdo
		
	@staticmethod
	def _getLabelPermutations():
		return Generator._getPerms(SoundSyns.key_mappings.keys())
		
	@staticmethod
	def _getPerms(items):
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
		
		
	
	
	