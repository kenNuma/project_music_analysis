from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import analyze.playTime as playtime
import analyze.bpm as bpm
import analyze.peakCount as peakCount
import analyze.sampleLate as sampleLate
import analyze.amplitude as amplitude
import tempfile
import random
import os

app = FastAPI()
# アクセス権の設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# WAVのコンテンツタイプ
ALLOWED_WAV_TYPES = {
    "audio/wav",
    "audio/x-wav",
    "audio/wave",
    "audio/vnd.wave"
}

# 評価画像表示の選択肢
SELECT_IMAGIS = [
    "img/hyouka.jpeg",
    "img/doryoku.jpg",
    "img/ok.jpeg",
    "img/saikou.jpg",
]

@app.post("/main")
async def upload_audio(audio: UploadFile = File(...)):
    
    # バリデーション処理 => wavファイルしか許容しない
    if audio.content_type not in ALLOWED_WAV_TYPES:
        raise HTTPException(status_code=400, detail="WAVファイルのみ解析可能です")
    
    # 受け取ったファイルを一時ファイルとして読み込む
    tmp_path = ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        contents = await audio.read()
        tmp.write(contents)
        tmp_path = tmp.name
        
    # 振れ幅解析（戻り値：ディクショナリ）
    amplitudes = amplitude.get_amplitude_stats(tmp_path)
    
    # 解析結果まとめをjsonとして返す
    result = {
        "fileName": audio.filename,
        "bpm": bpm.estimate_bpm(tmp_path),
        "playTime": playtime.get_duration(tmp_path),
        "smpleLate": sampleLate.get_sample_rate(tmp_path),
        "peakCount": len(peakCount.get_peak_indices(tmp_path)),
        "min_amplitude": amplitudes["min_amplitude"],
        "max_amplitude": amplitudes["max_amplitude"],
        "avg_amplitude": amplitudes["avg_amplitude"],
        "image_pass": random.choice(SELECT_IMAGIS)
    }
    
    print(result)
    
    # 一時ファイルの破棄
    os.remove(tmp_path)

    return result