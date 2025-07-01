# 🎮 Pokemon Phonetic Practice Worksheet

A Python project for generating Pokemon Bopomofo (Zhuyin) phonetic symbol practice sheets, helping children learn phonetic symbols by looking at Pokemon images and Chinese names.

**Other Languages:** [繁體中文](../../README.md) | [日本語](README_ja.md)

## 🌟 Features

- 📸 **Complete Database**: Includes 1025 Pokemon images and Chinese names
- 🎯 **Generation Selection**: Support single or multiple generation combinations
- 📄 **A4 Optimized**: Landscape print layout for practical use
- ✨ **Customizable Design**: Support font, size, and border adjustments
- 🚀 **Fast Loading**: Smart pagination design with small file sizes
- 🖊️ **Borderless Design**: Minimalist style focusing on content input

## 📋 Functionality Overview

### Core Functions
- 🎮 **Pokemon Data Collection**: Automatically download official images and Chinese names
- 📝 **Worksheet Generation**: Interactive generation selector
- 🛠️ **Integrated Management Tool**: One-click complete setup and data management
- 📊 **Status Check**: Real-time data integrity display

### Supported Generations
- 🌱 Generation 1 - Kanto Region (151 Pokemon)
- 🌸 Generation 2 - Johto Region (100 Pokemon)  
- 🌊 Generation 3 - Hoenn Region (135 Pokemon)
- ⛰️ Generation 4 - Sinnoh Region (107 Pokemon)
- 🌆 Generation 5 - Unova Region (156 Pokemon)
- 🌺 Generation 6 - Kalos Region (72 Pokemon)
- 🌴 Generation 7 - Alola Region (88 Pokemon)
- 🏰 Generation 8 - Galar Region (96 Pokemon)
- 🏔️ Generation 9 - Paldea Region (120 Pokemon)

## 🚀 Quick Start

### System Requirements
- Python 3.8+
- Internet connection (for downloading images)
- Approximately 150MB disk space

### Installation Steps
```bash
# 1. Clone the project
git clone https://github.com/tk009999/pokemon-phonetic-practice.git
cd pokemon-phonetic-practice

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run integrated management tool
python pokemon_manager.py
```

### Quick Generation
```bash
# Directly generate specific generations
python generate_generation_selector.py
```

## 📁 Project Structure

```
pokemon-phonetic-practice/
├── README.md                           # Project documentation
├── DOC_GUIDELINES.md                   # Documentation guidelines
├── pokemon_manager.py                  # Integrated management tool
├── generate_generation_selector.py     # Worksheet generator
├── main.py                             # Image downloader
├── get_pokemon_names_tw.py             # Name collector
├── requirements.txt                    # Python dependencies
├── fonts/                              # Font files
├── pokemon_data/                       # Pokemon data
├── pokemon_images/                     # Image data (1025 images)
├── docs/                               # Documentation
└── pokemon_gen*_phonetic.html          # Generated worksheets
```

## 🛠️ Usage Instructions

### Generation Selector
Run `generate_generation_selector.py` for quick worksheet generation:

- Single generation: `1` (Generation 1)
- Multiple generations: `1,2,3` (First three generations)
- Range: `1-3` (Generation 1 to 3)
- All: `10` (All nine generations)

## 📖 Detailed Documentation

- [📖 Project Story](../../STORY.md) - A Father and Child's Phonetic Adventure (繁體中文) ⭐
- [Environment Setup Guide](../SETUP.md) - Detailed installation and setup guide
- [Version History](../CHANGELOG.md) - Project update records
- [Font Size Adjustment Guide](../字級調整對照表.md) - Font size adjustment guide
- [Border Style Adjustment Guide](../虛線框調整指南.md) - Border style adjustment instructions

## 🤝 Contributing

Welcome to submit Issues and Pull Requests to improve this project!

## 📄 License

Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License

---

**🎮 Enjoy Pokemon Phonetic Practice!** 