#!/usr/bin/env python3
"""
Migration Script - Extract Hardcoded Data to JSON/YAML Files
=============================================================
Extracts all hardcoded dictionaries from existing modules
and saves them as external JSON/YAML files
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List
import sys


def create_directory_structure():
    """Create the data directory structure"""
    dirs = [
        "data/dictionaries",
        "data/patterns", 
        "data/configs/domains"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✅ Created directory structure")


def extract_forex_terms():
    """Extract forex terms and save to JSON"""
    
    # Hardcoded terms from enhanced_forex_dictionary.py
    forex_terms = {
        "metadata": {
            "version": "1.0.0",
            "description": "Forex trading terminology",
            "language_pair": "th-en"
        },
        "terms": [
            # Currency Pairs
            {"thai": "ยูโร/ดอลลาร์", "english": "EUR/USD", "category": "currency_pairs", "priority": 1, "pronunciation": "euro dollar"},
            {"thai": "ปอนด์/ดอลลาร์", "english": "GBP/USD", "category": "currency_pairs", "priority": 1, "pronunciation": "cable"},
            {"thai": "ดอลลาร์/เยน", "english": "USD/JPY", "category": "currency_pairs", "priority": 1, "pronunciation": "dollar yen"},
            {"thai": "ทองคำ", "english": "XAU/USD", "category": "currency_pairs", "priority": 1, "pronunciation": "gold"},
            
            # Trading Actions
            {"thai": "ซื้อ", "english": "Buy/Long", "category": "trading_actions", "priority": 1, "description": "Opening a long position"},
            {"thai": "ขาย", "english": "Sell/Short", "category": "trading_actions", "priority": 1, "description": "Opening a short position"},
            {"thai": "ปิดออเดอร์", "english": "Close order", "category": "trading_actions", "priority": 1},
            {"thai": "เปิดออเดอร์", "english": "Open order", "category": "trading_actions", "priority": 1},
            {"thai": "ตั้งออเดอร์", "english": "Place order", "category": "trading_actions", "priority": 1},
            
            # Technical Analysis
            {"thai": "การวิเคราะห์เทคนิค", "english": "Technical analysis", "category": "technical_analysis", "priority": 1},
            {"thai": "การวิเคราะห์พื้นฐาน", "english": "Fundamental analysis", "category": "technical_analysis", "priority": 1},
            {"thai": "การวิเคราะห์โมเมนตัม", "english": "Momentum analysis", "category": "technical_analysis", "priority": 1, "spoken_variations": ["แรงซื้อแรงขาย"]},
            {"thai": "แนวโน้ม", "english": "Trend", "category": "technical_analysis", "priority": 1, "spoken_variations": ["เทรนด์"]},
            {"thai": "แนวโน้มขาขึ้น", "english": "Uptrend", "category": "technical_analysis", "priority": 1, "spoken_variations": ["ขาขึ้น"]},
            {"thai": "แนวโน้มขาลง", "english": "Downtrend", "category": "technical_analysis", "priority": 1, "spoken_variations": ["ขาลง"]},
            
            # Support & Resistance
            {"thai": "แนวรับ", "english": "Support", "category": "support_resistance", "priority": 1, "spoken_variations": ["ซัพพอร์ต"]},
            {"thai": "แนวต้าน", "english": "Resistance", "category": "support_resistance", "priority": 1, "spoken_variations": ["รีซิสแตนซ์"]},
            {"thai": "จุดพิวอต", "english": "Pivot point", "category": "support_resistance", "priority": 2},
            
            # Indicators
            {"thai": "อาร์เอสไอ", "english": "RSI", "category": "indicators", "priority": 1, "pronunciation": "aar-es-ai"},
            {"thai": "แมคดี", "english": "MACD", "category": "indicators", "priority": 1, "pronunciation": "mak-dee"},
            {"thai": "ค่าเฉลี่ยเคลื่อนที่", "english": "Moving Average", "category": "indicators", "priority": 1, "abbreviation": "MA"},
            {"thai": "โบลลิงเจอร์แบนด์", "english": "Bollinger Bands", "category": "indicators", "priority": 1},
            {"thai": "ฟีโบนักชี", "english": "Fibonacci", "category": "indicators", "priority": 1},
            
            # Candlesticks
            {"thai": "แท่งเทียน", "english": "Candlestick", "category": "candlesticks", "priority": 1, "spoken_variations": ["แท่ง", "เทียน"]},
            {"thai": "โดจิ", "english": "Doji", "category": "candlesticks", "priority": 1},
            {"thai": "แฮมเมอร์", "english": "Hammer", "category": "candlesticks", "priority": 1, "spoken_variations": ["ค้อน"]},
            {"thai": "ชูตติ้งสตาร์", "english": "Shooting star", "category": "candlesticks", "priority": 1},
            
            # Price Action
            {"thai": "พินบาร์", "english": "Pin bar", "category": "price_action", "priority": 1, "spoken_variations": ["พิน บาร์"]},
            {"thai": "อินไซด์บาร์", "english": "Inside bar", "category": "price_action", "priority": 1},
            {"thai": "เอ็นกัลฟิ่ง", "english": "Engulfing", "category": "price_action", "priority": 1, "spoken_variations": ["กลืนกิน"]},
            {"thai": "เบรคเอาท์", "english": "Breakout", "category": "price_action", "priority": 1},
            
            # Risk Management
            {"thai": "การจัดการความเสี่ยง", "english": "Risk management", "category": "risk_management", "priority": 1},
            {"thai": "สต็อปลอส", "english": "Stop loss", "category": "risk_management", "priority": 1, "abbreviation": "SL"},
            {"thai": "เทคโปรฟิต", "english": "Take profit", "category": "risk_management", "priority": 1, "abbreviation": "TP"},
            {"thai": "ความเสี่ยงต่อผลตอบแทน", "english": "Risk-reward ratio", "category": "risk_management", "priority": 1, "abbreviation": "RR"},
            {"thai": "เลเวอเรจ", "english": "Leverage", "category": "risk_management", "priority": 1},
            {"thai": "มาร์จิ้น", "english": "Margin", "category": "risk_management", "priority": 1},
        ]
    }
    
    # Save to file
    filepath = Path("data/dictionaries/forex_terms.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(forex_terms, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Saved {len(forex_terms['terms'])} forex terms to {filepath}")
    return len(forex_terms['terms'])


def extract_colloquialisms():
    """Extract colloquial phrases and save to JSON"""
    
    colloquialisms = {
        "metadata": {
            "version": "1.0.0",
            "description": "Thai colloquial phrases in Forex context",
            "source": "ep-02.txt and Forex Terminology Guide"
        },
        "phrases": [
            {"thai": "ฝรั่งบอก", "english": "As Westerners say", "category": "colloquial", "context": "introducing_concept", "priority": 1},
            {"thai": "เข้าเนื้อกันดีกว่า", "english": "Let's dive into the details", "category": "colloquial", "context": "transition", "priority": 1},
            {"thai": "ฝั่งไหนครองเกมอยู่", "english": "Which side is dominating", "category": "colloquial", "context": "market_control", "priority": 1},
            {"thai": "อ่านแผนที่นำทาง", "english": "Read the market roadmap", "category": "colloquial", "context": "navigation", "priority": 1},
            {"thai": "แต่งให้มันเป็นนิทาน", "english": "Turn it into your own narrative", "category": "colloquial", "context": "personalization", "priority": 2},
            {"thai": "กองทัพซะมากกว่า", "english": "More like an army", "category": "colloquial", "context": "military_metaphor", "priority": 1},
            {"thai": "มีกำลังในการบุก", "english": "Has the strength to advance", "category": "colloquial", "context": "military_metaphor", "priority": 1},
            {"thai": "เมืองสองเมืองจะยึด", "english": "Two cities battling for control", "category": "colloquial", "context": "military_metaphor", "priority": 2},
            {"thai": "ฝั่งกระทิง", "english": "Bull side", "category": "colloquial", "context": "market_forces", "priority": 1},
            {"thai": "ฝั่งหมี", "english": "Bear side", "category": "colloquial", "context": "market_forces", "priority": 1},
            {"thai": "แรงเหวี่ยง", "english": "Momentum", "category": "colloquial", "context": "physics_metaphor", "priority": 1},
            {"thai": "เหวี่ยงลูกตุ้ม", "english": "Like a swinging pendulum", "category": "colloquial", "context": "physics_metaphor", "priority": 2},
            {"thai": "หมดกำลัง", "english": "Running out of steam", "category": "colloquial", "context": "energy", "priority": 1},
            {"thai": "เหยียบเบรค", "english": "Hitting the brakes", "category": "colloquial", "context": "car_metaphor", "priority": 1},
            {"thai": "ยูเทิร์นกลับ", "english": "Making a U-turn", "category": "colloquial", "context": "car_metaphor", "priority": 1},
            {"thai": "แท่งมันค่อยๆ เล็กลงๆ", "english": "The candles are gradually shrinking", "category": "colloquial", "context": "technical", "priority": 1},
            {"thai": "แรงขายเริ่มน้อยลง", "english": "Selling pressure is weakening", "category": "colloquial", "context": "market_analysis", "priority": 1},
            {"thai": "เริ่มมีการสู้คืน", "english": "Starting to fight back", "category": "colloquial", "context": "military_metaphor", "priority": 1},
            {"thai": "กำแพงเมือง", "english": "City wall (major resistance)", "category": "colloquial", "context": "military_metaphor", "priority": 1},
        ]
    }
    
    # Save to file
    filepath = Path("data/dictionaries/colloquialisms.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(colloquialisms, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Saved {len(colloquialisms['phrases'])} colloquialisms to {filepath}")
    return len(colloquialisms['phrases'])


def extract_metaphors():
    """Extract metaphor mappings and save to JSON"""
    
    metaphors = {
        "metadata": {
            "version": "1.0.0",
            "description": "Metaphor domains and mappings for Thai Forex content"
        },
        "domains": {
            "military": {
                "pattern": "กองทัพ|ทหาร|แม่ทัพ|ยึด|เมือง|บุก|รุกราน|ศัตรู|สู้|กำแพง",
                "description": "Military metaphors for market battles",
                "mappings": {
                    "กองทัพ": "forces",
                    "ทหาร": "traders",
                    "แม่ทัพ": "major players",
                    "ยึดเมือง": "capture levels",
                    "บุก": "advance",
                    "รุกราน": "push through",
                    "ศัตรู": "opposing force",
                    "สู้คืน": "fight back",
                    "กำแพงเมือง": "major resistance"
                }
            },
            "automotive": {
                "pattern": "รถ|เบรค|คันเร่ง|ยูเทิร์น|เลี้ยว|ความเร็ว",
                "description": "Car metaphors for momentum",
                "mappings": {
                    "เหยียบเบรค": "slowing down",
                    "เหยียบคันเร่ง": "accelerating",
                    "ยูเทิร์น": "reversing direction",
                    "เลี้ยว": "changing direction",
                    "ความเร็ว": "speed/momentum"
                }
            },
            "physics": {
                "pattern": "แรง|เหวี่ยง|ลูกตุ้ม|โมเมนตัม|พลังงาน",
                "description": "Physics metaphors for market forces",
                "mappings": {
                    "แรงเหวี่ยง": "momentum force",
                    "เหวี่ยงลูกตุ้ม": "pendulum swing",
                    "สูญเสียพลังงาน": "losing energy",
                    "แรงซื้อแรงขาย": "buying and selling pressure"
                }
            },
            "sports": {
                "pattern": "ครองเกม|ชนะ|แพ้|เกม|แข่งขัน",
                "description": "Sports metaphors for competition",
                "mappings": {
                    "ครองเกม": "dominating the game",
                    "ชนะ": "winning",
                    "แพ้": "losing",
                    "เกม": "the game"
                }
            },
            "nature": {
                "pattern": "คลื่น|ลม|พายุ|น้ำ|ไฟ",
                "description": "Nature metaphors for market movements",
                "mappings": {
                    "คลื่นใหญ่": "major wave",
                    "พายุ": "storm/volatility",
                    "น้ำท่วม": "overwhelming force"
                }
            }
        }
    }
    
    # Save to file
    filepath = Path("data/dictionaries/metaphors.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(metaphors, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Saved {len(metaphors['domains'])} metaphor domains to {filepath}")
    return len(metaphors['domains'])


def extract_speech_patterns():
    """Extract speech patterns and save to YAML"""
    
    patterns = {
        "metadata": {
            "version": "1.0.0",
            "description": "Thai speech patterns for recognition"
        },
        "patterns": {
            "questions": {
                "description": "Question patterns",
                "patterns": [
                    ".*ไหม$",
                    ".*มั้ย$", 
                    ".*หรือเปล่า$",
                    ".*หรือไม่$",
                    ".*ได้ไหม$",
                    "^ทำไม.*",
                    "^อะไร.*",
                    "^ยังไง.*"
                ]
            },
            "continuations": {
                "description": "Continuation words",
                "patterns": [
                    "^และ",
                    "^แต่",
                    "^หรือ",
                    "^ดังนั้น",
                    "^เพราะ",
                    "^แล้ว"
                ]
            },
            "fillers": {
                "description": "Filler words to remove",
                "words": [
                    "ครับ",
                    "ค่ะ",
                    "นะ",
                    "นะครับ",
                    "นะคะ",
                    "อ่า",
                    "เอ่อ",
                    "อืม"
                ]
            },
            "emphasis": {
                "description": "Emphasis patterns",
                "patterns": [
                    ".*จริงๆ",
                    ".*มากๆ",
                    ".*เลย$",
                    ".*อย่างมาก"
                ]
            }
        }
    }
    
    # Save to file
    filepath = Path("data/patterns/speech_patterns.yaml")
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(patterns, f, allow_unicode=True, default_flow_style=False)
    
    print(f"✅ Saved speech patterns to {filepath}")
    return len(patterns['patterns'])


def create_empty_custom_terms():
    """Create empty custom terms file for user additions"""
    
    custom_terms = {
        "metadata": {
            "version": "1.0.0",
            "description": "User-added custom terms",
            "note": "Add your custom terms here"
        },
        "terms": []
    }
    
    # Save to file
    filepath = Path("data/dictionaries/custom_terms.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(custom_terms, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Created empty custom_terms.json")
    return 0


def create_config_file():
    """Create domain configuration file"""
    
    config = {
        "domain": "forex",
        "version": "1.0.0",
        "settings": {
            "source_language": "th",
            "target_language": "en",
            "preserve_terminology": True,
            "use_metaphor_detection": True,
            "colloquialism_handling": "translate_natural"
        },
        "priorities": {
            "terminology_consistency": 0.95,
            "timing_preservation": 1.0,
            "natural_language": 0.85
        }
    }
    
    # Save to file
    filepath = Path("data/configs/domains/forex.yaml")
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
    
    print(f"✅ Created forex domain config")


def main():
    """Run the migration"""
    
    print("=" * 60)
    print("📦 Data Migration Script")
    print("=" * 60)
    print("\nExtracting hardcoded data to external files...\n")
    
    # Create directories
    create_directory_structure()
    
    # Extract data
    stats = {
        "forex_terms": extract_forex_terms(),
        "colloquialisms": extract_colloquialisms(),
        "metaphor_domains": extract_metaphors(),
        "speech_patterns": extract_speech_patterns(),
        "custom_terms": create_empty_custom_terms()
    }
    
    # Create config
    create_config_file()
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Migration Complete!")
    print("=" * 60)
    print("\n📊 Summary:")
    print(f"  • Forex terms: {stats['forex_terms']}")
    print(f"  • Colloquialisms: {stats['colloquialisms']}")
    print(f"  • Metaphor domains: {stats['metaphor_domains']}")
    print(f"  • Speech pattern types: {stats['speech_patterns']}")
    print(f"  • Custom terms: {stats['custom_terms']} (empty file)")
    
    print("\n📁 Files created in:")
    print("  data/")
    print("  ├── dictionaries/")
    print("  │   ├── forex_terms.json")
    print("  │   ├── colloquialisms.json")
    print("  │   ├── metaphors.json")
    print("  │   └── custom_terms.json")
    print("  ├── patterns/")
    print("  │   └── speech_patterns.yaml")
    print("  └── configs/")
    print("      └── domains/")
    print("          └── forex.yaml")
    
    print("\n✨ Next steps:")
    print("  1. Review and edit the JSON files as needed")
    print("  2. Add more terms to custom_terms.json")
    print("  3. Use data_management_system.py to load these files")
    
    return stats


if __name__ == "__main__":
    stats = main()
