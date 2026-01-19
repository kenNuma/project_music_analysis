from fastapi import APIRouter, File, UploadFile, HTTPException
import tempfile
import random
import os

import analyze.playTime as playTime
import analyze.bpm as bpm
import analyze.peakCount as peakCount
import analyze.sampleLate as sampleLate
import analyze.amplitude as amplitude


router = APIRouter(
    prefix="/analyze",
    tags=["analyze"],
)

# WAVのコンテンツタイプ
ALLOWED_WAV_TYPES = {
    "audio/wav",
    "audio/x-wav",
    "audio/wave",
    "audio/vnd.wave",
}

# 評価画像表示の選択肢
SELECT_IMAGES = [
    "img/hyouka.jpeg",
    "img/doryoku.jpg",
    "img/ok.jpeg",
    "img/saikou.jpg",
]

@router.post("/")
async def upload_audio(audio: UploadFile = File(...)):
    """
    音声ファイル（WAV）を受け取り、各種解析結果を返す
    """

    # バリデーション処理 => wavファイルしか許容しない
    if audio.content_type not in ALLOWED_WAV_TYPES:
        raise HTTPException(
            status_code=400,
            detail="WAVファイルのみ解析可能です"
        )

    tmp_path = ""
    try:
        # 受け取ったファイルを一時ファイルとして読み込む
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            contents = await audio.read()
            tmp.write(contents)
            tmp_path = tmp.name

        # 振れ幅解析（戻り値 -> ディクショナリ）
        amplitudes = amplitude.get_amplitude_stats(tmp_path)

        result = {
            "fileName": audio.filename,
            "bpm": bpm.estimate_bpm(tmp_path),
            "playTime": playTime.get_duration(tmp_path),
            "sampleRate": sampleLate.get_sample_rate(tmp_path),
            "peakCount": len(peakCount.get_peak_indices(tmp_path)),
            "min_amplitude": amplitudes["min_amplitude"],
            "max_amplitude": amplitudes["max_amplitude"],
            "avg_amplitude": amplitudes["avg_amplitude"],
            "image_path": random.choice(SELECT_IMAGES),
        }

        return result

    finally:
        # 一時ファイルを削除
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)