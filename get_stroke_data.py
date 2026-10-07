import csv
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor

import requests

# 筆畫中線資料來源：Hanzi Writer Data（取自 Make Me a Hanzi，Arphic Public License）
base_url = "https://cdn.jsdelivr.net/npm/hanzi-writer-data@2.0/{}.json"
csv_path = os.path.join("pokemon_data", "pokemon_names_tw.csv")
output_path = os.path.join("pokemon_data", "stroke_medians.json")

# 收集所有寶可夢名稱用到的漢字
characters = set()
with open(csv_path, "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        characters.update(re.findall(r'[一-鿿]', row["name"]))

session = requests.Session()

def fetch_medians(char):
    """抓取一個字每一筆的中線，找不到回傳 None"""
    try:
        response = session.get(base_url.format(char), timeout=20)
        if response.status_code != 200:
            return char, None
        return char, response.json()["medians"]
    except Exception as e:
        print(f"❌ {char} 下載失敗: {e}")
        return char, None

print(f"🔄 下載筆畫資料中，共 {len(characters)} 個字...")
with ThreadPoolExecutor(max_workers=8) as executor:
    results = dict(executor.map(fetch_medians, sorted(characters)))

medians = {char: data for char, data in results.items() if data}
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(medians, f, ensure_ascii=False, separators=(",", ":"))

missing = sorted(characters - set(medians))
print(f"✅ 已儲存 {len(medians)} 個字的筆畫資料到: {output_path}")
if missing:
    print(f"⚠️ 找不到筆畫資料的字 ({len(missing)}): {''.join(missing)}")
