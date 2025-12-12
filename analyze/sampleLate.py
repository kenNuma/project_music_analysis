import wave

# ----------------------------------------
# サンプルレートを返す
# ----------------------------------------
def get_sample_rate(filepath: str) -> int:
    with wave.open(filepath, "rb") as wf:
        return wf.getframerate()
