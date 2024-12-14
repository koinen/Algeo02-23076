from audio_processing import MidiProcessing
from audio_recognition import openProcessedDatabaseMIDI, processQueryMIDI, queryMIDI
from general_processing import GeneralProcessing
import numpy as np
import pretty_midi

if __name__ == "__main__":
    midi = np.load("../uploads/dataset/audio_data.npy", allow_pickle=True)
    query_midi = pretty_midi.PrettyMIDI("../uploads/FF3_Battle_(Piano).mid")
    # ff3 = midi[24][0]
    # final = processQueryMIDI("FF3_Battle_(Piano).mid")
    # ff3s = final[0]
    index = queryMIDI("FF3_Battle_(Piano).mid")
    print(index)