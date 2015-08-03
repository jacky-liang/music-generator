import wave
import numpy as np
from numpy.fft import rfft, irfft

SAMPLERATE=44100
BITWIDTH=8
CHANNELS=2

def gensine(freq, dur):
    t = np.linspace(0, dur, round(dur*SAMPLERATE))
    x = np.sin(2.0*np.pi*freq*t)
    if BITWIDTH==8:
        x = x+abs(min(x))
        x = np.array( np.round( (x/max(x)) * 255) , dtype=np.dtype('<u1'))
    else:
        x = np.array(np.round(x * ((2**(BITWIDTH-1))-1)), dtype=np.dtype('<i%d' % (BITWIDTH/8)))

    return np.repeat(x,CHANNELS).reshape((len(x),CHANNELS))

output_file="test.wav"

outfile = wave.open(output_file, mode='wb')
outfile.setparams((CHANNELS, BITWIDTH/8, SAMPLERATE, 0, 'NONE', 'not compressed'))

A = gensine(440, 2)
outfile.writeframes(A.tostring())
outfile.close()