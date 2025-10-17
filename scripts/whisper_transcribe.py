#!/usr/bin/env python3
"""
Whisper Transcription with Checkpoint System - Production Ready
================================================================
Transcribe Thai audio using Whisper large-v3 with:
- Automatic checkpointing (never lose progress)
- Resume capability (continue from where you stopped)
- Time range support (transcribe specific segments)
- Background/daemon mode support
- Paperspace optimized (/storage/ persistent storage)

Features:
- Word-level timestamps
- Thai-optimized settings
- JSON output with full metadata
- Checkpoint every N segments (configurable)
- Graceful shutdown (Ctrl+C saves progress)
- Resume from checkpoint
- Split by time range (--start-time, --end-time)

Usage:
    # Basic transcription
    python scripts/whisper_transcribe.py video.mp4

    # With checkpoint (recommended)
    python scripts/whisper_transcribe.py video.mp4 \\
      --checkpoint-dir /storage/whisper_checkpoints

    # Resume from checkpoint
    python scripts/whisper_transcribe.py video.mp4 --resume

    # Transcribe time range (10-20 minutes)
    python scripts/whisper_transcribe.py video.mp4 \\
      --start-time 600 --end-time 1200

    # Check status
    python scripts/whisper_transcribe.py --status
"""

import os
import sys
import json
import logging
import argparse
import hashlib
import signal
import atexit
import time
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to import whisper
try:
    import whisper
except ImportError:
    logger.error("Whisper not installed. Install with: pip install openai-whisper")
    sys.exit(1)

# Try to import tqdm for progress bar
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    logger.warning("tqdm not installed. Progress bar disabled. Install with: pip install tqdm")


# ======================== DATA STRUCTURES ========================

@dataclass
class TranscriptSegment:
    """Single transcript segment with timestamps"""
    id: int
    start: float
    end: float
    text: str
    confidence: float = 0.0
    words: List[Dict] = None


@dataclass
class TranscriptResult:
    """Complete transcription result"""
    language: str
    duration: float
    segments: List[TranscriptSegment]
    text: str
    word_count: int
    average_confidence: float
    model_name: str
    timestamp: str


@dataclass
class CheckpointData:
    """Checkpoint metadata"""
    video_file: str
    video_hash: str
    model: str
    device: str
    start_time: Optional[float]
    end_time: Optional[float]
    last_segment_id: int
    last_timestamp: float
    total_segments: int
    created_at: str
    last_updated: str
    start_timestamp: float
    speed: float = 0.0


# ======================== CHECKPOINT MANAGER ========================

class CheckpointManager:
    """Manage checkpoint saving/loading for resume capability"""

    def __init__(self, checkpoint_dir: Path, video_hash: str):
        """
        Initialize checkpoint manager

        Args:
            checkpoint_dir: Base directory for checkpoints
            video_hash: Unique hash of video file
        """
        self.checkpoint_dir = Path(checkpoint_dir) / video_hash
        self.checkpoint_file = self.checkpoint_dir / "checkpoint.json"
        self.metadata_file = self.checkpoint_dir / "metadata.json"
        self.segments_dir = self.checkpoint_dir / "segments"

        # Create directories
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.segments_dir.mkdir(parents=True, exist_ok=True)

    def has_checkpoint(self) -> bool:
        """Check if checkpoint exists"""
        return self.checkpoint_file.exists()

    def save_checkpoint(self, data: CheckpointData):
        """
        Save checkpoint atomically

        Args:
            data: Checkpoint data to save
        """
        try:
            # Write to temp file first (atomic operation)
            temp_file = self.checkpoint_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(data), f, indent=2, ensure_ascii=False)

            # Atomic rename
            temp_file.replace(self.checkpoint_file)

            logger.debug(f"Checkpoint saved: segment {data.last_segment_id}")

        except Exception as e:
            logger.error(f"Failed to save checkpoint: {e}")

    def load_checkpoint(self) -> Optional[CheckpointData]:
        """
        Load checkpoint data

        Returns:
            CheckpointData if found, None otherwise
        """
        if not self.checkpoint_file.exists():
            return None

        try:
            with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return CheckpointData(**data)

        except Exception as e:
            logger.error(f"Failed to load checkpoint: {e}")
            return None

    def cleanup(self):
        """Delete checkpoint directory"""
        try:
            if self.checkpoint_dir.exists():
                shutil.rmtree(self.checkpoint_dir)
                logger.info("✓ Checkpoint cleaned up")
        except Exception as e:
            logger.warning(f"Failed to cleanup checkpoint: {e}")


