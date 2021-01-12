# Impression-Checker-Bot
+ [Digital Emergency Exit](http://manbow.nothing.sh/event/event.cgi)で行われるBMSイベントのインプレッション情報を取得するdiscordbotです。
+ 2020/10/27時点で動作確認済み(DEEのレイアウトがちょっとでも変わったら動かなくなるのであしからず)
+ サーバーは[Heroku](https://jp.heroku.com/)を使っています。

## 各種ファイル情報
### src/app.py  
discordbotの本体ファイル メッセージ受け取り→返答部分はここ
### src/impression_fetcher.py
クローラとインプレ情報やイベント・BMS一覧情報を返却する関数ファイル
### Procfile
Herokuにデプロイ後に実行するコマンドを記載したファイル
ここworkerじゃないと動かないっぽいので注意
### runtime.txt
Heroku上の実行環境を記載したファイル
### requirementx.txt
各プログラム実行のためにインストールするライブラリ情報を記載したファイル

## デプロイの流れ
+ [基本これでOK](https://qiita.com/1ntegrale9/items/9d570ef8175cf178468f)
+ もし上記の流れでデプロイ後動かない場合は以下などを試してください
+ https://qiita.com/hirokik-0076/items/71c104158fa8b963ba85
+ Procfileのプロセス名(開幕に書くもの)をdiscordbot→workerに変更し、  
Heroku CLIで「heroku ps:scale worker=1」を実行

## TODO
+ 型ヒントをつける
+ heroku無料枠だと非稼働時間があるので適当に移植すべき