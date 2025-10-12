#!/usr/bin/env python3
"""
Context Analyzer - Core Module for Context-Aware Translation
=============================================================
Version: 1.0.0
Author: CodeMaster
Description: Analyzes full document context before translation to ensure
             accurate meaning preservation for Thai Forex content

This module addresses the critical issue: Thai spoken language requires
full context understanding before translation, not word-by-word translation.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import defaultdict, Counter
import hashlib


# ======================== DATA STRUCTURES ========================

class DocumentType(Enum):
    """Types of Forex documents"""
    TUTORIAL = "tutorial"           # การสอน
    ANALYSIS = "analysis"          # การวิเคราะห์
    NEWS = "news"                  # ข่าว
    COMMENTARY = "commentary"      # บรรยาย
    MIXED = "mixed"                # ผสม


class TradingContext(Enum):
    """Trading context/sentiment"""
    BULLISH = "bullish"            # ขาขึ้น
    BEARISH = "bearish"            # ขาลง
    NEUTRAL = "neutral"            # กลาง
    REVERSAL = "reversal"          # กลับตัว
    CONSOLIDATION = "consolidation" # พักตัว


class TimeReference(Enum):
    """Time references in content"""
    PAST = "past"                  # อดีต
    PRESENT = "present"            # ปัจจุบัน
    FUTURE = "future"              # อนาคต
    CONDITIONAL = "conditional"    # เงื่อนไข


@dataclass
class IdiomMatch:
    """Detected idiom with context"""
    idiom_id: int
    thai: str
    english_translation: str
    literal: str
    start_pos: int
    end_pos: int
    confidence: float
    is_figurative: bool = True


@dataclass
class SegmentContext:
    """Context for a single segment"""
    index: int
    text: str
    trading_context: TradingContext = TradingContext.NEUTRAL
    time_reference: TimeReference = TimeReference.PRESENT
    is_question: bool = False
    is_metaphor: bool = False
    confidence: float = 1.0
    related_segments: List[int] = field(default_factory=list)
    key_terms: List[str] = field(default_factory=list)
    sentiment_score: float = 0.0  # -1 (bearish) to +1 (bullish)
    # NEW: Idiom-specific fields
    idioms_detected: List[IdiomMatch] = field(default_factory=list)
    has_idioms: bool = False
    figurative_language: bool = False
    idiom_hints: Dict[str, str] = field(default_factory=dict)


@dataclass
class DocumentContext:
    """Full document context"""
    doc_type: DocumentType
    primary_topic: str
    trading_context: TradingContext
    key_concepts: List[str]
    forex_terms: Set[str]
    colloquialisms: Set[str]
    metaphor_domains: Set[str]
    segment_contexts: List[SegmentContext]
    term_frequency: Dict[str, int]
    consistency_score: float = 1.0


# ======================== COLLOQUIAL PATTERNS ========================

class ColloquialPatterns:
    """Patterns from actual Thai Forex speech"""
    
    # From the Forex Terminology Guide
    COLLOQUIALISMS = {
        "ฝรั่งบอก": {
            "english": "As Westerners say",
            "context": "introducing_foreign_concept",
            "formality": "informal"
        },
        "เข้าเนื้อกันดีกว่า": {
            "english": "Let's dive into the details",
            "context": "transition_to_main",
            "formality": "informal"
        },
        "ฝั่งไหนครองเกมอยู่": {
            "english": "Which side is dominating",
            "context": "market_control_question",
            "formality": "informal"
        },
        "อ่านแผนที่นำทาง": {
            "english": "Read the market roadmap",
            "context": "understanding_direction",
            "formality": "metaphorical"
        },
        "แต่งให้มันเป็นนิทาน": {
            "english": "Turn it into your own narrative",
            "context": "personalization",
            "formality": "informal"
        },
        "กองทัพซะมากกว่า": {
            "english": "More like an army",
            "context": "military_metaphor",
            "formality": "informal"
        },
        "มีกำลังในการบุก": {
            "english": "Has the strength to advance",
            "context": "military_metaphor",
            "formality": "metaphorical"
        },
        "เมืองสองเมืองจะยึด": {
            "english": "Two cities battling for control",
            "context": "military_metaphor",
            "formality": "metaphorical"
        },
        "แรงเหวี่ยง": {
            "english": "Momentum",
            "context": "physics_metaphor",
            "formality": "informal"
        },
        "เหวี่ยงลูกตุ้ม": {
            "english": "Like a swinging pendulum",
            "context": "physics_metaphor",
            "formality": "metaphorical"
        },
        "หมดกำลัง": {
            "english": "Running out of steam",
            "context": "momentum_fading",
            "formality": "informal"
        },
        "เหยียบเบรค": {
            "english": "Hitting the brakes",
            "context": "automotive_metaphor",
            "formality": "informal"
        },
        "ยูเทิร์นกลับ": {
            "english": "Making a U-turn",
            "context": "automotive_metaphor",
            "formality": "informal"
        },
        "แท่งมันค่อยๆ เล็กลงๆ": {
            "english": "The candles are gradually shrinking",
            "context": "technical_description",
            "formality": "informal"
        }
    }
    
    # Metaphor domains
    METAPHOR_PATTERNS = {
        "military": r"(กองทัพ|ทหาร|แม่ทัพ|ยึด|เมือง|บุก|รุกราน|ศัตรู|สู้|ต่อสู้|กำแพง)",
        "automotive": r"(รถ|เบรค|คันเร่ง|ยูเทิร์น|เลี้ยว|ความเร็ว|เครื่องยนต์)",
        "physics": r"(แรง|เหวี่ยง|ลูกตุ้ม|โมเมนตัม|พลังงาน|แรงดึง|แรงผลัก)",
        "sports": r"(ครองเกม|ชนะ|แพ้|เกม|การแข่งขัน|คะแนน|ประตู)",
        "nature": r"(คลื่น|ลม|พายุ|น้ำ|ไฟ|ภูเขา|หุบเขา)",
        "narrative": r"(นิทาน|เรื่องราว|บทละคร|ฉาก|ตัวละคร|พระเอก)"
    }
    
    # Question patterns
    QUESTION_PATTERNS = [
        r".*ไหม\s*$",
        r".*มั้ย\s*$",
        r".*หรือเปล่า\s*$",
        r".*หรือไม่\s*$",
        r".*ได้ไหม\s*$",
        r"^ทำไม.*",
        r"^อะไร.*",
        r"^เมื่อไหร่.*",
        r"^ที่ไหน.*",
        r"^ใคร.*",
        r"^ยังไง.*"
    ]
    
    # Sentiment indicators
    BULLISH_INDICATORS = [
        "ขึ้น", "บวก", "กระทิง", "ซื้อ", "แข็งแกร่ง", "ทะลุ", "ฝ่า", 
        "สูง", "ดี", "โต", "เพิ่ม", "พุ่ง", "ทะยาน", "ปรับตัวขึ้น"
    ]
    
    BEARISH_INDICATORS = [
        "ลง", "ลบ", "หมี", "ขาย", "อ่อนแอ", "หลุด", "ตก",
        "ต่ำ", "แย่", "ลด", "ร่วง", "ดิ่ง", "ปรับตัวลง", "ย่อ"
    ]


# ======================== MAIN CONTEXT ANALYZER ========================

class ContextAnalyzer:
    """
    Main context analysis engine
    Implements two-pass analysis for accurate translation
    """
    
    def __init__(self):
        """Initialize the context analyzer"""
        self.patterns = ColloquialPatterns()
        self.document_context = None
        self.segments = []
        self.analysis_cache = {}
        
    def analyze_document(self, text: str, doc_type: DocumentType = None) -> DocumentContext:
        """
        First pass: Analyze entire document to understand context
        
        Args:
            text: Full document text
            doc_type: Type of document (auto-detect if None)
            
        Returns:
            Complete document context
        """
        # Auto-detect document type if not provided
        if doc_type is None:
            doc_type = self._detect_document_type(text)
        
        # Split into segments
        self.segments = self._segment_text(text)
        
        # Initialize document context
        self.document_context = DocumentContext(
            doc_type=doc_type,
            primary_topic=self._detect_primary_topic(text),
            trading_context=self._detect_trading_context(text),
            key_concepts=[],
            forex_terms=set(),
            colloquialisms=set(),
            metaphor_domains=set(),
            segment_contexts=[],
            term_frequency=Counter()
        )
        
        # Analyze each segment
        for idx, segment in enumerate(self.segments):
            segment_ctx = self._analyze_segment(segment, idx)
            self.document_context.segment_contexts.append(segment_ctx)
            
            # Collect terms and patterns
            self._collect_terms(segment, segment_ctx)
        
        # Post-processing: Find relationships between segments
        self._find_segment_relationships()
        
        # Calculate consistency score
        self.document_context.consistency_score = self._calculate_consistency()
        
        # Identify key concepts
        self.document_context.key_concepts = self._extract_key_concepts()
        
        return self.document_context
    
    def _detect_document_type(self, text: str) -> DocumentType:
        """Detect the type of document"""
        # Check for tutorial indicators
        tutorial_patterns = ["วันนี้เราจะ", "มาดูกัน", "ขั้นตอน", "วิธี", "สอน"]
        if any(pattern in text for pattern in tutorial_patterns):
            return DocumentType.TUTORIAL
        
        # Check for analysis indicators
        analysis_patterns = ["วิเคราะห์", "แนวโน้ม", "คาดการณ์", "ตามกราฟ"]
        if any(pattern in text for pattern in analysis_patterns):
            return DocumentType.ANALYSIS
        
        # Check for news indicators
        news_patterns = ["ข่าว", "ประกาศ", "รายงาน", "ล่าสุด"]
        if any(pattern in text for pattern in news_patterns):
            return DocumentType.NEWS
        
        return DocumentType.MIXED
    
    def _detect_primary_topic(self, text: str) -> str:
        """Detect the primary topic of discussion"""
        topics = {
            "momentum": ["โมเมนตัม", "แรง", "พลัง", "เหวี่ยง"],
            "support_resistance": ["แนวรับ", "แนวต้าน", "ระดับ"],
            "candlestick": ["แท่งเทียน", "แท่ง", "เทียน"],
            "trend": ["แนวโน้ม", "เทรนด์", "ทิศทาง"],
            "pattern": ["รูปแบบ", "แพทเทิร์น", "ลักษณะ"],
            "indicator": ["ตัวชี้วัด", "อินดิเคเตอร์", "RSI", "MACD"]
        }
        
        topic_scores = {}
        for topic, keywords in topics.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                topic_scores[topic] = score
        
        if topic_scores:
            return max(topic_scores, key=topic_scores.get)
        return "general_trading"
    
    def _detect_trading_context(self, text: str) -> TradingContext:
        """Detect overall trading context/sentiment"""
        bullish_count = sum(1 for word in self.patterns.BULLISH_INDICATORS if word in text)
        bearish_count = sum(1 for word in self.patterns.BEARISH_INDICATORS if word in text)
        
        # Check for reversal patterns
        reversal_patterns = ["กลับตัว", "เปลี่ยนทิศ", "ยูเทิร์น", "พลิกกลับ"]
        if any(pattern in text for pattern in reversal_patterns):
            return TradingContext.REVERSAL
        
        # Check for consolidation
        consolidation_patterns = ["พักตัว", "ไซด์เวย์", "แกว่งตัว", "ค้างตัว"]
        if any(pattern in text for pattern in consolidation_patterns):
            return TradingContext.CONSOLIDATION
        
        # Determine by sentiment balance
        if bullish_count > bearish_count * 1.5:
            return TradingContext.BULLISH
        elif bearish_count > bullish_count * 1.5:
            return TradingContext.BEARISH
        else:
            return TradingContext.NEUTRAL
    
    def _segment_text(self, text: str) -> List[str]:
        """Split text into logical segments"""
        # Split by newlines first
        lines = text.strip().split('\n')
        
        segments = []
        for line in lines:
            line = line.strip()
            if line:
                # Further split by sentence endings if line is too long
                if len(line) > 200:
                    # Split by Thai sentence markers
                    sub_segments = re.split(r'[।।ๆ]+', line)
                    segments.extend([s.strip() for s in sub_segments if s.strip()])
                else:
                    segments.append(line)
        
        return segments
    
    def _analyze_segment(self, segment: str, idx: int) -> SegmentContext:
        """Analyze a single segment"""
        ctx = SegmentContext(
            index=idx,
            text=segment
        )
        
        # Check if question
        ctx.is_question = any(re.match(pattern, segment) 
                              for pattern in self.patterns.QUESTION_PATTERNS)
        
        # Check for metaphors
        for domain, pattern in self.patterns.METAPHOR_PATTERNS.items():
            if re.search(pattern, segment):
                ctx.is_metaphor = True
                self.document_context.metaphor_domains.add(domain)
                break
        
        # Detect time reference
        if any(word in segment for word in ["แล้ว", "เมื่อ", "ที่ผ่านมา", "ก่อน"]):
            ctx.time_reference = TimeReference.PAST
        elif any(word in segment for word in ["จะ", "กำลังจะ", "คาด", "น่าจะ"]):
            ctx.time_reference = TimeReference.FUTURE
        elif any(word in segment for word in ["ถ้า", "หาก", "เมื่อ", "ต่อเมื่อ"]):
            ctx.time_reference = TimeReference.CONDITIONAL
        
        # Calculate sentiment
        bullish = sum(1 for word in self.patterns.BULLISH_INDICATORS if word in segment)
        bearish = sum(1 for word in self.patterns.BEARISH_INDICATORS if word in segment)
        total = bullish + bearish
        if total > 0:
            ctx.sentiment_score = (bullish - bearish) / total
        
        # Detect trading context
        if ctx.sentiment_score > 0.3:
            ctx.trading_context = TradingContext.BULLISH
        elif ctx.sentiment_score < -0.3:
            ctx.trading_context = TradingContext.BEARISH
        else:
            ctx.trading_context = TradingContext.NEUTRAL
        
        return ctx
    
    def _collect_terms(self, segment: str, ctx: SegmentContext):
        """Collect terms and patterns from segment"""
        # Collect colloquialisms
        for thai_phrase, details in self.patterns.COLLOQUIALISMS.items():
            if thai_phrase in segment:
                self.document_context.colloquialisms.add(thai_phrase)
                ctx.key_terms.append(thai_phrase)
        
        # Update term frequency
        words = segment.split()
        self.document_context.term_frequency.update(words)
    
    def _find_segment_relationships(self):
        """Find relationships between segments"""
        for i, ctx in enumerate(self.document_context.segment_contexts):
            # Find related segments (before and after)
            if i > 0:
                # Check if previous segment is related
                prev = self.document_context.segment_contexts[i-1]
                if self._segments_related(prev, ctx):
                    ctx.related_segments.append(i-1)
            
            if i < len(self.document_context.segment_contexts) - 1:
                # Check if next segment is related
                next_seg = self.document_context.segment_contexts[i+1]
                if self._segments_related(ctx, next_seg):
                    ctx.related_segments.append(i+1)
    
    def _segments_related(self, seg1: SegmentContext, seg2: SegmentContext) -> bool:
        """Check if two segments are related"""
        # Check for continuation words
        continuation_words = ["และ", "แต่", "หรือ", "ดังนั้น", "เพราะ", "แล้ว"]
        if any(word in seg2.text[:20] for word in continuation_words):
            return True
        
        # Check for same trading context
        if seg1.trading_context == seg2.trading_context:
            return True
        
        # Check for Q&A pattern
        if seg1.is_question and not seg2.is_question:
            return True
        
        return False
    
    def _calculate_consistency(self) -> float:
        """Calculate document consistency score"""
        if not self.document_context.segment_contexts:
            return 1.0
        
        # Check sentiment consistency
        sentiments = [ctx.sentiment_score for ctx in self.document_context.segment_contexts]
        if sentiments:
            # Calculate variance
            mean_sentiment = sum(sentiments) / len(sentiments)
            variance = sum((s - mean_sentiment) ** 2 for s in sentiments) / len(sentiments)
            
            # Lower variance = higher consistency
            consistency = max(0, 1 - (variance * 2))
            return min(1.0, consistency)
        
        return 1.0
    
    def _extract_key_concepts(self) -> List[str]:
        """Extract key concepts from document"""
        # Get most frequent meaningful terms
        meaningful_terms = []
        
        for term, freq in self.document_context.term_frequency.most_common(20):
            # Skip common words
            if len(term) < 3:
                continue
            
            # Skip particles
            if term in ["ครับ", "ค่ะ", "นะ", "และ", "หรือ", "แต่", "ที่", "ของ"]:
                continue
            
            meaningful_terms.append(term)
            
            if len(meaningful_terms) >= 10:
                break
        
        return meaningful_terms
    
    def get_segment_with_context(self, segment_index: int, context_window: int = 2) -> Dict:
        """
        Get a segment with surrounding context
        
        Args:
            segment_index: Index of the segment
            context_window: Number of segments before/after to include
            
        Returns:
            Dictionary with segment and context
        """
        if not self.document_context or segment_index >= len(self.document_context.segment_contexts):
            return None
        
        segment = self.document_context.segment_contexts[segment_index]
        
        # Get surrounding segments
        start = max(0, segment_index - context_window)
        end = min(len(self.document_context.segment_contexts), segment_index + context_window + 1)
        
        before = self.document_context.segment_contexts[start:segment_index]
        after = self.document_context.segment_contexts[segment_index + 1:end]
        
        return {
            "segment": segment,
            "before": before,
            "after": after,
            "document_context": {
                "type": self.document_context.doc_type.value,
                "topic": self.document_context.primary_topic,
                "trading_context": self.document_context.trading_context.value,
                "key_concepts": self.document_context.key_concepts[:5]
            }
        }
    
    def create_translation_prompt(self, segment_index: int) -> str:
        """
        Create a context-aware translation prompt for a segment
        
        Args:
            segment_index: Index of segment to translate
            
        Returns:
            Formatted prompt for translation
        """
        context = self.get_segment_with_context(segment_index)
        if not context:
            return None
        
        segment = context["segment"]
        
        prompt = f"""Translate this Thai Forex trading segment to natural English.

