import wave
import numpy as np
from numpy.fft import rfft, irfft

class SoundSyns:

	key_mappings = {
		"B" : 246.9,
		"C" : 261.6,
		"D" : 293.7,
		"E" : 329.6,
		"F" : 349.2,
		"G" : 392,
		"A" : 440,
		"B2" : 493.9,
		"C2" : 523.3
		"D2" : 587.3
	}

	duration = 2 #seconds
	output_path = ""
	amplitutde_threshold = 0.95
	
	rate = 44100
	bitwidth = 8
	channels = 1
		
	def __init__(self):
		self.freqs = []
		self.duration = SoundSyns.duration
		self.output_path = SoundSyns.output_path
		self.amplitutde_threshold = SoundSyns.amplitutde_threshold
		self.rate = SoundSyns.rate
		self.bitwidth = SoundSyns.bitwidth
		self.channels = SoundSyns.channels
		self._dtype = None
		self._signal = None

	def add_key(self, key_name):
		if key_name in SoundSyns.key_mappings:
			self.freqs.append(SoundSyns.key_mappings[key_name])
		else:
			print "Invalid Key Name!"
			
	def add_freq(self, freq):
		self.freqs.append(freq)

	@property
	def dtype(self):
		if self._dtype is None:
			self._dtype = np.dtype('<u1') if self.bitwidth == 8 else np.dtype('<i%d' % (self.bitwidth/8))
		return self._dtype
		
	def _gen_sine(self, freq):
		t = np.linspace(0, self.duration, round(self.duration*self.rate))
		x = np.sin(2.0*np.pi*freq*t)
		if self.bitwidth==8:
			x = x+abs(min(x))
			x = np.array(np.round((x/max(x)) * 255) , dtype=self.dtype)
		else:
			x = np.array(np.round(x*((2**(self.bitwidth-1))-1)), dtype=self.dtype)
		return np.repeat(x,self.channels).reshape((len(x),self.channels))
		
	@property
	def signal(self):
		if self._signal is None and len(self.freqs) > 0:
			self._signal = self._gen_sine(self.freqs[0])
			if len(self.freqs) > 1:
				for i in range(1, len(self.freqs)):
					self._signal  = self._superpose(self._signal, self._gen_sine(self.freqs[i]), i + 1)
		return self._signal
		
	def _superpose(self, base, top, height):
		top /= height
		base = base / height * (height - 1)
		return base + top
		
	def _clean(self, signal):
		gap = 1 - self.amplitutde_threshold
		return signal
		
	def write(self, file_name, output_path = output_path):
		output_file = output_path + file_name
		outfile = wave.open(output_file, mode='wb')
		outfile.setparams((self.channels, self.bitwidth/8, self.rate, 0, 'NONE', 'not compressed'))
		outfile.writeframes(self._clean(self.signal).tostring())
		outfile.close()