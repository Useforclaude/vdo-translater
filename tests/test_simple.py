#!/usr/bin/env python3
"""
Simple Test Script - Works with existing files
==============================================
This script will work even without API key or missing modules
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Set mock mode to avoid API key error
os.environ['OPENAI_API_KEY'] = 'mock-key-for-testing'

print("=" * 60)
print("Thai→English Translation Pipeline - Simple Test")
print("=" * 60)
print()

# ============== MOCK CLASSES ==============

class MockConfig:
    """Minimal config for testing"""
    def __init__(self):
        self.mode = "mock"
        self.api = type('obj', (), {'mock_mode': True})()
        self.cache = type('obj', (), {
            'cache_dir': Path('.cache'),
            'strategy': 'memory'
        })()
        self.translation = type('obj', (), {
            'default_model': 'mock',
            'temperature': 0.3,
            'max_tokens': 500
        })()
        self.processing = type('obj', (), {
            'max_workers': 2,
            'batch_size': 5
        })()
        self.paths = type('obj', (), {
            'data_dir': Path('data'),
            'output_dir': Path('output')
        })()

class MockContextAnalyzer:
    """Mock context analyzer"""
    def analyze_document(self, text, doc_type=None):
        print("   Analyzing document context...")
        
        class MockDocContext:
            def __init__(self):
                self.doc_type = "forex_trading"
                self.primary_topic = "trading"
                self.trading_context = "technical_analysis"
                self.segment_contexts = []
                self.forex_terms = set(['momentum', 'trend', 'bull', 'bear'])
                self.colloquialisms = set(['ฝรั่งบอก'])
        
        return MockDocContext()

class MockDataManager:
    """Mock data management"""
    def __init__(self):
        self.terms = {
            'โมเมนตัม': 'momentum',
            'แนวโน้ม': 'trend',
            'กระทิง': 'bull',
            'หมี': 'bear',
            'แรงซื้อ': 'buying pressure',
            'แรงขาย': 'selling pressure'
        }
    
    def find_term(self, text):
        return None
    
    def search_terms(self, text):
        return []
    
    def extract_terms(self, text):
        found = []
        for thai, eng in self.terms.items():
            if thai in text:
                found.append(eng)
        return found

# ============== SIMPLE TRANSLATION PIPELINE ==============

class SimpleTranslationPipeline:
    """Simplified translation pipeline for testing"""
    
    def __init__(self):
        print("1. Initializing pipeline components...")
        self.config = MockConfig()
        self.context_analyzer = MockContextAnalyzer()
        self.data_manager = MockDataManager()
        self.cache = {}
        print("   ✓ Pipeline ready (mock mode)")
        print()
    
    def translate_segment(self, text: str, segment_id: int) -> Dict[str, Any]:
        """Simple translation logic"""
        # Check cache
        if text in self.cache:
            return self.cache[text]
        
        # Mock translation with simple dictionary
        translations = {
            'โมเมนตัม': 'momentum',
            'แรงเหวี่ยง': 'momentum force',
            'ลูกตุ้ม': 'pendulum',
            'กระทิง': 'bulls',
            'หมี': 'bears',
            'เทรด': 'trade',
            'ราคา': 'price',
            'แรงขับเคลื่อน': 'driving force',
            'ครองเกม': 'dominating the game',
            'ฝั่ง': 'side'
        }
        
        # Simple word-by-word with improvements
        result = text
        for thai, eng in translations.items():
            result = result.replace(thai, eng)
        
        # Add some structure
        if 'เหมือนกับ' in text:
            result = result.replace('เหมือนกับ', 'like')
        if 'ก็จะ' in text:
            result = result.replace('ก็จะ', 'will')
            
        # Cache it
        translation = {
            'segment_id': segment_id,
            'original': text,
            'translated': result,
            'model': 'mock-dictionary',
            'confidence': 0.75
        }
        
        self.cache[text] = translation
        return translation
    
    def process_transcript(self, segments: List[Dict]) -> tuple:
        """Process all segments"""
        print("2. Processing segments...")
        
        # Analyze full text
        full_text = " ".join([s['text'] for s in segments])
        context = self.context_analyzer.analyze_document(full_text)
        
        # Translate each segment
        results = []
        for seg in segments:
            result = self.translate_segment(seg['text'], seg['id'])
            results.append(result)
            print(f"   ✓ Segment {seg['id']} translated")
        
        # Stats
        stats = {
            'total_segments': len(segments),
            'cached_segments': 0,
            'processing_time': 0.5,
            'cache_hit_rate': 0.0,
            'total_cost': 0.0
        }
        
        print(f"   ✓ All {len(segments)} segments processed")
        print()
        
        return results, stats
    
    def generate_srt(self, segments: List[Dict], translations: List[Dict], filepath: Path) -> bool:
        """Generate SRT file"""
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                for seg, trans in zip(segments, translations):
                    # Format timestamp
                    start = self.format_timestamp(seg['start_time'])
                    end = self.format_timestamp(seg['end_time'])
                    
                    # Write SRT entry
                    f.write(f"{seg['id']}\n")
                    f.write(f"{start} --> {end}\n")
                    f.write(f"{trans['translated']}\n\n")
            
            return True
        except Exception as e:
            print(f"Error generating SRT: {e}")
            return False
    
    def format_timestamp(self, seconds: float) -> str:
        """Convert seconds to SRT timestamp"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


