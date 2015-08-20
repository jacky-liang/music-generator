from scipy.io.wavfile import read, write
from scipy.fftpack import rfft, irfft
from math import log
import numpy as np
from sound_bucket import SoundBucket

class SoundDecomposer:
	music_input_folder = "/"
	bucket_size = 1.0/12
	bucket_min_start = 4
	bucket_max_end = 14
	magic = 2.0
	
	def __init__(self, name):
		self.name = name
		self._reset()
		
	def readFile(self, fileName):
		self._reset()
		path = SoundDecomposer.music_input_folder + fileName
		rate, signal = read(path)
		self.readSignal(rate, signal)
		
	def readSignal(self, rate, signal):
		self._reset()
		self.rate = rate
		if len(signal[0]) > 1:
			signal = [e[0] for e in signal]
		self.raw = signal
	
	@property
	def normalized(self):
		if self._normalized is None:
			mu = np.average(self.raw)
			sigma = np.std(self.raw)
			self._normalized = [(e - mu)/sigma for e in self.raw]
		return self._normalized
	
	def _reset(self):
		self.raw = None
		self.rate = None
		self._rawFreq = None
		self._logFreq = None
		self._freqBuckets = None
		self._normalized = None
		self._rawFreqTable = None
		
	@property
	def rawFreq(self):
		if self._rawFreq is None:
			self._rawFreq = rfft(self.normalized)[1:]
		return self._rawFreq
		
	@property
	def rawFreqMap(self):
		if self._rawFreqTable is None:
			self._rawFreqTable = np.fft.fftfreq(len(self.rawFreq), SoundDecomposer.magic/self.rate)
		return self._rawFreqTable
	
	@property
	def logFreqTable(self):
		if self._logFreq is None:
			self._logFreq = [(log(abs(self.rawFreqMap[i]), 2), self.rawFreq[i]) for i in range(2, len(self.rawFreq))]
		return self._logFreq
		
	@property
	def freqBuckets(self):
		if self._freqBuckets is None:
			self._freqBuckets = []
			self._bucketize(self.logFreqTable, self._freqBuckets)
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