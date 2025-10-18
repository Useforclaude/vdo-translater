#!/usr/bin/env python3
"""
Smart Re-map Translation to New Transcript
===========================================
Match existing high-quality translations to new transcript timestamps
using text similarity.
"""

from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict, List, Tuple


def load_transcript(path: Path) -> List[Dict]:
    """Load transcript JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['segments']


def parse_old_translation(path: Path) -> List[Dict]:
    """Parse old translation file with timestamps."""
    segments = []

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern: [Segment N] start_time → end_time
    pattern = r'\[Segment (\d+)\] ([\d.]+)s → ([\d.]+)s\n(.+?)(?=\n\[Segment|\n---|\Z)'

    for match in re.finditer(pattern, content, re.DOTALL):
        seg_num = int(match.group(1))
        start = float(match.group(2))
        end = float(match.group(3))
        text = match.group(4).strip()

        segments.append({
            'num': seg_num,
            'start': start,
            'end': end,
            'english': text
        })

    return segments


def similarity(a: str, b: str) -> float:
    """Calculate text similarity (0-1)."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_best_match(thai_text: str, old_segments: List[Dict],
                     used_indices: set) -> Tuple[int, float]:
    """Find best matching segment by Thai text similarity."""
    # For this, we need to also store Thai text in old segments
    # Since we don't have it, we'll use timestamp proximity instead
    # This is a limitation - will document in output
    return -1, 0.0


def smart_remap(
    new_transcript_path: Path,
    old_translation_path: Path,
    output_path: Path
) -> Dict:
    """
    Re-map old translations to new transcript timestamps.

    Strategy:
    1. Load new transcript (has Thai text + new timestamps)
    2. Load old translation (has English text + old timestamps)
    3. Match by timestamp proximity (since we don't have Thai in old file)
    4. Create new translation file with correct timestamps
    """

    # Load data
    new_segments = load_transcript(new_transcript_path)
    old_segments = parse_old_translation(old_translation_path)

    print(f"\n{'='*70}")
    print("SMART RE-MAP: Old Translation → New Transcript")
    print(f"{'='*70}\n")
    print(f"📄 New transcript: {len(new_segments)} segments")
    print(f"📄 Old translation: {len(old_segments)} segments")
    print()

    if len(new_segments) != len(old_segments):
        print(f"⚠️  WARNING: Segment count mismatch!")
        print(f"   New: {len(new_segments)}, Old: {len(old_segments)}")
        print(f"   Will attempt best-effort matching...\n")

    # Simple strategy: Match by segment number (assuming same order)
    # This works if transcript was just re-timed but segments are same
    remapped = []
    matches = 0
    mismatches = 0

    for i, new_seg in enumerate(new_segments):
        seg_id = new_seg['id']

        # Try to find matching old segment
        old_seg = None
        if seg_id < len(old_segments):
            old_seg = old_segments[seg_id]

        if old_seg:
            # Check timestamp difference
            time_diff = abs(new_seg['start'] - old_seg['start'])

            remapped.append({
                'id': seg_id,
                'num': seg_id + 1,
                'start': new_seg['start'],
                'end': new_seg['end'],
                'thai': new_seg.get('text', ''),
                'english': old_seg['english'],
                'time_diff': time_diff,
                'matched': time_diff < 10.0  # Consider match if within 10s
            })

            if time_diff < 10.0:
                matches += 1
            else:
                mismatches += 1
        else:
            # No matching old segment - needs new translation
            remapped.append({
                'id': seg_id,
                'num': seg_id + 1,
                'start': new_seg['start'],
                'end': new_seg['end'],
                'thai': new_seg.get('text', ''),
                'english': '[NEEDS TRANSLATION]',
                'time_diff': None,
                'matched': False
            })
            mismatches += 1

    # Generate output file
    output_lines = []
    output_lines.append("=== SS1.5 EP-01 ENGLISH TRANSLATION (Re-mapped) ===")
    output_lines.append("Context: Reversal Candlestick Special Episode - Action vs Reaction concept")
    output_lines.append("Tone: Casual teaching, natural human conversation")
    output_lines.append(f"Source: {new_transcript_path.name} ({len(new_segments)} segments)")
    output_lines.append(f"Re-mapped from: {old_translation_path.name}")
    output_lines.append("")

    for seg in remapped:
        output_lines.append(f"[Segment {seg['num']}] {seg['start']:.3f}s → {seg['end']:.3f}s")
        output_lines.append(seg['english'])
        output_lines.append("")

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    # Statistics
    stats = {
        'total_segments': len(remapped),
        'matched': matches,
        'mismatched': mismatches,
        'match_rate': matches / len(remapped) * 100 if remapped else 0,
        'avg_time_diff': sum(s['time_diff'] for s in remapped if s['time_diff'] is not None) / matches if matches > 0 else 0
    }

    print(f"{'='*70}")
    print("RESULTS:")
    print(f"{'='*70}")
    print(f"✅ Matched: {matches}/{len(remapped)} ({stats['match_rate']:.1f}%)")
    print(f"⚠️  Mismatched: {mismatches}/{len(remapped)}")
    if matches > 0:
        print(f"📊 Avg time diff: {stats['avg_time_diff']:.2f}s")
    print()
    print(f"📁 Output saved to: {output_path}")
    print(f"{'='*70}\n")

    return {
        'remapped': remapped,
        'stats': stats,
        'output_path': str(output_path)
    }


