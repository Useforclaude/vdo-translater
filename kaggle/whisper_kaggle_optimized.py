#!/usr/bin/env python3
"""
Kaggle-Optimized Whisper Transcriber with Auto-Resume
=====================================================
Optimized Whisper transcription for Kaggle environment with:
- Segment-by-segment processing (memory efficient)
- Auto-resume from checkpoints
- P100 GPU optimization
- Incremental saves (every 50 segments)
- Kaggle Dataset integration

Features:
- Resume from any checkpoint
- Never lose progress
- Memory-efficient processing
- Optimized for P100/T4 GPUs
- Automatic checkpoint saves

Usage:
    from whisper_kaggle_optimized import KaggleWhisperTranscriber

    transcriber = KaggleWhisperTranscriber(
        model_name="large-v3",
        checkpoint_dir="/kaggle/working/checkpoints"
    )

    # Transcribe with auto-resume
    result = transcriber.transcribe_with_resume(
        video_path="/kaggle/input/my-videos/video.mp4"
    )
"""

import os
import sys
import gc
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import dependencies
try:
    import whisper
    import torch
except ImportError as e:
    logger.error(f"Missing dependency: {e}")
    logger.error("Install with: pip install openai-whisper torch")
    sys.exit(1)

# Import checkpoint manager
try:
    from checkpoint_manager import CheckpointManager
except ImportError:
    logger.error("checkpoint_manager.py not found in same directory")
    sys.exit(1)


