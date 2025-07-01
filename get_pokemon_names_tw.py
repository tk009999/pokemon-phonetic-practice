import os
import requests
from bs4 import BeautifulSoup
import time

# 設定範圍，抓取所有1025隻寶可夢
start_id = 1
end_id = 1025

# 建立資料夾
os.makedirs("pokemon_data", exist_ok=True)

# 建立編號對應名稱的資料結構
num2name = {}

print("🚀 開始從台灣官方圖鑑抓取寶可夢中文名稱...")

# 透過官方台灣圖鑑頁面抓取名稱
success_count = 0
for i in range(start_id, end_id + 1):
    num = str(i).zfill(3)
    url = f"https://tw.portal-pokemon.com/play/pokedex/{num}"
    
    print(f"📝 正在獲取 #{num}...", end=" ")
    
    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            print(f"❌ 無法存取頁面 (HTTP {res.status_code})")
            num2name[num] = "Unknown"
            continue

        soup = BeautifulSoup(res.text, "html.parser")
        
        # 嘗試多個可能的選擇器來找到寶可夢名稱
        name = "Unknown"
        
        # 方法1: 嘗試 h1 標籤
        title = soup.select_one("h1")
        if title and title.text.strip():
            name = title.text.strip().split()[0]
        
        # 方法2: 嘗試其他可能的標籤
        if name == "Unknown":
            name_element = soup.select_one(".pokemon-name") or soup.select_one(".name") or soup.select_one("h2")
            if name_element and name_element.text.strip():
                name = name_element.text.strip().split()[0]
        
        # 方法3: 從頁面標題中提取
        if name == "Unknown":
            page_title = soup.select_one("title")
            if page_title and "寶可夢圖鑑" in page_title.text:
                parts = page_title.text.split()
                for part in parts:
                    if part and part != "寶可夢圖鑑" and not part.isdigit():
                        name = part.replace("｜", "").replace("|", "").strip()
                        break
        
        num2name[num] = name
        
        if name != "Unknown":
            success_count += 1
            print(f"✅ {name}")
        else:
            print(f"❌ 無法找到名稱")
            
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        num2name[num] = "Unknown"
    
    # 避免對網站造成太大壓力
    time.sleep(0.5)

# 輸出對照表 CSV
csv_path = "pokemon_data/pokemon_names_tw.csv"
with open(csv_path, "w", encoding="utf-8") as f:
    f.write("number,name\n")
    for num in sorted(num2name.keys()):
        name = num2name[num]
        f.write(f"{num},{name}\n")

# 建立純文字版本
txt_path = "pokemon_data/pokemon_names_tw.txt"
with open(txt_path, "w", encoding="utf-8") as f:
    for num in sorted(num2name.keys()):
        name = num2name[num]
        if name != "Unknown":
            f.write(f"{num}. {name}\n")

print(f"\n🎉 完成！成功獲取 {success_count}/{end_id} 隻寶可夢中文名稱")
print(f"✅ 已儲存對照表到: {csv_path}")
print(f"✅ 已建立純文字版本: {txt_path}")
print("📚 這些中文名稱很適合轉換成注音符號給小朋友練習！") 