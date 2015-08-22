import numpy as np
class SoundBucket:
	
	def __init__(self, start, end, detailed = False):
		self.start = start
		self.end = end
		self._detailed = detailed
		self.freqTable = [] if detailed else None
		self.numSamples = 0
		self._reset()

	def _reset(self):
		self._muFreq = None
		self._muAmp = None
		self._flatFreq = None
		self._flatAmp = None
		self.maxAmp = None
		self.minAmp = None
		self.maxFreq = None
		self.minFreq = None
		
	def addDrop(self, freq, amp):
		self.numSamples += 1
		if self._detailed:
			self.freqTable.append((freq, amp))
			self._reset()
		else:
			self._updateBounds(freq, amp)
			
	def _updateBounds(self, freq, amp):
		if self.maxFreq is None:
			self.maxFreq = freq
		if self.minFreq is None:
			self.minFreq = freq
		if self.maxAmp is None:
			self.maxAmp = amp
		if self.minAmp is None:
			self.minAmp = amp
		
		if amp < self.minAmp:
			self.minAmp = amp
		elif amp > self.maxAmp:
			self.maxAmp = amp
		if freq < self.minFreq:
			self.minFreq = freq
		elif freq > self.maxFreq:
			self.maxFreq = freq
			
		if self.muFreq is None:
			self.muFreq = freq
		else:
			self.muFreq = (self.muFreq * (self.numSamples  - 1) + freq) / self.numSamples
		if self.muAmp is None:
			self.muAmp = amp
		else:
			self.muAmp = (self.muAmp * (self.numSamples  - 1) + amp) / self.numSamples
		
	@property
	def flatFreq(self):
		if not self._detailed:
			return None
		if self._flatFreq is None:
			self._flatFreq = [e[0] for e in self.freqTable]
		return self._flatFreq
		
	@property
	def flatAmp(self):
		if not self._detailed:
			return None
		if self._flatAmp is None:
			self._flatAmp = [e[1] for e in self.freqTable]
		return self._flatAmp
		
	@property
	def muFreq(self):
		if self._muFreq is None and self._detailed:
			self._muFreq = np.average(self.flatFreq)
		return self._muFreq
		
	@property
	def muAmp(self):
		if self._muAmp is None and self._detailed:
			self._muAmp = np.average(self.flatAmp)
		return self._muAmp