from scipy.io.wavfile import read, write
from scipy.fftpack import rfft, irfft
import numpy as np

class SoundObject:
	music_input_folder = "music_test_files/"
	music_output_folder = "music_output_files/"
	rate_default = 44100

	def __init__(self, name):
		self.name = name
		self.raw = None
		self.rate = None
		self._reset()
		
	def read(self, fileName):
		path = SoundObject.music_input_folder + fileName
		self.rate, self.raw = read(path)
		self._reset()
		
	def _reset(self):
		self._rawFreq = None
		self._processedFreq = None
		self._processed = None
		self.multiplier = 1
		
	@property
	def rawFreq(self):
		if self._rawFreq is None:
			self._rawFreq = rfft(self.raw)
		return self._rawFreq
		
	@property
	def processedFreq(self):
		if self._processedFreq is None:
			self._processedFreq = self.rawFreq
		return self._processedFreq

	@property
	def processed(self):
		if self._processed is None:
			self._processed = irfft(self.processedFreq)
			self._processed = np.multiply(self._processed, self.multiplier)
		return self._processed		
		
	def write(self, fileName):
		path = SoundObject.music_output_folder + fileName
		write(path, self.rate, self.processed)
	
	