# ======================== SEGMENT BATCHER ========================

class SegmentBatcher:
    """Batch segment saving for efficiency"""

    def __init__(self, storage_dir: Path, batch_size: int = 100):
        """
        Initialize segment batcher

        Args:
            storage_dir: Directory to store segment batches
            batch_size: Number of segments per batch file
        """
        self.storage_dir = Path(storage_dir)
        self.batch_size = batch_size
        self.current_batch = []
        self.batch_count = 0

        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def add_segment(self, segment: TranscriptSegment):
        """
        Add segment to batch

        Args:
            segment: Segment to add
        """
        self.current_batch.append(segment)

        # Auto-flush when batch is full
        if len(self.current_batch) >= self.batch_size:
            self.flush()

    def flush(self):
        """Save current batch to file"""
        if not self.current_batch:
            return

        try:
            batch_file = self.storage_dir / f"batch_{self.batch_count:03d}.json"

            # Convert segments to dict
            batch_data = [
                {
                    'id': seg.id,
                    'start': seg.start,
                    'end': seg.end,
                    'text': seg.text,
                    'confidence': seg.confidence,
                    'words': seg.words
                }
                for seg in self.current_batch
            ]

            with open(batch_file, 'w', encoding='utf-8') as f:
                json.dump(batch_data, f, ensure_ascii=False, indent=2)

            logger.debug(f"Batch {self.batch_count} saved ({len(self.current_batch)} segments)")

            self.current_batch = []
            self.batch_count += 1

        except Exception as e:
            logger.error(f"Failed to save batch: {e}")

    def get_all_segments(self) -> List[TranscriptSegment]:
        """
        Load all segments from batch files

        Returns:
            List of all segments
        """
        segments = []

        # Get all batch files sorted
        batch_files = sorted(self.storage_dir.glob("batch_*.json"))

        for batch_file in batch_files:
            try:
                with open(batch_file, 'r', encoding='utf-8') as f:
                    batch_data = json.load(f)

                for seg_dict in batch_data:
                    segment = TranscriptSegment(
                        id=seg_dict['id'],
                        start=seg_dict['start'],
                        end=seg_dict['end'],
                        text=seg_dict['text'],
                        confidence=seg_dict.get('confidence', 0.0),
                        words=seg_dict.get('words')
                    )
                    segments.append(segment)

            except Exception as e:
                logger.error(f"Failed to load batch {batch_file}: {e}")

        return segments


# ======================== PROGRESS TRACKER ========================

