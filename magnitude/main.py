from filterbanks import *
import scipy
from scipy import signal
from scipy.io import wavfile
import numpy as np

erb_band = EqualRectangularBandwidth(34, 0, 20000)
wav_path = "/home/hp/Downloads/babble_10dB.wav"
sample_rate, audio_sample = wavfile.read(wav_path)

print(audio_sample[:960, 0].shape)
f, t, Zxx = scipy.signal.stft(audio_sample[:960, 0], sample_rate, nperseg=960, axis=0)
print("Num freq:", f.shape)
print("Num time:", t.shape)
print("STFT shape", Zxx.shape)

bands = []
for i in range(34):
    filter = erb_band.filters[i]
    low_nfft_idx, high_nfft_idx = filter[0]
    band = []
    for frame in range(Zxx.shape[1]):
        s = 0
        spectrum = Zxx[:, frame]
        for j in range(low_nfft_idx, high_nfft_idx):
            real = np.real(spectrum[j])
            imag = np.imag(spectrum[j])
            tmp = real * real + imag * imag
            s += tmp * filter[1][j - low_nfft_idx]
        band.append(s)
    bands.append(np.array(band))

npbands = np.array(bands)
print(npbands.shape)
print("Yb(b=0):", npbands[0])