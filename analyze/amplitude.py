import wave
import struct

# ----------------------------------------
# 振幅統計を返す
# ----------------------------------------
def get_amplitude_stats(filepath: str) -> dict:
    with wave.open(filepath, "rb") as wf:
        n_frames = wf.getnframes()
        raw_data = wf.readframes(n_frames)
        n_channels = wf.getnchannels()
        samples = struct.unpack("<" + "h" * n_frames * n_channels, raw_data)
        samples = samples[::n_channels]  # モノラル化

        min_amp = min(samples)
        max_amp = max(samples)
        avg_amp = sum(abs(s) for s in samples) / len(samples)

        return {
            "min_amplitude": min_amp,
            "max_amplitude": max_amp,
            "avg_amplitude": avg_amp
        }