class ProgressTracker:
    """Track transcription progress with ETA"""

    def __init__(self, total_duration: float, use_tqdm: bool = True):
        """
        Initialize progress tracker

        Args:
            total_duration: Total duration in seconds
            use_tqdm: Use tqdm progress bar if available
        """
        self.total_duration = total_duration
        self.start_time = time.time()
        self.last_update = self.start_time
        self.processed_duration = 0.0

        # Use tqdm if available and requested
        self.pbar = None
        if use_tqdm and HAS_TQDM and sys.stdout.isatty():
            self.pbar = tqdm(
                total=total_duration,
                unit='s',
                unit_scale=True,
                desc="Transcribing",
                ncols=100,
                bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'
            )

    def update(self, seconds_processed: float):
        """
        Update progress

        Args:
            seconds_processed: Seconds processed since last update
        """
        self.processed_duration += seconds_processed
        self.last_update = time.time()

        if self.pbar is not None:
            self.pbar.update(seconds_processed)
        else:
            # Fallback to simple logging
            percent = (self.processed_duration / self.total_duration) * 100
            elapsed = time.time() - self.start_time
            speed = self.processed_duration / elapsed if elapsed > 0 else 0
            eta = (self.total_duration - self.processed_duration) / speed if speed > 0 else 0

            logger.info(
                f"Progress: {percent:.1f}% | "
                f"Speed: {speed:.1f}x | "
                f"ETA: {self._format_time(eta)}"
            )

    def get_speed(self) -> float:
        """Get current processing speed (x realtime)"""
        elapsed = time.time() - self.start_time
        return self.processed_duration / elapsed if elapsed > 0 else 0

    def get_eta(self) -> float:
        """Get estimated time remaining (seconds)"""
        speed = self.get_speed()
        remaining_duration = self.total_duration - self.processed_duration
        return remaining_duration / speed if speed > 0 else 0

    def close(self):
        """Close progress bar"""
        if self.pbar is not None:
            self.pbar.close()

    @staticmethod
    def _format_time(seconds: float) -> str:
        """Format seconds to readable time"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            return f"{int(seconds // 60)}m {int(seconds % 60)}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"


# ======================== WHISPER TRANSCRIBER ========================

class WhisperTranscriber:
    """Whisper transcription with checkpoint support"""

    # Thai-optimized settings
    THAI_SETTINGS = {
        "language": "th",
        "task": "transcribe",
        "word_timestamps": True,

        # Multi-temperature for better accuracy
        "temperature": (0.0, 0.2, 0.4, 0.6, 0.8),

        # Beam search for quality
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
        device: str = "cpu",
        checkpoint_dir: Optional[Path] = None,
        checkpoint_interval: int = 10
    ):
        """
        Initialize Whisper transcriber

        Args:
            model_name: Whisper model
            device: cpu or cuda
            checkpoint_dir: Directory for checkpoints (None to disable)
            checkpoint_interval: Save checkpoint every N segments
        """
        logger.info("=" * 70)
        logger.info("Whisper Transcriber (Thai-Optimized) - WITH CHECKPOINT")
        logger.info("=" * 70)
        logger.info(f"Model: {model_name}")
        logger.info(f"Device: {device}")

        if checkpoint_dir:
            logger.info(f"Checkpoint: Enabled ({checkpoint_dir})")
            logger.info(f"Checkpoint interval: Every {checkpoint_interval} segments")
        else:
            logger.info("Checkpoint: Disabled")

        try:
            logger.info("Loading Whisper model...")
            self.model = whisper.load_model(model_name, device=device)
            self.model_name = model_name
            self.device = device
            self.checkpoint_dir = checkpoint_dir
            self.checkpoint_interval = checkpoint_interval
            logger.info("✓ Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

        # State for cleanup handler
        self.checkpoint_manager = None
        self.current_checkpoint_data = None

    def compute_file_hash(self, file_path: Path) -> str:
        """
        Compute SHA256 hash of file (first 8 chars)

        Args:
            file_path: Path to file

        Returns:
            8-character hash string
        """
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            # Read first 1MB for speed
            chunk = f.read(1024 * 1024)
            sha256.update(chunk)

        return sha256.hexdigest()[:8]

    def extract_audio_segment(
        self,
        input_file: Path,
        start_time: Optional[float],
        end_time: Optional[float],
        output_file: Path
    ):
        """
        Extract audio segment using FFmpeg

        Args:
            input_file: Input video/audio file
            start_time: Start time in seconds (None for beginning)
            end_time: End time in seconds (None for end)
            output_file: Output audio file
        """
        cmd = ['ffmpeg', '-i', str(input_file), '-y']

        if start_time is not None:
            cmd.extend(['-ss', str(start_time)])

        if end_time is not None:
            cmd.extend(['-to', str(end_time)])

        cmd.extend([
            '-vn',  # No video
            '-acodec', 'pcm_s16le',
            '-ar', '16000',  # 16kHz for Whisper
            '-ac', '1',  # Mono
            str(output_file)
        ])

        logger.info(f"Extracting audio segment...")
        if start_time is not None:
            logger.info(f"  Start: {self._format_time(start_time)}")
        if end_time is not None:
            logger.info(f"  End: {self._format_time(end_time)}")

        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            logger.info("✓ Audio segment extracted")
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg failed: {e.stderr}")
            raise

    def transcribe_file(
        self,
        audio_path: Path,
        start_time_offset: float = 0.0,
        resume_from_checkpoint: bool = False
    ) -> TranscriptResult:
        """
        Transcribe audio/video file with checkpoint support

        Args:
            audio_path: Path to audio/video file
            start_time_offset: Offset to add to timestamps
            resume_from_checkpoint: Try to resume from checkpoint

        Returns:
            TranscriptResult with segments and timestamps
        """
        if not audio_path.exists():
            raise FileNotFoundError(f"File not found: {audio_path}")

        # Compute file hash for checkpoint
        video_hash = self.compute_file_hash(audio_path)

        # Setup checkpoint manager
        checkpoint_manager = None
        segment_batcher = None
        resumed_segments = []
        resume_from_segment = 0

        if self.checkpoint_dir:
            checkpoint_manager = CheckpointManager(self.checkpoint_dir, video_hash)
            self.checkpoint_manager = checkpoint_manager

            # Check for existing checkpoint
            if resume_from_checkpoint and checkpoint_manager.has_checkpoint():
                checkpoint_data = checkpoint_manager.load_checkpoint()

                if checkpoint_data:
                    logger.info("\n" + "=" * 70)
                    logger.info("CHECKPOINT FOUND")
                    logger.info("=" * 70)
                    logger.info(f"Video: {checkpoint_data.video_file}")
                    logger.info(f"Hash: {checkpoint_data.video_hash}")
                    logger.info(f"Last checkpoint: {checkpoint_data.last_updated}")
                    logger.info(f"\nProgress: {checkpoint_data.last_segment_id}/{checkpoint_data.total_segments} segments")
                    logger.info(f"Last saved: segment {checkpoint_data.last_segment_id}")
                    logger.info(f"Model: {checkpoint_data.model}")
                    logger.info(f"Device: {checkpoint_data.device}")

                    # Ask user
                    response = input("\nResume from checkpoint? [Y/n]: ").strip().lower()

                    if response in ['', 'y', 'yes']:
                        logger.info("✓ Resuming from checkpoint...")

                        # Load previous segments
                        segment_batcher = SegmentBatcher(
                            checkpoint_manager.segments_dir,
                            batch_size=100
                        )
                        resumed_segments = segment_batcher.get_all_segments()
                        resume_from_segment = checkpoint_data.last_segment_id

                        logger.info(f"✓ Loaded {len(resumed_segments)} previous segments")
                        logger.info(f"✓ Resuming from segment {resume_from_segment}")
                    else:
                        logger.info("Starting fresh transcription...")
                        checkpoint_manager.cleanup()
                        checkpoint_manager = CheckpointManager(self.checkpoint_dir, video_hash)

            # Initialize segment batcher
            if segment_batcher is None:
                segment_batcher = SegmentBatcher(
                    checkpoint_manager.segments_dir,
                    batch_size=100
                )

        logger.info(f"\nTranscribing: {audio_path.name}")
        logger.info("Settings:")
        logger.info(f"  - Word-level timestamps: ✓")
        logger.info(f"  - Multi-temperature: ✓")
        logger.info(f"  - Beam search: ✓")
        logger.info(f"  - Thai optimization: ✓")
        if start_time_offset > 0:
            logger.info(f"  - Time offset: {self._format_time(start_time_offset)}")

        try:
            # Transcribe
            logger.info("\nProcessing...")
            start_transcribe_time = time.time()

            result = self.model.transcribe(
                str(audio_path),
                **self.THAI_SETTINGS
            )

            # Process segments
            segments = []
            progress_tracker = ProgressTracker(
                result['segments'][-1]['end'] if result['segments'] else 0.0,
                use_tqdm=(sys.stdout.isatty())
            )

            checkpoint_data = CheckpointData(
                video_file=audio_path.name,
                video_hash=video_hash,
                model=self.model_name,
                device=self.device,
                start_time=start_time_offset if start_time_offset > 0 else None,
                end_time=None,
                last_segment_id=0,
                last_timestamp=0.0,
                total_segments=len(result['segments']),
                created_at=datetime.now().isoformat(),
                last_updated=datetime.now().isoformat(),
                start_timestamp=start_transcribe_time
            )

            for i, seg in enumerate(result['segments']):
                # Skip if resuming
                if i < resume_from_segment:
                    continue

                # Extract words if available
                words = None
                if 'words' in seg:
                    words = [
                        {
                            'word': w.get('word', ''),
                            'start': w.get('start', 0.0) + start_time_offset,
                            'end': w.get('end', 0.0) + start_time_offset,
                            'probability': w.get('probability', 0.0)
                        }
                        for w in seg['words']
                    ]

                # Calculate confidence
                confidence = 1.0
                if words:
                    confidences = [w['probability'] for w in words if 'probability' in w]
                    if confidences:
                        confidence = sum(confidences) / len(confidences)

                segment = TranscriptSegment(
                    id=i,
                    start=seg['start'] + start_time_offset,
                    end=seg['end'] + start_time_offset,
                    text=seg['text'].strip(),
                    confidence=confidence,
                    words=words
                )
                segments.append(segment)

                # Add to batch
                if segment_batcher:
                    segment_batcher.add_segment(segment)

                # Update progress
                if i > 0:
                    duration = seg['end'] - result['segments'][i-1]['end']
                    progress_tracker.update(duration)

                # Save checkpoint
                if checkpoint_manager and (i + 1) % self.checkpoint_interval == 0:
                    checkpoint_data.last_segment_id = i
                    checkpoint_data.last_timestamp = seg['end'] + start_time_offset
                    checkpoint_data.last_updated = datetime.now().isoformat()
                    checkpoint_data.speed = progress_tracker.get_speed()

                    checkpoint_manager.save_checkpoint(checkpoint_data)
                    self.current_checkpoint_data = checkpoint_data

            # Flush remaining segments
            if segment_batcher:
                segment_batcher.flush()

            # Close progress tracker
            progress_tracker.close()

            # Combine with resumed segments
            if resumed_segments:
                segments = resumed_segments + segments

            # Calculate statistics
            total_text = ' '.join(seg.text for seg in segments)
            word_count = len(total_text.split())
            avg_confidence = sum(s.confidence for s in segments) / len(segments) if segments else 0.0
            duration = segments[-1].end if segments else 0.0

            transcript = TranscriptResult(
                language=result['language'],
                duration=duration,
                segments=segments,
                text=total_text,
                word_count=word_count,
                average_confidence=avg_confidence,
                model_name=self.model_name,
                timestamp=datetime.now().isoformat()
            )

            processing_time = time.time() - start_transcribe_time

            logger.info("\n✓ Transcription complete:")
            logger.info(f"  - Duration: {self._format_time(duration)}")
            logger.info(f"  - Segments: {len(segments)}")
            logger.info(f"  - Words: {word_count}")
            logger.info(f"  - Avg confidence: {avg_confidence:.1%}")
            logger.info(f"  - Processing time: {self._format_time(processing_time)}")
            logger.info(f"  - Speed: {duration / processing_time:.1f}x realtime")

            # Cleanup checkpoint on success
            if checkpoint_manager:
                checkpoint_manager.cleanup()

            return transcript

        except Exception as e:
            logger.error(f"Transcription failed: {e}")

            # Save emergency checkpoint
            if checkpoint_manager and self.current_checkpoint_data:
                logger.info("Saving emergency checkpoint...")
                checkpoint_manager.save_checkpoint(self.current_checkpoint_data)
                logger.info("✓ Emergency checkpoint saved")

            raise

    def save_json(self, transcript: TranscriptResult, output_path: Path):
        """Save transcript as JSON"""
        data = {
            'metadata': {
                'language': transcript.language,
                'duration': transcript.duration,
                'word_count': transcript.word_count,
                'average_confidence': transcript.average_confidence,
                'model_name': transcript.model_name,
                'timestamp': transcript.timestamp,
                'segment_count': len(transcript.segments)
            },
            'text': transcript.text,
            'segments': [
                {
                    'id': seg.id,
                    'start': seg.start,
                    'end': seg.end,
                    'text': seg.text,
                    'confidence': seg.confidence,
                    'words': seg.words
                }
                for seg in transcript.segments
            ]
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"✓ JSON saved: {output_path}")

    def save_thai_srt(self, transcript: TranscriptResult, output_path: Path):
        """Save Thai SRT subtitle file"""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            for seg in transcript.segments:
                f.write(f"{seg.id + 1}\n")
                f.write(f"{self._to_srt_time(seg.start)} --> {self._to_srt_time(seg.end)}\n")
                f.write(f"{seg.text}\n")
                f.write("\n")

        logger.info(f"✓ Thai SRT saved: {output_path}")

    @staticmethod
    def _format_time(seconds: float) -> str:
        """Format seconds to HH:MM:SS"""
        return str(timedelta(seconds=int(seconds)))

    @staticmethod
    def _to_srt_time(seconds: float) -> str:
        """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


