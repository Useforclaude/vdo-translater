#!/usr/bin/env python3
"""
Whisper Transcription Status Checker
====================================
Quickly check status of active transcriptions without loading Whisper model.

Usage:
    # Check all active transcriptions
    python scripts/whisper_status.py

    # Check specific checkpoint directory
    python scripts/whisper_status.py --checkpoint-dir /storage/whisper_checkpoints

    # Watch mode (auto-refresh every 5 seconds)
    python scripts/whisper_status.py --watch

    # JSON output (for scripts)
    python scripts/whisper_status.py --json
"""

import json
import time
import sys
import argparse
from pathlib import Path
from datetime import timedelta
from typing import List, Dict


def format_time(seconds: float) -> str:
    """Format seconds to readable time"""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        return f"{int(seconds // 60)}m {int(seconds % 60)}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def load_checkpoint(checkpoint_file: Path) -> Dict:
    """Load checkpoint data from file"""
    with open(checkpoint_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_all_checkpoints(checkpoint_dir: Path) -> List[Path]:
    """Find all checkpoint files in directory"""
    if not checkpoint_dir.exists():
        return []

    return list(checkpoint_dir.glob("*/checkpoint.json"))


def get_checkpoint_status(checkpoint_file: Path) -> Dict:
    """Get status of a single checkpoint"""
    try:
        data = load_checkpoint(checkpoint_file)

        video_hash = checkpoint_file.parent.name
        progress_pct = (data['last_segment_id'] / data['total_segments'] * 100) if data['total_segments'] > 0 else 0
        elapsed = time.time() - data['start_timestamp']
        speed = data.get('speed', 0.0)

        remaining_segments = data['total_segments'] - data['last_segment_id']
        eta = (remaining_segments / speed) if speed > 0 else 0

        return {
            'video_file': data['video_file'],
            'video_hash': video_hash,
            'model': data['model'],
            'device': data['device'],
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time'),
            'progress': {
                'current': data['last_segment_id'],
                'total': data['total_segments'],
                'percentage': progress_pct
            },
            'timing': {
                'elapsed': elapsed,
                'speed': speed,
                'eta': eta
            },
            'timestamps': {
                'created_at': data['created_at'],
                'last_updated': data['last_updated']
            },
            'checkpoint_path': str(checkpoint_file.parent)
        }

    except Exception as e:
        return {
            'error': str(e),
            'checkpoint_path': str(checkpoint_file.parent)
        }


def print_status_human(statuses: List[Dict]):
    """Print status in human-readable format"""
    if not statuses:
        print("No active transcriptions found")
        return

    print("=" * 80)
    print("WHISPER TRANSCRIPTION STATUS")
    print("=" * 80)
    print(f"Active transcriptions: {len(statuses)}")
    print()

    for i, status in enumerate(statuses, 1):
        if 'error' in status:
            print(f"[{i}] Error: {status['error']}")
            print(f"    Path: {status['checkpoint_path']}")
            print()
            continue

        progress = status['progress']
        timing = status['timing']

        print(f"[{i}] {status['video_file']}")
        print(f"    Hash: {status['video_hash']}")
        print(f"    Model: {status['model']} ({status['device']})")

        if status.get('start_time') or status.get('end_time'):
            range_str = f"{format_time(status['start_time'] or 0)} - "
            range_str += format_time(status['end_time']) if status['end_time'] else "end"
            print(f"    Time range: {range_str}")

        print()
        print(f"    Progress: {progress['current']}/{progress['total']} segments ({progress['percentage']:.1f}%)")

        # Progress bar
        bar_width = 50
        filled = int(bar_width * progress['percentage'] / 100)
        bar = "█" * filled + "░" * (bar_width - filled)
        print(f"    [{bar}]")

        print()
        print(f"    Elapsed: {format_time(timing['elapsed'])}")
        print(f"    Speed: {timing['speed']:.1f}x realtime")

        if timing['eta'] > 0:
            print(f"    ETA: {format_time(timing['eta'])}")
        else:
            print(f"    ETA: Calculating...")

        print()
        print(f"    Created: {status['timestamps']['created_at']}")
        print(f"    Last updated: {status['timestamps']['last_updated']}")
        print(f"    Checkpoint: {status['checkpoint_path']}")
        print()

    print("=" * 80)
    print()
    print("Commands:")
    print("  Resume: python scripts/whisper_transcribe.py <video> --resume")
    print("  Stop: Ctrl+C (checkpoint will be saved)")
    print("=" * 80)


def print_status_json(statuses: List[Dict]):
    """Print status in JSON format"""
    output = {
        'active_transcriptions': len(statuses),
        'timestamp': time.time(),
        'statuses': statuses
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))


def watch_mode(checkpoint_dir: Path, interval: int = 5):
    """Watch mode - auto-refresh status"""
    try:
        while True:
            # Clear screen
            print("\033[2J\033[H", end="")

            # Get and print status
            checkpoint_files = find_all_checkpoints(checkpoint_dir)
            statuses = [get_checkpoint_status(f) for f in checkpoint_files]
            print_status_human(statuses)

            print(f"\nRefreshing every {interval}s... (Ctrl+C to exit)")

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\nExiting watch mode...")
        sys.exit(0)


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Check status of Whisper transcriptions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check status (default checkpoint directory)
  python scripts/whisper_status.py

  # Check specific directory
  python scripts/whisper_status.py --checkpoint-dir /storage/whisper_checkpoints

  # Watch mode (auto-refresh)
  python scripts/whisper_status.py --watch

  # JSON output (for scripts)
  python scripts/whisper_status.py --json

  # Watch with custom interval
  python scripts/whisper_status.py --watch --interval 10
        """
    )

    parser.add_argument(
        '--checkpoint-dir',
        type=Path,
        default=Path('/storage/whisper_checkpoints'),
        help='Checkpoint directory (default: /storage/whisper_checkpoints)'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format'
    )

    parser.add_argument(
        '--watch',
        action='store_true',
        help='Watch mode (auto-refresh)'
    )

    parser.add_argument(
        '--interval',
        type=int,
        default=5,
        help='Refresh interval in seconds for watch mode (default: 5)'
    )

    args = parser.parse_args()

    try:
        # Watch mode
        if args.watch:
            if args.json:
                print("Error: --watch and --json cannot be used together", file=sys.stderr)
                sys.exit(1)

            watch_mode(args.checkpoint_dir, args.interval)
            return

        # Single check
        checkpoint_files = find_all_checkpoints(args.checkpoint_dir)
        statuses = [get_checkpoint_status(f) for f in checkpoint_files]

        if args.json:
            print_status_json(statuses)
        else:
            print_status_human(statuses)

        sys.exit(0)

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
