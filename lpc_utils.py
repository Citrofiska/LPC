import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as signal

def stft(signal, fft_size=1024, hop_size=512):
    """
    Perform Short-Time Fourier Transform (STFT) on a signal.

    Args:
        signal (np.ndarray): Input signal.
        fft_size (int): Size of the FFT.
        hop_size (int): Hop size for the STFT.

    Returns:
        np.ndarray: STFT of the input signal.
    """
    return np.array([np.fft.fft(signal[i:i+fft_size]) for i in range(0, len(signal) - fft_size + 1, hop_size)])

def istft(stft_signal, hop_size=512):
    """
    Perform Inverse Short-Time Fourier Transform (ISTFT) on a signal.

    Args:
        stft_signal (np.ndarray): STFT of the signal.
        hop_size (int): Hop size for the ISTFT.

    Returns:
        np.ndarray: Inverse STFT of the input signal.
    """
    return np.array([np.fft.ifft(frame).real for frame in stft_signal]).flatten()[::hop_size]

def extract_lpc(signal, order=20):
    """
    Extract Linear Predictive Coding (LPC) coefficients from a signal.

    Args:
        signal (np.ndarray): Input signal.
        order (int): Order of LPC coefficients.

    Returns:
        np.ndarray: LPC coefficients.
    """
    _, lpc_coeffs, _ = signal.lpc(signal, order)
    return lpc_coeffs
