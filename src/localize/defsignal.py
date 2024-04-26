from scipy.fft import fft, ifft
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt


@dataclass
class constants:
    fs_rx: float = 44100  # TODO: which sampling frequency is required by specs?
    epsi: float = 0.001


@dataclass
class defsignal:
    signal: np.ndarray

    def __init__(self, y: np.ndarray) -> None:
        while type(self) == type(y):  # NOTE: nested signals are not supported,
            y = y.signal              # so we flatten it instead.
        assert y.ndim == 1, 'ERROR: signal should be flat'
        self.signal = y

    def convolve(self, x: np.ndarray) -> np.ndarray:
        """
        Calculate the convolution of the contained signal in @defsignal with
          the given signal.
        x: np.ndarray
        @out: np.ndarray
        """
        if type(x) == type(self):
            x = x.signal
        return np.convolve(self.signal, x)

    def channel(self, x: np.ndarray) -> np.ndarray:
        if type(x) == type(self):
            x = x.signal
        assert x.ndim == 1, 'ERROR: signal should be flat'

        x = x
        y = self.signal

        Nx = x.size
        Ny = y.size

        # Force x to be the same length as y
        x = np.pad(x, (0, Ny - Nx))

        # Deconvolution in the frequency domain.
        X = fft(x)
        Y = fft(y)

        with np.errstate(all='ignore'):
            H = Y/X

        # Threshold to avoid blow ups of noise during inversion.
        ii = np.absolute(X) < constants.epsi * max(np.absolute(X))
        H[ii] = 0

        # Ensure the result is real.
        h = np.real(ifft(H))

        # Return the calculated impulse response.
        return h

    def calculate_distance(self, h: np.ndarray) -> float:
        if type(h) == type(self):
            h = h.signal
        h0 = self.channel(h)
        h1 = self.channel(self.signal)
        distance = abs(np.argmax(h0) - np.argmax(h1)) / constants.fs_rx * 343
        return distance

    def naive_plot(self) -> None:
        y = self.signal
        plt.figure(figsize=(11, 4))
        plt.title('?')
        plt.xlabel('? [?]')
        plt.ylabel('? [?]')
        plt.plot(y)
        plt.show()
