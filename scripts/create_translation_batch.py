#!/usr/bin/env python3
"""
Create Translation Batch for Claude Code
========================================
Generate formatted text file from Whisper transcript for manual translation.

Features:
- Loads transcript JSON with timestamps
- Includes context (idioms, forex terms) for better translation
- Creates structured file with segment numbers
- Preserves all metadata for later SRT generation

Usage:
    python scripts/create_translation_batch.py transcript.json
    python scripts/create_translation_batch.py transcript.json -o workflow/02_for_translation/
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ======================== BATCH CREATOR ========================

class TranslationBatchCreator:
    """Create translation batch files from Whisper transcript"""

    def __init__(self, idiom_db_path: Path = None, forex_terms_path: Path = None):
        """
        Initialize batch creator

        Args:
            idiom_db_path: Path to thai_idioms.json (optional)
            forex_terms_path: Path to forex_terms.json (optional)
        """
        self.idioms = []
        self.forex_terms = []

        # Load idiom database if available
        if idiom_db_path and idiom_db_path.exists():
            with open(idiom_db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.idioms = data.get('idioms', [])
            logger.info(f"✓ Loaded {len(self.idioms)} idioms")

        # Load forex terms if available
        if forex_terms_path and forex_terms_path.exists():
            with open(forex_terms_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.forex_terms = data.get('terms', [])
            logger.info(f"✓ Loaded {len(self.forex_terms)} forex terms")

    def load_transcript(self, transcript_path: Path) -> Dict:
        """
        Load transcript JSON

        Args:
            transcript_path: Path to transcript JSON file

        Returns:
            Transcript dictionary
        """
        if not transcript_path.exists():
            raise FileNotFoundError(f"Transcript not found: {transcript_path}")

        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript = json.load(f)

        logger.info(f"✓ Loaded transcript: {transcript_path.name}")
        logger.info(f"  Segments: {len(transcript['segments'])}")
        logger.info(f"  Duration: {transcript['metadata']['duration']:.1f}s")

        return transcript

    def create_context_guide(self) -> str:
        """
        Create context guide with idioms and terms

        Returns:
            Context guide text
        """
        guide = []

        guide.append("=" * 80)
        guide.append("TRANSLATION CONTEXT GUIDE")
        guide.append("=" * 80)
        guide.append("")

        # General instructions
        guide.append("📋 GENERAL INSTRUCTIONS:")
        guide.append("-" * 80)
        guide.append("1. Translate Thai to natural English")
        guide.append("2. Preserve meaning, not literal words")
        guide.append("3. Keep forex/trading terminology accurate")
        guide.append("4. Maintain conversational tone")
        guide.append("5. DO NOT translate idioms literally!")
        guide.append("")

        # Idioms (sample)
        if self.idioms:
            guide.append("🎯 COMMON IDIOMS TO WATCH:")
            guide.append("-" * 80)
            for idiom in self.idioms[:10]:  # Show top 10
                thai = idiom.get('thai', '')
                literal = idiom.get('literal', '')
                meaning = idiom.get('meaning', '')
                guide.append(f"❌ '{thai}' → NOT '{literal}'")
                guide.append(f"✅ '{thai}' → '{meaning}'")
                guide.append("")

            if len(self.idioms) > 10:
                guide.append(f"... and {len(self.idioms) - 10} more idioms")
                guide.append("")

        # Forex terms (sample)
        if self.forex_terms:
            guide.append("💹 FOREX TERMINOLOGY:")
            guide.append("-" * 80)
            for term in self.forex_terms[:10]:  # Show top 10
                thai = term.get('thai', '')
                english = term.get('english', '')
                guide.append(f"  {thai} = {english}")

            if len(self.forex_terms) > 10:
                guide.append(f"  ... and {len(self.forex_terms) - 10} more terms")
            guide.append("")

        guide.append("=" * 80)
        guide.append("")

        return "\n".join(guide)

    def create_batch_file(
        self,
        transcript: Dict,
        output_path: Path,
        include_context: bool = True
    ):
        """
        Create batch translation file

        Args:
            transcript: Transcript dictionary
            output_path: Output file path
            include_context: Include context guide
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            # Header
            f.write("╔" + "=" * 78 + "╗\n")
            f.write("║" + " " * 78 + "║\n")
            f.write("║" + "THAI TO ENGLISH TRANSLATION BATCH".center(78) + "║\n")
            f.write("║" + " " * 78 + "║\n")
            f.write("╚" + "=" * 78 + "╝\n\n")

            # Metadata
            f.write(f"Source: {transcript['metadata'].get('timestamp', 'Unknown')}\n")
            f.write(f"Segments: {len(transcript['segments'])}\n")
            f.write(f"Duration: {transcript['metadata']['duration']:.1f}s\n")
            f.write(f"Model: {transcript['metadata'].get('model_name', 'Unknown')}\n")

            # Handle optional average_confidence field
            avg_conf = transcript['metadata'].get('average_confidence')
            if avg_conf is not None:
                f.write(f"Confidence: {avg_conf:.1%}\n")
            else:
                f.write(f"Confidence: N/A\n")
            f.write("\n")

            # Context guide
            if include_context:
                f.write(self.create_context_guide())

            # Instructions
            f.write("=" * 80 + "\n")
            f.write("TRANSLATION INSTRUCTIONS\n")
            f.write("=" * 80 + "\n\n")
            f.write("1. Each segment is numbered [001], [002], etc.\n")
            f.write("2. Translate the Thai text to natural English\n")
            f.write("3. Keep the segment numbers intact\n")
            f.write("4. Preserve the format exactly\n")
            f.write("5. Save as UTF-8 encoding\n\n")

            f.write("FORMAT:\n")
            f.write("-" * 80 + "\n")
            f.write("[001]\n")
            f.write("THAI: ข้อความภาษาไทย\n")
            f.write("EN: Your English translation here\n")
            f.write("\n")
            f.write("-" * 80 + "\n\n")

            # Segments
            f.write("=" * 80 + "\n")
            f.write("BEGIN TRANSLATION\n")
            f.write("=" * 80 + "\n\n")

            for seg in transcript['segments']:
                seg_id = seg['id']
                thai_text = seg['text']
                start = seg['start']
                end = seg['end']

                # Segment header
                f.write(f"[{seg_id + 1:03d}] ({self._format_timestamp(start)} → {self._format_timestamp(end)})\n")
                f.write(f"THAI: {thai_text}\n")
                f.write(f"EN: \n")  # Empty for user to fill
                f.write("\n")

            # Footer
            f.write("=" * 80 + "\n")
            f.write("END OF TRANSLATION\n")
            f.write("=" * 80 + "\n")

        logger.info(f"✓ Batch file created: {output_path}")

    def create_template_file(
        self,
        transcript: Dict,
        output_path: Path
    ):
        """
        Create simple template file (minimal format)

        Args:
            transcript: Transcript dictionary
            output_path: Output file path
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# TRANSLATION TEMPLATE\n")
            f.write("# Format: [SEG_NUM] English translation\n\n")

            for seg in transcript['segments']:
                seg_id = seg['id']
                thai_text = seg['text']

                f.write(f"# Thai: {thai_text}\n")
                f.write(f"[{seg_id + 1:03d}] \n\n")

        logger.info(f"✓ Template file created: {output_path}")

    @staticmethod
    def _format_timestamp(seconds: float) -> str:
        """Format seconds to MM:SS"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"


