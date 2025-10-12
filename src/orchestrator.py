#!/usr/bin/env python3
"""
Video Translation Orchestrator - Main Pipeline Controller
==========================================================
Version: 1.0.0
Description: Complete end-to-end orchestration of Thai→English
             video translation pipeline

Pipeline Stages:
1. Thai Transcription (Whisper large-v3)
2. Context Analysis (two-pass)
3. Translation (smart routing + caching)
4. Quality Validation
5. SRT Generation
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Local imports
try:
    from .thai_transcriber import ThaiTranscriber, TranscriptionResult
    from .context_analyzer import ContextAnalyzer, DocumentType
    from .translation_pipeline import TranslationPipeline, TranscriptionSegment
    from .config import Config, ConfigMode
except ImportError:
    try:
        from thai_transcriber import ThaiTranscriber, TranscriptionResult
        from context_analyzer import ContextAnalyzer, DocumentType
        from translation_pipeline import TranslationPipeline, TranscriptionSegment
        from config import Config, ConfigMode
    except ImportError:
        logger.error("Failed to import required modules")
        sys.exit(1)


# ======================== DATA STRUCTURES ========================

@dataclass
class OrchestratorResult:
    """Complete pipeline result"""
    input_file: Path
    output_files: Dict[str, Path]
    stats: Dict[str, any]
    success: bool
    error: Optional[str] = None
    duration_seconds: float = 0.0


# ======================== ORCHESTRATOR ========================

class VideoTranslationOrchestrator:
    """
    Main pipeline orchestrator
    Manages complete workflow from video to English SRT
    """

    def __init__(
        self,
        whisper_model: str = "large-v3",
        config_mode: ConfigMode = ConfigMode.PRODUCTION,
        device: str = "cpu"
    ):
        """
        Initialize orchestrator

        Args:
            whisper_model: Whisper model for transcription
            config_mode: Pipeline configuration mode
            device: Device for Whisper ('cpu' or 'cuda')
        """
        logger.info("=" * 60)
        logger.info("Video Translation Orchestrator")
        logger.info("=" * 60)

        # Initialize configuration
        self.config = Config(mode=config_mode)
        logger.info(f"Configuration: {config_mode.value}")

        # Initialize components
        try:
            self.transcriber = ThaiTranscriber(model_name=whisper_model, device=device)
            self.context_analyzer = ContextAnalyzer()
            self.translator = TranslationPipeline(config=self.config)
            logger.info("✓ All components initialized")
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            raise

    def process_video(
        self,
        input_path: Path,
        output_dir: Optional[Path] = None,
        doc_type: DocumentType = DocumentType.TUTORIAL
    ) -> OrchestratorResult:
        """
        Process video through complete pipeline

        Args:
            input_path: Path to input video/audio file
            output_dir: Output directory (default: ./output)
            doc_type: Document type for context analysis

        Returns:
            OrchestratorResult with all outputs and statistics
        """
        start_time = datetime.now()

        # Validate input
        input_path = Path(input_path)
        if not input_path.exists():
            return OrchestratorResult(
                input_file=input_path,
                output_files={},
                stats={},
                success=False,
                error=f"Input file not found: {input_path}"
            )

        # Setup output directory
        if output_dir is None:
            output_dir = Path("output")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_base = output_dir / input_path.stem
        output_files = {}

        logger.info(f"\n{'='*60}")
        logger.info(f"Processing: {input_path.name}")
        logger.info(f"{'='*60}")

        try:
            # ==================== STAGE 1: TRANSCRIPTION ====================
            logger.info("\n[Stage 1/5] Thai Transcription")
            logger.info("-" * 60)

            thai_transcription = self.transcriber.transcribe_file(input_path)

            # Save Thai SRT
            thai_srt_path = output_base.with_name(f"{output_base.name}_thai.srt")
            self.transcriber.save_srt(thai_transcription, thai_srt_path)
            output_files['thai_srt'] = thai_srt_path

            # Save Thai JSON
            thai_json_path = output_base.with_name(f"{output_base.name}_thai.json")
            self.transcriber.save_json(thai_transcription, thai_json_path)
            output_files['thai_json'] = thai_json_path

            logger.info(f"✓ Stage 1 complete:")
            logger.info(f"  - Segments: {len(thai_transcription.segments)}")
            logger.info(f"  - Duration: {thai_transcription.duration:.2f}s")
            logger.info(f"  - Confidence: {thai_transcription.average_confidence:.2%}")

            # ==================== STAGE 2: CONTEXT ANALYSIS ====================
            logger.info("\n[Stage 2/5] Context Analysis")
            logger.info("-" * 60)

            document_context = self.context_analyzer.analyze_document(
                thai_transcription.text,
                doc_type=doc_type
            )

            # Save context analysis
            context_path = output_base.with_name(f"{output_base.name}_context.json")
            self.context_analyzer.export_analysis(context_path)
            output_files['context'] = context_path

            logger.info(f"✓ Stage 2 complete:")
            logger.info(f"  - Document type: {document_context.doc_type.value}")
            logger.info(f"  - Primary topic: {document_context.primary_topic}")
            logger.info(f"  - Colloquialisms: {len(document_context.colloquialisms)}")
            logger.info(f"  - Metaphor domains: {len(document_context.metaphor_domains)}")

            # ==================== STAGE 3: TRANSLATION ====================
            logger.info("\n[Stage 3/5] Translation")
            logger.info("-" * 60)

            # Convert to TranscriptionSegment format
            segments = [
                TranscriptionSegment(
                    id=seg.id,
                    start_time=seg.start,
                    end_time=seg.end,
                    text=seg.text,
                    confidence=seg.confidence
                )
                for seg in thai_transcription.segments
            ]

            # Translate
            translation_results, translation_stats = self.translator.process_transcript(
                segments,
                doc_type=doc_type
            )

            logger.info(f"✓ Stage 3 complete:")
            logger.info(f"  - Segments translated: {len(translation_results)}")
            logger.info(f"  - Cache hit rate: {translation_stats.cache_hit_rate:.1%}")
            logger.info(f"  - Estimated cost: ${translation_stats.total_cost:.4f}")

            # ==================== STAGE 4: SRT GENERATION ====================
            logger.info("\n[Stage 4/5] SRT Generation")
            logger.info("-" * 60)

            # Generate English SRT
            english_srt_path = output_base.with_name(f"{output_base.name}_english.srt")
            self.translator.generate_srt(segments, translation_results, english_srt_path)
            output_files['english_srt'] = english_srt_path

            logger.info(f"✓ Stage 4 complete:")
            logger.info(f"  - English SRT: {english_srt_path}")

            # ==================== STAGE 5: STATISTICS ====================
            logger.info("\n[Stage 5/5] Statistics & Summary")
            logger.info("-" * 60)

            duration = (datetime.now() - start_time).total_seconds()

            stats = {
                "input_file": str(input_path),
                "duration_seconds": thai_transcription.duration,
                "processing_time_seconds": duration,
                "thai_segments": len(thai_transcription.segments),
                "thai_words": thai_transcription.word_count,
                "thai_confidence": thai_transcription.average_confidence,
                "translation_cache_hits": translation_stats.cached_segments,
                "translation_cache_rate": translation_stats.cache_hit_rate,
                "gpt35_segments": translation_stats.gpt35_segments,
                "gpt4_segments": translation_stats.gpt4_segments,
                "estimated_cost": translation_stats.total_cost,
                "cost_per_minute": translation_stats.total_cost / (thai_transcription.duration / 60) if thai_transcription.duration > 0 else 0,
                "processing_speed": thai_transcription.duration / duration if duration > 0 else 0,
                "timestamp": datetime.now().isoformat()
            }

            # Save statistics
            stats_path = output_base.with_name(f"{output_base.name}_stats.json")
            with open(stats_path, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            output_files['stats'] = stats_path

            logger.info(f"✓ Stage 5 complete")
            logger.info(f"\n{'='*60}")
            logger.info("PIPELINE SUMMARY")
            logger.info(f"{'='*60}")
            logger.info(f"✓ Input: {input_path.name}")
            logger.info(f"✓ Duration: {thai_transcription.duration:.2f}s")
            logger.info(f"✓ Processing time: {duration:.2f}s")
            logger.info(f"✓ Speed: {stats['processing_speed']:.1f}x realtime")
            logger.info(f"✓ Cost: ${stats['estimated_cost']:.4f}")
            logger.info(f"✓ Cost/min: ${stats['cost_per_minute']:.4f}")
            logger.info(f"\nOutput files:")
            for name, path in output_files.items():
                logger.info(f"  - {name}: {path}")

            return OrchestratorResult(
                input_file=input_path,
                output_files=output_files,
                stats=stats,
                success=True,
                duration_seconds=duration
            )

        except Exception as e:
            logger.error(f"\n❌ Pipeline failed: {e}")
            import traceback
            traceback.print_exc()

            return OrchestratorResult(
                input_file=input_path,
                output_files=output_files,
                stats={},
                success=False,
                error=str(e),
                duration_seconds=(datetime.now() - start_time).total_seconds()
            )


# ======================== CLI INTERFACE ========================

def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Thai→English Video Translation Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process video with default settings
  python orchestrator.py input.mp4

  # Specify output directory
  python orchestrator.py input.mp4 -o output/

  # Use different Whisper model
  python orchestrator.py input.mp4 -m medium

  # Use cost-optimized mode
  python orchestrator.py input.mp4 --mode cost_optimized

  # Use GPU for Whisper
  python orchestrator.py input.mp4 --device cuda
        """
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input video/audio file"
    )

    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("output"),
        help="Output directory (default: output/)"
    )

    parser.add_argument(
        "-m", "--model",
        type=str,
        default="large-v3",
        choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
        help="Whisper model (default: large-v3)"
    )

    parser.add_argument(
        "--mode",
        type=str,
        default="production",
        choices=["development", "production", "quality_focus", "cost_optimized", "mock"],
        help="Pipeline mode (default: production)"
    )

    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        choices=["cpu", "cuda"],
        help="Device for Whisper (default: cpu)"
    )

    parser.add_argument(
        "--doc-type",
        type=str,
        default="tutorial",
        choices=["tutorial", "analysis", "news", "commentary", "mixed"],
        help="Document type (default: tutorial)"
    )

    args = parser.parse_args()

    # Convert mode string to enum
    mode_map = {
        "development": ConfigMode.DEVELOPMENT,
        "production": ConfigMode.PRODUCTION,
        "quality_focus": ConfigMode.QUALITY_FOCUS,
        "cost_optimized": ConfigMode.COST_OPTIMIZED,
        "mock": ConfigMode.MOCK
    }
    config_mode = mode_map[args.mode]

    # Convert doc_type string to enum
    doc_type_map = {
        "tutorial": DocumentType.TUTORIAL,
        "analysis": DocumentType.ANALYSIS,
        "news": DocumentType.NEWS,
        "commentary": DocumentType.COMMENTARY,
        "mixed": DocumentType.MIXED
    }
    doc_type = doc_type_map[args.doc_type]

    try:
        # Initialize orchestrator
        orchestrator = VideoTranslationOrchestrator(
            whisper_model=args.model,
            config_mode=config_mode,
            device=args.device
        )

        # Process video
        result = orchestrator.process_video(
            input_path=args.input,
            output_dir=args.output,
            doc_type=doc_type
        )

        # Exit with appropriate code
        sys.exit(0 if result.success else 1)

    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Pipeline interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
