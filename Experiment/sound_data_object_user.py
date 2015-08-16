from sound_data_object import SoundDataObject
from sound_syns import SoundSyns

sdo = SoundDataObject("test")
sdo.save()

newSdo = SoundDataObject.loadSdo("test")