import csv
import os

# 世代資訊
generations = [
    {"name": "🌱 第一世代 - 關東地區", "start": 1, "end": 151, "count": 151},
    {"name": "🌸 第二世代 - 城都地區", "start": 152, "end": 251, "count": 100},
    {"name": "🌊 第三世代 - 豐緣地區", "start": 252, "end": 386, "count": 135},
    {"name": "⛰️ 第四世代 - 神奧地區", "start": 387, "end": 493, "count": 107},
    {"name": "🌆 第五世代 - 合眾地區", "start": 494, "end": 649, "count": 156},
    {"name": "🌺 第六世代 - 卡洛斯地區", "start": 650, "end": 721, "count": 72},
    {"name": "🌴 第七世代 - 阿羅拉地區", "start": 722, "end": 809, "count": 88},
    {"name": "🏰 第八世代 - 伽勒爾地區", "start": 810, "end": 905, "count": 96},
    {"name": "🏔️ 第九世代 - 帕底亞地區", "start": 906, "end": 1025, "count": 120}
]

def read_pokemon_data():
    """讀取寶可夢資料"""
    pokemon_data = {}
    try:
        with open('pokemon_data/pokemon_names_tw.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                number = int(row['number'])
                name = row['name']
                if name != "Unknown":
                    pokemon_data[number] = name
    except Exception as e:
        print(f"讀取檔案錯誤: {e}")
        return {}
    return pokemon_data

def generate_html_for_generations(selected_generations, pokemon_data):
    """為選定的世代生成HTML"""
    
    # 計算總數和頁數
    total_pokemon = sum(gen["count"] for gen in selected_generations)
    estimated_pages = (total_pokemon + 14) // 15  # 每頁15隻，向上取整
    
    gen_names = " + ".join([f"第{i+1}世代" for i, gen in enumerate(generations) if gen in selected_generations])
    
    html_header = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>寶可夢注音符號練習表 - {gen_names}</title>
    <style>
        @font-face {{
            font-family: 'BpmfGenSen';
            src: url('fonts/BpmfGenYoMin-R.ttf') format('truetype');
            font-display: swap;
        }}
        
        /* A4橫式印刷設定 */
        @page {{
            size: A4 landscape;
            margin: 12mm 10mm 18mm 10mm;
        }}
        
        body {{
            font-family: 'BpmfGenSen', "PingFang TC", "Microsoft JhengHei", sans-serif;
            margin: 0;
            padding: 0 0 25px 0;
            font-size: 14px;
            line-height: 1.3;
            background: white;
            position: relative;
        }}
        
        .page-header {{
            text-align: center;
            margin-bottom: 12px;
            padding: 8px;
            border-bottom: 3px solid #333;
            page-break-after: avoid;
        }}
        
        .page-header h1 {{
            margin: 0;
            font-size: 22px;
            color: #333;
            font-weight: bold;
        }}
        
        .page-header p {{
            margin: 4px 0 0 0;
            font-size: 12px;
            color: #666;
        }}
        
        /* 表格樣式 - 一排一隻 */
        .pokemon-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
            font-size: 14px;
        }}
        
        .pokemon-table th,
        .pokemon-table td {{
            border: 2px solid #333;
            padding: 8px;
            text-align: center;
            vertical-align: middle;
        }}
        
        .pokemon-table th {{
            background-color: #f0f0f0;
            font-weight: bold;
            font-size: 16px;
            height: 35px;
        }}
        
        .pokemon-row {{
            height: 80px;
            page-break-inside: avoid;
        }}
        
        .number-col {{
            width: 10%;
            font-weight: bold;
            color: #333;
            font-size: 14px;
        }}
        
        .image-col {{
            width: 25%;
            padding: 5px;
        }}
        
        .name-col {{
            width: 30%;
            font-weight: bold;
            font-size: 40px;
        }}
        
        .phonetic-col {{
            width: 35%;
            background-color: #fafafa;
        }}
        
        .pokemon-img {{
            width: 70px;
            height: 70px;
            object-fit: contain;
            border-radius: 5px;
            border: 1px solid #ddd;
        }}
        
        .phonetic-input {{
            width: 90%;
            height: 50px;
            border: none;
            background: white;
            text-align: center;
            font-family: 'BpmfGenSen', monospace;
            font-size: 28px;
            border-radius: 5px;
            padding: 4px;
            color: #333;
            outline: none;
        }}
        
        /* 世代分隔 */
        .generation-divider {{
            background-color: #e9ecef;
            font-weight: bold;
            font-size: 16px;
            height: 40px;
            color: #495057;
        }}
        
        .generation-divider td {{
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            font-weight: bold;
            border: 3px solid #333;
        }}
        
        /* 頁面底部資訊區 */
        .page-footer {{
            position: relative;
            margin-top: 15px;
            padding-top: 8px;
            border-top: 1px solid #ddd;
        }}
        
        /* 頁面計數器 - 修正位置 */
        .page-info {{
            position: absolute;
            bottom: 5px;
            right: 0;
            font-size: 10px;
            color: #666;
            background: white;
            padding: 2px 5px;
            border-radius: 3px;
        }}
        
        /* 使用說明 - 調整位置避免重疊 */
        .usage-info {{
            text-align: center;
            margin: 8px 0;
            padding-right: 80px;
            font-size: 11px;
            color: #666;
        }}
        
        .usage-info p {{
            margin: 3px 0;
            line-height: 1.4;
        }}
        
        /* 印刷優化 */
        @media print {{
            body {{
                font-size: 12px;
                padding-bottom: 20px;
            }}
            
            .pokemon-table {{
                font-size: 12px;
            }}
            
            .pokemon-row {{
                height: 75px;
            }}
            
            .pokemon-img {{
                width: 65px;
                height: 65px;
            }}
            
            .phonetic-input {{
                height: 25px;
                font-size: 12px;
            }}
            
            .page-header h1 {{
                font-size: 20px;
            }}
            
            .usage-info {{
                font-size: 10px;
                padding-right: 70px;
            }}
            
            .page-info {{
                font-size: 9px;
            }}
            
            /* 確保不會分頁切斷 */
            .pokemon-row {{
                page-break-inside: avoid;
            }}
            
            .generation-divider {{
                page-break-after: avoid;
            }}
            
            .page-footer {{
                page-break-inside: avoid;
            }}
        }}
        
        /* 分頁控制 */
        .page-break {{
            page-break-before: always;
        }}
    </style>
