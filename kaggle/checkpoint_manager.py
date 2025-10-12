#!/usr/bin/env python3
"""
Kaggle Checkpoint Manager - Auto-Resume System
===============================================
Manages checkpoints for Whisper transcription on Kaggle with auto-resume capability.

Features:
- Save checkpoints every N segments (default: 50)
- Auto-detect existing checkpoints
- Resume from last saved position
- Merge multiple checkpoint files
- Validate checkpoint integrity
- Kaggle Dataset integration

Usage:
    from checkpoint_manager import CheckpointManager

    mgr = CheckpointManager(video_name="ep-01", output_dir="/kaggle/working/checkpoints")

    # Check for existing work
    if mgr.has_checkpoint():
        segments, metadata = mgr.load_checkpoint()
        print(f"Resume from segment {len(segments)}")

    # Save progress
    mgr.save_checkpoint(segments, metadata)

    # Final save
    mgr.save_final(segments, metadata)
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import hashlib

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CheckpointManager:
    """Manages checkpoints for Kaggle Whisper transcription"""

    def __init__(
        self,
        video_name: str,
        output_dir: str = "/kaggle/working/checkpoints",
        checkpoint_interval: int = 50
    ):
        """
        Initialize checkpoint manager

        Args:
            video_name: Video file name (without extension)
            output_dir: Directory to save checkpoints
            checkpoint_interval: Save checkpoint every N segments
        """
        self.video_name = video_name
        self.output_dir = Path(output_dir)
        self.checkpoint_interval = checkpoint_interval

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Checkpoint file patterns
        self.checkpoint_pattern = f"{video_name}_checkpoint_*.json"
        self.final_file = self.output_dir / f"{video_name}_final_transcript.json"

        logger.info(f"Checkpoint Manager initialized")
        logger.info(f"  Video: {video_name}")
        logger.info(f"  Output: {output_dir}")
        logger.info(f"  Interval: every {checkpoint_interval} segments")

    def has_checkpoint(self) -> bool:
        """
        Check if any checkpoint exists

        Returns:
            True if checkpoint found, False otherwise
        """
        # Check for final transcript first
        if self.final_file.exists():
            logger.info(f"✅ Final transcript found: {self.final_file}")
            return True

        # Check for checkpoint files
        checkpoints = list(self.output_dir.glob(self.checkpoint_pattern))

        if checkpoints:
            logger.info(f"🔄 Found {len(checkpoints)} checkpoint(s)")
            return True

        logger.info("🆕 No checkpoint found - starting fresh")
        return False

    def load_checkpoint(self) -> Tuple[List[Dict], Dict]:
        """
        Load most recent checkpoint

        Returns:
            Tuple of (segments, metadata)
            - segments: List of completed segments
            - metadata: Checkpoint metadata

        Raises:
            FileNotFoundError: If no checkpoint exists
        """
        # Try final transcript first
        if self.final_file.exists():
            logger.info(f"📂 Loading final transcript: {self.final_file}")
            with open(self.final_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return data['segments'], data['metadata']

        # Find most recent checkpoint
        checkpoints = sorted(
            self.output_dir.glob(self.checkpoint_pattern),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        if not checkpoints:
            raise FileNotFoundError("No checkpoint found")

        latest = checkpoints[0]
        logger.info(f"📂 Loading checkpoint: {latest.name}")

        with open(latest, 'r', encoding='utf-8') as f:
            data = json.load(f)

        segments = data.get('segments', [])
        metadata = data.get('metadata', {})

        logger.info(f"✓ Loaded {len(segments)} segments")
        logger.info(f"  Progress: {metadata.get('progress_percentage', 0):.1f}%")
        logger.info(f"  Status: {metadata.get('status', 'unknown')}")

        return segments, metadata

    def save_checkpoint(
        self,
        segments: List[Dict],
        metadata: Dict,
        force: bool = False
    ) -> Optional[Path]:
        """
        Save checkpoint if interval reached

        Args:
            segments: List of segments to save
            metadata: Metadata to include
            force: Force save even if interval not reached

        Returns:
            Path to saved checkpoint, or None if not saved
        """
        segment_count = len(segments)

        # Check if we should save
        if not force and segment_count % self.checkpoint_interval != 0:
            return None

        # Create checkpoint filename
        checkpoint_file = self.output_dir / f"{self.video_name}_checkpoint_{segment_count:04d}.json"

        # Calculate progress
        total_duration = segments[-1]['end'] if segments else 0

        # Build checkpoint data
        checkpoint_data = {
            'video_name': self.video_name,
            'timestamp': datetime.now().isoformat(),
            'metadata': {
                **metadata,
                'total_segments': segment_count,
                'last_segment_time': total_duration,
                'progress_percentage': (segment_count / metadata.get('estimated_total', segment_count)) * 100,
                'status': 'in_progress',
                'checkpoint_file': checkpoint_file.name
            },
            'segments': segments
        }

        # Save checkpoint
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, ensure_ascii=False, indent=2)

        file_size = checkpoint_file.stat().st_size / 1024

        logger.info(f"💾 Checkpoint saved: {checkpoint_file.name}")
        logger.info(f"   Segments: {segment_count}")
        logger.info(f"   Size: {file_size:.1f} KB")
        logger.info(f"   Progress: {checkpoint_data['metadata']['progress_percentage']:.1f}%")

        return checkpoint_file

    def save_final(
        self,
        segments: List[Dict],
        metadata: Dict
    ) -> Path:
        """
        Save final completed transcript

        Args:
            segments: All completed segments
            metadata: Final metadata

        Returns:
            Path to final transcript file
        """
        # Calculate statistics
        duration = segments[-1]['end'] if segments else 0
        word_count = sum(len(seg.get('text', '').split()) for seg in segments)

        # Calculate average confidence
        total_confidence = 0
        confidence_count = 0

        for seg in segments:
            if 'words' in seg and seg['words']:
                for word in seg['words']:
                    if 'probability' in word:
                        total_confidence += word['probability']
                        confidence_count += 1

        avg_confidence = total_confidence / confidence_count if confidence_count > 0 else 0.0

        # Build final transcript
        final_data = {
            'video_name': self.video_name,
            'timestamp': datetime.now().isoformat(),
            'metadata': {
                **metadata,
                'language': 'th',
                'duration': duration,
                'word_count': word_count,
                'segment_count': len(segments),
                'average_confidence': avg_confidence,
                'status': 'completed',
                'model_name': metadata.get('model_name', 'large-v3')
            },
            'text': ' '.join(seg.get('text', '') for seg in segments),
            'segments': segments
        }

        # Save final file
        with open(self.final_file, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)

        file_size = self.final_file.stat().st_size / 1024

        logger.info("=" * 70)
        logger.info("✅ FINAL TRANSCRIPT SAVED")
        logger.info("=" * 70)
        logger.info(f"File: {self.final_file.name}")
        logger.info(f"Size: {file_size:.1f} KB")
        logger.info(f"Segments: {len(segments)}")
        logger.info(f"Duration: {int(duration // 60)}:{int(duration % 60):02d}")
        logger.info(f"Words: {word_count}")
        logger.info(f"Confidence: {avg_confidence:.1%}")
        logger.info("=" * 70)

        # Clean up intermediate checkpoints
        self._cleanup_checkpoints()

        return self.final_file

    def get_resume_point(self) -> Tuple[int, float]:
        """
        Get resume point from checkpoint

        Returns:
            Tuple of (segment_count, last_time)
        """
        try:
            segments, metadata = self.load_checkpoint()
            segment_count = len(segments)
            last_time = segments[-1]['end'] if segments else 0.0

            logger.info(f"📍 Resume point: Segment {segment_count}, Time {last_time:.1f}s")
            return segment_count, last_time

        except FileNotFoundError:
            logger.info(f"📍 Resume point: Start from beginning")
            return 0, 0.0

    def validate_checkpoint(self, checkpoint_file: Path = None) -> bool:
        """
        Validate checkpoint file integrity

        Args:
            checkpoint_file: Path to checkpoint (default: most recent)

        Returns:
            True if valid, False otherwise
        """
        if checkpoint_file is None:
            try:
                segments, metadata = self.load_checkpoint()
                checkpoint_file = self.final_file
            except FileNotFoundError:
                logger.warning("No checkpoint to validate")
                return False

        try:
            with open(checkpoint_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check required fields
            required = ['video_name', 'metadata', 'segments']
            for field in required:
                if field not in data:
                    logger.error(f"Missing required field: {field}")
                    return False

            # Check segments structure
            segments = data['segments']
            if not isinstance(segments, list):
                logger.error("Segments must be a list")
                return False

            # Validate segment structure
            for i, seg in enumerate(segments):
                if not all(k in seg for k in ['id', 'start', 'end', 'text']):
                    logger.error(f"Segment {i} missing required fields")
                    return False

                # Check time ordering
                if i > 0 and seg['start'] < segments[i-1]['end']:
                    logger.error(f"Segment {i} time ordering invalid")
                    return False

            logger.info(f"✓ Checkpoint valid: {checkpoint_file.name}")
            return True

        except Exception as e:
            logger.error(f"Checkpoint validation failed: {e}")
            return False

    def merge_checkpoints(self) -> List[Dict]:
        """
        Merge all checkpoint files into one segment list

        Returns:
            Merged list of segments
        """
        checkpoints = sorted(
            self.output_dir.glob(self.checkpoint_pattern),
            key=lambda p: int(p.stem.split('_')[-1])
        )

        if not checkpoints:
            logger.warning("No checkpoints to merge")
            return []

        logger.info(f"Merging {len(checkpoints)} checkpoint files...")

        all_segments = []
        seen_ids = set()

        for cp_file in checkpoints:
            with open(cp_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for seg in data.get('segments', []):
                seg_id = seg['id']
                if seg_id not in seen_ids:
                    all_segments.append(seg)
                    seen_ids.add(seg_id)

        # Sort by ID
        all_segments.sort(key=lambda s: s['id'])

        logger.info(f"✓ Merged {len(all_segments)} unique segments")
        return all_segments

    def _cleanup_checkpoints(self):
        """Clean up intermediate checkpoint files after final save"""
        checkpoints = list(self.output_dir.glob(self.checkpoint_pattern))

        if checkpoints:
            logger.info(f"🧹 Cleaning up {len(checkpoints)} intermediate checkpoints...")
            for cp_file in checkpoints:
                cp_file.unlink()
            logger.info("✓ Cleanup complete")

    def get_statistics(self) -> Dict:
        """
        Get checkpoint statistics

        Returns:
            Dictionary with checkpoint stats
        """
        stats = {
            'has_final': self.final_file.exists(),
            'checkpoint_count': len(list(self.output_dir.glob(self.checkpoint_pattern))),
            'total_size_kb': 0,
            'latest_checkpoint': None,
            'total_segments': 0,
            'progress_percentage': 0
        }

        # Calculate total size
        all_files = [self.final_file] if self.final_file.exists() else []
        all_files.extend(self.output_dir.glob(self.checkpoint_pattern))

        for f in all_files:
            if f.exists():
                stats['total_size_kb'] += f.stat().st_size / 1024

        # Get latest info
        if self.has_checkpoint():
            try:
                segments, metadata = self.load_checkpoint()
                stats['total_segments'] = len(segments)
                stats['progress_percentage'] = metadata.get('progress_percentage', 0)
                stats['latest_checkpoint'] = metadata.get('checkpoint_file', 'final')
            except:
                pass

        return stats

    def __repr__(self) -> str:
        """String representation"""
        stats = self.get_statistics()
        return (
            f"CheckpointManager(video='{self.video_name}', "
            f"checkpoints={stats['checkpoint_count']}, "
            f"segments={stats['total_segments']}, "
            f"progress={stats['progress_percentage']:.1f}%)"
        )


# ======================== UTILITY FUNCTIONS ========================

def create_checkpoint_manager(
    video_path: str,
    output_dir: str = "/kaggle/working/checkpoints",
    checkpoint_interval: int = 50
) -> CheckpointManager:
    """
    Create checkpoint manager from video path

    Args:
        video_path: Path to video file
        output_dir: Checkpoint output directory
        checkpoint_interval: Save interval

    Returns:
        CheckpointManager instance
    """
    video_name = Path(video_path).stem
    return CheckpointManager(video_name, output_dir, checkpoint_interval)


def demo():
    """Demo checkpoint manager"""
    print("=" * 70)
    print("Checkpoint Manager Demo")
    print("=" * 70)

    # Create manager
    mgr = CheckpointManager(
        video_name="demo_video",
        output_dir="/tmp/test_checkpoints",
        checkpoint_interval=10
    )

    print(f"\n{mgr}")

    # Simulate segments
    segments = []
    for i in range(25):
        seg = {
            'id': i,
            'start': i * 10.0,
            'end': (i + 1) * 10.0,
            'text': f'Segment {i}',
            'words': [
                {'word': f'word{j}', 'probability': 0.95}
                for j in range(5)
            ]
        }
        segments.append(seg)

        # Save checkpoint every 10 segments
        checkpoint = mgr.save_checkpoint(
            segments,
            {'model_name': 'large-v3', 'estimated_total': 100}
        )

        if checkpoint:
            print(f"\n✓ Checkpoint saved at segment {i+1}")

    # Save final
    final = mgr.save_final(segments, {'model_name': 'large-v3'})
    print(f"\n✓ Final transcript: {final}")

    # Statistics
    stats = mgr.get_statistics()
    print(f"\nStatistics:")
    print(f"  Final exists: {stats['has_final']}")
    print(f"  Total segments: {stats['total_segments']}")
    print(f"  Total size: {stats['total_size_kb']:.1f} KB")

    print("\n" + "=" * 70)


if __name__ == '__main__':
    demo()
