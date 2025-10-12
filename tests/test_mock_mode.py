#!/usr/bin/env python3
"""
Test Script - Works without API Key (Mock Mode)
===============================================
"""

import sys
from pathlib import Path

# Use the updated config
sys.path.insert(0, str(Path(__file__).parent))

# Mock the modules if they don't exist
class MockContextAnalyzer:
    def analyze_document(self, text, doc_type=None):
        class MockContext:
            doc_type = "forex_trading"
            primary_topic = "trading"
            trading_context = "technical_analysis"
            segment_contexts = []
        return MockContext()

class MockDataManagementSystem:
    def find_term(self, text):
        return None
    def search_terms(self, text):
        return []
    def extract_terms(self, text):
        return []

# Try to import real modules, fallback to mocks
try:
    from context_analyzer import ContextAnalyzer, DocumentType
except ImportError:
    print("⚠ context_analyzer.py not found, using mock")
    ContextAnalyzer = MockContextAnalyzer
    class DocumentType:
        FOREX_TRADING = "forex_trading"

try:
    from data_management_system import DataManagementSystem
except ImportError:
    print("⚠ data_management_system.py not found, using mock")
    DataManagementSystem = MockDataManagementSystem

# Import the updated config (should work now)
from config_updated import Config, ConfigMode

# Import translation pipeline
from translation_pipeline import TranslationPipeline, TranscriptionSegment

def main():
    """Run test in mock mode"""
    print("=" * 60)
    print("Thai→English Translation Pipeline - MOCK MODE TEST")
    print("=" * 60)
    print()
    
    # Create config in MOCK mode
    print("1. Initializing in MOCK mode (no API needed)...")
    config = Config(mode=ConfigMode.MOCK)
    print(f"   ✓ Mock mode: {config.api.mock_mode}")
    print()
    
    # Initialize pipeline
    print("2. Creating translation pipeline...")
    pipeline = TranslationPipeline(config)
    print("   ✓ Pipeline ready")
    print()
    
    # Sample segments from ep-02.txt
    print("3. Loading sample segments...")
    segments = [
        TranscriptionSegment(
            id=1,
            start_time=0.0,
            end_time=5.2,
            text="ที่นี่ อย่างเช่น โมเมนตัมนะครับ แสดงถึงการที่ราคามันมีแรงเหวี่ยง",
            confidence=0.95
        ),
        TranscriptionSegment(
            id=2,
            start_time=5.2,
            end_time=10.5,
            text="เหมือนกับเวลาที่เราเหวี่ยงลูกตุ้ม ลูกตุ้มมันจะมีแรงเหวี่ยง",
            confidence=0.93
        ),
        TranscriptionSegment(
            id=3,
            start_time=10.5,
            end_time=15.8,
            text="พอมันเหวี่ยงไปถึงจุดสูงสุด มันก็จะเริ่มหมดแรง แล้วก็เหวี่ยงกลับ",
            confidence=0.94
        ),
        TranscriptionSegment(
            id=4,
            start_time=15.8,
            end_time=21.0,
            text="ในการเทรด Forex ก็เหมือนกัน ราคามันจะมีโมเมนตัม มีแรงขับเคลื่อน",
            confidence=0.96
        ),
        TranscriptionSegment(
            id=5,
            start_time=21.0,
            end_time=26.5,
            text="เราต้องดูว่า ฝั่งไหนครองเกมอยู่ ฝั่งกระทิงหรือฝั่งหมี",
            confidence=0.92
        ),
    ]
    print(f"   ✓ Loaded {len(segments)} segments")
    print()
    
    # Process through pipeline
    print("4. Processing segments...")
    try:
        results, stats = pipeline.process_transcript(segments)
        print("   ✓ Processing complete")
        print()
        
        # Show results
        print("5. Translation Results (MOCK):")
        print("-" * 50)
        for i, result in enumerate(results[:3], 1):
            print(f"\n[Segment {result.segment_id}]")
            print(f"Thai:    {result.original_text[:50]}...")
            print(f"English: {result.translated_text}")
            print(f"Model:   {result.model_used}")
        
        print("\n" + "-" * 50)
        print("\n6. Pipeline Statistics:")
        print(f"   Total segments: {stats.total_segments}")
        print(f"   Cached: {stats.cached_segments}")
        print(f"   Cache hit rate: {stats.cache_hit_rate:.1%}")
        print(f"   Processing time: {stats.total_time:.2f}s")
        print(f"   Cost (mock): ${stats.total_cost:.4f}")
        
        # Generate SRT
        print("\n7. Generating SRT file...")
        output_path = Path("output/test_mock.srt")
        if pipeline.generate_srt(segments, results, output_path):
            print(f"   ✓ SRT saved to: {output_path}")
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ Mock test completed successfully!")
    print("\nTo use real translation:")
    print("1. Add your OpenAI API key to .env file")
    print("2. Run with ConfigMode.COST_OPTIMIZED instead of MOCK")
    print("=" * 60)


if __name__ == "__main__":
    main()