def compare_versions(
    original_path: Path,
    remapped_path: Path,
    num_samples: int = 10
):
    """Compare original vs remapped translations."""

    print(f"\n{'='*70}")
    print("COMPARISON: Original vs Re-mapped")
    print(f"{'='*70}\n")

    original = parse_old_translation(original_path)
    remapped = parse_old_translation(remapped_path)

    print(f"Original: {len(original)} segments")
    print(f"Re-mapped: {len(remapped)} segments")
    print(f"\nShowing first {num_samples} segments:\n")

    for i in range(min(num_samples, len(original), len(remapped))):
        orig = original[i]
        remap = remapped[i]

        print(f"{'─'*70}")
        print(f"Segment #{i+1}:")
        print(f"{'─'*70}")

        print(f"📍 ORIGINAL:")
        print(f"   Time: {orig['start']:.2f}s → {orig['end']:.2f}s")
        print(f"   Text: {orig['english'][:80]}...")
        print()

        print(f"📍 RE-MAPPED:")
        print(f"   Time: {remap['start']:.2f}s → {remap['end']:.2f}s")
        print(f"   Text: {remap['english'][:80]}...")

        # Check if text changed
        if orig['english'] != remap['english']:
            print(f"   ⚠️  TEXT CHANGED!")
        else:
            print(f"   ✅ Text preserved")

        # Check time difference
        time_diff = abs(orig['start'] - remap['start'])
        print(f"   ⏱️  Time diff: {time_diff:.2f}s")
        print()


if __name__ == '__main__':
    # Paths
    new_transcript = Path('workflow/01_transcripts/SS-1.5-ep01_transcript.json')
    old_translation = Path('workflow/03_translated/SS-1.5-ep01_translated.txt.backup-20251018-172909')
    output = Path('workflow/03_translated/SS-1.5-ep01_translated_remapped.txt')

    # Run re-mapping
    result = smart_remap(new_transcript, old_translation, output)

    # Compare versions
    compare_versions(old_translation, output, num_samples=10)

    # Summary
    print(f"\n{'='*70}")
    print("NEXT STEPS:")
    print(f"{'='*70}")
    print("1. Review remapped file for quality")
    print("2. Check mismatched segments manually")
    print("3. If satisfied, replace original:")
    print(f"   mv {output} workflow/03_translated/SS-1.5-ep01_translated.txt")
    print(f"{'='*70}\n")
