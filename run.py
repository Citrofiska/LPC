from lpc_utils import *
import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as signal

def load_audio(file_path):
    """
    Load audio file and return sampling rate and signal.

    Args:
        file_path (str): Path to the audio file.

    Returns:
        tuple: Sampling rate and audio signal.
    """
    rate, signal = wav.read(file_path)
    return rate, signal.astype(np.float32)

def main(modulator_file, carrier_file, output_file):
    # Load modulator and carrier signals
    rate_mod, modulator_signal = load_audio(modulator_file)
    rate_car, carrier_signal = load_audio(carrier_file)

    # Ensure same sampling rate
    assert rate_mod == rate_car, "Sampling rates of modulator and carrier signals must be the same."

    # Trim signals to same length
    min_len = min(len(modulator_signal), len(carrier_signal))
    modulator_signal = modulator_signal[:min_len]
    carrier_signal = carrier_signal[:min_len]

    # Perform Short-Time Fourier Transform (STFT)
    modulator_stft = stft(modulator_signal)
    carrier_stft = stft(carrier_signal)

    # Extract LPC coefficients from modulator signal
    lpc_coeffs = extract_lpc(modulator_signal)

    # Apply LPC filter to the carrier signal
    filtered_carrier_stft = np.array([np.fft.fft(signal.lfilter([1], lpc_coeffs, frame)) for frame in carrier_stft])

    # Perform Inverse Short-Time Fourier Transform (ISTFT)
    synthesized_signal = istft(filtered_carrier_stft)

    # Save synthesized signal to file
    wav.write(output_file, rate_mod, synthesized_signal.astype(np.int16))

if __name__ == "__main__":
    modulator_file = "modulator.wav"
    carrier_file = "carrier.wav"
    output_file = "synthesized.wav"
    main(modulator_file, carrier_file, output_file)
