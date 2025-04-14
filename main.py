import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

def band_filter(data, lowcut, highcut, fs, gain_db, order=4):
    # Bandpass filter design
    sos = butter(order, [lowcut, highcut], btype='band', fs=fs, output='sos')
    filtered = sosfilt(sos, data)
    
    # Convert dB to gain factor
    gain = 10 ** (gain_db / 20)
    
    # Apply gain to the filtered band
    boosted = filtered * gain
    
    # Add to original for boost (or subtract if gain < 1)
    enhanced = data + boosted
    
    # Normalize to avoid clipping
    max_val = np.max(np.abs(enhanced))
    if np.issubdtype(data.dtype, np.integer):
        enhanced = enhanced / max_val * np.iinfo(data.dtype).max
        enhanced = enhanced.astype(data.dtype)
    
    return enhanced

# Load file
fs, data = wavfile.read("voice.wav")
if data.ndim > 1:
    data = data[:, 0]

# Boost low frequencies 20–300 Hz by +6 dB (chatgpt say +3 to +6)
output_low = band_filter(data, 20, 300, fs, gain_db=6)

# Cut high frequencies 2000–6000 Hz by -4 dB (chatgpt says -2 to -4)
output_high_cut = band_filter(output_low, 2000, 6000, fs, gain_db=-4)

# Save result
wavfile.write("enhanced_output.wav", fs, output_high_cut)
