#!/usr/bin/env python3
"""
Compare Three Versions: Thai → English → AI Rewrite
====================================================
Show side-by-side comparison for top violations
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
    compute_wpm
)


def compare_three_versions(episode: str, top_n: int = 10):
    """Compare Thai original vs English translation vs AI rewrite."""

    if episode not in EPISODE_CONFIG:
        raise ValueError(f"Unknown episode: {episode}")

    config = EPISODE_CONFIG[episode]

    # Load data
    print(f"\n{'='*80}")
    print(f"THREE-WAY COMPARISON: Thai → English → AI Rewrite")
    print(f"Episode: {episode}")
    print(f"{'='*80}\n")

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

    # Filter out errors and sort
    violations = [v for v in violations if v['duration'] >= 0.5]
    violations.sort(key=lambda x: x['wpm'], reverse=True)

    print(f"📊 Total violations: {len(violations)}")
    print(f"📋 Analyzing top {top_n} worst cases\n")

    # AI Rewrite suggestions (manual - based on analysis)
    ai_rewrites = {
        14: {
            'v1': "Many different tools.",
            'v2': "So many tools.",
            'recommended': "v1",
            'words': 3,
            'wpm': 115.4,
            'note': "Removes fillers 'and yeah, people use all kinds of stuff' - redundant with next segment"
        },
        86: {
            'v1': "Bunched together, not clean.",
            'v2': "They cluster together.",
            'recommended': "v2",
            'words': 3,
            'wpm': 104.7,
            'note': "Keeps meaning: candlesticks form in cluster, not cleanly separated"
        },
        95: {
            'v1': "We think it'll go this way.",
            'v2': "Looks like it'll go.",
            'recommended': "v1",
            'words': 6,
            'wpm': 240.0,
            'note': "Still over target (need ≤3) - should merge with segment 94"
        },
        87: {
            'v1': "Combined: this formation.",
            'v2': "Combine them: formation.",
            'recommended': "v1",
            'words': 3,
            'wpm': 114.0,
            'note': "Perfect compression while keeping meaning"
        },
        82: {
            'v1': "Price fell, combine candlesticks...",
            'v2': "Price down, candlesticks combine.",
            'recommended': "v2",
            'words': 4,
            'wpm': 123.3,
            'note': "Active voice, natural flow"
        },
        38: {
            'v1': "Patterns aren't enough - know WHY they work.",
            'v2': "Not just patterns - understand WHY.",
            'recommended': "v2",
            'words': 5,
            'wpm': 92.0,
            'note': "Under target, complete meaning"
        },
        43: {
            'v1': "You'll see this or that pattern.",
            'v2': "This pattern or that.",
            'recommended': "v1",
            'words': 6,
            'wpm': 157.9,
            'note': "Slightly over but more natural"
        },
        50: {
            'v1': "What's Action and Reaction?",
            'v2': "Action and Reaction?",
            'recommended': "v1",
            'words': 4,
            'wpm': 102.6,
            'note': "Question form keeps teaching tone"
        },
        51: {
            'v1': "Like forces. Action force.",
            'v2': "Forces - Action force.",
            'recommended': "v1",
            'words': 4,
            'wpm': 121.2,
            'note': "Natural teaching explanation"
        },
        93: {
            'v1': "But not always.",
            'v2': "Not always though.",
            'recommended': "v1",
            'words': 3,
            'wpm': 115.4,
            'note': "Perfect - concise and complete"
        },
    }

    # Process top N
    for i, violation in enumerate(violations[:top_n], 1):
        seg_id = violation['id']
        seg_num = violation['num']

        # Get Thai original
        thai_text = ""
        if seg_id < len(transcript_data['segments']):
            thai_text = transcript_data['segments'][seg_id].get('text', '')

        print(f"\n{'='*80}")
        print(f"CASE {i}/{top_n}: Segment #{seg_num}")
        print(f"{'='*80}")
        print(f"Duration: {violation['duration']:.2f}s")
        print(f"Target: ≤{violation.get('max_words', 0)} words (≤140 WPM)")
        print()

        # Thai original
        print(f"🇹🇭 THAI ORIGINAL:")
        print(f"   {thai_text}")
        print()

        # English translation
        print(f"🇬🇧 ENGLISH TRANSLATION (Current):")
        print(f"   {violation['text']}")
        print(f"   📊 {violation['word_count']} words, {violation['wpm']:.1f} WPM")
        print()

        # AI Rewrite
        if seg_num in ai_rewrites:
            rewrite = ai_rewrites[seg_num]
            recommended = rewrite[rewrite['recommended']]

            print(f"🤖 AI REWRITE (Recommended):")
            print(f"   {recommended}")
            print(f"   📊 {rewrite['words']} words, {rewrite['wpm']:.1f} WPM")
            print(f"   💡 {rewrite['note']}")

            if 'v1' in rewrite and 'v2' in rewrite and rewrite['recommended'] != 'v1':
                print(f"   Alternative: {rewrite['v1']}")
        else:
            print(f"🤖 AI REWRITE:")
            print(f"   [Need manual rewrite - too complex for auto-suggestion]")
            print(f"   Strategy: Check if should MERGE with adjacent segments")

        print(f"\n{'─'*80}")

    # Summary statistics
    print(f"\n\n{'='*80}")
    print("📊 SUMMARY STATISTICS")
    print(f"{'='*80}")

    total_words_original = sum(v['word_count'] for v in violations[:top_n])
    ai_rewrite_total = sum(ai_rewrites[v['num']]['words'] for v in violations[:top_n] if v['num'] in ai_rewrites)
    ai_rewrite_count = len([v for v in violations[:top_n] if v['num'] in ai_rewrites])

    print(f"Original: {total_words_original} words total")
    print(f"AI Rewrite ({ai_rewrite_count} segments): {ai_rewrite_total} words")
    print(f"Reduction: {total_words_original - ai_rewrite_total} words (-{((total_words_original - ai_rewrite_total) / total_words_original * 100):.1f}%)")
    print()

    meets_target = len([v for v in violations[:top_n] if v['num'] in ai_rewrites and ai_rewrites[v['num']]['wpm'] <= 140])
    print(f"✅ Meets WPM target: {meets_target}/{ai_rewrite_count} ({meets_target/ai_rewrite_count*100:.0f}%)")
    print(f"{'='*80}\n")


if __name__ == '__main__':
    compare_three_versions('SS-1.5-ep01', top_n=10)
