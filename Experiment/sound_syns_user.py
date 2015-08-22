from sound_syns import SoundSyns

chordC = SoundSyns()
chordC.bitwidth = 32
chordC.add_key("C")
chordC.add_key("E")
chordC.add_key("G")
chordC.write("chordC.wav")

chordD = SoundSyns()
chordD.bitwidth = 32
chordD.add_key("D")
chordD.add_key("F")
chordD.add_key("A")
chordD.write("chordD.wav")