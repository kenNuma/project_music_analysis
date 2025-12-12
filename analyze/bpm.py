import wave
import struct

# ----------------------------------------
# 簡易BPM推定（ピーク数から目安）
# ----------------------------------------
def estimate_bpm(filepath: str) -> float:
    
    with wave.open(filepath, "rb") as wf:
        n_frames = wf.getnframes()
        raw_data = wf.readframes(n_frames)
        n_channels = wf.getnchannels()
        samples = struct.unpack("<" + "h" * n_frames * n_channels, raw_data)
        samples = samples[::n_channels]  # モノラル化

        avg_amp = sum(abs(s) for s in samples) / len(samples)
        threshold = avg_amp

        min_interval = int(0.3 * wf.getframerate())  # 0.3秒以上あけて次のピーク
        last_peak = -min_interval
        peak_count = 0
        for i, s in enumerate(samples):
            if abs(s) > threshold and i - last_peak >= min_interval:
                peak_count += 1
                last_peak = i

        duration = n_frames / wf.getframerate()
        if duration == 0:
            return 0.0

        bpm = peak_count / duration * 60
        return bpm