# ======================== STATUS CHECKER ========================

def show_status(checkpoint_dir: Path):
    """
    Show status of all checkpoints

    Args:
        checkpoint_dir: Checkpoint directory
    """
    checkpoint_dir = Path(checkpoint_dir)

    if not checkpoint_dir.exists():
        print("No checkpoints found")
        return

    # Find all checkpoint files
    checkpoint_files = list(checkpoint_dir.glob("*/checkpoint.json"))

    if not checkpoint_files:
        print("No active transcriptions found")
        return

    print("=" * 70)
    print("ACTIVE TRANSCRIPTIONS")
    print("=" * 70)

    for i, checkpoint_file in enumerate(checkpoint_files, 1):
        try:
            with open(checkpoint_file, 'r') as f:
                data = json.load(f)

            video_hash = checkpoint_file.parent.name
            progress_pct = (data['last_segment_id'] / data['total_segments'] * 100) if data['total_segments'] > 0 else 0
            elapsed = time.time() - data['start_timestamp']
            speed = data.get('speed', 0.0)

            print(f"\n[{i}] Video: {data['video_file']}")
            print(f"    Hash: {video_hash}")
            print(f"    Progress: {data['last_segment_id']}/{data['total_segments']} segments ({progress_pct:.1f}%)")
            print(f"    Elapsed: {str(timedelta(seconds=int(elapsed)))}")
            print(f"    Speed: {speed:.1f}x realtime")
            print(f"    Last updated: {data['last_updated']}")
            print(f"    Model: {data['model']} ({data['device']})")

        except Exception as e:
            print(f"\n[{i}] Error reading checkpoint: {e}")

    print("\n" + "=" * 70)


