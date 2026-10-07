import json
import os
import re

from generate_generation_selector import generations, read_pokemon_data, get_user_selection

# 格線類型
grid_types = {
    "1": {"key": "tian", "name": "田字格", "suffix": ""},
    "2": {"key": "mi", "name": "米字格", "suffix": "_mi"},
    "3": {"key": "blank", "name": "空白格", "suffix": "_blank"},
}

# 格子尺寸 (mm)
grid_sizes = {
    "1": {"mm": 20, "name": "大格 20mm (低年級)", "suffix": ""},
    "2": {"mm": 15, "name": "中格 15mm (中年級)", "suffix": "_m"},
    "3": {"mm": 12, "name": "小格 12mm (高年級)", "suffix": "_s"},
}

# 描紅樣式
trace_styles = {
    "1": {"key": "dashed", "name": "虛線字 (沿著筆畫中間的虛線描)", "suffix": ""},
    "2": {"key": "gray", "name": "淺色字 (照著淺色字描)", "suffix": "_gray"},
}

# A4 橫式扣掉邊界與左側資訊欄後，可放格子的寬度 (mm)
GRID_AREA_WIDTH = 232

# 格線用 SVG 當背景，虛線才能跟著格子尺寸縮放
GRID_LINES = {
    "tian": "M50 0V100M0 50H100",
    "mi": "M50 0V100M0 50H100M0 0L100 100M100 0L0 100",
    "blank": "",
}

# 筆畫中線資料的座標：1024 見方、y 軸朝上、基線在 124
MEDIAN_EM = 1024
MEDIAN_TOP = 900
# 字佔格子的比例，範字和虛線字共用
CHAR_SCALE = 0.8

# 虛線字的線條樣式；<use> 引用的內容吃不到頁面 CSS，直接寫在 symbol 上
STROKE_STYLE = ('fill="none" stroke="#777" stroke-width="22" stroke-dasharray="38 34" '
                'stroke-linecap="round" stroke-linejoin="round"')

