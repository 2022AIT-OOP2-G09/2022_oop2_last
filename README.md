# 仕様
## モジュール
Flask(2.2.2), sqlite3(3.37.0), datetime, pytz(2022.7)
を導入してもらう必要がある


## 新規登録ページ
<br> - 基本入力情報はユーザIDとパスワードだが、識別IDとして別に「ID」を持たせておく。 
<br> - 新規登録欄のIDは被らないようにpyhtonで処理 
<br> - データベースにユーザID・パスワードを追加するテーブルは、ID_pass_database内のuser_ID_Passテーブルにお願いします。 


## ログインページ 
<br> - ユーザIDを入力された際にdatabeseからそのユーザIDが存在するかをみる  

## 投稿内容の表示画面 
<br> - 投稿内容は ID_pass_database内のtweetテーブルに入れるようにする 
<br> - 投稿内容には投稿者がわかるようにIDとの紐付けがあるといい 

 

## アプリ完成イメージ
- 大まかな構想を書き記した写真をK21010参考資料内に入れている

## 作業分担
<br>岡田：ログイン画面の入力に対してデータベースを参照しユーザIDが存在するのか検証処理（ページ２） 完了
<br>今泉：データベースにIDとパスワードを保存する処理（ページ１） 完了
<br>山田：今後のcssデザインに向けての構想および予習（ページ１〜３） 完了
<br>熊本：データベースからユーザIDと投稿内容の表示（ページ３）　完了
<br>伊藤：HTML五枚を大まかに作成し、デバッグに使えるようにする＋エラー表示の作成　　完了
<br>波多野：データベースからユーザIDとパスワード一致しているかの検証（ページ２） 完了
<br>熊本：投稿内容とユーザ名の紐付け 完了
<br>波多野、今泉：投稿内容の保存と画像をdbにパスとして保存する。　完了
<br>熊本：投稿リストの順番を変えての投稿　完了


<br>(データベースに書き込み、呼び出し、同じIDは登録不可) 


