import pretty_midi
import numpy as np
from .atb import histograms
from .general_processing import GeneralProcessing
from typing import List

# Note: start, end, pitch, velocity
# process: get channel, normalize tempo and pitch, split channel into windowed beats (20 beats, 4 windows), make Tone Transition Vector and Tone Distribution Vector 
# (Absolute Tone Based, Relative Tone Based, First Tone Based)

class MidiProcessing:
    def __init__(self):
        pass

    @staticmethod
    def create_fuzzy_histogram(data, bins, sigma):
        histogram = np.zeros(len(bins))
        
        for value in data:
            weights = np.exp(-((bins - value) ** 2) / (2 * sigma ** 2))
            histogram += weights

        histogram /= np.sum(histogram)
        
        return histogram

    @staticmethod
    def processMidi(path):
        WINDOW_SIZE = 20 
        HOP_SIZE = 4
        midi_data = pretty_midi.PrettyMIDI(path)
        melody_notes = midi_data.instruments[0].notes
        queryBPM = midi_data.estimate_tempo()
        melody_notes = np.array([[note.start, note.end, note.pitch, note.velocity] for note in melody_notes])
        for note in melody_notes:
            note[0] = note[0] * (120 / queryBPM) #BPM = 120
            note[1] = note[1] * (120 / queryBPM)
        
        beat = 60 / 120 #BPM
        windows = []
        current_time = 0
        while current_time + WINDOW_SIZE * beat < melody_notes[-1][1]:
            windows.append(melody_notes[(melody_notes[:, 0] >= current_time) & (melody_notes[:, 0] < current_time + WINDOW_SIZE * beat)][:, 2])
            current_time += HOP_SIZE * beat

        windows = [window for window in windows if len(window) > 0]
        
        window_feature_vector = np.array([])
        for window in windows:
            first_tone = window[0]
            fuzzy_atb = MidiProcessing.create_fuzzy_histogram(window, np.arange(129), 1)
            fuzzy_rtb = MidiProcessing.create_fuzzy_histogram(np.diff(window), np.arange(-127, 129), 1)
            fuzzy_ftb = MidiProcessing.create_fuzzy_histogram(window - first_tone, np.arange(-127, 129), 1)
            current_window_feature_vector = np.concatenate((fuzzy_atb, fuzzy_rtb, fuzzy_ftb))
            
            window_feature_vector = np.append(window_feature_vector, current_window_feature_vector)
        
        return window_feature_vector