# ============== MAIN TEST FUNCTION ==============

def main():
    """Run the simple test"""
    
    # Sample segments from ep-02.txt
    segments = [
        {
            'id': 1,
            'start_time': 0.0,
            'end_time': 5.2,
            'text': "ที่นี่ อย่างเช่น โมเมนตัมนะครับ แสดงถึงการที่ราคามันมีแรงเหวี่ยง",
            'confidence': 0.95
        },
        {
            'id': 2,
            'start_time': 5.2,
            'end_time': 10.5,
            'text': "เหมือนกับเวลาที่เราเหวี่ยงลูกตุ้ม ลูกตุ้มมันจะมีแรงเหวี่ยง",
            'confidence': 0.93
        },
        {
            'id': 3,
            'start_time': 10.5,
            'end_time': 15.8,
            'text': "พอมันเหวี่ยงไปถึงจุดสูงสุด มันก็จะเริ่มหมดแรง แล้วก็เหวี่ยงกลับ",
            'confidence': 0.94
        },
        {
            'id': 4,
            'start_time': 15.8,
            'end_time': 21.0,
            'text': "ในการเทรด Forex ก็เหมือนกัน ราคามันจะมีโมเมนตัม มีแรงขับเคลื่อน",
            'confidence': 0.96
        },
        {
            'id': 5,
            'start_time': 21.0,
            'end_time': 26.5,
            'text': "เราต้องดูว่า ฝั่งไหนครองเกมอยู่ ฝั่งกระทิงหรือฝั่งหมี",
            'confidence': 0.92
        },
    ]
    
    # Initialize pipeline
    pipeline = SimpleTranslationPipeline()
    
    # Process segments
    results, stats = pipeline.process_transcript(segments)
    
    # Show results
    print("3. Translation Results:")
    print("-" * 50)
    for result in results[:3]:
        print(f"\n[Segment {result['segment_id']}]")
        print(f"Thai:    {result['original']}")
        print(f"English: {result['translated']}")
        print(f"Model:   {result['model']}")
    
    print("\n" + "-" * 50)
    
    # Show statistics
    print("\n4. Pipeline Statistics:")
    print(f"   Total segments: {stats['total_segments']}")
    print(f"   Processing time: {stats['processing_time']}s")
    print(f"   Cost: ${stats['total_cost']:.4f} (mock mode)")
    print()
    
    # Generate SRT
    print("5. Generating SRT file...")
    output_path = Path("output/test_simple.srt")
    if pipeline.generate_srt(segments, results, output_path):
        print(f"   ✓ SRT saved to: {output_path}")
        
        # Show sample of SRT content
        print("\n6. Sample SRT content:")
        print("-" * 50)
        with open(output_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:12]  # First 3 entries
            print("".join(lines))
    
    print("=" * 60)
    print("✅ Test completed successfully!")
    print("\nNext steps:")
    print("1. Create .env file with: OPENAI_API_KEY=your-key-here")
    print("2. Install dependencies: pip install openai python-dotenv")
    print("3. Use the full pipeline with real translation")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        print("\nPlease check that all required files exist.")
