from sound_syns import SoundSyns

chord = SoundSyns()
chord.bitwidth = 32
chord.add_key("C")
chord.add_key("E")
chord.add_key("G")
chord.write("chord.wav")	