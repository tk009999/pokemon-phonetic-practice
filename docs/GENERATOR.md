# 🛠️ 自己生成練習表

需要 Python 3.8+、網路連線、約 150MB 磁碟空間。

```bash
git clone https://github.com/tk009999/pokemon-phonetic-practice.git
cd pokemon-phonetic-practice
python3 -m venv venv
source venv/bin/activate        # Windows 改用 venv\Scripts\activate
pip install -r requirements.txt
```

| 指令 | 用途 |
|------|------|
| `python generate_generation_selector.py` | 選擇世代，生成注音練習表 |
| `python generate_handwriting.py` | 選擇世代、格線與尺寸，生成手寫練習表 |
| `python get_stroke_data.py` | 重新下載虛線字用的筆畫資料（名稱資料更新後才需要） |
| `python generate_site_data.py` | 重新產生網站用的名稱資料（名稱資料更新後才需要） |
| `python pokemon_manager.py` | 統合管理：下載圖片、抓取名稱、生成練習表、檢查資料 |

## 世代選擇器的輸入方式

| 輸入 | 結果 |
|------|------|
| `1` | 第一世代 |
| `1,2,3` | 第一、二、三世代 |
| `1-3` | 第一到第三世代 |
| `10` | 全部九個世代（檔案較大） |

## 手寫練習表的選項

| 選項 | 可選值 | 預設 |
|------|--------|------|
| 格線類型 | 田字格、米字格、空白格 | 田字格 |
| 格子尺寸 | 大格 20mm、中格 15mm、小格 12mm | 大格 20mm |
| 描紅格數 | 0 以上的整數（0 為不描紅） | 3 |
| 描紅樣式 | 虛線字（筆畫中線）、淺色字 | 虛線字 |
| 運筆描線暖身頁 | 加入、不加入 | 加入 |

## 📁 專案結構

| 路徑 | 說明 |
|------|------|
| `pokemon_manager.py` | 統合管理工具 |
| `generate_generation_selector.py` | 注音練習表生成器 |
| `generate_handwriting.py` | 手寫練習表生成器 |
| `main.py` | 圖片下載器 |
| `get_pokemon_names_tw.py` | 中文名稱收集器 |
| `get_stroke_data.py` | 筆畫資料收集器 |
| `generate_site_data.py` | 網站資料產生器 |
| `index.html` | 一頁式練習表網站（GitHub Pages） |
| `requirements.txt` | Python 依賴 |
| `fonts/` | 注音字型、教育部標準楷書 |
| `pokemon_data/` | 寶可夢中文名稱（CSV / TXT）、筆畫中線資料（JSON） |
| `pokemon_images/` | 寶可夢圖片（1025 張） |
| `pokemon_gen*_phonetic.html` | 已生成的各世代注音練習表 |
| `pokemon_gen*_handwriting.html` | 已生成的各世代手寫練習表 |
| `docs/` | 文檔 |


## 🔄 更新歷史

- 2026-10-07 by Ace: 由 README 拆出
