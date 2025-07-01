# 🛠️ 環境設置說明

## 系統需求

### 作業系統支援
- ✅ macOS 10.14+
- ✅ Windows 10+
- ✅ Linux (Ubuntu 18.04+)

### 軟體需求
- **Python 3.8+** (建議 3.9+)
- **pip** (Python 套件管理器)
- **Git** (版本控制)
- **網路連線** (用於下載寶可夢資料)

### 硬體需求
- **磁碟空間**：至少 150MB 可用空間
  - 程式碼：約 20MB
  - 寶可夢圖片：約 129MB (1025張圖片)
  - 生成的 HTML 檔案：約 1-10MB
- **記憶體**：至少 512MB RAM
- **網路頻寬**：建議 10Mbps+ (首次下載圖片時)

## 🚀 安裝步驟

### 1. 複製專案
```bash
# 使用 HTTPS
git clone https://github.com/tk009999/pokemon-phonetic-practice.git

# 或使用 SSH (如果已設置 SSH Key)
git clone git@github.com:tk009999/pokemon-phonetic-practice.git

# 進入專案目錄
cd pokemon-phonetic-practice
```

### 2. Python 環境檢查
```bash
# 檢查 Python 版本
python3 --version
# 應該顯示 Python 3.8.0 或更高版本

# 檢查 pip 版本
pip3 --version
```

**如果沒有 Python**：
- **macOS**：`brew install python3` 或從 [python.org](https://python.org) 下載
- **Windows**：從 [python.org](https://python.org) 下載安裝包
- **Linux**：`sudo apt-get install python3 python3-pip`

### 3. 建立虛擬環境
```bash
# 建立虛擬環境
python3 -m venv venv

# 啟動虛擬環境
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# 成功啟動後，命令列前方會顯示 (venv)
```

### 4. 安裝 Python 依賴
```bash
# 升級 pip 到最新版本
pip install --upgrade pip

# 安裝專案依賴
pip install -r requirements.txt
```

**依賴套件說明**：
- `requests>=2.32.0` - HTTP 請求庫，用於下載圖片和網頁內容
- `beautifulsoup4>=4.13.0` - HTML 解析庫，用於抓取寶可夢名稱

### 5. 驗證安裝
```bash
# 檢查已安裝的套件
pip list

# 測試核心功能
python -c "import requests, bs4; print('依賴安裝成功！')"
```

## 🎮 首次使用設置

### 自動設置 (推薦)
```bash
# 執行統合管理工具
python pokemon_manager.py

# 選擇選項 4：一鍵完整設置
# 此選項會自動：
# 1. 下載全部 1025 張寶可夢圖片
# 2. 抓取台灣官方中文名稱
# 3. 驗證資料完整性
```

### 手動設置
```bash
# 1. 下載寶可夢圖片 (約 5-10 分鐘)
python main.py

# 2. 抓取中文名稱 (約 1-2 分鐘)
python get_pokemon_names_tw.py

# 3. 生成練習表
python generate_generation_selector.py
```

## 📁 目錄結構驗證

設置完成後，專案目錄應該包含：

```
pokemon-phonetic-practice/
├── venv/                    ✅ 虛擬環境
├── pokemon_images/          ✅ 1025 張圖片
│   ├── 001.png
│   ├── 002.png
│   └── ... (共 1025 張)
├── pokemon_data/            ✅ 名稱資料
│   ├── pokemon_names_tw.csv
│   └── pokemon_names_tw.txt
├── fonts/                   ✅ 字型檔案
│   ├── BpmfGenSenRounded-R.ttf
│   └── BpmfGenYoMin-R.ttf
└── docs/                    ✅ 文檔
```

## 🔧 常見問題與解決方案

### Python 版本問題
**問題**：`python3` 命令找不到
```bash
# 解決方案：使用 python 而非 python3
python --version

# 或創建別名 (macOS/Linux)
alias python3=python
```

### 套件安裝失敗
**問題**：`pip install` 失敗
```bash
# 解決方案1：升級 pip
python -m pip install --upgrade pip

# 解決方案2：使用國內鏡像 (中國用戶)
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 解決方案3：檢查網路連線
ping pypi.org
```

### 圖片下載緩慢
**問題**：寶可夢圖片下載很慢
```bash
# 解決方案：分批下載
python pokemon_manager.py
# 選擇選項 1，按世代分批下載
```

### 虛擬環境問題
**問題**：虛擬環境無法啟動
```bash
# 解決方案：重新建立虛擬環境
rm -rf venv  # 刪除舊環境
python3 -m venv venv  # 重新建立
source venv/bin/activate  # 重新啟動
```

### 權限問題 (Linux/macOS)
**問題**：沒有寫入權限
```bash
# 解決方案：檢查目錄權限
ls -la
chmod 755 .  # 給予執行權限
```

### Windows 路徑問題
**問題**：路徑包含中文字符
```bash
# 解決方案：使用英文路徑
# 建議將專案放在 C:\pokemon-phonetic\ 等英文路徑下
```

## 📊 效能優化建議

### 記憶體優化
- 如果記憶體不足，可分批生成練習表（單一世代）
- 避免同時開啟多個大型 HTML 檔案

### 磁碟空間管理
```bash
# 檢查各目錄大小
du -sh pokemon_images/  # 約 129MB
du -sh pokemon_data/    # 約 1MB
du -sh *.html          # 各檔案 50KB-500KB

# 清理不需要的 HTML 檔案
rm pokemon_gen*_phonetic.html
```

### 網路優化
- 使用穩定的網路連線進行首次設置
- 考慮在非尖峰時段下載圖片
- 如有網路限制，可使用行動熱點

## 🎯 驗證清單

設置完成後，請確認以下項目：

- [ ] Python 版本 3.8+
- [ ] 虛擬環境已啟動 (命令列顯示 `(venv)`)
- [ ] 依賴套件已安裝 (`pip list` 顯示 requests, beautifulsoup4)
- [ ] 寶可夢圖片已下載 (1025 張 PNG 檔案)
- [ ] 中文名稱已收集 (CSV 和 TXT 檔案存在)
- [ ] 字型檔案已就位 (2 個 TTF 檔案)
- [ ] 可成功生成練習表 (HTML 檔案生成)

## 🔄 更新與維護

### 更新專案
```bash
# 拉取最新版本
git pull origin main

# 更新依賴
pip install -r requirements.txt --upgrade
```

### 重新設置
```bash
# 完全重置 (謹慎使用)
rm -rf pokemon_images/ pokemon_data/ *.html
python pokemon_manager.py  # 選擇選項 4
```

## 🔄 更新歷史
- 2024-07-01 by Assistant: 初始版本建立，包含完整安裝指南 