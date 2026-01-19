

let waveform;       //waveSurfer
let music_file;     //音声ファイル
let isFirst = true; //再生ボタン表示用

//インプットタグへの変更イベント
document.getElementById('audioFile').addEventListener('change', function(e){
    music_file = e.target.files[0];

    //波形の画面を表示中（存在する）ならリセット
    if(waveform) waveform.destroy();

    // 解析内容をリセット
    document.querySelector("#results").classList.add("analyze-none");
    document.querySelector("#assess-img").classList.add("analyze-none");

    // 再度生成
    waveform = WaveSurfer.create({
        container: '#waveform',
        waveColor: 'white',
        progressColor: 'skyblue',
        height: 200
    });

    if(music_file){
        waveform.load(URL.createObjectURL(music_file));
    }

    // 再生ボタンの表示
    if(isFirst) {
        isFirst = false;
        document.querySelector("#playStopBtn").classList.remove("none");
    }
});

//解析ボタン押下時の処理
document.getElementById('analyzeBtn').addEventListener('click', async function(){
    //音声の選択がない場合、即時 return
    if(!music_file){ 
        alert("ファイルを選択してください");
        return;
    }

    // 解析中表示取得
    const loader = document.getElementById("loading");
    loader.style.display = "flex";

    // 音声ファイルをAPIに受け渡すデータとして保持
    const formData = new FormData();
    formData.append("audio", music_file);
    try {
        // API通信(main.py)
        const res = await fetch(`http://127.0.0.1:8000/analyze`, {
            method: 'POST',
            body: formData
        });

        // 解析結果のjson受け取り
        const data = await res.json();
        
        if(!res.ok) {
            // 解析不能（WAV以外弾く）
            alert(data.detail)
            return;
        }
        
        //解析結果入れ込み
        document.querySelector("#results").classList.remove("analyze-none");
        document.querySelector("#assess-img").classList.remove("analyze-none");
        document.getElementById("name").innerText = `🎵 ファイル名: ${data.fileName}`;
        document.getElementById("bpm").innerText = `🥁 BPM: ${Math.round(data.bpm)}`;
        document.getElementById("nagasa").innerText = `⏳ 長さ: ${Math.round(data.playTime)} 秒`;
        document.getElementById("sample").innerText = `📊 サンプルレート: ${data.sampleRate}`;
        document.getElementById("piack").innerText = `🔊 ピークカウント: ${data.peakCount}`;
        document.getElementById("avg-amp").innerText = `⚡ avg_amplitude: ${data.avg_amplitude}`;

        //評価イメージパス取得
        img_element = document.getElementById("select-img")
        if(img_element && data.image_path){
            img_element.src = data.image_path;
        }

    } catch(err) {
        //サーバーエラーその他の例外時
        console.error("ERROR: ", err)
        alert("通信エラーが発生しました！")
    } finally {
        // 解析中のアニメーションの非表示
        loader.style.display = "none";
    }
});

// 音声再生・ポーズ処理
document.getElementById("playStopBtn").addEventListener("click", () => {
    if(!waveform) return;

    //再生または停止する（反転）
    waveform.playPause();

    if (waveform.isPlaying()) {
        document.getElementById("playStopBtn").innerText = "⏸ 停止";
    } else {
        document.getElementById("playStopBtn").innerText = "▶ 再生";
    }
})