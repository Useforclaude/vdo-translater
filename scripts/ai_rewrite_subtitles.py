#!/usr/bin/env python3
"""
AI-Assisted Intelligent Subtitle Rewriting
===========================================
Rewrite subtitles to fit WPM constraints while preserving 100% of meaning.

Features:
- Preserves all meaning (no truncation!)
- Uses AI to intelligently rephrase
- Considers context from surrounding segments
- Respects duration constraints
- Uses contractions, shorter synonyms, removes fillers

Usage:
    # Rewrite single segment
    python scripts/ai_rewrite_subtitles.py --episode SS-1.5-ep01 --segment 4

    # Rewrite all violations in episode
    python scripts/ai_rewrite_subtitles.py --episode SS-1.5-ep01 --auto

    # Interactive mode (review each change)
    python scripts/ai_rewrite_subtitles.py --episode SS-1.5-ep01 --interactive
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from batch_to_srt import BatchToSRTConverter, count_words

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


EPISODE_CONFIG = {
    "SS-1.5-ep01": {
        "transcript": Path("workflow/01_transcripts/SS-1.5-ep01_transcript.json"),
        "translated": Path("workflow/03_translated/SS-1.5-ep01_translated.txt"),
        "srt": Path("workflow/04_final_srt/SS-1.5-ep01_english.srt"),
    },
    "SS-1.5-ep02": {
        "transcript": Path("workflow/01_transcripts/SS-1.5-ep02_transcript.json"),
        "translated": Path("workflow/03_translated/SS-1.5-ep02_translated.txt"),
        "srt": Path("workflow/04_final_srt/SS-1.5-ep02_english.srt"),
    },
    "SS-1.5-ep03": {
        "transcript": Path("workflow/01_transcripts/SS-1.5-ep03_transcript.json"),
        "translated": Path("workflow/03_translated/SS-1.5-ep03_translated.txt"),
        "srt": Path("workflow/04_final_srt/SS-1.5-ep03_english.srt"),
    },
    "SS1.5-ep04-part-1": {
        "transcript": Path("workflow/01_transcripts/SS1.5-ep-04-part-1_transcript.json"),
        "translated": Path("workflow/03_translated/SS1.5-ep04-part-1_translated.txt"),
        "srt": Path("workflow/04_final_srt/SS1.5-ep04-part-1_english.srt"),
    },
    "SS-1.5-ep04-part-2": {
        "transcript": Path("workflow/01_transcripts/SS-1.5-ep-04-part-2_transcript.json"),
        "translated": Path("workflow/03_translated/SS-1.5-ep04-part-2_translated.txt"),
        "srt": Path("workflow/04_final_srt/SS-1.5-ep04-part-2_english.srt"),
    },
    "SS-1.5-ep05": {
        "transcript": Path("workflow/01_transcripts/SS-1.5-ep05_transcript.json"),
        "translated": Path("workflow/03_translated/SS-1.5-ep05_translated.txt"),
        "srt": Path("workflow/04_final_srt/SS-1.5-ep05_english.srt"),
    },
}


def compute_wpm(word_count: int, duration: float) -> float:
    """Calculate words per minute."""
    if duration <= 0:
        return float('inf') if word_count > 0 else 0.0
    return (word_count / duration) * 60.0


def find_violations(
    segments: List[Dict],
    translations: Dict[int, Dict],
    max_wpm: float = 140.0,
    min_duration: float = 1.5
) -> List[Dict]:
    """Find segments that violate WPM or duration constraints."""
    violations = []

    for seg in segments:
        seg_id = seg['id']
        duration = max(seg['end'] - seg['start'], 0.0)

        if seg_id not in translations:
            continue

        entry = translations[seg_id]
        text = entry.get('text', '')
        word_count = entry.get('word_count', count_words(text))

        if duration < min_duration:
            violations.append({
                'id': seg_id,
                'num': seg_id + 1,
                'type': 'duration',
                'duration': duration,
                'word_count': word_count,
                'wpm': compute_wpm(word_count, duration),
                'text': text
            })
        else:
            wpm = compute_wpm(word_count, duration)
            if wpm > max_wpm:
                violations.append({
                    'id': seg_id,
                    'num': seg_id + 1,
                    'type': 'wpm',
                    'duration': duration,
                    'word_count': word_count,
                    'wpm': wpm,
                    'max_words': int(max_wpm * duration / 60.0),
                    'text': text
                })

    return violations


def get_context(
    seg_id: int,
    segments: List[Dict],
    translations: Dict[int, Dict],
    context_window: int = 2
) -> Dict:
    """Get surrounding context for a segment."""
    context = {
        'before': [],
        'current': None,
        'after': []
    }

    # Get segments before
    for i in range(max(0, seg_id - context_window), seg_id):
        if i in translations:
            context['before'].append({
                'num': i + 1,
                'text': translations[i].get('text', '')
            })

    # Current segment
    if seg_id < len(segments):
        seg = segments[seg_id]
        context['current'] = {
            'num': seg_id + 1,
            'duration': seg['end'] - seg['start'],
            'thai': seg.get('text', ''),
            'english': translations.get(seg_id, {}).get('text', '')
        }

    # Get segments after
    for i in range(seg_id + 1, min(len(segments), seg_id + context_window + 1)):
        if i in translations:
            context['after'].append({
                'num': i + 1,
                'text': translations[i].get('text', '')
            })

    return context


def generate_rewrite_prompt(
    violation: Dict,
    context: Dict,
    max_wpm: float = 140.0
) -> str:
    """Generate prompt for AI to rewrite segment."""

    target_words = violation.get('max_words',
                                  int(max_wpm * violation['duration'] / 60.0))

    prompt = f"""You are an expert subtitle editor for Forex trading educational videos.

