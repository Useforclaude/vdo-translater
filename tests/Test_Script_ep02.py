#!/usr/bin/env python3
"""
Test Script - ทดสอบ modules กับ ep-02.txt
"""

from pathlib import Path
import json

# Import modules
from context_analyzer import ContextAnalyzer
from data_management_system import DictionaryManager, SimpleDictionaryAPI
from config import Config

def test_with_ep02():
    """ทดสอบกับข้อมูลจริงจาก ep-02.txt"""
    
    print("=" * 60)
    print("🧪 Testing with ep-02.txt")
    print("=" * 60)
    
    # 1. Load ep-02.txt
    with open("ep-02.txt", "r", encoding="utf-8") as f:
        text = f.read()
    
    print(f"\n📄 Loaded {len(text)} characters")
    
    # 2. Initialize modules
    print("\n🚀 Initializing modules...")
    
    # Dictionary
    dict_manager = DictionaryManager(Path("data"))
    print(f"  ✅ Dictionary: {dict_manager.get_total_terms()} terms")
    
    # Context Analyzer
    analyzer = ContextAnalyzer()
    
    # Config
    config = Config()
    print(f"  ✅ Config: {config.processing.mode.value} mode")
    
    # 3. Test Context Analysis
    print("\n📊 Analyzing Context...")
    doc_context = analyzer.analyze_document(text)
    
    print(f"  Document Type: {doc_context.doc_type.value}")
    print(f"  Primary Topic: {doc_context.primary_topic}")
    print(f"  Trading Context: {doc_context.trading_context.value}")
    print(f"  Segments: {len(doc_context.segment_contexts)}")
    print(f"  Colloquialisms: {len(doc_context.colloquialisms)}")
    print(f"  Metaphors: {', '.join(doc_context.metaphor_domains)}")
    
    # 4. Test Term Finding
    print("\n🔍 Finding Terms...")
    
    # Take first few segments
    for i, segment_ctx in enumerate(doc_context.segment_contexts[:5]):
        print(f"\nSegment {i+1}: {segment_ctx.text[:50]}...")
        
        # Find terms
        terms_found = dict_manager.manager.find_all_terms_in_text(segment_ctx.text)
        print(f"  Terms found: {len(terms_found)}")
        
        for match, entry in terms_found[:3]:  # Show first 3
            print(f"    • {match} → {entry.english}")
    
    # 5. Test Translation Prompt Generation
    print("\n📝 Generating Translation Prompts...")
    
    for i in range(min(3, len(doc_context.segment_contexts))):
        prompt = analyzer.create_translation_prompt(i)
        print(f"\nSegment {i+1} prompt length: {len(prompt)} chars")
        print("Preview:", prompt[:200] + "...")
    
    # 6. Test Cost Estimation
    print("\n💰 Cost Estimation:")
    costs = config.estimate_cost(len(doc_context.segment_contexts))
    print(f"  Segments: {len(doc_context.segment_contexts)}")
    print(f"  Without cache: ${costs['without_cache']:.2f}")
    print(f"  With cache: ${costs['with_cache']:.2f}")
    print(f"  Savings: ${costs['savings']:.2f}")
    
    # 7. Export results
    print("\n💾 Exporting Results...")
    
    # Export context analysis
    analyzer.export_analysis(Path("ep02_analysis.json"))
    print("  ✅ Context analysis → ep02_analysis.json")
    
    # Export found terms
    terms_data = {
        "total_segments": len(doc_context.segment_contexts),
        "terms_by_segment": []
    }
    
    for segment_ctx in doc_context.segment_contexts[:10]:
        terms = dict_manager.manager.find_all_terms_in_text(segment_ctx.text)
        terms_data["terms_by_segment"].append({
            "text": segment_ctx.text,
            "terms_found": [(match, entry.english) for match, entry in terms]
        })
    
    with open("ep02_terms_found.json", "w", encoding="utf-8") as f:
        json.dump(terms_data, f, ensure_ascii=False, indent=2)
    print("  ✅ Terms found → ep02_terms_found.json")
    
    print("\n✅ Test Complete!")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print("=" * 60)
    print(f"  Total segments: {len(doc_context.segment_contexts)}")
    print(f"  Avg segment length: {len(text) / len(doc_context.segment_contexts):.0f} chars")
    print(f"  Colloquialisms detected: {len(doc_context.colloquialisms)}")
    print(f"  Metaphor domains: {len(doc_context.metaphor_domains)}")
    print(f"  Estimated processing cost: ${costs['with_cache']:.2f}")
    
    return doc_context

if __name__ == "__main__":
    # Run test
    result = test_with_ep02()