</head>
<body>
    <div class="page-header">
        <h1>🎮 寶可夢注音符號練習表</h1>
        <p>{gen_names} • 共{total_pokemon}隻 • A4橫式印刷版 • 一排一隻放大版</p>
    </div>
    
    <table class="pokemon-table">
        <thead>
            <tr>
                <th class="number-col">編號</th>
                <th class="image-col">寶可夢圖片</th>
                <th class="name-col">寶可夢名稱</th>
                <th class="phonetic-col">注音符號練習</th>
            </tr>
        </thead>
        <tbody>
'''
    
    html_content = []
    row_count = 0
    page_count = 1
    
    for gen in selected_generations:
        # 添加世代分隔線
        html_content.append(f'            <tr class="generation-divider">')
        html_content.append(f'                <td colspan="4">{gen["name"]} ({gen["start"]}-{gen["end"]}) • {gen["count"]}隻</td>')
        html_content.append(f'            </tr>')
        
        # 添加該世代的寶可夢
        for num in range(gen["start"], gen["end"] + 1):
            if num in pokemon_data:
                name = pokemon_data[num]
                num_str = str(num).zfill(3)
                
                html_content.append(f'            <tr class="pokemon-row">')
                html_content.append(f'                <td class="number-col">#{num_str}</td>')
                html_content.append(f'                <td class="image-col">')
                html_content.append(f'                    <img src="pokemon_images/{num_str}.png" alt="{name}" class="pokemon-img">')
                html_content.append(f'                </td>')
                html_content.append(f'                <td class="name-col">{name}</td>')
                html_content.append(f'                <td class="phonetic-col">')
                html_content.append(f'                    <input type="text" class="phonetic-input" placeholder="">')
                html_content.append(f'                </td>')
                html_content.append(f'            </tr>')
                
                row_count += 1
                
                # 每15隻寶可夢分頁
                if row_count % 15 == 0 and row_count < total_pokemon:
                    page_count += 1
                    html_content.append('        </tbody>')
                    html_content.append('    </table>')
                    html_content.append('    <div class="page-footer">')
                    html_content.append('        <div class="usage-info">')
                    html_content.append('            <p>📝 列印後可直接在注音符號欄位填寫練習 • 🎯 使用寶可夢注音專用字型</p>')
                    html_content.append('        </div>')
                    html_content.append(f'        <div class="page-info">第 {page_count-1} 頁</div>')
                    html_content.append('    </div>')
                    html_content.append('    <div class="page-break"></div>')
                    html_content.append('    <div class="page-header">')
                    html_content.append('        <h1>🎮 寶可夢注音符號練習表</h1>')
                    html_content.append(f'        <p>{gen_names} • 第 {page_count} 頁 • 一排一隻放大版</p>')
                    html_content.append('    </div>')
                    html_content.append('    <table class="pokemon-table">')
                    html_content.append('        <thead>')
                    html_content.append('            <tr>')
                    html_content.append('                <th class="number-col">編號</th>')
                    html_content.append('                <th class="image-col">寶可夢圖片</th>')
                    html_content.append('                <th class="name-col">寶可夢名稱</th>')
                    html_content.append('                <th class="phonetic-col">注音符號練習</th>')
                    html_content.append('            </tr>')
                    html_content.append('        </thead>')
                    html_content.append('        <tbody>')
    
    html_footer = f'''        </tbody>
    </table>
    
    <div class="page-footer">
        <div class="usage-info">
            <p>📝 使用方法：列印後可直接在注音符號欄位填寫練習 • 適合小朋友學習注音符號</p>
            <p>🎯 字型：使用寶可夢注音專用字型 • 🖊️ 完全空白，讓小朋友自己練習填寫</p>
            <p>📏 格式：A4橫式，一排一隻，放大顯示 • 🚀 小檔案，快速載入</p>
        </div>
        <div class="page-info">第 {page_count} 頁 (共 {page_count} 頁)</div>
    </div>
