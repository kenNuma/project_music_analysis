import wave

# ----------------------------------------
# 再生時間を返す
# ----------------------------------------
def get_duration(filepath: str) -> float:
    with wave.open(filepath, "rb") as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        return frames / rate  # 秒

