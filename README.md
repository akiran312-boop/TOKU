# TOKU 自動検索版

この版は「TOKUを開くたびに手作業で検索する」のではなく、
GitHub Actions が毎朝 7:15（日本時間）にOpenAIのWeb検索を実行し、
最新のお得情報を `deals.json` に自動反映します。

## 初回設定

### 1. GitHubに新しいリポジトリを作る
例: `toku`

このZIPの中身をリポジトリ直下へアップロードします。

### 2. OpenAI APIキーをGitHubのSecretに登録
GitHubのリポジトリで:

Settings
→ Secrets and variables
→ Actions
→ New repository secret

Name:
OPENAI_API_KEY

Secret:
OpenAI Platformで作成したAPIキー

※ ChatGPTの契約とAPI料金は別です。

### 3. GitHub PagesをON
Settings
→ Pages
→ Build and deployment
→ Source: Deploy from a branch
→ Branch: main / root
→ Save

少し待つとTOKUのURLが発行されます。

## 動作
- 毎日 7:15 JST に自動検索
- 公式情報を優先
- 期限切れを除外
- `deals.json` を自動更新
- TOKU画面は最新 `deals.json` を自動読込
- 「今日やると得」「得した記録」「購入候補」は各端末のブラウザに保存

## 手動で今すぐ更新
GitHub
→ Actions
→ 「TOKU 毎朝お得情報更新」
→ Run workflow

## 支払いルール
- Amazon: Amazonカード
- Amazon以外: Recruit Card

## 注意
GitHub ActionsでOpenAI APIを利用するため、API利用料金が発生します。
