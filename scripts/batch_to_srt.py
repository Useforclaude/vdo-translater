#!/usr/bin/env python3
"""
Convert Translated Batch to SRT
===============================
Convert Claude Code translated text file back to SRT format with timestamps.

Features:
- Reads original transcript JSON (timestamps)
- Reads translated text file
- Matches translations to timestamps
- Generates professional SRT file

Usage:
    python scripts/batch_to_srt.py transcript.json translated.txt
    python scripts/batch_to_srt.py transcript.json translated.txt -o output/final.srt
"""

import os
import sys
import json
import re
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import timedelta

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ======================== SRT CONVERTER ========================

class BatchToSRTConverter:
    """Convert translated batch file to SRT with timestamps"""

    def __init__(self):
        """Initialize converter"""
        self.transcript = None
        self.translations = {}

    def load_transcript(self, transcript_path: Path) -> Dict:
        """
        Load original transcript with timestamps

        Args:
            transcript_path: Path to transcript JSON

        Returns:
            Transcript dictionary
        """
        if not transcript_path.exists():
            raise FileNotFoundError(f"Transcript not found: {transcript_path}")

        with open(transcript_path, 'r', encoding='utf-8') as f:
            self.transcript = json.load(f)

        logger.info(f"✓ Loaded transcript: {transcript_path.name}")
        logger.info(f"  Segments: {len(self.transcript['segments'])}")
        logger.info(f"  Duration: {self.transcript['metadata']['duration']:.1f}s")

        return self.transcript

    def parse_translated_file(self, translated_path: Path) -> Dict[int, str]:
        """
        Parse translated text file

        Args:
            translated_path: Path to translated text file

        Returns:
            Dictionary mapping segment IDs to translations
        """
        if not translated_path.exists():
            raise FileNotFoundError(f"Translated file not found: {translated_path}")

        translations = {}
        current_id = None
        current_translation = []

        with open(translated_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip()

                # Match segment ID: [001], [002], etc.
                id_match = re.match(r'\[(\d+)\]', line)
                if id_match:
                    # Save previous segment if exists
                    if current_id is not None and current_translation:
                        trans_text = ' '.join(current_translation).strip()
                        if trans_text:
                            translations[current_id] = trans_text

                    # Start new segment
                    current_id = int(id_match.group(1)) - 1  # Convert to 0-indexed
                    current_translation = []
                    continue

                # Match translation line: EN: ...
                en_match = re.match(r'EN:\s*(.*)', line)
                if en_match and current_id is not None:
                    trans = en_match.group(1).strip()
                    if trans:
                        current_translation.append(trans)
                    continue

                # Match simple format: just translation after [ID]
                if current_id is not None and line and not line.startswith(('#', 'THAI:', '-', '=')):
                    current_translation.append(line.strip())

            # Save last segment
            if current_id is not None and current_translation:
                trans_text = ' '.join(current_translation).strip()
                if trans_text:
                    translations[current_id] = trans_text

        logger.info(f"✓ Parsed translations: {translated_path.name}")
        logger.info(f"  Found {len(translations)} translated segments")

        self.translations = translations
        return translations

    def validate_translations(self) -> Tuple[List[int], List[int]]:
        """
        Validate translations match transcript

        Returns:
            Tuple of (missing_ids, extra_ids)
        """
        transcript_ids = set(seg['id'] for seg in self.transcript['segments'])
        translation_ids = set(self.translations.keys())

        missing = sorted(transcript_ids - translation_ids)
        extra = sorted(translation_ids - transcript_ids)

        if missing:
            logger.warning(f"⚠️  Missing translations for {len(missing)} segments: {missing[:10]}")
        if extra:
            logger.warning(f"⚠️  Extra translations (not in transcript): {extra[:10]}")

        return missing, extra

    def generate_srt(self, output_path: Path, fill_missing: bool = True):
        """
        Generate SRT file

        Args:
            output_path: Output SRT file path
            fill_missing: Fill missing translations with original Thai text
        """
        if not self.transcript:
            raise ValueError("No transcript loaded")
        if not self.translations:
            raise ValueError("No translations loaded")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        missing_count = 0
        written_count = 0

        with open(output_path, 'w', encoding='utf-8') as f:
            for seg in self.transcript['segments']:
                seg_id = seg['id']
                start = seg['start']
                end = seg['end']

                # Get translation
                if seg_id in self.translations:
                    text = self.translations[seg_id]
                elif fill_missing:
                    text = f"[MISSING] {seg['text']}"
                    missing_count += 1
                else:
                    continue

                # Write SRT entry
                f.write(f"{seg_id + 1}\n")
                f.write(f"{self._to_srt_time(start)} --> {self._to_srt_time(end)}\n")
                f.write(f"{text}\n")
                f.write("\n")

                written_count += 1

        logger.info(f"✓ SRT file created: {output_path}")
        logger.info(f"  Written segments: {written_count}")
        if missing_count > 0:
            logger.warning(f"  Missing translations: {missing_count}")

    def generate_stats(self, output_path: Path):
        """
        Generate translation statistics

        Args:
            output_path: Output JSON file path
        """
        missing, extra = self.validate_translations()

        stats = {
            'timestamp': self.transcript['metadata']['timestamp'],
            'source_segments': len(self.transcript['segments']),
            'translated_segments': len(self.translations),
            'missing_segments': len(missing),
            'extra_segments': len(extra),
            'coverage': len(self.translations) / len(self.transcript['segments']) * 100,
            'missing_ids': missing[:20],  # First 20
            'extra_ids': extra[:20]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)

        logger.info(f"✓ Stats saved: {output_path}")

    @staticmethod
    def _to_srt_time(seconds: float) -> str:
        """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


# ======================== CLI INTERFACE ========================

def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Convert translated batch to SRT with timestamps",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic conversion
  python scripts/batch_to_srt.py transcript.json translated.txt

  # Specify output file
  python scripts/batch_to_srt.py transcript.json translated.txt \\
    -o workflow/04_final_srt/video_english.srt

  # Skip missing segments (don't fill with Thai)
  python scripts/batch_to_srt.py transcript.json translated.txt \\
    --no-fill-missing

  # Generate stats
  python scripts/batch_to_srt.py transcript.json translated.txt \\
    --stats stats.json

Expected Format in Translated File:
  [001]
  THAI: ข้อความภาษาไทย
  EN: English translation here

  [002]
  THAI: อีกข้อความ
  EN: Another translation

  OR simple format:
  [001] English translation here
  [002] Another translation
        """
    )

    parser.add_argument(
        'transcript',
        type=Path,
        help='Original transcript JSON file'
    )

    parser.add_argument(
        'translated',
        type=Path,
        help='Translated text file'
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output SRT file (default: auto-generated)'
    )

    parser.add_argument(
        '--no-fill-missing',
        action='store_true',
        help='Skip segments with missing translations'
    )

    parser.add_argument(
        '--stats',
        type=Path,
        help='Save statistics to JSON file'
    )

    args = parser.parse_args()

    try:
        # Setup output path
        if args.output:
            output_path = args.output
        else:
            base_name = args.transcript.stem.replace('_transcript', '')
            output_path = Path('workflow/04_final_srt') / f"{base_name}_english.srt"

        # Initialize converter
        converter = BatchToSRTConverter()

        logger.info("=" * 70)
        logger.info("Batch to SRT Converter")
        logger.info("=" * 70)

        # Load files
        converter.load_transcript(args.transcript)
        converter.parse_translated_file(args.translated)

        # Validate
        logger.info("\nValidating...")
        missing, extra = converter.validate_translations()

        coverage = len(converter.translations) / len(converter.transcript['segments']) * 100
        logger.info(f"  Coverage: {coverage:.1f}%")

        # Generate SRT
        logger.info("\nGenerating SRT...")
        converter.generate_srt(
            output_path,
            fill_missing=not args.no_fill_missing
        )

        # Generate stats if requested
        if args.stats:
            converter.generate_stats(args.stats)

        # Summary
        logger.info("\n" + "=" * 70)
        logger.info("CONVERSION COMPLETE")
        logger.info("=" * 70)
        logger.info(f"✓ Output SRT: {output_path}")
        logger.info(f"  Total segments: {len(converter.transcript['segments'])}")
        logger.info(f"  Translated: {len(converter.translations)}")
        logger.info(f"  Coverage: {coverage:.1f}%")

        if missing:
            logger.warning(f"\n⚠️  {len(missing)} segments missing translation")
            if args.no_fill_missing:
                logger.info("  These were skipped (--no-fill-missing)")
            else:
                logger.info("  These were filled with [MISSING] marker")

        logger.info("\n" + "=" * 70)
        logger.info("NEXT STEPS")
        logger.info("=" * 70)
        logger.info("1. Review the SRT file:")
        logger.info(f"   cat {output_path}")
        logger.info("2. Fix any [MISSING] segments if needed")
        logger.info("3. Merge with video:")
        logger.info(f"   python scripts/merge_srt_video.py video.mp4 {output_path}")

        sys.exit(0 if not missing else 1)

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
