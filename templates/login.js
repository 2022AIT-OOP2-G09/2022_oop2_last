// <input type="submit" value="ログイン">
const lb = document.querySelector("#login-submit")
lb.addEventListener("click", (ev) => {
    ev.preventDefault() // HTMLが本来持っている他の正常なボタン処理をなかったことにする
    console.log("ログインボタンが押されました")

    // パラメータの取得
    // <input type="text" name="username" id="username">
    // <input type="password" name="password" id="password">
    const param = new URLSearchParams()
    param.append("username", document.querySelector("#username").value)
    param.append("password", document.querySelector("#password").value)

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