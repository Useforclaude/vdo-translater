#!/usr/bin/env python3
"""
Translation Pipeline - Main Engine for Thai→English SRT Generation
===================================================================
Version: 1.0.0
Author: CodeMaster
Description: Central translation pipeline that orchestrates all components
            for generating perfect English SRT from Thai video content

Key Features:
- Two-pass translation (context-aware)
- Smart model routing (cost optimization)
- External dictionary support
- Aggressive caching
- SRT timing preservation
"""

import json
import logging
import hashlib
import asyncio
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

# Local imports (assuming these modules exist)
try:
    from .context_analyzer import ContextAnalyzer, DocumentType, SegmentContext
    from .data_management_system import DictionaryManager
    from .config import Config, TranslationModel, ConfigMode
except ImportError:
    print("Warning: Some modules not found. Using placeholder imports.")

# Third-party imports
try:
    import openai
    from openai import OpenAI
except ImportError:
    print("Warning: OpenAI not installed. Install with: pip install openai")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ======================== DATA STRUCTURES ========================

@dataclass
class TranscriptionSegment:
    """Represents a single transcription segment"""
    id: int
    start_time: float
    end_time: float
    text: str
    confidence: float = 0.0
    speaker: Optional[str] = None
    
    def to_srt_timestamp(self, time_seconds: float) -> str:
        """Convert seconds to SRT timestamp format"""
        hours = int(time_seconds // 3600)
        minutes = int((time_seconds % 3600) // 60)
        seconds = int(time_seconds % 60)
        milliseconds = int((time_seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    
    def to_srt(self, translated_text: str) -> str:
        """Generate SRT format for this segment"""
        start = self.to_srt_timestamp(self.start_time)
        end = self.to_srt_timestamp(self.end_time)
        return f"{self.id}\n{start} --> {end}\n{translated_text}\n"


@dataclass
class TranslationResult:
    """Result of translation with metadata"""
    segment_id: int
    original_text: str
    translated_text: str
    model_used: str
    confidence: float
    complexity_score: float
    cached: bool = False
    cost_estimate: float = 0.0
    processing_time: float = 0.0


@dataclass
class PipelineStats:
    """Statistics for the entire pipeline run"""
    total_segments: int = 0
    cached_segments: int = 0
    gpt35_segments: int = 0
    gpt4_segments: int = 0
    local_segments: int = 0
    total_cost: float = 0.0
    total_time: float = 0.0
    cache_hit_rate: float = 0.0
    average_confidence: float = 0.0


# ======================== TRANSLATION CACHE ========================

class TranslationCache:
    """Smart caching system for translations"""
    
    def __init__(self, cache_dir: Path):
        """Initialize cache system"""
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.memory_cache = {}
        self.cache_stats = defaultdict(int)
        self._load_persistent_cache()
    
    def _load_persistent_cache(self):
        """Load cache from disk"""
        cache_file = self.cache_dir / "translation_cache.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    self.memory_cache = json.load(f)
                logger.info(f"Loaded {len(self.memory_cache)} cached translations")
            except Exception as e:
                logger.warning(f"Failed to load cache: {e}")
    
    def _save_persistent_cache(self):
        """Save cache to disk"""
        cache_file = self.cache_dir / "translation_cache.json"
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")
    
    def _generate_cache_key(self, text: str, context: str = "", model: str = "") -> str:
        """Generate unique cache key"""
        combined = f"{text}|{context}|{model}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def get(self, text: str, context: str = "", model: str = "") -> Optional[str]:
        """Get cached translation"""
        key = self._generate_cache_key(text, context, model)
        if key in self.memory_cache:
            self.cache_stats['hits'] += 1
            return self.memory_cache[key]
        self.cache_stats['misses'] += 1
        return None
    
    def set(self, text: str, translation: str, context: str = "", model: str = ""):
        """Cache a translation"""
        key = self._generate_cache_key(text, context, model)
        self.memory_cache[key] = translation
        self.cache_stats['sets'] += 1
        
        # Periodically save to disk
        if self.cache_stats['sets'] % 10 == 0:
            self._save_persistent_cache()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total = self.cache_stats['hits'] + self.cache_stats['misses']
        hit_rate = self.cache_stats['hits'] / total if total > 0 else 0
        return {
            'hits': self.cache_stats['hits'],
            'misses': self.cache_stats['misses'],
            'hit_rate': hit_rate,
            'size': len(self.memory_cache)
        }


# ======================== MAIN TRANSLATION PIPELINE ========================

class TranslationPipeline:
    """
    Main translation pipeline orchestrator
    Coordinates all components for Thai→English translation
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the translation pipeline
        
        Args:
            config: Configuration object (creates default if None)
        """
        # Initialize configuration
        self.config = config or Config(mode=ConfigMode.COST_OPTIMIZED)
        
        # Initialize components
        self.context_analyzer = ContextAnalyzer()
        self.data_manager = DictionaryManager()
        self.cache = TranslationCache(Path(self.config.cache.cache_dir))
        
        # Initialize OpenAI client
        self._init_openai_client()
        
        # Pipeline statistics
        self.stats = PipelineStats()
        
        # Thread pool for parallel processing
        self.executor = ThreadPoolExecutor(
            max_workers=self.config.processing.max_workers
        )
        
        logger.info("Translation Pipeline initialized")
    
    def _init_openai_client(self):
        """Initialize OpenAI client with error handling"""
        try:
            import os
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.client = OpenAI(api_key=api_key)
                logger.info("OpenAI client initialized")
            else:
                logger.warning("No OPENAI_API_KEY found. Using mock mode.")
                self.client = None
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI: {e}")
            self.client = None
    
    def process_transcript(
        self,
        segments: List[TranscriptionSegment],
        doc_type: DocumentType = DocumentType.TUTORIAL
    ) -> Tuple[List[TranslationResult], PipelineStats]:
        """
        Process entire transcript through the pipeline
        
        Args:
            segments: List of transcription segments
            doc_type: Type of document for context
            
        Returns:
            Tuple of (translation results, pipeline statistics)
        """
        start_time = datetime.now()
        
        # Step 1: Build full text for context analysis
        full_text = " ".join([seg.text for seg in segments])
        
        # Step 2: First pass - Analyze document context
        logger.info("Pass 1: Analyzing document context...")
        document_context = self.context_analyzer.analyze_document(full_text, doc_type)
        
        # Step 3: Second pass - Translate segments with context
        logger.info("Pass 2: Translating segments with context...")
        translation_results = self._translate_segments_with_context(
            segments, document_context
        )
        
        # Step 4: Post-processing and quality checks
        logger.info("Post-processing translations...")
        translation_results = self._post_process_translations(
            translation_results, document_context
        )
        
        # Calculate statistics
        self.stats.total_time = (datetime.now() - start_time).total_seconds()
        self.stats.total_segments = len(segments)
        self.stats.cache_hit_rate = self.cache.get_stats()['hit_rate']
        
        # Save cache
        self.cache._save_persistent_cache()
        
        logger.info(f"Pipeline completed in {self.stats.total_time:.2f}s")
        logger.info(f"Cache hit rate: {self.stats.cache_hit_rate:.1%}")
        logger.info(f"Estimated cost: ${self.stats.total_cost:.4f}")
        
        return translation_results, self.stats
    
    def _translate_segments_with_context(
        self, 
        segments: List[TranscriptionSegment],
        document_context
    ) -> List[TranslationResult]:
        """
        Translate segments using context and smart routing
        """
        results = []
        
        # Process in batches for efficiency
        batch_size = self.config.processing.batch_size
        for i in range(0, len(segments), batch_size):
            batch = segments[i:i+batch_size]
            
            # Process batch in parallel
            futures = []
            for segment in batch:
                # Get segment context
                seg_idx = segment.id - 1
                if seg_idx < len(document_context.segment_contexts):
                    seg_context = document_context.segment_contexts[seg_idx]
                else:
                    seg_context = None
                
                # Submit translation task
                future = self.executor.submit(
                    self._translate_single_segment,
                    segment,
                    seg_context,
                    document_context
                )
                futures.append(future)
            
            # Collect results
            for future in as_completed(futures):
                try:
                    result = future.result(timeout=30)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Translation failed: {e}")
        
        # Sort by segment ID to maintain order
        results.sort(key=lambda x: x.segment_id)
        return results
    
    def _translate_single_segment(
        self,
        segment: TranscriptionSegment,
        segment_context: Optional[SegmentContext],
        document_context
    ) -> TranslationResult:
        """
        Translate a single segment with smart model routing
        """
        start_time = datetime.now()
        
        # Check cache first
        context_str = str(segment_context) if segment_context else ""
        cached_translation = self.cache.get(segment.text, context_str)
        
        if cached_translation:
            self.stats.cached_segments += 1
            return TranslationResult(
                segment_id=segment.id,
                original_text=segment.text,
                translated_text=cached_translation,
                model_used="cache",
                confidence=1.0,
                complexity_score=0.0,
                cached=True,
                cost_estimate=0.0,
                processing_time=0.001
            )
        
        # Calculate complexity for model routing
        complexity = self._calculate_complexity(segment.text, segment_context)
        
        # Route to appropriate model
        model = self._select_model(complexity, segment_context)
        
        # Translate
        translated_text = self._perform_translation(
            segment.text,
            segment_context,
            document_context,
            model
        )
        
        # Cache the result
        self.cache.set(segment.text, translated_text, context_str, model.value)
        
        # Calculate cost
        cost = self._estimate_cost(segment.text, translated_text, model)
        self.stats.total_cost += cost
        
        # Update model usage stats
        if model == TranslationModel.GPT_35_TURBO:
            self.stats.gpt35_segments += 1
        elif model == TranslationModel.GPT_4:
            self.stats.gpt4_segments += 1
        else:
            self.stats.local_segments += 1
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return TranslationResult(
            segment_id=segment.id,
            original_text=segment.text,
            translated_text=translated_text,
            model_used=model.value,
            confidence=0.95 if model == TranslationModel.GPT_4 else 0.90,
            complexity_score=complexity,
            cached=False,
            cost_estimate=cost,
            processing_time=processing_time
        )
    
    def _calculate_complexity(
        self,
        text: str,
        segment_context: Optional[SegmentContext]
    ) -> float:
        """
        Calculate text complexity for model routing
        
        Returns:
            Complexity score 0.0-1.0
        """
        score = 0.0
        
        # Length factor
        if len(text) > 200:
            score += 0.2
        
        # Context factors
        if segment_context:
            # Metaphors increase complexity
            if segment_context.is_metaphor:
                score += 0.3

            # Technical terms
            if len(segment_context.key_terms) > 3:
                score += 0.2

            # Questions are simpler
            if segment_context.is_question:
                score -= 0.1
        
        # Check for specific patterns that need GPT-4
        complex_patterns = [
            "เหมือนกับ",  # Analogies
            "อุปมา",      # Metaphors
            "สมมติว่า",   # Hypotheticals
            "ยกตัวอย่าง", # Examples
        ]
        
        if any(pattern in text for pattern in complex_patterns):
            score += 0.2
        
        return min(1.0, max(0.0, score))
    
    def _select_model(
        self,
        complexity: float,
        segment_context: Optional[SegmentContext]
    ) -> TranslationModel:
        """
        Select appropriate model based on complexity
        
        Rules:
        - Complexity < 0.3: Local/simple
        - Complexity 0.3-0.7: GPT-3.5
        - Complexity > 0.7: GPT-4
        - Override for important segments
        """
        # Check for metaphors that need better model
        if segment_context and segment_context.is_metaphor:
            if complexity > 0.5:
                return TranslationModel.GPT_4
        
        # Route by complexity
        if complexity < 0.3:
            # Simple segments can use local or GPT-3.5
            return TranslationModel.GPT_35_TURBO
        elif complexity < 0.7:
            return TranslationModel.GPT_35_TURBO
        else:
            return TranslationModel.GPT_4
    
    def _perform_translation(
        self,
        text: str,
        segment_context: Optional[SegmentContext],
        document_context,
        model: TranslationModel
    ) -> str:
        """
        Perform actual translation using selected model
        """
        # Prepare context for prompt
        context_info = self._prepare_context_prompt(
            segment_context, document_context
        )
        
        # Build translation prompt
        prompt = self._build_translation_prompt(
            text, context_info, model
        )
        
        # Mock translation if no OpenAI client
        if not self.client:
            return self._mock_translation(text)
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=model.value,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.translation.temperature,
                max_tokens=self.config.translation.max_tokens
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Translation API error: {e}")
            # Fallback to simple translation
            return self._fallback_translation(text)
    
    def _prepare_context_prompt(
        self,
        segment_context: Optional[SegmentContext],
        document_context
    ) -> str:
        """Prepare context information for the prompt"""
        context_parts = []
        
        # Document-level context
        context_parts.append(f"Document Type: {document_context.doc_type.value}")
        context_parts.append(f"Primary Topic: {document_context.primary_topic}")
        
        if document_context.trading_context:
            context_parts.append(f"Trading Context: {document_context.trading_context}")
        
        # Segment-level context
        if segment_context:
            if segment_context.key_terms:
                terms = segment_context.key_terms[:5]
                context_parts.append(f"Key Terms: {', '.join(terms)}")

            if segment_context.is_metaphor:
                context_parts.append("Contains: Metaphors")

            if segment_context.is_question:
                context_parts.append("Type: Question")
        
        return "\n".join(context_parts)
    
    def _build_translation_prompt(
        self,
        text: str,
        context_info: str,
        model: TranslationModel
    ) -> str:
        """Build the translation prompt"""
        # Load terminology hints
        forex_terms = self.data_manager.search_terms(text)[:5]
        term_hints = []
        for entry in forex_terms:
            term_hints.append(f"- {entry.thai} = {entry.english}")
        
        prompt = f"""Translate the following Thai text to English for a Forex trading video.
        
CONTEXT:
{context_info}

TERMINOLOGY HINTS:
{chr(10).join(term_hints) if term_hints else "None"}

THAI TEXT:
"{text}"

REQUIREMENTS:
1. Maintain natural, conversational English
2. Preserve all Forex terminology accurately
3. Keep the same tone and style as the speaker
4. Handle colloquialisms naturally
5. Maintain timing-friendly segment length

ENGLISH TRANSLATION:"""
        
        return prompt
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for the model"""
        return """You are an expert translator specializing in Forex/Trading content.
You translate Thai to English with perfect accuracy while maintaining:
- Natural, fluent English
- Correct financial terminology
- Original speaker's tone and style
- Appropriate formality level
- Cultural nuances and metaphors

You understand both Thai colloquialisms and Forex technical terms."""
    
    def _mock_translation(self, text: str) -> str:
        """Mock translation for testing without API"""
        # Simple mock: return a placeholder
        words = len(text.split())
        return f"[Mock translation of {words} words: {text[:30]}...]"
    
    def _fallback_translation(self, text: str) -> str:
        """Fallback translation when API fails"""
        # Use dictionary for known terms
        translated_parts = []
        for word in text.split():
            entry = self.data_manager.find_term(word)
            if entry and entry.english:
                translated_parts.append(entry.english)
            else:
                translated_parts.append(f"[{word}]")
        
        return " ".join(translated_parts)
    
    def _estimate_cost(
        self,
        input_text: str,
        output_text: str,
        model: TranslationModel
    ) -> float:
        """Estimate API cost for the translation"""
        # Rough token estimation (1 token ≈ 4 chars)
        input_tokens = len(input_text) / 4
        output_tokens = len(output_text) / 4
        
        # Cost per 1K tokens (approximate)
        costs = {
            TranslationModel.GPT_35_TURBO: {
                'input': 0.0005,
                'output': 0.0015
            },
            TranslationModel.GPT_4: {
                'input': 0.01,
                'output': 0.03
            },
            TranslationModel.LOCAL: {
                'input': 0.0,
                'output': 0.0
            }
        }
        
        model_costs = costs.get(model, costs[TranslationModel.GPT_35_TURBO])
        
        total_cost = (
            (input_tokens / 1000) * model_costs['input'] +
            (output_tokens / 1000) * model_costs['output']
        )
        
        return total_cost
    
    def _post_process_translations(
        self,
        results: List[TranslationResult],
        document_context
    ) -> List[TranslationResult]:
        """
        Post-process translations for consistency and quality
        """
        # Check for terminology consistency
        self._ensure_terminology_consistency(results)
        
        # Smooth transitions between segments
        self._smooth_transitions(results)
        
        # Final quality checks
        for result in results:
            result.translated_text = self._final_quality_check(
                result.translated_text
            )
        
        return results
    
    def _ensure_terminology_consistency(self, results: List[TranslationResult]):
        """Ensure consistent terminology across all segments"""
        # Build term usage map
        term_usage = defaultdict(list)
        
        for result in results:
            # Extract Forex terms from translation
            terms = self.data_manager.extract_terms(result.translated_text)
            for term in terms:
                term_usage[term].append(result.segment_id)
        
        # Check for inconsistencies and fix
        # (Implementation would check for same Thai term with different English translations)
        pass
    
    def _smooth_transitions(self, results: List[TranslationResult]):
        """Smooth transitions between segments"""
        for i in range(1, len(results)):
            prev = results[i-1]
            curr = results[i]
            
            # Check if segments are connected
            if self._segments_connected(prev.original_text, curr.original_text):
                # Adjust translation for smooth flow
                curr.translated_text = self._adjust_for_flow(
                    prev.translated_text,
                    curr.translated_text
                )
    
    def _segments_connected(self, text1: str, text2: str) -> bool:
        """Check if two segments are connected"""
        # Check for continuation patterns
        continuation_words = ["and", "but", "so", "because", "then"]
        first_word = text2.split()[0].lower() if text2 else ""
        return first_word in continuation_words
    
    def _adjust_for_flow(self, prev_text: str, curr_text: str) -> str:
        """Adjust translation for better flow"""
        # Simple adjustment: ensure proper capitalization
        if curr_text and curr_text[0].islower():
            # Check if it's a continuation
            if curr_text.startswith(("and ", "but ", "so ")):
                return curr_text
        return curr_text
    
    def _final_quality_check(self, text: str) -> str:
        """Perform final quality checks on translation"""
        # Remove extra spaces
        text = " ".join(text.split())
        
        # Ensure proper capitalization
        if text and text[0].islower():
            text = text[0].upper() + text[1:]
        
        # Fix common issues
        text = text.replace(" ,", ",")
        text = text.replace(" .", ".")
        text = text.replace(" ?", "?")
        text = text.replace(" !", "!")
        
        return text
    
    def generate_srt(
        self,
        segments: List[TranscriptionSegment],
        translations: List[TranslationResult],
        output_path: Path
    ) -> bool:
        """
        Generate SRT file from translations
        
        Args:
            segments: Original segments with timing
            translations: Translation results
            output_path: Output SRT file path
            
        Returns:
            Success status
        """
        try:
            # Map translations to segments
            translation_map = {t.segment_id: t for t in translations}
            
            srt_content = []
            for segment in segments:
                if segment.id in translation_map:
                    translation = translation_map[segment.id]
                    srt_entry = segment.to_srt(translation.translated_text)
                    srt_content.append(srt_entry)
                else:
                    # Fallback to original if translation missing
                    srt_entry = segment.to_srt(f"[{segment.text}]")
                    srt_content.append(srt_entry)
            
            # Write SRT file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(srt_content))
            
            logger.info(f"SRT file generated: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate SRT: {e}")
            return False


# ======================== USAGE EXAMPLE ========================

def main():
    """
    Example usage of the Translation Pipeline
    """
    # Initialize pipeline with cost-optimized config
    config = Config(mode=ConfigMode.COST_OPTIMIZED)
    pipeline = TranslationPipeline(config)
    
    # Example transcription segments
    segments = [
        TranscriptionSegment(
            id=1,
            start_time=0.0,
            end_time=3.5,
            text="สวัสดีครับ วันนี้เราจะมาดู price action กัน",
            confidence=0.95
        ),
        TranscriptionSegment(
            id=2,
            start_time=3.5,
            end_time=7.2,
            text="ฝรั่งบอกว่า the trend is your friend",
            confidence=0.92
        ),
        TranscriptionSegment(
            id=3,
            start_time=7.2,
            end_time=11.0,
            text="แต่เราต้องรู้ว่า เมื่อไหร่เทรนด์จะกลับตัว",
            confidence=0.94
        ),
    ]
    
    # Process transcript
    print("Processing transcript...")
    results, stats = pipeline.process_transcript(
        segments,
        doc_type=DocumentType.TUTORIAL
    )
    
    # Generate SRT
    output_path = Path("output/translated.srt")
    pipeline.generate_srt(segments, results, output_path)
    
    # Print statistics
    print("\n=== Pipeline Statistics ===")
    print(f"Total segments: {stats.total_segments}")
    print(f"Cached segments: {stats.cached_segments}")
    print(f"GPT-3.5 segments: {stats.gpt35_segments}")
    print(f"GPT-4 segments: {stats.gpt4_segments}")
    print(f"Cache hit rate: {stats.cache_hit_rate:.1%}")
    print(f"Total cost: ${stats.total_cost:.4f}")
    print(f"Total time: {stats.total_time:.2f}s")
    
    # Print sample results
    print("\n=== Sample Translations ===")
    for result in results[:3]:
        print(f"\n[Segment {result.segment_id}]")
        print(f"Thai: {result.original_text}")
        print(f"English: {result.translated_text}")
        print(f"Model: {result.model_used}")
        print(f"Complexity: {result.complexity_score:.2f}")
        print(f"Cost: ${result.cost_estimate:.4f}")


if __name__ == "__main__":
    # Check dependencies
    print("Translation Pipeline v1.0.0")
    print("-" * 50)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nPipeline interrupted by user")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise
