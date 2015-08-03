from sound_object import SoundObject
import numpy as np

test440 = SoundObject("440")
test440.	read("440.wav")
test440.multiplier = 0.1
test440.write("test440.wav")