# ======================== CLI INTERFACE ========================

def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Create translation batch from Whisper transcript",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic: Create translation batch
  python scripts/create_translation_batch.py transcript.json

  # Specify output directory
  python scripts/create_translation_batch.py transcript.json \\
    -o workflow/02_for_translation/

  # With idiom database
  python scripts/create_translation_batch.py transcript.json \\
    --idioms data/dictionaries/thai_idioms.json

  # Minimal template only
  python scripts/create_translation_batch.py transcript.json \\
    --template-only

Output Files:
  - <video>_batch.txt         # Full batch with context guide
  - <video>_template.txt      # Simple template
        """
    )

    parser.add_argument(
        'transcript',
        type=Path,
        help='Input transcript JSON file'
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=Path('workflow/02_for_translation'),
        help='Output directory (default: workflow/02_for_translation/)'
    )

    parser.add_argument(
        '--idioms',
        type=Path,
        help='Path to thai_idioms.json (optional)'
    )

    parser.add_argument(
        '--forex-terms',
        type=Path,
        help='Path to forex_terms.json (optional)'
    )

    parser.add_argument(
        '--template-only',
        action='store_true',
        help='Create minimal template only'
    )

    parser.add_argument(
        '--no-context',
        action='store_true',
        help='Skip context guide in batch file'
    )

    args = parser.parse_args()

    try:
        # Auto-find dictionaries if not specified
        if not args.idioms:
            auto_idioms = Path('data/dictionaries/thai_idioms.json')
            if auto_idioms.exists():
                args.idioms = auto_idioms

        if not args.forex_terms:
            auto_forex = Path('data/dictionaries/forex_terms.json')
            if auto_forex.exists():
                args.forex_terms = auto_forex

        # Initialize creator
        creator = TranslationBatchCreator(
            idiom_db_path=args.idioms,
            forex_terms_path=args.forex_terms
        )

        # Load transcript
        transcript = creator.load_transcript(args.transcript)

        # Setup output paths
        output_dir = args.output
        output_dir.mkdir(parents=True, exist_ok=True)

        base_name = args.transcript.stem.replace('_transcript', '')
        batch_path = output_dir / f"{base_name}_batch.txt"
        template_path = output_dir / f"{base_name}_template.txt"

        logger.info("\n" + "=" * 70)
        logger.info("Creating Translation Files")
        logger.info("=" * 70)

        # Create files
        if not args.template_only:
            creator.create_batch_file(
                transcript,
                batch_path,
                include_context=not args.no_context
            )

        creator.create_template_file(transcript, template_path)

        # Summary
        logger.info("\n" + "=" * 70)
        logger.info("FILES CREATED")
        logger.info("=" * 70)
        if not args.template_only:
            logger.info(f"✓ Batch file: {batch_path}")
        logger.info(f"✓ Template file: {template_path}")

        logger.info("\n" + "=" * 70)
        logger.info("NEXT STEPS")
        logger.info("=" * 70)
        logger.info("1. Open batch file in text editor")
        logger.info("2. Copy Thai segments to Claude Code")
        logger.info("3. Get translations from Claude")
        logger.info("4. Paste translations in EN: lines")
        logger.info("5. Save file (keep UTF-8 encoding)")
        logger.info("6. Convert to SRT:")
        logger.info(f"   python scripts/batch_to_srt.py {args.transcript} {batch_path}")

        sys.exit(0)

    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
