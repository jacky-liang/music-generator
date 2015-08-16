from scipy.io.wavfile import read, write
from scipy.fftpack import rfft, irfft
from math import log
import numpy as np
from sound_bucket import SoundBucket

class SoundDecomposer:
	music_input_folder = "music_input_files/"
	bucket_size = 1.0/12
	bucket_min_start = 4
	bucket_max_end = 14
	
	def __init__(self, name):
		self.name = name
		self.raw = None
		self.rate = None
		self._reset()
		
	def readFile(self, fileName):
		path = SoundDecomposer.music_input_folder + fileName
		self.rate, self.raw = read(path)
		if len(self.raw[0]) > 1:
			self.raw = [e[0] for e in self.raw]
		self._reset()
		
	def readSignal(self, signal):
		self.raw =signal
		self._reset()
	
	@property
	def normalized(self):
		if self._normalized is None:
			mu = np.average(self.raw)
			sigma = np.std(self.raw)
			self._normalized = [(e - mu)/sigma for e in self.raw]
		return self._normalized
	
	def _reset(self):
		self._rawFreq = None
		self._logFreq = None
		self._freqBuckets = None
		self._normalized = None
		
	@property
	def rawFreq(self):
		if self._rawFreq is None:
			self._rawFreq = rfft(self.normalized)
		return self._rawFreq

	@property
	def logFreq(self):
		if self._logFreq is None:
			self._logFreq = []
			for i in range(2, len(self.rawFreq)):
				self._logFreq.append((log(i, 2), self.rawFreq[i]))
		return self._logFreq
		
	@property
	def freqBuckets(self):
		if self._freqBuckets is None:
			self._freqBuckets = []
			self._bucketize(self.logFreq, self._freqBuckets)
		return self._freqBuckets

	def _bucketize(self, logFreq, buckets):
		cur_start = SoundDecomposer.bucket_min_start
		cur_end = cur_start + SoundDecomposer.bucket_size
		cur_bucket = 0
		buckets.append(SoundBucket(cur_start, cur_end))
		for i in range(len(logFreq)):
			freq = logFreq[i][0]
			amp = logFreq[i][1]
			if freq > SoundDecomposer.bucket_max_end:
				break
			if freq < cur_start:
				continue
			if freq > cur_end:
				cur_start = cur_end
				cur_end += SoundDecomposer.bucket_size
				buckets.append(SoundBucket(cur_start, cur_end))
				cur_bucket += 1
			buckets[cur_bucket].addDrop(freq, amp)