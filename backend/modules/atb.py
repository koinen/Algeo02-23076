import numpy as np
from typing import Dict

def histograms(inputPitch: np.ndarray) -> Dict[str, np.ndarray]:
    """
    Menghitung histogram ATB, RTB, dan FTB dari inputPitch sequence pitch yang dinormalisasi [0...1].

    Parameters:
    inputPitch (np.ndarray): array dengan panjang 20 yang merepresentasikan pitch pada beat [0...1].

    Returns:
    dict: berisi histogram untuk ATB, RTB, dan FTB
    """

    # Ubah pitch ke scale MIDI (0...127)
    midi = (np.array(inputPitch) * 127).astype(int)

    # ATB
    atb = np.histogram(midi, bins=128, range=(0, 127))[0]

    # RTB
    rtbDiff = np.diff(midi)
    rtb = np.histogram(rtbDiff, bins=255, range=(-127, 127))[0]

    # FTB
    ftbDiff = midi[1:] - midi[0]
    ftb = np.histogram(ftbDiff, bins=255, range=(-127, 127))[0]

    return {
        "ATB": atb,
        "RTB": rtb,
        "FTB": ftb
    }

if __name__ == "__main__":
    # Test Case Placeholder
    inputPitch = np.random.rand(20)  # Array pitch, panjang 20 [0...1]
    res = histograms(inputPitch)

    print("ATB:\n", res["ATB"])
    print("RTB:\n", res["RTB"])
    print("FTB:\n", res["FTB"])