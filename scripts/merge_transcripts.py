#!/usr/bin/env python3
"""
Merge Multiple Whisper Transcripts
==================================
Merge transcripts from multiple time ranges into a single file.

Use case:
- Transcribed a 2-hour video in 4 chunks (0-30, 30-60, 60-90, 90-120 min)
- Each chunk has its own transcript JSON
- Merge all chunks into one complete transcript

Features:
- Merge multiple JSON transcripts
- Sort segments by timestamp
- Re-index segment IDs
- Detect and handle gaps/overlaps
- Output merged JSON + Thai SRT

Usage:
    # Merge multiple transcripts
    python scripts/merge_transcripts.py \\
      video_part1_transcript.json \\
      video_part2_transcript.json \\
      video_part3_transcript.json \\
      -o merged_transcript.json

    # Auto-find and merge (pattern matching)
    python scripts/merge_transcripts.py \\
      --pattern "video_part*_transcript.json" \\
      -o merged_transcript.json
"""

import json
import sys
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import timedelta

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_transcript(file_path: Path) -> Dict:
    """Load transcript JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        logger.info(f"✓ Loaded: {file_path.name}")
        logger.info(f"  Segments: {len(data['segments'])}")
        logger.info(f"  Duration: {format_time(data['metadata']['duration'])}")

        return data

    except Exception as e:
        logger.error(f"Failed to load {file_path}: {e}")
        raise


def validate_transcripts(transcripts: List[Dict]) -> Tuple[bool, List[str]]:
    """
    Validate transcripts for merging

    Returns:
        (is_valid, warnings)
    """
    warnings = []

    if len(transcripts) < 2:
        return False, ["Need at least 2 transcripts to merge"]

    # Check all have segments
    for i, trans in enumerate(transcripts):
        if 'segments' not in trans or not trans['segments']:
            warnings.append(f"Transcript {i+1} has no segments")
            return False, warnings

    # Sort by first timestamp
    sorted_trans = sorted(transcripts, key=lambda t: t['segments'][0]['start'])

    # Check for gaps and overlaps
    for i in range(len(sorted_trans) - 1):
        current_end = sorted_trans[i]['segments'][-1]['end']
        next_start = sorted_trans[i+1]['segments'][0]['start']

        gap = next_start - current_end

        if gap > 5.0:
            warnings.append(
                f"Gap detected: {format_time(gap)} between "
                f"transcript {i+1} (ends {format_time(current_end)}) and "
                f"transcript {i+2} (starts {format_time(next_start)})"
            )
        elif gap < -5.0:
            warnings.append(
                f"Overlap detected: {format_time(abs(gap))} between "
                f"transcript {i+1} (ends {format_time(current_end)}) and "
                f"transcript {i+2} (starts {format_time(next_start)})"
            )

    return True, warnings


def merge_transcripts(transcripts: List[Dict]) -> Dict:
    """
    Merge multiple transcripts into one

    Args:
        transcripts: List of transcript dictionaries

    Returns:
        Merged transcript dictionary
    """
    logger.info(f"Merging {len(transcripts)} transcripts...")

    # Collect all segments
    all_segments = []

    for trans in transcripts:
        all_segments.extend(trans['segments'])

    # Sort by start time
    all_segments.sort(key=lambda seg: seg['start'])

    # Re-index segment IDs
    for i, seg in enumerate(all_segments):
        seg['id'] = i

    # Calculate merged metadata
    total_text = ' '.join(seg['text'] for seg in all_segments)
    word_count = len(total_text.split())

    # Calculate average confidence
    confidences = [seg.get('confidence', 0.0) for seg in all_segments]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

    # Get duration
    duration = all_segments[-1]['end'] if all_segments else 0.0

    # Get model name (from first transcript)
    model_name = transcripts[0]['metadata'].get('model_name', 'unknown')

    # Create merged transcript
    merged = {
        'metadata': {
            'language': 'th',
            'duration': duration,
            'word_count': word_count,
            'average_confidence': avg_confidence,
            'model_name': model_name,
            'timestamp': transcripts[-1]['metadata']['timestamp'],  # Use latest
            'segment_count': len(all_segments),
            'merged_from': len(transcripts)
        },
        'text': total_text,
        'segments': all_segments
    }

    logger.info("✓ Merge complete:")
    logger.info(f"  - Total segments: {len(all_segments)}")
    logger.info(f"  - Total duration: {format_time(duration)}")
    logger.info(f"  - Total words: {word_count}")
    logger.info(f"  - Avg confidence: {avg_confidence:.1%}")

    return merged


def save_merged_json(merged: Dict, output_path: Path):
    """Save merged transcript as JSON"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    logger.info(f"✓ Merged JSON saved: {output_path}")


