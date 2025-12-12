import wave
import struct
from typing import List

# ----------------------------------------
# 簡易ピークインデックスを返す
# ----------------------------------------
def get_peak_indices(filepath: str) -> List[int]:
    with wave.open(filepath, "rb") as wf:
        n_frames = wf.getnframes()
        n_channels = wf.getnchannels()
        raw_data = wf.readframes(n_frames)
        samples = struct.unpack("<" + "h" * n_frames * n_channels, raw_data)
        samples = samples[::n_channels]  # モノラル化
        avg_amp = sum(abs(s) for s in samples) / len(samples)
        threshold = avg_amp
        peaks = [i for i, s in enumerate(samples) if abs(s) > threshold]
        return peaks