#!/usr/bin/env python3
"""
Demo AI Rewrite - Show Top 5 Violations with AI Prompts
========================================================
Non-interactive demo showing what AI rewrite prompts look like
"""

from __future__ import annotations

import sys
sys.path.insert(0, 'scripts')

from pathlib import Path
from batch_to_srt import BatchToSRTConverter, count_words

# Import from ai_rewrite_subtitles
from ai_rewrite_subtitles import (
    EPISODE_CONFIG,
    find_violations,
    get_context,
    generate_rewrite_prompt,
    compute_wpm
)


def demo_top_violations(episode: str, top_n: int = 5):
    """Demo showing AI rewrite prompts for top violations."""

    if episode not in EPISODE_CONFIG:
        raise ValueError(f"Unknown episode: {episode}")

    config = EPISODE_CONFIG[episode]

    # Load data
    print(f"\n{'='*70}")
    print(f"DEMO: AI Rewrite Prompts for {episode}")
    print(f"{'='*70}\n")

    converter = BatchToSRTConverter()
    transcript_data = converter.load_transcript(config['transcript'])
    translations = converter.parse_translated_file(config['translated'])

    # Find violations
    violations = find_violations(
        transcript_data['segments'],
        translations,
        max_wpm=140.0,
        min_duration=1.5
    )

    # Filter out clearly erroneous segments (duration < 0.5s = transcription errors)
    violations = [v for v in violations if v['duration'] >= 0.5]

    # Sort by WPM (worst first)
    violations.sort(key=lambda x: x['wpm'], reverse=True)

    print(f"📊 Total violations found: {len(violations)}")
    print(f"📋 Showing top {top_n} worst cases:\n")

    # Process top N
    for i, violation in enumerate(violations[:top_n], 1):
        print(f"\n{'='*70}")
        print(f"EXAMPLE {i}/{top_n}: Segment #{violation['num']}")
        print(f"{'='*70}")
        print(f"Duration: {violation['duration']:.2f}s")
        print(f"Current: {violation['word_count']} words, {violation['wpm']:.1f} WPM")
        print(f"Target: ≤{violation.get('max_words', 0)} words, ≤140 WPM")
        print(f"\nOriginal text:")
        print(f'"{violation["text"]}"')

        # Get context
        context = get_context(
            violation['id'],
            transcript_data['segments'],
            translations
        )

        # Generate prompt
        prompt = generate_rewrite_prompt(violation, context, max_wpm=140.0)

        print(f"\n{'─'*70}")
        print("AI REWRITE PROMPT:")
        print(f"{'─'*70}")
        print(prompt)
        print(f"{'─'*70}")

        # Sample AI rewrites (manual examples)
        if i == 1:  # Segment #4
            print("\n💡 SAMPLE AI REWRITE:")
            print('REWRITTEN: "If you\'re new, let me catch you up."')
            print("WORD_COUNT: 7")
            print("WPM: 133.8")
            print("EXPLANATION: Removed 'here' (context clear), 'fill you in a bit' → 'catch you up'")
        elif i == 2:  # Segment #6
            print("\n💡 SAMPLE AI REWRITE:")
            print('REWRITTEN: "Students asked, \\"What\'s different between Season 1 and 2?\\""')
            print("WORD_COUNT: 9")
            print("WPM: 125.6")
            print("EXPLANATION: 'were asking' → 'asked', 'difference' → 'different', '2' instead of 'Season 2'")

        print(f"\n{'='*70}\n")

    print(f"\n{'='*70}")
    print("📋 NEXT STEPS:")
    print(f"{'='*70}")
    print("1. Copy each AI REWRITE PROMPT above")
    print("2. Paste to Claude/GPT-4")
    print("3. Get intelligent rewrite suggestion")
    print("4. Apply to SRT file")
    print()
    print(f"Or use interactive mode:")
    print(f".venv/bin/python scripts/ai_rewrite_subtitles.py --episode {episode} --interactive")
    print(f"{'='*70}\n")


if __name__ == '__main__':
    demo_top_violations('SS-1.5-ep01', top_n=5)