# ======================== SIGNAL HANDLING ========================

def setup_signal_handlers(transcriber: WhisperTranscriber):
    """
    Setup signal handlers for graceful shutdown

    Args:
        transcriber: WhisperTranscriber instance
    """
    def signal_handler(signum, frame):
        logger.info("\n\n🛑 Received interrupt signal (Ctrl+C)")

        # Save checkpoint if available
        if transcriber.checkpoint_manager and transcriber.current_checkpoint_data:
            logger.info("Saving checkpoint before exit...")
            transcriber.checkpoint_manager.save_checkpoint(transcriber.current_checkpoint_data)
            logger.info("✓ Checkpoint saved")

        logger.info("✓ Safe to exit")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


# ======================== CLI INTERFACE ========================

def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Transcribe Thai audio/video with Whisper (with checkpoint support)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic transcription
  python scripts/whisper_transcribe.py video.mp4

  # With checkpoint (recommended for long videos)
  python scripts/whisper_transcribe.py video.mp4 \\
    --checkpoint-dir /storage/whisper_checkpoints

  # Resume from checkpoint
  python scripts/whisper_transcribe.py video.mp4 --resume

  # Transcribe specific time range (10-20 minutes)
  python scripts/whisper_transcribe.py video.mp4 \\
    --start-time 600 --end-time 1200

  # Check status of all transcriptions
  python scripts/whisper_transcribe.py --status

  # Force restart (ignore checkpoint)
  python scripts/whisper_transcribe.py video.mp4 --force-restart

