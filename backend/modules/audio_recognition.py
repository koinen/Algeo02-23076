from audio_processing import MidiProcessing
from general_processing import GeneralProcessing
import numpy as np
import os
import pretty_midi


def openProcessedDatabaseMIDI():
    if not os.path.exists("../uploads/processed/project_dataset_midi.npy"):
        return None
    project_dataset = np.load("../uploads/processed/project_dataset_midi.npy")
    return project_dataset

def processQueryMIDI(midi_file_name):
    window_feature_vectors = MidiProcessing.processMidi(f"../uploads/{midi_file_name}")
    return window_feature_vectors

def queryMIDI(midi_file_name):
    project_query = processQueryMIDI(midi_file_name)
    # project_dataset = np.load("../uploads/processed/project_dataset_midi.npy") ### dataset[i][j][k] = i-th song, j-th window, k-th feature
    project_dataset = np.load("../uploads/dataset/audio_data.npy", allow_pickle=True)
    closest = []
    for i in range(len(project_query)):
        for j in range(len(project_dataset)):
            for k in range(len(project_dataset[j])):
                distance = GeneralProcessing.cosineSimilarity(project_query[i], project_dataset[j][k])
                closest.append((distance, i, j, k))
    #check absolute window for now, might change to check song                
    top_5 = sorted(closest, key=lambda x: x[0], reverse=True)[:5]
    return top_5

    