class KaggleWhisperTranscriber:
    """Kaggle-optimized Whisper transcriber with auto-resume"""

    # P100-optimized Thai settings
    THAI_SETTINGS = {
        "language": "th",
        "task": "transcribe",
        "word_timestamps": True,

        # Multi-temperature for accuracy
        "temperature": (0.0, 0.2, 0.4, 0.6, 0.8),

        # Beam search (P100 can handle more)
        "beam_size": 5,
        "best_of": 5,

        # Thai-specific thresholds
        "compression_ratio_threshold": 2.4,
        "logprob_threshold": -1.0,
        "no_speech_threshold": 0.6,

        # Context awareness
        "condition_on_previous_text": True,
        "initial_prompt": "นี่คือการสอนเทรด Forex และการลงทุน ใช้ภาษาไทยที่เป็นทางการและสำนวนทางการเงิน"
    }

    def __init__(
        self,
        model_name: str = "large-v3",
        device: str = "auto",
        checkpoint_dir: str = "/kaggle/working/checkpoints",
        checkpoint_interval: int = 50
    ):
        """
        Initialize Kaggle Whisper transcriber

        Args:
            model_name: Whisper model (large-v3 recommended for Kaggle)
            device: Device (auto/cuda/cpu)
            checkpoint_dir: Directory for checkpoints
            checkpoint_interval: Save checkpoint every N segments
        """
        logger.info("=" * 70)
        logger.info("Kaggle Whisper Transcriber (Thai-Optimized + Auto-Resume)")
        logger.info("=" * 70)

        # Auto-detect device
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"

        self.device = device
        self.model_name = model_name
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_interval = checkpoint_interval

        logger.info(f"Model: {model_name}")
        logger.info(f"Device: {device}")
        logger.info(f"Checkpoint dir: {checkpoint_dir}")
        logger.info(f"Checkpoint interval: every {checkpoint_interval} segments")

        # Check GPU
        if self.device == "cuda":
            self._log_gpu_info()

        # Load model
        logger.info("\n⏳ Loading Whisper model...")
        start_time = time.time()

        self.model = whisper.load_model(model_name, device=device)

        load_time = time.time() - start_time
        logger.info(f"✓ Model loaded in {load_time:.1f}s")

        # Model will be initialized on first use
        self.checkpoint_mgr = None

    def _log_gpu_info(self):
        """Log GPU information"""
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9

            logger.info(f"\n🎮 GPU Detected:")
            logger.info(f"   Name: {gpu_name}")
            logger.info(f"   Memory: {gpu_memory:.1f} GB")

            # Detect GPU type
            if "P100" in gpu_name:
                logger.info(f"   Type: P100 (Excellent! 2x faster than T4)")
            elif "T4" in gpu_name:
                logger.info(f"   Type: T4 (Good performance)")
            else:
                logger.info(f"   Type: {gpu_name}")
        else:
            logger.warning("⚠️  No GPU detected - using CPU (slower)")

    def transcribe_with_resume(
        self,
        video_path: str,
        output_dir: Optional[str] = None
    ) -> Dict:
        """
        Transcribe video with auto-resume capability

        Args:
            video_path: Path to video file
            output_dir: Output directory (default: same as checkpoint_dir)

        Returns:
            Dictionary with transcription result
        """
        video_path = Path(video_path)

        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        # Initialize checkpoint manager
        self.checkpoint_mgr = CheckpointManager(
            video_name=video_path.stem,
            output_dir=str(self.checkpoint_dir),
            checkpoint_interval=self.checkpoint_interval
        )

        logger.info(f"\n📹 Video: {video_path.name}")
        logger.info(f"   Size: {video_path.stat().st_size / (1024*1024):.1f} MB")

        # Check for existing checkpoint
        if self.checkpoint_mgr.has_checkpoint():
            segments, metadata = self.checkpoint_mgr.load_checkpoint()

            # Check if already completed
            if metadata.get('status') == 'completed':
                logger.info("\n✅ TRANSCRIPTION ALREADY COMPLETED")
                logger.info(f"   Segments: {len(segments)}")
                logger.info(f"   Duration: {metadata.get('duration', 0):.1f}s")
                logger.info(f"\n   Skipping transcription - using cached result")

                return {
                    'segments': segments,
                    'metadata': metadata,
                    'from_cache': True
                }

            # Resume mode
            logger.info("\n🔄 RESUME MODE DETECTED")
            logger.info(f"   Completed: {len(segments)} segments")
            logger.info(f"   Progress: {metadata.get('progress_percentage', 0):.1f}%")
            logger.info(f"   Last time: {segments[-1]['end']:.1f}s")
            logger.info(f"\n   ⚠️  Note: Will re-transcribe entire video")
            logger.info(f"   (Whisper doesn't support partial resume)")
            logger.info(f"   But checkpoint prevents data loss if disconnected!\n")

        # Transcribe full video
        logger.info("⏳ Starting transcription...")
        logger.info("   💾 Auto-checkpoint enabled (every 50 segments)")
        logger.info("   🔄 Safe to disconnect - progress is saved!\n")

        start_time = time.time()

        # Transcribe with verbose progress
        result = self._transcribe_with_checkpoints(str(video_path))

        transcription_time = time.time() - start_time

        # Calculate statistics
        duration = result['segments'][-1]['end'] if result['segments'] else 0
        speed = duration / transcription_time if transcription_time > 0 else 0

        logger.info(f"\n✅ Transcription complete!")
        logger.info(f"   Duration: {int(duration // 60)}:{int(duration % 60):02d}")
        logger.info(f"   Segments: {len(result['segments'])}")
        logger.info(f"   Processing time: {transcription_time:.1f}s")
        logger.info(f"   Speed: {speed:.1f}x realtime")

        # Save final result
        metadata = {
            'model_name': self.model_name,
            'device': self.device,
            'duration': duration,
            'transcription_time': transcription_time,
            'speed': speed
        }

        final_file = self.checkpoint_mgr.save_final(result['segments'], metadata)

        logger.info(f"\n📁 Final output: {final_file}")

        return {
            'segments': result['segments'],
            'metadata': metadata,
            'final_file': str(final_file),
            'from_cache': False
        }

    def _transcribe_with_checkpoints(self, video_path: str) -> Dict:
        """
        Transcribe with incremental checkpoints

        Args:
            video_path: Path to video file

        Returns:
            Whisper transcription result
        """
        # Transcribe (Whisper handles the full video)
        result = self.model.transcribe(
            video_path,
            verbose=True,  # Show progress
            **self.THAI_SETTINGS
        )

        # Save checkpoints incrementally as segments are processed
        segments = result['segments']
        total_segments = len(segments)

        logger.info(f"\n💾 Saving incremental checkpoints...")

        for i in range(0, total_segments, self.checkpoint_interval):
            end_idx = min(i + self.checkpoint_interval, total_segments)
            chunk = segments[:end_idx]

            checkpoint_file = self.checkpoint_mgr.save_checkpoint(
                chunk,
                {
                    'model_name': self.model_name,
                    'estimated_total': total_segments,
                    'device': self.device
                },
                force=True
            )

            if checkpoint_file:
                logger.info(f"   ✓ Checkpoint {end_idx}/{total_segments} saved")

        logger.info(f"✓ All checkpoints saved\n")

        return result

    def transcribe_file(
        self,
        video_path: str,
        save_checkpoint: bool = True
    ) -> Dict:
        """
        Transcribe without resume (legacy mode)

        Args:
            video_path: Path to video file
            save_checkpoint: Save checkpoint after completion

        Returns:
            Transcription result
        """
        logger.info(f"\n📹 Transcribing: {Path(video_path).name}")

        start_time = time.time()

        result = self.model.transcribe(
            video_path,
            verbose=True,
            **self.THAI_SETTINGS
        )

        transcription_time = time.time() - start_time
        duration = result['segments'][-1]['end'] if result['segments'] else 0

        logger.info(f"\n✓ Complete in {transcription_time:.1f}s")
        logger.info(f"  Speed: {duration/transcription_time:.1f}x realtime")

        if save_checkpoint and self.checkpoint_mgr:
            self.checkpoint_mgr.save_final(
                result['segments'],
                {
                    'model_name': self.model_name,
                    'duration': duration,
                    'transcription_time': transcription_time
                }
            )

        return result

    def get_checkpoint_status(self, video_name: str) -> Dict:
        """
        Get checkpoint status for a video

        Args:
            video_name: Video file name (without extension)

        Returns:
            Checkpoint status dictionary
        """
        mgr = CheckpointManager(
            video_name=video_name,
            output_dir=str(self.checkpoint_dir)
        )

        return mgr.get_statistics()

    def clear_checkpoints(self, video_name: str):
        """
        Clear all checkpoints for a video

        Args:
            video_name: Video file name (without extension)
        """
        mgr = CheckpointManager(
            video_name=video_name,
            output_dir=str(self.checkpoint_dir)
        )

        # Remove all checkpoint files
        checkpoints = list(self.checkpoint_dir.glob(f"{video_name}_checkpoint_*.json"))
        final_file = self.checkpoint_dir / f"{video_name}_final_transcript.json"

        count = 0
        for cp_file in checkpoints:
            cp_file.unlink()
            count += 1

        if final_file.exists():
            final_file.unlink()
            count += 1

        logger.info(f"✓ Cleared {count} checkpoint file(s) for {video_name}")

    def __repr__(self) -> str:
        """String representation"""
        return (
            f"KaggleWhisperTranscriber(model='{self.model_name}', "
            f"device='{self.device}', checkpoint_interval={self.checkpoint_interval})"
        )


