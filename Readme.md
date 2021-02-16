# Impression-Checker-Bot
+ [Digital Emergency Exit](http://manbow.nothing.sh/event/event.cgi)で行われるイベントのインプレを取得してきてくれるDiscordbot
+ 2020/10/27時点で動作確認済み(DEEのレイアウトがちょっとでも変わったら動かなくなるのであしからず)
+ サーバーは[Heroku](https://jp.heroku.com/)の無料枠
    + 月末は動かなくなる

## デプロイの流れ
+ [基本これでOK](https://qiita.com/1ntegrale9/items/9d570ef8175cf178468f)
+ もし上記の流れでデプロイ後動かない場合は以下などを試してください
+ https://qiita.com/hirokik-0076/items/71c104158fa8b963ba85
+ Procfileのプロセス名(開幕に書くもの)をdiscordbot→workerに変更し、  
Heroku CLIで「heroku ps:scale worker=1」を実行

## TODO
+ 型ヒントをつける
+ heroku無料枠だと月末に止まるので、他に移植したい