</body>
</html>'''
    
    # 組合完整HTML
    complete_html = html_header + '\n'.join(html_content) + '\n' + html_footer
    return complete_html, total_pokemon, page_count

def show_generation_menu():
    """顯示世代選擇選單"""
    print("\n🎮 寶可夢注音符號練習表 - 世代選擇器")
    print("=" * 50)
    print("選擇要生成的世代 (可選擇多個)：")
    print()
    
    for i, gen in enumerate(generations, 1):
        print(f"{i}. {gen['name']} ({gen['count']}隻)")
    
    print(f"{len(generations)+1}. 📚 全部世代 (1025隻) - 大檔案，載入較慢")
    print("0. ❌ 退出")
    print()

def get_user_selection():
    """獲取用戶選擇"""
    while True:
        try:
            choices = input("請輸入選擇 (例如: 1,2,3 或 1-3): ").strip()
            
            if choices == "0":
                return None
            
            selected_indices = []
            
            if choices == str(len(generations)+1):
                # 選擇全部
                selected_indices = list(range(len(generations)))
            else:
                # 解析輸入
                for part in choices.split(','):
                    part = part.strip()
                    if '-' in part:
                        start, end = map(int, part.split('-'))
                        selected_indices.extend(range(start-1, end))
                    else:
                        selected_indices.append(int(part)-1)
            
            # 驗證選擇
            valid_indices = [i for i in selected_indices if 0 <= i < len(generations)]
            
            if not valid_indices:
                print("❌ 無效選擇，請重新輸入")
                continue
                
            return [generations[i] for i in sorted(set(valid_indices))]
            
        except (ValueError, IndexError):
            print("❌ 輸入格式錯誤，請重新輸入")

def main():
    """主程式"""
    print("🔄 讀取寶可夢資料...")
    pokemon_data = read_pokemon_data()
    
    if not pokemon_data:
        print("❌ 無法讀取寶可夢資料，請確認檔案存在")
        return
    
    while True:
        show_generation_menu()
        selected_generations = get_user_selection()
        
        if selected_generations is None:
            print("👋 再見！")
            break
        
        print(f"\n🔄 正在生成...")
        print(f"📊 選擇的世代: {len(selected_generations)}個")
        
        html_content, total_pokemon, total_pages = generate_html_for_generations(selected_generations, pokemon_data)
        
        # 生成檔案名稱
        if len(selected_generations) == 1:
            gen_num = next(i+1 for i, gen in enumerate(generations) if gen == selected_generations[0])
            filename = f"pokemon_gen{gen_num}_phonetic.html"
        elif len(selected_generations) == len(generations):
            filename = "pokemon_all_generations_phonetic.html"
        else:
            gen_nums = [str(i+1) for i, gen in enumerate(generations) if gen in selected_generations]
            filename = f"pokemon_gen{'_'.join(gen_nums)}_phonetic.html"
        
        # 寫入檔案
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)
        
        # 顯示結果
        file_size = os.path.getsize(filename) / 1024  # KB
        print(f"\n✅ 生成完成！")
        print(f"📄 檔案名稱: {filename}")
        print(f"🎮 寶可夢數量: {total_pokemon}隻")
        print(f"📑 預估頁數: {total_pages}頁")
        print(f"💾 檔案大小: {file_size:.1f}KB")
        print(f"🚀 載入速度: {'超快' if file_size < 100 else '快' if file_size < 200 else '中等'}")
        print(f"🖊️ 注音欄位: 完全空白，適合練習")
        print()
        
        continue_choice = input("🔄 要繼續生成其他世代嗎？(y/n): ").strip().lower()
        if continue_choice != 'y':
            print("👋 再見！")
            break

if __name__ == "__main__":
    main() 