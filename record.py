import sounddevice as sd
import numpy as np
from scipy.signal import butter, lfilter
import wave

# Parameters
sample_rate = 44100  # CD quality
channels = 1
duration = 3  # seconds to record
cutoff_low = 20
cutoff_high = 300
order = 4

# Band-pass filter
def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, data)

# Buffer to store processed data
processed_audio = []

def callback(indata, frames, time, status):
    if status:
        print(status)

    # Flatten and filter
    audio = indata[:, 0]
    #filtered = bandpass_filter(audio, cutoff_low, cutoff_high, sample_rate, order)
    filtered = audio
    processed_audio.append(filtered.copy())

# Start stream
with sd.InputStream(channels=channels, samplerate=sample_rate, callback=callback):
    print("Recording with bass emphasis...")
    sd.sleep(duration * 1000)

# Convert to 16-bit PCM and save
output = np.concatenate(processed_audio)
output = np.int16(output / np.max(np.abs(output)) * 32767)

with wave.open("voice.wav", 'w') as wf:
    wf.setnchannels(channels)
    wf.setsampwidth(2)  # 16-bit
    wf.setframerate(sample_rate)
    wf.writeframes(output.tobytes())

print("Done. File saved.")
