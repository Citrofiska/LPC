import config
import numpy as np
import soundfile as sf
import scipy.signal as signal
import librosa


def compute_lpc_coefficients(frame, order):
    """
    Compute LPC coefficients for a single frame.

    Parameters:
    - frame: Input frame (1D numpy array)
    - order: LPC order

    Returns:
    - lpc_coeffs: Array of LPC coefficients
    """
    lpc_coeffs = librosa.lpc(frame, order)
    return lpc_coeffs


def apply_lpc_to_stft(stft_carrier, stft_modulator, lpc_order, sr):
    """
    Apply LPC coefficients of the modulator to the STFT of the carrier signal.

    Parameters:
    - stft_carrier: STFT of the carrier signal (2D numpy array)
    - stft_modulator: STFT of the modulator signal (2D numpy array)
    - lpc_order: Order of LPC
    - sr: Sampling rate

    Returns:
    - modified_stft: Modified STFT of the carrier signal
    """
    n_frames = stft_carrier.shape[1]
    n_fft = stft_carrier.shape[0]
    modified_stft = np.zeros_like(stft_carrier, dtype=complex)

    for i in range(n_frames):
        modulator_frame = stft_modulator[:, i]
        carrier_frame = stft_carrier[:, i]

        # Apply LPC to the magnitude of the modulator frame
        magnitude_modulator = np.abs(modulator_frame)
        lpc_coeffs = compute_lpc_coefficients(magnitude_modulator, lpc_order)

        freqs, response = signal.freqz([1], lpc_coeffs, worN=n_fft, fs=sr)
        spectral_envelope = np.abs(response)

        # Apply the spectral envelope to the carrier frame
        modified_stft[:, i] = carrier_frame * spectral_envelope

    return modified_stft


def cross_synthesis(modulator_file, carrier_file, output_file, lpc_order, n_fft, hop_length):
    # Load the carrier and modulator signals
    carrier, sr = librosa.load(carrier_file, sr=None)
    modulator, _ = librosa.load(modulator_file, sr=sr)

    # Compute the STFT of both signals
    stft_carrier = librosa.stft(carrier, n_fft=n_fft, hop_length=hop_length)
    stft_modulator = librosa.stft(modulator, n_fft=n_fft, hop_length=hop_length)

    # Apply the LPC coefficients of the modulator to the STFT of the carrier signal
    modified_stft = apply_lpc_to_stft(stft_carrier, stft_modulator, lpc_order, sr)

    # Perform ISTFT to get the synthesized signal
    synthesized_signal = librosa.istft(modified_stft, hop_length=hop_length)

    sf.write(output_file, synthesized_signal, sr)

if __name__ == "__main__":
    cross_synthesis(config.modulator_file, config.carrier_file, config.output_file,
                    config.lpc_order, config.fft_size, config.hop_size)