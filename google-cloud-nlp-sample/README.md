# Google Cloud Natural Language API サンプルプログラム

Google Cloud の **Cloud Natural Language API** を使用して、日本語テキストの感情分析（ポジティブ／ネガティブ）およびエンティティ（地名や固有名詞など）の抽出を行うサンプル Python プログラムです。

## 前提条件

このサンプルを実行するには、以下が必要です。
1. **Google Cloud プロジェクト**
2. **`uv`** (高速な Python パッケージ/プロジェクト管理ツール)

---

## 1. Google Cloud 側の準備

API を実行するために、GCP コンソールで以下の設定を行います。

1. **Natural Language API の有効化**:
   - [Google Cloud コンソール](https://console.cloud.google.com/) にログインします。
   - 上部検索バーで「Cloud Natural Language API」と検索し、API を有効にします。

2. **サービスアカウントの作成とキーの取得**:
   - IAM と管理 > 「サービスアカウント」メニューを開きます。
   - 「サービスアカウントを作成」をクリックし、任意の名前（例: `nlp-api-client`）を入力します。
   - ロールは必要に応じて「Natural Language API 閲覧者（またはサービスアカウントユーザー）」を選択するか、あるいはロールなしで進めます（基本的には API が有効であれば呼び出し可能です）。
   - 作成後、該当 of サービスアカウントの詳細画面を開き、「キー（KEYS）」タブを選択します。
   - 「鍵を追加」 > 「新しい鍵を作成」をクリックし、**JSON** 形式でキーファイルをダウンロードします。
   - ダウンロードしたキーファイルを安全な場所に保管してください（例: `~/keys/gcp-service-account.json`）。

---

## 2. 環境構築と実行手順

### 環境変数の設定

ダウンロードしたサービスアカウントの JSON キーファイルのパスを、環境変数 `GOOGLE_APPLICATION_CREDENTIALS` に設定します。

```bash
# macOS / Linux の場合
export GOOGLE_APPLICATION_CREDENTIALS="/Users/mkiyota1/keys/gcp-service-account.json"
```

### プログラムの実行

`gcp-nlp-sample` ディレクトリに移動してから `uv` を使用してプロジェクトを実行します。

```bash
cd gcp-nlp-sample
```

#### デフォルトテキストで実行する場合:
```bash
uv run analyze_text.py
```

#### 任意のテキストで実行する場合:
```bash
uv run analyze_text.py "今日の天気はとても良くて、散歩をするのが最高に気持ちよかったです。"
```

---

## 3. 出力例

実行に成功すると、以下のような形式で分析結果がターミナルに出力されます。

```text
=== Analyzing Text ===
Input: 今日の天気はとても良くて、散歩をするのが最高に気持ちよかったです。

--- Sentiment Analysis ---
Score: 0.90 (ranges from -1.0 to 1.0)
Magnitude: 0.90 (strength of emotion, >= 0.0)
Interpretation: Positive 🟢

--- Entity Analysis ---
- Name: 天気
  Type: OTHER
  Salience (Importance): 54.32%

- Name: 散歩
  Type: OTHER
  Salience (Importance): 45.68%
```