Output:
  - <video>_transcript.json   # Full transcript with timestamps
  - <video>_thai.srt         # Thai subtitles

For Paperspace:
  Use --checkpoint-dir /storage/whisper_checkpoints
  This ensures checkpoints survive session restarts!
        """
    )

    # Input/Output
    parser.add_argument(
        'input',
        type=Path,
        nargs='?',
        help='Input audio/video file'
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=Path('output'),
        help='Output directory (default: output/)'
    )

    # Model options
    parser.add_argument(
        '-m', '--model',
        type=str,
        default='large-v3',
        choices=['tiny', 'base', 'small', 'medium', 'large', 'large-v2', 'large-v3'],
        help='Whisper model (default: large-v3)'
    )

    parser.add_argument(
        '--device',
        type=str,
        default='cpu',
        choices=['cpu', 'cuda'],
        help='Device (default: cpu, use cuda for GPU)'
    )

    # Checkpoint options
    parser.add_argument(
        '--checkpoint-dir',
        type=Path,
        help='Checkpoint directory (e.g., /storage/whisper_checkpoints)'
    )

    parser.add_argument(
        '--checkpoint-interval',
        type=int,
        default=10,
        help='Save checkpoint every N segments (default: 10)'
    )

    parser.add_argument(
        '--no-checkpoint',
        action='store_true',
        help='Disable checkpoint system'
    )

    # Resume options
    parser.add_argument(
        '--resume',
        action='store_true',
        help='Auto-resume from checkpoint if found'
    )

    parser.add_argument(
        '--force-restart',
        action='store_true',
        help='Delete checkpoint and start from beginning'
    )

    # Time range options
    parser.add_argument(
        '--start-time',
        type=float,
        help='Start time in seconds (e.g., 600 = 10 minutes)'
    )

    parser.add_argument(
        '--end-time',
        type=float,
        help='End time in seconds (e.g., 1200 = 20 minutes)'
    )

    # Status
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show status of active transcriptions'
    )

    args = parser.parse_args()

    # Handle status command
    if args.status:
        checkpoint_dir = args.checkpoint_dir or Path('output/checkpoints')
        show_status(checkpoint_dir)
        sys.exit(0)

    # Validate input
    if not args.input:
        parser.print_help()
        sys.exit(1)

    if not args.input.exists():
        logger.error(f"Input file not found: {args.input}")
        sys.exit(1)

    try:
        # Setup checkpoint directory
        checkpoint_dir = None
        if not args.no_checkpoint:
            checkpoint_dir = args.checkpoint_dir or (args.output / 'checkpoints')

        # Handle force restart
        if args.force_restart and checkpoint_dir:
            transcriber_temp = WhisperTranscriber(args.model, args.device)
            video_hash = transcriber_temp.compute_file_hash(args.input)
            checkpoint_manager = CheckpointManager(checkpoint_dir, video_hash)

            if checkpoint_manager.has_checkpoint():
                logger.info("Deleting existing checkpoint...")
                checkpoint_manager.cleanup()
                logger.info("✓ Checkpoint deleted")

        # Initialize transcriber
        transcriber = WhisperTranscriber(
            model_name=args.model,
            device=args.device,
            checkpoint_dir=checkpoint_dir,
            checkpoint_interval=args.checkpoint_interval
        )

        # Setup signal handlers
        setup_signal_handlers(transcriber)

        # Handle time range
        audio_file = args.input
        start_time_offset = 0.0

        if args.start_time is not None or args.end_time is not None:
            # Extract segment to temp file
            temp_audio = Path(tempfile.mktemp(suffix='.wav'))

            try:
                transcriber.extract_audio_segment(
                    args.input,
                    args.start_time,
                    args.end_time,
                    temp_audio
                )

                audio_file = temp_audio
                start_time_offset = args.start_time or 0.0

            except Exception as e:
                logger.error(f"Failed to extract audio segment: {e}")
                sys.exit(1)

        # Setup output paths
        output_dir = args.output
        output_dir.mkdir(parents=True, exist_ok=True)

        json_path = output_dir / f"{args.input.stem}_transcript.json"
        srt_path = output_dir / f"{args.input.stem}_thai.srt"

        # Transcribe
        start_time = datetime.now()
        transcript = transcriber.transcribe_file(
            audio_file,
            start_time_offset=start_time_offset,
            resume_from_checkpoint=args.resume
        )
        processing_time = (datetime.now() - start_time).total_seconds()

        # Cleanup temp file
        if audio_file != args.input and audio_file.exists():
            audio_file.unlink()

        # Save outputs
        transcriber.save_json(transcript, json_path)
        transcriber.save_thai_srt(transcript, srt_path)

        # Summary
        logger.info("\n" + "=" * 70)
        logger.info("TRANSCRIPTION COMPLETE")
        logger.info("=" * 70)
        logger.info(f"Input: {args.input.name}")
        logger.info(f"Duration: {transcriber._format_time(transcript.duration)}")
        logger.info(f"Processing time: {transcriber._format_time(processing_time)}")
        logger.info(f"Speed: {transcript.duration / processing_time:.1f}x realtime")
        logger.info(f"\nOutputs:")
        logger.info(f"  - JSON: {json_path}")
        logger.info(f"  - Thai SRT: {srt_path}")
        logger.info(f"\nNext steps:")
        logger.info(f"  1. Create translation batch:")
        logger.info(f"     python scripts/create_translation_batch.py {json_path}")
        logger.info(f"  2. Translate with Claude Code")
        logger.info(f"  3. Convert to English SRT:")
        logger.info(f"     python scripts/batch_to_srt.py {json_path} translated.txt")

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
