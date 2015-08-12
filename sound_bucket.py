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
		self._flatFreq = None
		self._flatAmp = None
		
	def addDrop(self, freq, amp):
		self.freqTable.append((freq, amp))
		self._reset()
		
	@property
	def flatFreq(self):
		if self._flatFreq is None:
			self._flatFreq = [e[0] for e in self.freqTable]
		return self._flatFreq
		
	@property
	def flatAmp(self):
		if self._flatAmp is None:
			self._flatAmp = [e[1] for e in self.freqTable]
		return self._flatAmp
		
	@property
	def muFreq(self):
		if self._muFreq is None:
			self._muFreq = np.average(self.flatFreq)
		return self._muFreq
		
	@property
	def muAmp(self):
		if self._muAmp is None:
			self._muAmp = np.average(self.flatAmp)
		return self._muAmp