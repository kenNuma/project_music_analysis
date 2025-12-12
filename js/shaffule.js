MENBERS = [
    {id: 1, name: "楠田"},
    {id: 1, name: "三村"},
    {id: 2, name: "千々岩"},
    {id: 2, name: "進"},
    {id: 3, name: "西首"},
    {id: 3, name: "嘉村"},
    {id: 4, name: "富田"},
    {id: 4, name: "祁内"},
    {id: 5, name: "入佐"},
    {id: 5, name: "古川"},
    {id: 6, name: "黒田"},
    {id: 6, name: "青木"},
    {id: 7, name: "秋森"},
    {id: 7, name: "山田"},
    {id: 8, name: "大瀬"},
    {id: 8, name: "久保"},
    {id: 9, name: "巽"},
    {id: 9, name: "古野"},
    {id: 10, name: "トーマス"},
    {id: 10, name: "成富"},
];


// 音声再生・ポーズ処理
document.getElementById("shaffuleBtn").addEventListener("click", () => {

    const listItems = document.querySelectorAll(".table-list li");

    // シャッフル（元配列を壊さない）
    const shuffled = [...MENBERS];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }

    // 名前セット & 色リセット（黒）
    listItems.forEach((li, index) => {
        li.textContent = shuffled[index]?.name ?? "";
        li.style.color = "black";
    });

    // インデックスの偶奇で隣を判定（偶数→右 / 奇数→左）
    for (let i = 0; i < shuffled.length; i++) {
        const current = shuffled[i];
        const targetIndex = (i % 2 === 0) ? i + 1 : i - 1;

        if (targetIndex < 0 || targetIndex >= shuffled.length) continue;

        const target = shuffled[targetIndex];

        if (current.id === target.id) {
            // 見つかったら両方赤にする（片方だけならここを調整）
            listItems[i].style.color = "red";
            listItems[targetIndex].style.color = "red";
        }
    }
})