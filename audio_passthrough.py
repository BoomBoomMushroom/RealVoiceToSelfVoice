import sounddevice as sd
import numpy as np
from scipy.signal import butter, sosfilt

# Filter setup
def make_band_filter(lowcut, highcut, fs, gain_db, order=4):
    sos = butter(order, [lowcut, highcut], btype='band', fs=fs, output='sos')
    gain = 10 ** (gain_db / 20)
    return lambda data: data + gain * sosfilt(sos, data)

# Example filter: boost lows and cut highs
fs = 48000  # Discord's preferred sample rate
boost_lows = make_band_filter(20, 300, fs, gain_db=6)
cut_highs = make_band_filter(2000, 6000, fs, gain_db=-9)

def audio_callback(indata, outdata, frames, time, status):
    data = indata[:, 0]  # mono
    processed = boost_lows(data)
    processed = cut_highs(processed)
    outdata[:, 0] = processed  # mono output

print(sd.query_devices())
sd.default.device = [1,10]

print(sd.default.device)

# Stream audio
with sd.Stream(channels=1, callback=audio_callback, samplerate=fs, dtype='float32'):
    print("Processing... Press Ctrl+C to stop.")
    try:
        while True:
            sd.sleep(1000)
    except KeyboardInterrupt:
        print("Stopped.")
