from .audio_processing import MidiProcessing
from .general_processing import GeneralProcessing
import numpy as np
import pretty_midi

def queryMidi(midi: pretty_midi.PrettyMIDI, dataset: np.ndarray, projectedDataset: np.ndarray, kval: int) -> np.ndarray:
    if kval == -1:
        kval = dataset.shape[1]
    matrix: np.ndarray = MidiProcessing.midiToMatrix(midi)
    meanDataset: np.ndarray = GeneralProcessing.meanMatrix(dataset) #an array of means
    centeredMatrix: np.ndarray = matrix - meanDataset
    principalComponents: np.ndarray = GeneralProcessing.principalComponent(dataset, kval)
    projectedMatrix: np.ndarray = GeneralProcessing.projectMatrix(centeredMatrix, principalComponents, kval)
    top: int = 5
    closest = []
    for i in range(projectedDataset.shape[0]):
        distance: float = GeneralProcessing.cosineSimilarity(projectedMatrix, projectedDataset[i])
        closest.append(distance)

    closest = sorted(closest, reverse=True)
    return closest[:top]