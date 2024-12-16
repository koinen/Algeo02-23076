import librosa
import numpy as np
import pretty_midi
import time

def wav_to_midi(wav_file):
    start_time = time.time()
    y, sr = librosa.load(f"../uploads/{wav_file}", sr=None)

    f0, voiced_flag, _ = librosa.pyin(
        y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), sr=sr
    )

    midi_notes = librosa.hz_to_midi(f0)

    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, backtrack=True)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    midi = pretty_midi.PrettyMIDI()
    piano = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano
    
    for onset in onset_times:
        frame_idx = librosa.time_to_frames(onset, sr=sr)
        if 0 <= frame_idx < len(midi_notes) and voiced_flag[frame_idx]: 
            pitch = int(round(midi_notes[frame_idx]))
            start = onset
            end = start + 0.5 
            if not np.isnan(pitch):  
                note = pretty_midi.Note(velocity=100, pitch=pitch, start=start, end=end)
                piano.notes.append(note)

    midi.instruments.append(piano)

    midi.write("uploads/output.mid")
    print(f"MIDI file saved to: uploads/output.mid")
    return time.time() - start_time


if __name__ == "__main__":
    wav_to_midi("./test.wav")