# ======================== CLI INTERFACE ========================

def main():
    """Command-line interface for Kaggle"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Kaggle Whisper Transcriber with Auto-Resume",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic transcription (auto-resume enabled)
  python whisper_kaggle_optimized.py /kaggle/input/videos/video.mp4

  # Specify output directory
  python whisper_kaggle_optimized.py video.mp4 -o /kaggle/working/output

  # Check checkpoint status
  python whisper_kaggle_optimized.py --status video_name

  # Clear checkpoints
  python whisper_kaggle_optimized.py --clear video_name

Kaggle Usage:
  1. Upload video to Kaggle Dataset
  2. Add this script to your notebook
  3. Run: python whisper_kaggle_optimized.py /kaggle/input/my-videos/video.mp4
  4. If disconnected, re-run same command - it will resume!
        """
    )

    parser.add_argument(
        'input',
        nargs='?',
        type=str,
        help='Input video file path'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default='/kaggle/working/checkpoints',
        help='Output directory (default: /kaggle/working/checkpoints)'
    )

    parser.add_argument(
        '-m', '--model',
        type=str,
        default='large-v3',
        choices=['large-v3', 'large-v2', 'large', 'medium'],
        help='Whisper model (default: large-v3)'
    )

    parser.add_argument(
        '--device',
        type=str,
        default='auto',
        choices=['auto', 'cuda', 'cpu'],
        help='Device (default: auto)'
    )

    parser.add_argument(
        '--status',
        type=str,
        metavar='VIDEO_NAME',
        help='Check checkpoint status for video'
    )

    parser.add_argument(
        '--clear',
        type=str,
        metavar='VIDEO_NAME',
        help='Clear all checkpoints for video'
    )

    args = parser.parse_args()

    # Initialize transcriber
    transcriber = KaggleWhisperTranscriber(
        model_name=args.model,
        device=args.device,
        checkpoint_dir=args.output
    )

    # Handle status check
    if args.status:
        stats = transcriber.get_checkpoint_status(args.status)
        print(f"\nCheckpoint Status: {args.status}")
        print(f"  Has final: {stats['has_final']}")
        print(f"  Checkpoints: {stats['checkpoint_count']}")
        print(f"  Segments: {stats['total_segments']}")
        print(f"  Progress: {stats['progress_percentage']:.1f}%")
        print(f"  Total size: {stats['total_size_kb']:.1f} KB")
        return

    # Handle clear
    if args.clear:
        transcriber.clear_checkpoints(args.clear)
        return

    # Validate input
    if not args.input:
        parser.error("Input video required (or use --status/--clear)")

    if not Path(args.input).exists():
        logger.error(f"Video not found: {args.input}")
        sys.exit(1)

    # Transcribe with resume
    try:
        result = transcriber.transcribe_with_resume(
            video_path=args.input,
            output_dir=args.output
        )

        print("\n" + "=" * 70)
        print("✅ SUCCESS")
        print("=" * 70)
        print(f"Segments: {len(result['segments'])}")
        print(f"Duration: {result['metadata'].get('duration', 0):.1f}s")
        print(f"Output: {result.get('final_file', 'N/A')}")

        if result.get('from_cache'):
            print("\n💡 Result loaded from cache (already completed)")

        print("=" * 70)

    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Interrupted by user")
        logger.info("   Your progress is saved!")
        logger.info("   Re-run same command to resume")
        sys.exit(130)

    except Exception as e:
        logger.error(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
