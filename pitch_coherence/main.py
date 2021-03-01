from pyrapt import * 

import scipy
from scipy import signal
from scipy.io import wavfile
import numpy as np

def main(audio_sample, sample_rate):
    frame_rapt_sec = 0.02
    frame_comb_sec = 0.01

    if len(audio_sample.shape) > 1:
        audio_sample = audio_sample[:, 0]/2.0 + audio_sample[:, 1]/2.0
        audio_sample = audio_sample.astype(int)

    frame_len = int(frame_rapt_sec * sample_rate) 
    frame_comb_len = int(frame_comb_sec * sample_rate)
    sample_len = len(audio_sample)

    frames_for_rapt = np.array([audio_sample[x:x + frame_len] for x in
                        np.arange(0, sample_len, frame_len)])
    
    frequencies = []
    pitch_corrs = []

    for frame in frames_for_rapt:
        frequency, pitch_corr = rapt_sample(frame, sample_rate)
        frequencies+=frequency
        pitch_corrs.append(pitch_corr)
    print("Total frames:", frames_for_rapt.shape)
    print(len(pitch_corrs))
    print(pitch_corrs)

    return 

if __name__ == "__main__":
    wav_path = '/home/hp/Downloads/rnn_alto_examples/frame_step_64/01_mixed.wav'
    sample_rate, audio_sample = wavfile.read(wav_path)
    # new_samples = 
    # scipy.io.wavfile.write("./sample.wav", sample_rate, new_samples)
    main(audio_sample, sample_rate)
    print("Done")
