from scipy.io.wavfile import read, write
from scipy.fftpack import rfft, irfft
import numpy as np

music_input_folder = "music_test_files/"
music_output_folder = "music_output_files/"
rate_default = 44100

def load_music_file(fileName):
	path = music_input_folder + fileName
	return read(path)
	
def load_fft_from_file(fileName):
	rate, input = load_music_file(fileName)
	transformed = rfft(input)
	return rate, transformed

def write_fft_to_wav(fft, fileName, rate = rate_default):
	path = music_output_folder + fileName
	output = irfft(fft)
	write(path, rate, output)

rate, transformed = load_fft_from_file("440.wav")
write_fft_to_wav(transformed, "test.wav")
	