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
		
	def read(self, fileName):
		path = SoundDecomposer.music_input_folder + fileName
		self.rate, self.raw = read(path)
		self._reset()
		
	def _reset(self):
		self._rawFreq = None
		self._logFreq = None
		self._freqBuckets = None
		
	@property
	def rawFreq(self):
		if self._rawFreq is None:
			self._rawFreq = rfft(self.raw)
		return self._rawFreq

	@property
	def logFreq(self):
		if self._logFreq is None:
			self._logFreq = {"left":[], "right":[]}
			#assumes input has 2 channels.
			for i in range(2, len(self.rawFreq)):
				self._logFreq["left"].append((log(i, 2), self.rawFreq[i][0]))
				self._logFreq["right"].append((log(i, 2), self.rawFreq[i][1]))
		return self._logFreq
		
	@property
	def freqBuckets(self):
		if self._freqBuckets is None:
			self._freqBuckets = {"left":[], "right":[]}
			self._bucketize(self.logFreq["left"], self._freqBuckets["left"])
			self._bucketize(self.logFreq["right"], self._freqBuckets["right"])			
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