def save_merged_srt(merged: Dict, output_path: Path):
    """Save merged transcript as Thai SRT"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        for seg in merged['segments']:
            f.write(f"{seg['id'] + 1}\n")
            f.write(f"{to_srt_time(seg['start'])} --> {to_srt_time(seg['end'])}\n")
            f.write(f"{seg['text']}\n")
            f.write("\n")

    logger.info(f"✓ Merged SRT saved: {output_path}")


def to_srt_time(seconds: float) -> str:
    """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def format_time(seconds: float) -> str:
    """Format seconds to HH:MM:SS"""
    return str(timedelta(seconds=int(seconds)))


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Merge multiple Whisper transcripts into one",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Merge specific files
  python scripts/merge_transcripts.py \\
    part1_transcript.json \\
    part2_transcript.json \\
    part3_transcript.json \\
    -o merged_transcript.json

  # Auto-find with pattern
  python scripts/merge_transcripts.py \\
    --pattern "video_part*_transcript.json" \\
    -o merged_transcript.json

  # Include SRT output
  python scripts/merge_transcripts.py \\
    part*.json \\
    -o merged.json \\
    --srt merged_thai.srt

Use case:
  You transcribed a 2-hour video in 4 chunks:
  - video_0-1800_transcript.json    (0-30 min)
  - video_1800-3600_transcript.json (30-60 min)
  - video_3600-5400_transcript.json (60-90 min)
  - video_5400-7200_transcript.json (90-120 min)

  Merge them:
  python scripts/merge_transcripts.py video_*_transcript.json -o video_full.json
        """
    )

    parser.add_argument(
        'inputs',
        type=Path,
        nargs='*',
        help='Input transcript JSON files'
    )

    parser.add_argument(
        '--pattern',
        type=str,
        help='Glob pattern to find input files (e.g., "part*_transcript.json")'
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        required=True,
        help='Output merged JSON file'
    )

    parser.add_argument(
        '--srt',
        type=Path,
        help='Output Thai SRT file (optional)'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Force merge even with warnings'
    )

    args = parser.parse_args()

    try:
        # Collect input files
        input_files = []

        if args.pattern:
            # Find files by pattern
            pattern_files = list(Path.cwd().glob(args.pattern))
            if not pattern_files:
                logger.error(f"No files found matching pattern: {args.pattern}")
                sys.exit(1)

            input_files.extend(pattern_files)
            logger.info(f"Found {len(pattern_files)} files matching pattern")

        if args.inputs:
            input_files.extend(args.inputs)

        if not input_files:
            logger.error("No input files specified")
            parser.print_help()
            sys.exit(1)

        # Remove duplicates and sort
        input_files = sorted(set(input_files))

        logger.info("=" * 70)
        logger.info("MERGE TRANSCRIPTS")
        logger.info("=" * 70)
        logger.info(f"Input files: {len(input_files)}")
        for f in input_files:
            logger.info(f"  - {f.name}")
        logger.info("")

        # Load all transcripts
        transcripts = [load_transcript(f) for f in input_files]
        logger.info("")

        # Validate
        logger.info("Validating transcripts...")
        is_valid, warnings = validate_transcripts(transcripts)

        if warnings:
            logger.warning("Validation warnings:")
            for warning in warnings:
                logger.warning(f"  ⚠️  {warning}")
            logger.info("")

        if not is_valid and not args.force:
            logger.error("Validation failed. Use --force to merge anyway.")
            sys.exit(1)

        if warnings and not args.force:
            response = input("Continue with warnings? [y/N]: ").strip().lower()
            if response not in ['y', 'yes']:
                logger.info("Merge cancelled")
                sys.exit(0)

        # Merge
        merged = merge_transcripts(transcripts)

        # Save outputs
        logger.info("")
        save_merged_json(merged, args.output)

        if args.srt:
            save_merged_srt(merged, args.srt)

        # Summary
        logger.info("")
        logger.info("=" * 70)
        logger.info("MERGE COMPLETE")
        logger.info("=" * 70)
        logger.info(f"Output JSON: {args.output}")
        if args.srt:
            logger.info(f"Output SRT: {args.srt}")

        logger.info("")
        logger.info("Next steps:")
        logger.info("  1. Create translation batch:")
        logger.info(f"     python scripts/create_translation_batch.py {args.output}")
        logger.info("  2. Translate with Claude Code")
        logger.info("  3. Convert to English SRT:")
        logger.info(f"     python scripts/batch_to_srt.py {args.output} translated.txt")

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
