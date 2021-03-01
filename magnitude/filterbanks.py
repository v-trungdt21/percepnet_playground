"""
Created 06/03/2018
@author: Will Wilkinson
"""

import numpy as np


class EqualRectangularBandwidth:
    def __init__(self, N, low_lim, high_lim, freqRangePerBin=50):
        # make cutoffs evenly spaced on an erb scale
        self.N = N
        self.low_lim = low_lim
        self.high_lim = high_lim
        self.freqRangePerBin = freqRangePerBin

        erb_low = self.freq2erb(self.low_lim)
        erb_high = self.freq2erb(self.high_lim)
        erb_lims = np.linspace(erb_low, erb_high, self.N + 2)
        self.cutoffs = self.erb2freq(erb_lims)
        self.filters = self.make_filters()

    def freq2erb(self, freq_Hz):
        n_erb = 9.265 * np.log(1 + np.divide(freq_Hz, 24.7 * 9.265))
        return n_erb

    def erb2freq(self, n_erb):
        freq_Hz = 24.7 * 9.265 * (np.exp(np.divide(n_erb, 9.265)) - 1)
        return freq_Hz

    def make_filters(self):
        cos_filts = []
        for k in range(self.N):
            l_k = self.cutoffs[k]
            h_k = self.cutoffs[k + 2]  # adjacent filters overlap by 50%
            # impose minimum 100hz
            if h_k - l_k < 100:
                h_k = l_k + 100

            l_nfftind = (int)(l_k / self.freqRangePerBin) + 1
            h_nfftind = (int)(h_k / self.freqRangePerBin)

            avg = (self.freq2erb(l_k) + self.freq2erb(h_k)) / 2
            rnge = self.freq2erb(h_k) - self.freq2erb(l_k)

            kth_filter_array = []
            for i in range(l_nfftind, h_nfftind + 1):
                kth_filter_array.append(
                    np.cos(
                        (self.freq2erb(self.freqRangePerBin * i) - avg) / rnge * np.pi
                    )
                )
            cos_filts.append(((l_nfftind, h_nfftind + 1), np.array(kth_filter_array)))
        return np.array(cos_filts, dtype=object)
