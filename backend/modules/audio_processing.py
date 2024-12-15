import pretty_midi
import numpy as np

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

        if np.sum(histogram) != 0:
            histogram /= np.sum(histogram)
        else:
            histogram = [-99999]
        
        return histogram

    @staticmethod
    def shrink_atb(atb, distance):
        mean = 0
        n = 0
        for i in range(len(atb)):
            mean += i * atb[i]
            n += atb[i]
        
        if n == 0:  # Handle edge case where `atb` is empty or all values are zero
            return np.zeros(2 * distance + 1)
        
        mean_note = round(mean / n)  # Use floating-point division and round to nearest integer
        new_atb = np.zeros(2 * distance + 1)
        
        # Determine bounds
        bottom = max(0, mean_note - distance)
        upper = min(127, mean_note + distance)
        
        # Merge in-range notes into `new_atb`
        for i in range(bottom, upper + 1):
            new_atb[i - bottom] = atb[i]
        
        # Sum out-of-range values
        sum_bottom = np.sum(atb[:bottom])  # Values to the left of `bottom`
        sum_upper = np.sum(atb[upper + 1:])  # Values to the right of `upper`
        
        # Assign to the edges of `new_atb`
        new_atb[0] = sum_bottom  # Leftmost bin
        new_atb[-1] = sum_upper  # Rightmost bin
        
        return new_atb
    
    @staticmethod
    def shrink_ignore(atb, distance):
        mean = 0
        n = 0
        for i in range(len(atb)):
            mean += i * atb[i]
            n += atb[i]
        
        if n == 0:  # Handle edge case where `atb` is empty or all values are zero
            return np.zeros(2 * distance + 1)
        
        mean_note = round(mean / n)  # Use floating-point division and round to nearest integer
        new_atb = np.zeros(2 * distance + 1)
        
        # Determine bounds
        bottom = max(0, mean_note - distance)
        upper = min(127, mean_note + distance)
        
        # Merge in-range notes into `new_atb`
        for i in range(bottom, upper + 1):
            new_atb[i - bottom] = atb[i]
        
        return new_atb





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
        while current_time < melody_notes[-1][1]:
        # while current_time + WINDOW_SIZE * beat < melody_notes[-1][1]:
            windows.append(melody_notes[(melody_notes[:, 0] >= current_time) & (melody_notes[:, 0] < current_time + WINDOW_SIZE * beat)][:, 2])
            current_time += HOP_SIZE * beat

        windows = [window for window in windows if len(window) > 0]
        
        window_feature_vector = []
        for window in windows:
            first_tone = window[0]
            fuzzy_atb = MidiProcessing.create_fuzzy_histogram(window, np.arange(129), 1)
            if fuzzy_atb[0] == -99999:
                continue
            fuzzy_atb = MidiProcessing.shrink_atb(fuzzy_atb, 25)
            fuzzy_rtb = MidiProcessing.create_fuzzy_histogram(np.diff(window), np.arange(-127, 129), 1)
            if fuzzy_rtb[0] == -99999:
                continue
            fuzzy_rtb = MidiProcessing.shrink_ignore(fuzzy_rtb, 25)
            fuzzy_ftb = MidiProcessing.create_fuzzy_histogram(window - first_tone, np.arange(-127, 129), 1)
            if fuzzy_ftb[0] == -99999:
                continue
            fuzzy_ftb = MidiProcessing.shrink_ignore(fuzzy_ftb, 25)
            current_window_feature_vector = np.concatenate((fuzzy_atb, fuzzy_rtb, fuzzy_ftb))
            
            window_feature_vector.append(current_window_feature_vector)
        
        return np.array(window_feature_vector)