# 🎮 ポケモン注音記号練習シート

ポケモンの画像と中国語名を見ながら、子供たちが注音記号を練習できるようにするためのPythonプロジェクトです。

**他の言語:** [繁體中文](../../README.md) | [English](README_en.md)

## 🌟 プロジェクトの特徴

- 📸 **完全なデータベース**：1025匹のポケモン画像と中国語名を含む
- 🎯 **世代選択**：単一世代または複数世代の組み合わせ生成をサポート
- 📄 **A4最適化**：横向き印刷レイアウト、実用的な使用に適合
- ✨ **カスタマイズ可能なデザイン**：フォント、サイズ、境界線など複数項目の調整をサポート
- 🚀 **高速読み込み**：スマートページネーション設計、小さなファイルで高速開放
- 🖊️ **境界線なしデザイン**：ミニマルスタイル、コンテンツ入力に集中

## 📋 機能概要

### コア機能
- 🎮 **ポケモンデータ収集**：公式画像と中国語名の自動ダウンロード
- 📝 **練習シート生成**：インタラクティブな世代選択器
- 🛠️ **統合管理ツール**：ワンクリック完全設定とデータ管理
- 📊 **ステータスチェック**：リアルタイムデータ整合性表示

### サポート世代
- 🌱 第1世代 - カントー地方 (151匹)
- 🌸 第2世代 - ジョウト地方 (100匹)  
- 🌊 第3世代 - ホウエン地方 (135匹)
- ⛰️ 第4世代 - シンオウ地方 (107匹)
- 🌆 第5世代 - イッシュ地方 (156匹)
- 🌺 第6世代 - カロス地方 (72匹)
- 🌴 第7世代 - アローラ地方 (88匹)
- 🏰 第8世代 - ガラル地方 (96匹)
- 🏔️ 第9世代 - パルデア地方 (120匹)

## 🚀 クイックスタート

### システム要件
- Python 3.8+
- インターネット接続 (画像ダウンロード用)
- 約150MBのディスク容量

### インストール手順
```bash
# 1. プロジェクトのクローン
git clone https://github.com/tk009999/pokemon-phonetic-practice.git
cd pokemon-phonetic-practice

# 2. 仮想環境の作成
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# または venv\Scripts\activate  # Windows

# 3. 依存関係のインストール
pip install -r requirements.txt

# 4. 統合管理ツールの実行
python pokemon_manager.py
```

### クイック生成
```bash
# 特定の世代を直接生成
python generate_generation_selector.py
```

## 📁 プロジェクト構造

```
pokemon-phonetic-practice/
├── README.md                           # プロジェクト説明
├── DOC_GUIDELINES.md                   # ドキュメントガイドライン
├── pokemon_manager.py                  # 統合管理ツール
├── generate_generation_selector.py     # 練習シートジェネレーター
├── main.py                             # 画像ダウンローダー
├── get_pokemon_names_tw.py             # 名前コレクター
├── requirements.txt                    # Python依存関係
├── fonts/                              # フォントファイル
├── pokemon_data/                       # ポケモンデータ
├── pokemon_images/                     # 画像データ (1025枚)
├── docs/                               # ドキュメント
└── pokemon_gen*_phonetic.html          # 生成された練習シート
```

## 🛠️ 使用方法

### 世代選択器
`generate_generation_selector.py`を実行して練習シートを素早く生成：

- 単一世代：`1` (第1世代)
- 複数世代：`1,2,3` (最初の3世代)
- 範囲：`1-3` (第1世代から第3世代)
- 全て：`10` (全9世代)

## 📖 詳細ドキュメント

- [環境設定ガイド](../SETUP.md) - 詳細なインストールと設定ガイド
- [バージョン履歴](../CHANGELOG.md) - プロジェクト更新記録
- [フォントサイズ調整表](../字級調整對照表.md) - フォントサイズ調整ガイド
- [境界線調整ガイド](../虛線框調整指南.md) - 境界線スタイル調整説明

## 🤝 貢献

このプロジェクトを改善するためのIssueやPull Requestの提出を歓迎します！

## 📄 ライセンス

Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License

---

**�� ポケモン注音記号練習を楽しもう！** 