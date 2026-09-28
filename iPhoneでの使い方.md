# TOKU iPhone版

これはGitHub Pagesで公開して、iPhoneのホーム画面へ追加して使うPWA版です。

## 最初の設定
1. GitHubにこのフォルダの中身をアップロード
2. GitHub ActionsのSecretに `OPENAI_API_KEY` を登録
3. GitHub Pagesを有効化
4. 発行されたTOKUのURLをiPhoneのSafariで開く

## iPhoneへの入れ方
SafariでTOKUを開く
→ 共有ボタン
→ 「ホーム画面に追加」
→ 「追加」

これでホーム画面にTOKUアイコンが出ます。

## 普段
TOKUアイコンをタップするだけ。

毎朝7:15ごろにGitHub Actionsが最新のお得情報を検索し、
TOKUの `deals.json` を自動更新します。

## 補足
- App Storeへの公開は不要
- iPhoneを起動していなくてもサーバー側の毎朝更新は動く
- TOKUを開くと最新のお得情報を読み込む
- AmazonはAmazonカード、それ以外はRecruit Cardを基本ルールに設定
