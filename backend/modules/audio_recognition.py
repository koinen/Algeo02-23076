from .audio_processing import MidiProcessing
from .general_processing import GeneralProcessing
import numpy as np
import os
import pretty_midi


def openProcessedDatabaseMIDI():
    if not os.path.exists("../uploads/processed/project_dataset_midi.npy"):
        return None
    project_dataset = np.load("../uploads/processed/project_dataset_midi.npy")
    return project_dataset

def processQueryMIDI(midi_file_name):
    midi_data = pretty_midi.PrettyMIDI(f"../uploads/{midi_file_name}")
    window_feature_vectors, song_idx = MidiProcessing.makeMidi(midi_data, 0, 20, 4)
    return window_feature_vectors, song_idx

def queryMIDI(midi_file_name, mean, pca):
    project_query = processQueryMIDI(midi_file_name, mean, pca)
    project_dataset = np.load("../uploads/processed/project_dataset_midi.npy") ### dataset[i][j][k] = i-th song, j-th window, k-th feature
    closest = []
    for i in range(len(project_query)):
        for j in range(len(project_dataset)):
            for k in range(len(project_dataset[j])):
                distance = GeneralProcessing.cosineSimilarity(project_query[i], project_dataset[j][k])
                closest.append((distance, j, k))
    #check absolute window for now, might change to check song                
    top_5 = sorted(closest, key=lambda x: x[0])[:5]
    return top_5

    
