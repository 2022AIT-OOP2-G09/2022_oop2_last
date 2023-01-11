// <input type="submit" value="登録">
const sb = document.querySelector("#signUp-submit")
lb.addEventListener("click", (ev) => {
    ev.preventDefault() // HTMLが本来持っている他の正常なボタン処理をなかったことにする
    console.log("登録ボタンが押されました")

    // パラメータの取得
    // <input type="text" id="your_id" name="id">
    // <input type="text" id="your_password" name="password">
    // <input type="text" id="your_password2" name="password2">
    const param = new URLSearchParams()
    param.append("id", document.querySelector("#your_id").value)
    param.append("password", document.querySelector("#your_password").value)
    param.append("password2", document.querySelector("#your_password2").value)

    console.log(param.toString())
    // データ検索のWeb APIは/addressをGETメソッドで呼び出す
    fetch("/login?"+param.toString()).then(response => {
        console.log(response);
        if (response == 1) {
            window.location.href = 'パス名';
        }else{
            const form = document.querySelector("#form");
            let pElm = document.createElement('p');
            pElm.innerHTML = '入力ミスがあります'
            pElm.style.color = 'red';
        }
    });
})