**Task**: Rewrite the following subtitle to be MORE CONCISE while preserving 100% of the meaning.

**Constraints**:
- Duration: {violation['duration']:.2f} seconds
- Current words: {violation['word_count']}
- Target words: ≤{target_words} words (to achieve ≤{max_wpm} WPM)
- Current WPM: {violation['wpm']:.1f} (too fast!)

**Context** (for reference only, don't modify these):
"""

    if context['before']:
        prompt += "\n**Previous segments**:\n"
        for seg in context['before']:
            prompt += f"- [{seg['num']}] {seg['text']}\n"

    prompt += f"\n**CURRENT SEGMENT TO REWRITE**:\n"
    prompt += f"[{context['current']['num']}] {context['current']['english']}\n"

    if context['after']:
        prompt += "\n**Following segments**:\n"
        for seg in context['after']:
            prompt += f"- [{seg['num']}] {seg['text']}\n"

    prompt += f"""
**Rewriting strategies** (use ALL that apply):
1. **Contractions**: "we will" → "we'll", "let us" → "let's", "it is" → "it's"
2. **Remove fillers**: "basically", "actually", "you know", "I mean", "right?"
3. **Shorter synonyms**: "utilize" → "use", "purchase" → "buy", "demonstrate" → "show"
4. **Combine ideas**: Merge related clauses if it shortens text
5. **Active voice**: Prefer active over passive when shorter
6. **Remove redundancy**: "free gift" → "gift", "past history" → "history"

**CRITICAL RULES**:
✅ Preserve 100% of the meaning and information
✅ Maintain casual teaching tone (this is conversational, not formal)
✅ Keep all technical terms (Price Action, candlestick, etc.)
✅ Must be ≤{target_words} words
❌ NO truncation with "..."
❌ NO removing important information
❌ NO changing meaning

**Output format**:
REWRITTEN: [your rewritten version here]
WORD_COUNT: [number]
EXPLANATION: [brief note on what you changed]

Now rewrite the segment:
"""

    return prompt


def ai_rewrite_segment(
    violation: Dict,
    context: Dict,
    max_wpm: float = 140.0,
    model: str = "manual"
) -> Optional[Dict]:
    """
    AI-assisted rewrite of a segment.

    For now, this is a MANUAL process where we show the prompt
    and user can paste Claude's response.

    In future: Could integrate with Claude API or OpenAI API.
    """
    prompt = generate_rewrite_prompt(violation, context, max_wpm)

    print("\n" + "="*70)
    print("AI REWRITE PROMPT")
    print("="*70)
    print(prompt)
    print("="*70)

    if model == "manual":
        print("\n📋 Copy the prompt above and paste to Claude/GPT-4")
        print("Then paste the REWRITTEN text here (or press Enter to skip):\n")

        rewritten = input("REWRITTEN: ").strip()
        if not rewritten:
            return None

        word_count = len(rewritten.split())

        print(f"\nWord count: {word_count} (target: ≤{violation.get('max_words', 0)})")

        if word_count > violation.get('max_words', 0):
            print(f"⚠️  Warning: Still exceeds target!")
            confirm = input("Use anyway? (y/n): ").strip().lower()
            if confirm != 'y':
                return None

        return {
            'original': violation['text'],
            'rewritten': rewritten,
            'original_words': violation['word_count'],
            'rewritten_words': word_count,
            'original_wpm': violation['wpm'],
            'rewritten_wpm': compute_wpm(word_count, violation['duration'])
        }

    # TODO: Implement API integration
    else:
        raise NotImplementedError("API integration coming soon")


def interactive_rewrite_session(
    episode: str,
    max_wpm: float = 140.0,
    min_duration: float = 1.5
):
    """Interactive session to rewrite violations one by one."""

    if episode not in EPISODE_CONFIG:
        raise ValueError(f"Unknown episode: {episode}")

    config = EPISODE_CONFIG[episode]

    # Load data
    logger.info(f"Loading {episode}...")
    converter = BatchToSRTConverter()
    transcript_data = converter.load_transcript(config['transcript'])
    translations = converter.parse_translated_file(config['translated'])

    # Find violations
    violations = find_violations(
        transcript_data['segments'],
        translations,
        max_wpm,
        min_duration
    )

    logger.info(f"Found {len(violations)} violations")

    if not violations:
        logger.info("✅ No violations found!")
        return

    # Show summary
    print("\n" + "="*70)
    print(f"VIOLATION SUMMARY - {episode}")
    print("="*70)
    for i, v in enumerate(violations[:10], 1):
        print(f"{i}. Segment #{v['num']}: {v['word_count']} words, "
              f"{v['wpm']:.1f} WPM, {v['duration']:.2f}s")
        print(f"   \"{v['text'][:60]}...\"")
    if len(violations) > 10:
        print(f"   ... and {len(violations) - 10} more")
    print("="*70)

    # Process violations
    rewrites = []
    for i, violation in enumerate(violations, 1):
        print(f"\n{'='*70}")
        print(f"VIOLATION {i}/{len(violations)}")
        print(f"{'='*70}")
        print(f"Segment #{violation['num']}")
        print(f"Duration: {violation['duration']:.2f}s")
        print(f"Current: {violation['word_count']} words, {violation['wpm']:.1f} WPM")
        print(f"Target: ≤{violation.get('max_words', 0)} words, ≤{max_wpm} WPM")
        print(f"\nOriginal text:")
        print(f'"{violation["text"]}"')

        # Get context
        context = get_context(
            violation['id'],
            transcript_data['segments'],
            translations
        )

        # Options
        print("\nOptions:")
        print("  [r] Rewrite with AI assistance")
        print("  [s] Skip this segment")
        print("  [q] Quit and save progress")

        choice = input("\nChoice: ").strip().lower()

        if choice == 'q':
            break
        elif choice == 's':
            continue
        elif choice == 'r':
            result = ai_rewrite_segment(violation, context, max_wpm)
            if result:
                result['segment_id'] = violation['id']
                result['segment_num'] = violation['num']
                rewrites.append(result)
                print(f"✅ Saved rewrite for segment #{violation['num']}")

    # Save results
    if rewrites:
        output_path = Path(f"workflow/rewrites/{episode}_rewrites.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'episode': episode,
                'total_violations': len(violations),
                'rewrites': rewrites,
                'stats': {
                    'processed': len(rewrites),
                    'total_words_saved': sum(r['original_words'] - r['rewritten_words']
                                            for r in rewrites),
                    'avg_compression': (
                        sum(r['rewritten_words'] / r['original_words']
                            for r in rewrites) / len(rewrites)
                        if rewrites else 0
                    )
                }
            }, f, indent=2, ensure_ascii=False)

        logger.info(f"\n✅ Saved {len(rewrites)} rewrites to: {output_path}")
        logger.info(f"   Total words saved: {sum(r['original_words'] - r['rewritten_words'] for r in rewrites)}")
    else:
        logger.info("\nNo rewrites saved")


def main():
    parser = argparse.ArgumentParser(
        description="AI-assisted intelligent subtitle rewriting"
    )

    parser.add_argument(
        '--episode',
        choices=sorted(EPISODE_CONFIG.keys()),
        required=True,
        help='Episode to process'
    )

    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Interactive rewriting session'
    )

    parser.add_argument(
        '--max-wpm',
        type=float,
        default=140.0,
        help='Maximum WPM (default: 140)'
    )

    parser.add_argument(
        '--min-duration',
        type=float,
        default=1.5,
        help='Minimum duration in seconds (default: 1.5)'
    )

    args = parser.parse_args()

    if args.interactive:
        interactive_rewrite_session(
            args.episode,
            args.max_wpm,
            args.min_duration
        )
    else:
        logger.error("Currently only --interactive mode is supported")
        logger.info("Usage: python scripts/ai_rewrite_subtitles.py --episode SS-1.5-ep01 --interactive")
        sys.exit(1)


if __name__ == '__main__':
    main()
