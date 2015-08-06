import numpy as np
class SoundBucket:
	
	def __init__(self, start, end):
		self.start = start
		self.end = end
		self.freqTable = []
		self._reset()
		
	def _reset(self):
		self._muFreq = None
		self._muAmp = None
		
	def addDrop(self, freq, amp):
		self.freqTable.append((freq, amp))
		self._reset()
		
	@property
	def muFreq(self):
		if self._muFreq is None:
			self._muFreq = np.average([elem[0] for elem in self.freqTable])
		return self._muFreq
		
	@property
	def muAmp(self):
		if self._muAmp is None:
			self._muAmp = np.average([elem[1] for elem in self.freqTable])
		return self._muAmp