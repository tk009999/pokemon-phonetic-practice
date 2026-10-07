import json

from generate_generation_selector import read_pokemon_data

# index.html 用 <script> 載入這個檔案，直接用瀏覽器開啟本機檔案也能運作
output_path = "pokemon_data/pokemon_names_tw.js"

pokemon_data = read_pokemon_data()
names = [[number, name] for number, name in sorted(pokemon_data.items())]

with open(output_path, "w", encoding="utf-8") as f:
    f.write("window.POKEMON_NAMES = ")
    json.dump(names, f, ensure_ascii=False, separators=(",", ":"))
    f.write(";\n")

print(f"✅ 已儲存 {len(names)} 隻寶可夢的網站資料到: {output_path}")
