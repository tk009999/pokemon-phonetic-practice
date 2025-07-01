import os
import requests

# 設定下載範圍（所有九個世代 001 ~ 1025）
start_id = 1
end_id = 1025

# 圖片儲存資料夾
save_dir = "pokemon_images"
os.makedirs(save_dir, exist_ok=True)

# 基礎 URL 模板
base_url = "https://assets.pokemon.com/assets/cms2/img/pokedex/full/{}.png"

# 開始下載
for i in range(start_id, end_id + 1):
    number_str = str(i).zfill(3)
    url = base_url.format(number_str)
    filename = f"{number_str}.png"
    save_path = os.path.join(save_dir, filename)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(f"✅ 已下載：{filename}")
        else:
            print(f"❌ 找不到圖片：{url}")
    except Exception as e:
        print(f"⚠️ 錯誤：{filename} - {e}")