def read_stroke_medians():
    """讀取筆畫中線資料（由 get_stroke_data.py 產生）"""
    try:
        with open('pokemon_data/stroke_medians.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"讀取筆畫資料錯誤: {e}")
        return {}

def stroke_symbol(char, medians):
    """把一個字的筆畫中線轉成可重複引用的 SVG symbol"""
    view_size = MEDIAN_EM / CHAR_SCALE
    offset = (MEDIAN_EM - view_size) / 2
    paths = []
    for stroke in medians:
        points = " ".join(f"{x} {MEDIAN_TOP - y}" for x, y in stroke)
        paths.append(f'<path d="M{points}"/>')
    return (f'<symbol id="u{ord(char):x}" viewBox="{offset:.0f} {offset:.0f} {view_size:.0f} {view_size:.0f}" {STROKE_STYLE}>'
            f'{"".join(paths)}</symbol>')

# 運筆描線暖身頁的路徑寬高 (mm)
STROKE_WIDTH = 220
STROKE_HEIGHT = 22

def stroke_paths():
    """運筆描線的路徑：橫線、鋸齒、波浪、城牆、彈跳、圈圈"""
    w, top, mid, bottom = STROKE_WIDTH, 3, STROKE_HEIGHT // 2, STROKE_HEIGHT - 3
    zigzag = " ".join(f"L{x} {top if i % 2 == 0 else bottom}" for i, x in enumerate(range(10, w + 1, 10)))
    wave = " ".join(f"Q{x + 5} {top - 6 if i % 2 == 0 else bottom + 6} {x + 10} {mid}"
                    for i, x in enumerate(range(0, w, 10)))
    castle = " ".join(f"V{top if i % 2 == 0 else bottom} H{x + 11}" for i, x in enumerate(range(0, w, 11)))
    bounce = " ".join(f"A10 {bottom - top} 0 0 1 {x + 20} {bottom}" for x in range(0, w, 20))
    loops = " ".join(f"C{x + 16} {bottom} {x + 22} {top - 4} {x + 12} {top - 4} "
                     f"C{x + 2} {top - 4} {x + 4} {bottom} {x + 20} {bottom}" for x in range(0, w, 20))
    return [
        f"M0 {mid} H{w}",
        f"M0 {bottom} {zigzag}",
        f"M0 {mid} {wave}",
        f"M0 {bottom} {castle}",
        f"M0 {bottom} {bounce}",
        f"M0 {bottom} {loops}",
    ]

POKE_BALL = ('<svg class="poke-ball" viewBox="0 0 100 100">'
             '<circle cx="50" cy="50" r="46" fill="#fff" stroke="#333" stroke-width="5"/>'
             '<path d="M4 50a46 46 0 0 1 92 0z" fill="#e53935" stroke="#333" stroke-width="5"/>'
             '<circle cx="50" cy="50" r="13" fill="#fff" stroke="#333" stroke-width="5"/></svg>')

def warmup_page(pokemon_numbers):
    """運筆描線暖身頁：從寶可夢一路描到精靈球"""
    html = ['    <div class="warmup-page">',
            '        <div class="generation-divider">🖍️ 運筆描線暖身 • 沿著虛線，把寶可夢送回精靈球</div>']
    for num, path in zip(pokemon_numbers, stroke_paths()):
        num_str = str(num).zfill(3)
        html.append('        <div class="stroke-row">')
        html.append(f'            <img src="pokemon_images/{num_str}.png" alt="" class="stroke-img">')
        html.append(f'            <svg class="stroke-path" viewBox="0 0 {STROKE_WIDTH} {STROKE_HEIGHT}"><path d="{path}"/></svg>')
        html.append(f'            {POKE_BALL}')
        html.append('        </div>')
    html.append('    </div>')
    return html

PAGE_CSS = '''
        @font-face {
            font-family: 'BpmfGenSen';
            src: url('fonts/BpmfGenYoMin-R.ttf') format('truetype');
            font-display: swap;
        }

        /* 教育部標準楷書，範字和淺色字使用 */
        @font-face {
            font-family: 'MoeKai';
            src: url('fonts/edukai-5.0.ttf') format('truetype');
            font-display: swap;
        }

        /* A4橫式印刷設定 */
        @page {
            size: A4 landscape;
            margin: 10mm;
        }

        body {
            font-family: "PingFang TC", "Microsoft JhengHei", sans-serif;
            margin: 0;
            padding: 0;
            background: white;
            color: #333;
            /* 沒勾「背景圖形」也要印出格線 */
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }

        .page-header {
            text-align: center;
            margin-bottom: 4mm;
            padding: 2mm;
            border-bottom: 3px solid #333;
        }

        .page-header h1 {
            margin: 0;
            font-size: 22px;
        }

        .page-header p {
            margin: 4px 0 0 0;
            font-size: 12px;
            color: #666;
        }

        .generation-divider {
            margin: 4mm 0 3mm 0;
            padding: 2mm;
            text-align: center;
            font-weight: bold;
            font-size: 16px;
            border: 2px solid #333;
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            page-break-after: avoid;
        }

        /* 一隻寶可夢一個區塊，不跨頁 */
        .pokemon-block {
            display: flex;
            align-items: center;
            margin-bottom: 5mm;
            page-break-inside: avoid;
            break-inside: avoid;
        }

        .pokemon-info {
            width: 42mm;
            flex-shrink: 0;
            text-align: center;
        }

        .pokemon-number {
            font-size: 12px;
            font-weight: bold;
            color: #666;
        }

        .pokemon-img {
            width: 26mm;
            height: 26mm;
            object-fit: contain;
        }

        .pokemon-name {
            font-family: 'BpmfGenSen', "PingFang TC", "Microsoft JhengHei", sans-serif;
            font-size: 20px;
            font-weight: bold;
        }

        .char-row {
            display: flex;
        }

        /* 手寫格 */
        .cell {
            box-sizing: border-box;
            flex-shrink: 0;
            margin: 0 -0.3mm -0.3mm 0;
            border: 0.3mm solid #333;
            background-size: 100% 100%;
            font-family: 'MoeKai', "BiauKai", "Kaiti TC", "DFKai-SB", "標楷體", serif;
            font-style: normal;
            text-align: center;
            overflow: hidden;
        }

        .cell.model {
            color: #222;
        }

        .cell.trace {
            color: #d0d0d0;
        }

        /* 虛線字：筆畫中線，一筆一條虛線 */
        .stroke-defs {
            position: absolute;
            width: 0;
            height: 0;
        }

        /* 運筆描線暖身頁 */
        .warmup-page {
            page-break-after: always;
            break-after: page;
        }

        .stroke-row {
            display: flex;
            align-items: center;
            margin-bottom: 3mm;
        }

        .stroke-img {
            width: 22mm;
            height: 22mm;
            object-fit: contain;
            flex-shrink: 0;
        }

        .stroke-path {
            width: 220mm;
            height: 22mm;
            margin: 0 4mm;
            flex-shrink: 0;
            overflow: visible;
        }

        .stroke-path path {
            fill: none;
            stroke: #888;
            stroke-width: 0.7;
            stroke-dasharray: 2.5 2;
            stroke-linecap: round;
            stroke-linejoin: round;
        }

        .poke-ball {
            width: 14mm;
            height: 14mm;
            flex-shrink: 0;
        }

        .usage-info {
            margin-top: 4mm;
            padding-top: 2mm;
            border-top: 1px solid #ddd;
            text-align: center;
            font-size: 11px;
            color: #666;
        }
'''

def grid_css(grid_key, size_mm):
    """依格線類型與尺寸產生手寫格的 CSS"""
    lines = GRID_LINES[grid_key]
    background = "none"
    if lines:
        svg = (f"%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100' preserveAspectRatio='none'%3E"
               f"%3Cpath d='{lines}' stroke='%23aaa' stroke-width='1' stroke-dasharray='4 4' fill='none'/%3E%3C/svg%3E")
        background = f'url("data:image/svg+xml,{svg}")'

    return f'''
        .cell {{
            width: {size_mm}mm;
            height: {size_mm}mm;
            line-height: {size_mm}mm;
            font-size: {size_mm * CHAR_SCALE:.1f}mm;
            background-image: {background};
        }}
'''

def generate_handwriting_html(selected_generations, pokemon_data, grid_type, grid_size, trace_count=3, trace_style=None, warmup=True):
    """為選定的世代生成手寫練習表HTML"""

    size_mm = grid_size["mm"]
    cells_per_row = GRID_AREA_WIDTH // size_mm
    trace_count = max(0, min(trace_count, cells_per_row - 1))
    blank_count = cells_per_row - 1 - trace_count
    trace_style = trace_style or trace_styles["1"]
    stroke_medians = read_stroke_medians() if trace_style["key"] == "dashed" else {}
    used_characters = set()

    def trace_cell(char):
        # 沒有筆畫資料的字退回淺色字
        if char in stroke_medians:
            used_characters.add(char)
            return f'<svg class="cell"><use href="#u{ord(char):x}"/></svg>'
        return f'<i class="cell trace">{char}</i>'

    gen_names = " + ".join([f"第{i+1}世代" for i, gen in enumerate(generations) if gen in selected_generations])
    size_name = grid_size["name"].split(" (")[0]

    html_content = []
    total_pokemon = 0

    if warmup:
        numbers = [num for gen in selected_generations
                   for num in range(gen["start"], gen["end"] + 1) if num in pokemon_data]
        html_content.extend(warmup_page(numbers))

    for gen in selected_generations:
        html_content.append(f'    <div class="generation-divider">{gen["name"]} ({gen["start"]}-{gen["end"]}) • {gen["count"]}隻</div>')

        for num in range(gen["start"], gen["end"] + 1):
            if num not in pokemon_data:
                continue

            name = pokemon_data[num]
            num_str = str(num).zfill(3)
            # 只練習漢字，略過「・」「：」「Ｚ」等符號
            characters = re.findall(r'[一-鿿]', name)

            html_content.append('    <div class="pokemon-block">')
            html_content.append('        <div class="pokemon-info">')
            html_content.append(f'            <div class="pokemon-number">#{num_str}</div>')
            html_content.append(f'            <img src="pokemon_images/{num_str}.png" alt="{name}" class="pokemon-img">')
            html_content.append(f'            <div class="pokemon-name">{name}</div>')
            html_content.append('        </div>')
            html_content.append('        <div class="char-grid">')
            for char in characters:
                cells = (f'<i class="cell model">{char}</i>'
                         + trace_cell(char) * trace_count
                         + '<i class="cell"></i>' * blank_count)
                html_content.append(f'            <div class="char-row">{cells}</div>')
            html_content.append('        </div>')
            html_content.append('    </div>')

            total_pokemon += 1

    html_header = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>寶可夢手寫練習表 - {gen_names}</title>
    <style>{PAGE_CSS}{grid_css(grid_type["key"], size_mm)}    </style>
</head>
<body>
    <div class="page-header">
        <h1>✏️ 寶可夢手寫練習表</h1>
        <p>{gen_names} • 共{total_pokemon}隻 • {grid_type["name"]} • {size_name} • A4橫式印刷版</p>
    </div>
'''

    if used_characters:
        symbols = "".join(stroke_symbol(char, stroke_medians[char]) for char in sorted(used_characters))
        html_content.append(f'    <svg class="stroke-defs">{symbols}</svg>')

    html_footer = '''    <div class="usage-info">
        <p>✏️ 使用方法：第一格是範字，接著照著描，空白格自己寫 • 🖨️ 建議 A4 橫式列印</p>
        <p>範字字型：中華民國教育部標準楷書（CC BY-ND 3.0 TW）• 筆畫資料：Make Me a Hanzi（Arphic Public License）</p>
        <p>非官方粉絲自製，僅供家庭與教學的非商業使用，請勿販售。寶可夢名稱與圖片 ©Pokémon. ©Nintendo / Creatures Inc. / GAME FREAK inc.</p>
    </div>
</body>
</html>'''

    complete_html = html_header + '\n'.join(html_content) + '\n' + html_footer
    return complete_html, total_pokemon

def build_filename(selected_generations, grid_type, grid_size, trace_style=None):
    """生成檔案名稱"""
    if len(selected_generations) == len(generations):
        base = "pokemon_all_generations"
    else:
        gen_nums = [str(i+1) for i, gen in enumerate(generations) if gen in selected_generations]
        base = f"pokemon_gen{'_'.join(gen_nums)}"
    trace_suffix = trace_style["suffix"] if trace_style else ""
    return f"{base}_handwriting{grid_type['suffix']}{grid_size['suffix']}{trace_suffix}.html"

def show_generation_menu():
    """顯示世代選擇選單"""
    print("\n✏️ 寶可夢手寫練習表 - 世代選擇器")
    print("=" * 50)
    print("選擇要生成的世代 (可選擇多個)：")
    print()

    for i, gen in enumerate(generations, 1):
        print(f"{i}. {gen['name']} ({gen['count']}隻)")

    print(f"{len(generations)+1}. 📚 全部世代 (1025隻) - 大檔案，載入較慢")
    print("0. ❌ 退出")
    print()

def get_option(title, options, default="1"):
    """從選項中選一個，直接按 Enter 使用預設"""
    print(f"\n{title}")
    for key, option in options.items():
        print(f"{key}. {option['name']}")

    choice = input(f"請輸入選擇 (預設 {default}): ").strip() or default
    if choice not in options:
        print(f"❌ 無效選擇，使用預設 {default}")
        choice = default
    return options[choice]

def get_trace_count(default=3):
    """每個字要描紅幾格"""
    choice = input(f"\n每個字描紅幾格？(0 = 不描紅，預設 {default}): ").strip()
    if not choice:
        return default
    try:
        return max(0, int(choice))
    except ValueError:
        print(f"❌ 格式錯誤，使用預設 {default}")
        return default

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

        grid_type = get_option("🔲 選擇格線類型：", grid_types)
        grid_size = get_option("📏 選擇格子尺寸：", grid_sizes)
        trace_count = get_trace_count()
        trace_style = get_option("🖍️ 選擇描紅樣式：", trace_styles) if trace_count else trace_styles["1"]

        warmup = input("\n🖍️ 要在最前面加一頁運筆描線暖身嗎？(y/n，預設 y): ").strip().lower() != 'n'

        print(f"\n🔄 正在生成...")

        html_content, total_pokemon = generate_handwriting_html(
            selected_generations, pokemon_data, grid_type, grid_size, trace_count, trace_style, warmup)
        filename = build_filename(selected_generations, grid_type, grid_size, trace_style)

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)

        file_size = os.path.getsize(filename) / 1024  # KB
        print(f"\n✅ 生成完成！")
        print(f"📄 檔案名稱: {filename}")
        print(f"🎮 寶可夢數量: {total_pokemon}隻")
        print(f"🔲 格線: {grid_type['name']} • {grid_size['name']}")
        print(f"🖍️ 描紅: {trace_count}格" + (f" • {trace_style['name']}" if trace_count else ""))
        print(f"💾 檔案大小: {file_size:.1f}KB")
        print()

        continue_choice = input("🔄 要繼續生成其他世代嗎？(y/n): ").strip().lower()
        if continue_choice != 'y':
            print("👋 再見！")
            break

if __name__ == "__main__":
    main()