DOCUMENT CONTEXT:
- Document Type: {context['document_context']['type']}
- Main Topic: {context['document_context']['topic']}
- Trading Direction: {context['document_context']['trading_context']}
- Key Concepts: {', '.join(context['document_context']['key_concepts'])}

PREVIOUS CONTEXT:
{chr(10).join([f"[{i}] {s.text}" for i, s in enumerate(context['before'])])}

SEGMENT TO TRANSLATE (#{segment.index}):
{segment.text}

FOLLOWING CONTEXT:
{chr(10).join([f"[{i}] {s.text}" for i, s in enumerate(context['after'])])}

SEGMENT ANALYSIS:
- Type: {'Question' if segment.is_question else 'Statement'}
- Time Reference: {segment.time_reference.value}
- Contains Metaphor: {segment.is_metaphor}
- Sentiment: {segment.trading_context.value}
- Key Terms Found: {', '.join(segment.key_terms)}

TRANSLATION REQUIREMENTS:
1. Preserve the meaning based on full context, not word-for-word
2. Use appropriate Forex terminology consistently
3. Convert Thai metaphors to equivalent English expressions
4. Maintain conversational teaching tone
5. Remove Thai particles (ครับ, ค่ะ, นะ)
6. Ensure the translation makes sense with previous and following segments

Natural English Translation:"""
        
        return prompt
    
    def export_analysis(self, filepath: Path):
        """Export analysis results to JSON"""
        if not self.document_context:
            return
        
        export_data = {
            "document_type": self.document_context.doc_type.value,
            "primary_topic": self.document_context.primary_topic,
            "trading_context": self.document_context.trading_context.value,
            "consistency_score": self.document_context.consistency_score,
            "key_concepts": self.document_context.key_concepts,
            "forex_terms": list(self.document_context.forex_terms),
            "colloquialisms": list(self.document_context.colloquialisms),
            "metaphor_domains": list(self.document_context.metaphor_domains),
            "segments": [
                {
                    "index": ctx.index,
                    "text": ctx.text,
                    "trading_context": ctx.trading_context.value,
                    "time_reference": ctx.time_reference.value,
                    "is_question": ctx.is_question,
                    "is_metaphor": ctx.is_metaphor,
                    "sentiment_score": ctx.sentiment_score,
                    "related_segments": ctx.related_segments,
                    "key_terms": ctx.key_terms
                }
                for ctx in self.document_context.segment_contexts
            ]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)


# ======================== USAGE EXAMPLE ========================

def example_usage():
    """Example of how to use the Context Analyzer"""
    
    # Sample text from actual transcription
    sample_text = """
    ฝรั่งบอก beyond the basics of candlesticks
    การวิเคราะห์โมเมนตัม แรงซื้อแรงขาย
    ฝั่งไหนครองเกมอยู่
    อ่านแผนที่นำทาง
    แต่งให้มันเป็นนิทานหรือเป็นนิยายหรือเป็นสตอรี่ส่วนตัวของคุณ
    กองทัพซะมากกว่า
    เมืองสองเมืองจะยึด
    ฝั่งผู้ซื้อกับฝั่งผู้ขาย ฝั่งไหนที่จะมีชัย
    มีกำลังในการบุก มีพลทหาร มีแม่ทัพที่เก่งๆ ลุยเข้ามา
    เข้าเนื้อกันดีกว่า
    ฝั่งกระทิงจะชนะ
    ฝั่งหมี
    กระทิงหมายถึงขึ้นนะครับ ขาขึ้น
    หมีก็คือขาลง
    แรงเหวี่ยง
    เหวี่ยงลูกตุ้ม
    หมดกำลัง
    แท่งมันค่อยๆ เล็กลงๆ
    แรงขายเริ่มน้อยลง
    เปรียบเสมือนรถยนต์
    ยูเทิร์นกลับ
    เหยียบเบรค
    """
    
    print("=" * 60)
    print("🔍 Context Analyzer - Example Usage")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = ContextAnalyzer()
    
    # Analyze document (Pass 1)
    print("\n📊 PASS 1: Analyzing Document Context...")
    doc_context = analyzer.analyze_document(sample_text)
    
    print(f"\n📄 Document Type: {doc_context.doc_type.value}")
    print(f"📌 Primary Topic: {doc_context.primary_topic}")
    print(f"📈 Trading Context: {doc_context.trading_context.value}")
    print(f"✅ Consistency Score: {doc_context.consistency_score:.2f}")
    print(f"\n🔑 Key Concepts: {', '.join(doc_context.key_concepts[:5])}")
    print(f"💬 Colloquialisms Found: {len(doc_context.colloquialisms)}")
    print(f"🎭 Metaphor Domains: {', '.join(doc_context.metaphor_domains)}")
    
    # Translate segments with context (Pass 2)
    print("\n" + "=" * 60)
    print("📝 PASS 2: Context-Aware Translation")
    print("=" * 60)
    
    # Example: Translate a few segments
    for i in range(min(3, len(doc_context.segment_contexts))):
        segment = doc_context.segment_contexts[i]
        print(f"\n🔹 Segment {i + 1}:")
        print(f"   Thai: {segment.text}")
        print(f"   Context: {segment.trading_context.value}")
        print(f"   Type: {'Question' if segment.is_question else 'Statement'}")
        if segment.is_metaphor:
            print(f"   Metaphor: Yes")
        if segment.key_terms:
            print(f"   Key Terms: {', '.join(segment.key_terms)}")
        
        # Show how to get translation prompt
        if i == 0:
            print("\n📋 Translation Prompt Example:")
            prompt = analyzer.create_translation_prompt(i)
            print(prompt[:500] + "...")
    
    # Export analysis
    export_path = Path("context_analysis_result.json")
    analyzer.export_analysis(export_path)
    print(f"\n💾 Analysis exported to {export_path}")


if __name__ == "__main__":
    example_usage()
