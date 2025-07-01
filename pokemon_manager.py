import os
import requests
from bs4 import BeautifulSoup
import time
import csv

class PokemonManager:
    def __init__(self):
        self.total_pokemon = 1025
        self.save_dir = "pokemon_images"
        self.data_dir = "pokemon_data"
        self.base_url = "https://assets.pokemon.com/assets/cms2/img/pokedex/full/{}.png"
        
        # 建立必要資料夾
        os.makedirs(self.save_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
    
    def show_main_menu(self):
        """顯示主選單"""
        print("\n" + "="*60)
        print("🎮 寶可夢注音符號練習表 - 管理工具")
        print("="*60)
        print("請選擇要執行的功能：")
        print()
        print("1. 📥 下載寶可夢圖片")
        print("2. 📝 抓取寶可夢中文名稱")
        print("3. 📋 生成注音符號練習表")
        print("4. 🚀 一鍵完整設置（圖片+名稱+練習表）")
        print("5. 📊 檢查現有資料狀態")
        print("6. 🧹 清理資料")
        print("0. ❌ 退出程式")
        print()
    
    def download_pokemon_images(self, start_id=1, end_id=None):
        """下載寶可夢圖片"""
        if end_id is None:
            end_id = self.total_pokemon
        
        print(f"\n🚀 開始下載寶可夢圖片 ({start_id}-{end_id})...")
        print(f"📁 儲存位置: {self.save_dir}/")
        
        success_count = 0
        failed_count = 0
        
        for i in range(start_id, end_id + 1):
            number_str = str(i).zfill(3)
            url = self.base_url.format(number_str)
            filename = f"{number_str}.png"
            save_path = os.path.join(self.save_dir, filename)
            
            # 如果檔案已存在，跳過
            if os.path.exists(save_path):
                print(f"⏭️  已存在：{filename}")
                success_count += 1
                continue
            
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    with open(save_path, "wb") as f:
                        f.write(response.content)
                    print(f"✅ 已下載：{filename}")
                    success_count += 1
                else:
                    print(f"❌ 找不到圖片：{filename} (HTTP {response.status_code})")
                    failed_count += 1
            except Exception as e:
                print(f"⚠️ 錯誤：{filename} - {e}")
                failed_count += 1
            
            # 避免對伺服器造成壓力
            time.sleep(0.1)
        
        print(f"\n📊 下載完成！")
        print(f"✅ 成功：{success_count} 張")
        print(f"❌ 失敗：{failed_count} 張")
        return success_count, failed_count
    
    def fetch_pokemon_names(self, start_id=1, end_id=None):
        """抓取寶可夢中文名稱"""
        if end_id is None:
            end_id = self.total_pokemon
        
        print(f"\n🚀 開始從台灣官方圖鑑抓取寶可夢中文名稱 ({start_id}-{end_id})...")
        
        num2name = {}
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
        
        # 儲存結果
        self.save_pokemon_names(num2name)
        
        print(f"\n📊 抓取完成！")
        print(f"✅ 成功獲取：{success_count}/{end_id-start_id+1} 隻寶可夢中文名稱")
        return success_count, num2name
    
    def save_pokemon_names(self, num2name):
        """儲存寶可夢名稱資料"""
        # 輸出對照表 CSV
        csv_path = os.path.join(self.data_dir, "pokemon_names_tw.csv")
        with open(csv_path, "w", encoding="utf-8") as f:
            f.write("number,name\n")
            for num in sorted(num2name.keys()):
                name = num2name[num]
                f.write(f"{num},{name}\n")

        # 建立純文字版本
        txt_path = os.path.join(self.data_dir, "pokemon_names_tw.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            for num in sorted(num2name.keys()):
                name = num2name[num]
                if name != "Unknown":
                    f.write(f"{num}. {name}\n")

        print(f"✅ 已儲存對照表到: {csv_path}")
        print(f"✅ 已建立純文字版本: {txt_path}")
    
    def generate_practice_sheet(self):
        """生成注音符號練習表"""
        print("\n🚀 啟動注音符號練習表生成器...")
        
        # 檢查是否有必要的資料
        csv_path = os.path.join(self.data_dir, "pokemon_names_tw.csv")
        if not os.path.exists(csv_path):
            print("❌ 找不到寶可夢中文名稱資料！")
            print("💡 請先執行選項 2 抓取寶可夢中文名稱")
            return False
        
        # 執行生成器
        try:
            import subprocess
            result = subprocess.run(["python", "generate_generation_selector.py"], 
                                  capture_output=False, text=True)
            return True
        except Exception as e:
            print(f"❌ 執行生成器時發生錯誤: {e}")
            print("💡 請確認 generate_generation_selector.py 檔案存在")
            return False
    
    def check_data_status(self):
        """檢查現有資料狀態"""
        print("\n📊 檢查現有資料狀態...")
        print("-" * 50)
        
        # 檢查圖片
        image_count = 0
        if os.path.exists(self.save_dir):
            image_files = [f for f in os.listdir(self.save_dir) if f.endswith('.png')]
            image_count = len(image_files)
        
        print(f"📥 寶可夢圖片: {image_count}/{self.total_pokemon} 張")
        
        # 檢查名稱資料
        csv_path = os.path.join(self.data_dir, "pokemon_names_tw.csv")
        name_count = 0
        valid_names = 0
        
        if os.path.exists(csv_path):
            try:
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        name_count += 1
                        if row['name'] != "Unknown":
                            valid_names += 1
            except Exception as e:
                print(f"❌ 讀取名稱資料時發生錯誤: {e}")
        
        print(f"📝 寶可夢中文名稱: {valid_names}/{self.total_pokemon} 個有效名稱")
        print(f"   (總計 {name_count} 筆記錄)")
        
        # 檢查練習表生成器
        generator_exists = os.path.exists("generate_generation_selector.py")
        print(f"📋 練習表生成器: {'✅ 已安裝' if generator_exists else '❌ 未找到'}")
        
        # 檢查字型檔案
        font_exists = os.path.exists("fonts/BpmfGenSenRounded-R.ttf")
        print(f"🎨 注音字型檔案: {'✅ 已安裝' if font_exists else '❌ 未找到'}")
        
        print("-" * 50)
        
        # 給出建議
        if image_count < self.total_pokemon:
            print(f"💡 建議: 執行選項 1 下載剩餘的 {self.total_pokemon - image_count} 張圖片")
        
        if valid_names < self.total_pokemon * 0.8:  # 少於80%
            print(f"💡 建議: 執行選項 2 抓取更多寶可夢中文名稱")
        
        if not generator_exists:
            print("💡 建議: 練習表生成器檔案遺失，請重新建立")
        
        return {
            'images': image_count,
            'names': valid_names,
            'generator': generator_exists,
            'font': font_exists
        }
    
    def clean_data(self):
        """清理資料"""
        print("\n🧹 資料清理選項:")
        print("1. 🗑️ 清理所有圖片")
        print("2. 🗑️ 清理名稱資料")
        print("3. 🗑️ 清理全部資料")
        print("0. ⬅️ 返回主選單")
        
        choice = input("\n請選擇清理選項: ").strip()
        
        if choice == "1":
            confirm = input("⚠️ 確定要刪除所有圖片嗎？(y/N): ").strip().lower()
            if confirm == 'y':
                import shutil
                if os.path.exists(self.save_dir):
                    shutil.rmtree(self.save_dir)
                    os.makedirs(self.save_dir, exist_ok=True)
                print("✅ 已清理所有圖片")
        
        elif choice == "2":
            confirm = input("⚠️ 確定要刪除名稱資料嗎？(y/N): ").strip().lower()
            if confirm == 'y':
                csv_path = os.path.join(self.data_dir, "pokemon_names_tw.csv")
                txt_path = os.path.join(self.data_dir, "pokemon_names_tw.txt")
                for path in [csv_path, txt_path]:
                    if os.path.exists(path):
                        os.remove(path)
                print("✅ 已清理名稱資料")
        
        elif choice == "3":
            confirm = input("⚠️ 確定要刪除全部資料嗎？這個動作無法復原！(y/N): ").strip().lower()
            if confirm == 'y':
                import shutil
                for dir_path in [self.save_dir, self.data_dir]:
                    if os.path.exists(dir_path):
                        shutil.rmtree(dir_path)
                        os.makedirs(dir_path, exist_ok=True)
                print("✅ 已清理全部資料")
    
    def full_setup(self):
        """一鍵完整設置"""
        print("\n🚀 開始一鍵完整設置...")
        print("這將執行：下載圖片 → 抓取名稱 → 生成練習表")
        
        confirm = input("\n⏰ 這個過程可能需要20-30分鐘，確定要繼續嗎？(y/N): ").strip().lower()
        if confirm != 'y':
            print("❌ 已取消")
            return
        
        # 步驟1: 下載圖片
        print("\n📥 步驟 1/3：下載寶可夢圖片...")
        success_img, failed_img = self.download_pokemon_images()
        
        # 步驟2: 抓取名稱
        print("\n📝 步驟 2/3：抓取寶可夢中文名稱...")
        success_name, _ = self.fetch_pokemon_names()
        
        # 步驟3: 生成練習表
        print("\n📋 步驟 3/3：生成注音符號練習表...")
        generator_success = self.generate_practice_sheet()
        
        # 總結
        print("\n" + "="*50)
        print("🎉 一鍵設置完成！")
        print("="*50)
        print(f"📥 圖片下載: {success_img}/{self.total_pokemon} 張成功")
        print(f"📝 名稱抓取: {success_name}/{self.total_pokemon} 個成功")
        print(f"📋 練習表生成: {'✅ 成功' if generator_success else '❌ 失敗'}")
        print("="*50)
        print("🎮 現在可以開始使用寶可夢注音符號練習表了！")
    
    def get_range_input(self):
        """獲取範圍輸入"""
        print(f"\n請輸入範圍 (預設: 1-{self.total_pokemon}):")
        print("範例: 1-151 (第一世代), 1-10 (測試用)")
        
        range_input = input("輸入範圍或直接按 Enter 使用預設: ").strip()
        
        if not range_input:
            return 1, self.total_pokemon
        
        try:
            if '-' in range_input:
                start, end = map(int, range_input.split('-'))
                return max(1, start), min(self.total_pokemon, end)
            else:
                num = int(range_input)
                return num, num
        except ValueError:
            print("❌ 格式錯誤，使用預設範圍")
            return 1, self.total_pokemon
    
    def run(self):
        """主程式執行"""
        while True:
            self.show_main_menu()
            choice = input("請選擇功能 (0-6): ").strip()
            
            if choice == "0":
                print("👋 再見！感謝使用寶可夢注音符號練習表管理工具！")
                break
            
            elif choice == "1":
                start, end = self.get_range_input()
                self.download_pokemon_images(start, end)
            
            elif choice == "2":
                start, end = self.get_range_input()
                self.fetch_pokemon_names(start, end)
            
            elif choice == "3":
                self.generate_practice_sheet()
            
            elif choice == "4":
                self.full_setup()
            
            elif choice == "5":
                self.check_data_status()
            
            elif choice == "6":
                self.clean_data()
            
            else:
                print("❌ 無效選擇，請重新輸入")
            
            # 暫停讓用戶看到結果
            if choice != "0":
                input("\n按 Enter 繼續...")

if __name__ == "__main__":
    print("🎮 寶可夢注音符號練習表管理工具啟動中...")
    manager = PokemonManager()
    manager.run() 