import pretty_midi
import numpy as np
from atb import histograms
from general_processing import GeneralProcessing
from typing import List

# Note: start, end, pitch, velocity
# process: get channel, normalize tempo and pitch, split channel into windowed beats (20 beats, 4 windows), make Tone Transition Vector and Tone Distribution Vector 
# (Absolute Tone Based, Relative Tone Based, First Tone Based)

class MidiProcessing:
    def __init__(self):
        pass

    @staticmethod
    #TAKES FIRST CHANNEL ONLY, only takes start, end, pitch
    def midiToMatrix(midi : pretty_midi.PrettyMIDI) -> np.ndarray:
        matrixSong: List[List[float]] = []
        #takes first channel
        channel = midi.instruments[0]
        for note in channel.notes:
            #start, end, pitch
            matrixSong.append([note.start, note.end, note.pitch, note.velocity])

        res: np.ndarray = np.array(matrixSong)
        return res
    
    # normalize tempo and pitch, use min max normalization
    @staticmethod    
    def normalizePitch(midi: pretty_midi.PrettyMIDI) -> pretty_midi.PrettyMIDI:
        min_pitch = float('inf')
        max_pitch = float('-inf')
        
        for instrument in midi.instruments:
            for note in instrument.notes:
                if note.pitch < min_pitch:
                    min_pitch = note.pitch
                if note.pitch > max_pitch:
                    max_pitch = note.pitch
        
        for instrument in midi.instruments:
            for note in instrument.notes:
                note.pitch = (note.pitch - min_pitch) / (max_pitch - min_pitch)
        
        return midi
        
    @staticmethod
    # window 20 beat, slide 4 beat
    def windowingMatrix(matrix: np.ndarray, bpm: int) -> List[np.ndarray]:
        time: float = 0
        timeDelay: float = 60 / bpm
        windowedMatrix: List[np.ndarray] = []
        while time <= matrix[-1][1]:
            currentWindow: np.ndarray = np.zeros((20, 4))
            for i in range(20):
                start_time = time + i * timeDelay
                end_time = time + (i + 1) * timeDelay
                notes_in_window = matrix[(start_time <= matrix[:, 0]) & (matrix[:, 0] < end_time)]
                
                # ambil velocity paling besar
                if len(notes_in_window) > 1:
                    max_velocity = notes_in_window[0][3]
                    max_note = notes_in_window[0]
                    for note in notes_in_window:
                        if note[3] > max_velocity:
                            max_velocity = note[3]
                            max_note = note
                    currentWindow[i] = max_note
                elif len(notes_in_window) > 0:
                    currentWindow[i] = notes_in_window[0]                    
            windowedMatrix.append(currentWindow)
            time += 4 * timeDelay
        return windowedMatrix

    @staticmethod
    def pitchVector(windowedMatrix: np.ndarray) -> np.ndarray:
        pitchVector: List[int] = []
        for window in windowedMatrix:
            pitchVector.append(window[:, 2])
        pitchVector = np.array(pitchVector)
        return pitchVector
    
    @staticmethod
    def toneTransitionVector(pitchVector: np.ndarray) -> np.ndarray:
        toneTransitionVector: List[int] = []
        for pitch in pitchVector:
            toneTransitionVector.append(np.diff(pitch))
        toneTransitionVector = np.array(toneTransitionVector)
        return toneTransitionVector
    
    @staticmethod
    def processMidi(midi: pretty_midi.PrettyMIDI, bpm: int) -> np.ndarray:
        processedMidi: np.ndarray = MidiProcessing.midiToMatrix(midi)
        processedMidi = MidiProcessing.normalizePitch(processedMidi)
        windowedMatrix: List[np.ndarray] = MidiProcessing.windowingMatrix(processedMidi, bpm)
        resultMatrix: List[np.ndarray] = []
        for window in windowedMatrix:
            pitchVector: np.ndarray = MidiProcessing.pitchVector(window)
            toneTransitionVector: np.ndarray = MidiProcessing.toneTransitionVector(pitchVector)
            histogramsResult = histograms(pitchVector)
            resultMatrix.append(np.concatenate((toneTransitionVector, histogramsResult["ATB"], histogramsResult["RTB"], histogramsResult["FTB"])))
        return np.array(resultMatrix)
        
        
    
