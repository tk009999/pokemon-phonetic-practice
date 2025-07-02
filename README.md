# 🎮 寶可夢注音符號練習表

一個用於生成寶可夢注音符號練習表的 Python 專案，讓小朋友可以看著寶可夢圖片和中文名稱來練習填寫注音符號。

**其他語言 / Other Languages:** [English](docs/i18n/README_en.md) | [日本語](docs/i18n/README_ja.md)

## 🌟 專案特色

- 📸 **完整資料庫**：包含 1025 隻寶可夢圖片與中文名稱
- 🎯 **世代選擇**：支援單一世代或多世代組合生成
- 📄 **A4 優化**：橫式列印版面，適合實際使用
- ✨ **客製化設計**：支援字型、字級、邊框等多項調整
- 🚀 **快速載入**：智能分頁設計，小檔案快速開啟
- 🖊️ **無邊框設計**：極簡風格，專注內容填寫

## 📋 功能概覽

### 核心功能
- 🎮 **寶可夢資料收集**：自動下載官方圖片與中文名稱
- 📝 **練習表生成**：互動式世代選擇器
- 🛠️ **統合管理工具**：一鍵完整設置與資料管理
- 📊 **狀態檢查**：即時顯示資料完整性

### 支援世代
- 🌱 第一世代 - 關東地區 (151隻)
- 🌸 第二世代 - 城都地區 (100隻)  
- 🌊 第三世代 - 豐緣地區 (135隻)
- ⛰️ 第四世代 - 神奧地區 (107隻)
- 🌆 第五世代 - 合眾地區 (156隻)
- 🌺 第六世代 - 卡洛斯地區 (72隻)
- 🌴 第七世代 - 阿羅拉地區 (88隻)
- 🏰 第八世代 - 伽勒爾地區 (96隻)
- 🏔️ 第九世代 - 帕底亞地區 (120隻)

## 📄 快速下載練習表

🎯 **一鍵下載各世代注音練習表** - 為家長和老師準備的直接連結

### 🌟 各世代快速連結
> 點擊下載後即可直接列印，建議使用 A4 橫式列印

| 世代 | 地區 | 寶可夢數量 | 下載連結 |
|------|------|------------|----------|
| 🌱 第一世代 | 關東地區 | 151隻 | [📥 下載練習表](pokemon_gen1_phonetic.html) |
| 🌸 第二世代 | 城都地區 | 100隻 | [📥 下載練習表](pokemon_gen2_phonetic.html) |
| 🌊 第三世代 | 豐緣地區 | 135隻 | [📥 下載練習表](pokemon_gen3_phonetic.html) |
| ⛰️ 第四世代 | 神奧地區 | 107隻 | [📥 下載練習表](pokemon_gen4_phonetic.html) |
| 🌆 第五世代 | 合眾地區 | 156隻 | [📥 下載練習表](pokemon_gen5_phonetic.html) |
| 🌺 第六世代 | 卡洛斯地區 | 72隻 | [📥 下載練習表](pokemon_gen6_phonetic.html) |
| 🌴 第七世代 | 阿羅拉地區 | 88隻 | [📥 下載練習表](pokemon_gen7_phonetic.html) |
| 🏰 第八世代 | 伽勒爾地區 | 96隻 | [📥 下載練習表](pokemon_gen8_phonetic.html) |
| 🏔️ 第九世代 | 帕底亞地區 | 120隻 | [📥 下載練習表](pokemon_gen9_phonetic.html) |

### 📝 使用小貼士
- 🖨️ **列印設定**：建議使用 A4 橫式列印，效果最佳
- ✏️ **練習方式**：讓小朋友看著寶可夢圖片和名稱，在空白欄位填寫注音符號
- 🎯 **專用字型**：內建寶可夢注音專用字型，清晰易讀
- 📚 **分批使用**：可以先從第一世代開始，循序漸進

## 🚀 快速開始

### 環境需求
- Python 3.8+
- 網路連線 (用於下載圖片)
- 約 150MB 磁碟空間

### 安裝步驟
```bash
# 1. 複製專案
git clone https://github.com/tk009999/pokemon-phonetic-practice.git
cd pokemon-phonetic-practice

# 2. 建立虛擬環境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 執行統合管理工具
python pokemon_manager.py
```

### 快速生成練習表
```bash
# 直接生成特定世代
python generate_generation_selector.py
```

## 📁 專案結構

```
pokemon-phonetic-practice/
├── README.md                           # 專案說明
├── DOC_GUIDELINES.md                   # 文檔規範
├── pokemon_manager.py                  # 統合管理工具
├── generate_generation_selector.py     # 練習表生成器
├── main.py                             # 圖片下載器
├── get_pokemon_names_tw.py             # 名稱收集器
├── requirements.txt                    # Python 依賴
├── fonts/                              # 字型檔案
├── pokemon_data/                       # 寶可夢資料
├── pokemon_images/                     # 圖片資料 (1025張)
├── docs/                               # 文檔
└── pokemon_gen*_phonetic.html          # 生成的練習表
```

## 🛠️ 使用說明

### 世代選擇器
執行 `generate_generation_selector.py` 快速生成練習表：

- 支援單一世代：`1` (第一世代)
- 支援多世代：`1,2,3` (前三世代)
- 支援範圍：`1-3` (第一到第三世代)
- 支援全部：`10` (全部九個世代)

## 📖 詳細文檔

- [📖 專案背後的故事](STORY.md) - 一位爸爸與寶貝的拼音冒險 ⭐
- [環境設置說明](docs/SETUP.md) - 詳細的安裝與設置指南
- [版本歷史](docs/CHANGELOG.md) - 專案更新記錄
- [字級調整對照表](docs/字級調整對照表.md) - 字體大小調整指南
- [虛線框調整指南](docs/虛線框調整指南.md) - 邊框樣式調整說明

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request 來改善這個專案！

## 📄 授權

Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License

---

## 🔄 更新歷史

最後更新：2024年7月1日  
版本：v1.2.2  
新增功能：九個世代練習表快速下載連結

---

**🎮 享受寶可夢注音符號練習的樂趣！** 