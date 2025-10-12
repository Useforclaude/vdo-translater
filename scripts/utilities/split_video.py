#!/usr/bin/env python3
"""
Video Splitter - Auto-split long videos into chunks
===================================================
Automatically splits long video files into manageable chunks for processing.

Features:
- Auto-detect video duration
- Split into configurable chunk sizes (default: 1 hour)
- Preserve audio/video quality
- Generate manifest JSON for batch processing
- Smart chunking at scene boundaries (optional)

Usage:
    python scripts/split_video.py video.mp4
    python scripts/split_video.py video.mp4 --max-duration 3600
    python scripts/split_video.py video.mp4 --output chunks/ --manifest
"""

import os
import sys
import json
import logging
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import timedelta

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ======================== DATA STRUCTURES ========================

@dataclass
class VideoInfo:
    """Video file information"""
    path: Path
    duration: float  # seconds
    width: int
    height: int
    fps: float
    codec: str
    bitrate: int
    audio_codec: str
    audio_bitrate: int
    size_mb: float


@dataclass
class ChunkInfo:
    """Video chunk information"""
    index: int
    start_time: float
    end_time: float
    duration: float
    output_path: Path


@dataclass
class SplitManifest:
    """Splitting manifest for batch processing"""
    source_video: Path
    total_duration: float
    chunk_duration: float
    chunks: List[ChunkInfo]
    timestamp: str


# ======================== VIDEO ANALYZER ========================

class VideoAnalyzer:
    """Analyze video files using FFmpeg"""

    @staticmethod
    def get_video_info(video_path: Path) -> VideoInfo:
        """
        Get video file information using ffprobe

        Args:
            video_path: Path to video file

        Returns:
            VideoInfo object with video metadata
        """
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        try:
            # Run ffprobe to get video info
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                str(video_path)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)

            # Extract video stream info
            video_stream = next(
                (s for s in data['streams'] if s['codec_type'] == 'video'),
                None
            )

            # Extract audio stream info
            audio_stream = next(
                (s for s in data['streams'] if s['codec_type'] == 'audio'),
                None
            )

            if not video_stream:
                raise ValueError("No video stream found")

            # Parse FPS
            fps_str = video_stream.get('r_frame_rate', '0/1')
            fps_parts = fps_str.split('/')
            fps = float(fps_parts[0]) / float(fps_parts[1]) if len(fps_parts) == 2 else 0.0

            # Get file size
            size_mb = video_path.stat().st_size / (1024 * 1024)

            return VideoInfo(
                path=video_path,
                duration=float(data['format'].get('duration', 0)),
                width=int(video_stream.get('width', 0)),
                height=int(video_stream.get('height', 0)),
                fps=fps,
                codec=video_stream.get('codec_name', 'unknown'),
                bitrate=int(data['format'].get('bit_rate', 0)),
                audio_codec=audio_stream.get('codec_name', 'unknown') if audio_stream else 'none',
                audio_bitrate=int(audio_stream.get('bit_rate', 0)) if audio_stream else 0,
                size_mb=size_mb
            )

        except subprocess.CalledProcessError as e:
            logger.error(f"FFprobe failed: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse ffprobe output: {e}")
            raise


# ======================== VIDEO SPLITTER ========================

class VideoSplitter:
    """Split long videos into chunks"""

    def __init__(self, max_chunk_duration: int = 3600):
        """
        Initialize video splitter

        Args:
            max_chunk_duration: Maximum chunk duration in seconds (default: 3600 = 1 hour)
        """
        self.max_chunk_duration = max_chunk_duration
        self.analyzer = VideoAnalyzer()

    def calculate_chunks(
        self,
        video_info: VideoInfo,
        overlap: int = 0
    ) -> List[ChunkInfo]:
        """
        Calculate chunk boundaries

        Args:
            video_info: Video information
            overlap: Overlap between chunks in seconds (for continuity)

        Returns:
            List of ChunkInfo objects
        """
        chunks = []
        total_duration = video_info.duration
        current_time = 0.0
        chunk_index = 0

        while current_time < total_duration:
            start_time = max(0, current_time - overlap) if chunk_index > 0 else 0
            end_time = min(current_time + self.max_chunk_duration, total_duration)
            duration = end_time - start_time

            # Generate output filename
            output_name = f"{video_info.path.stem}_chunk_{chunk_index:03d}{video_info.path.suffix}"

            chunks.append(ChunkInfo(
                index=chunk_index,
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                output_path=Path(output_name)
            ))

            current_time += self.max_chunk_duration
            chunk_index += 1

        return chunks

    def split_video(
        self,
        video_path: Path,
        output_dir: Path,
        chunks: List[ChunkInfo],
        copy_streams: bool = True
    ) -> List[Path]:
        """
        Split video file into chunks

        Args:
            video_path: Input video path
            output_dir: Output directory
            chunks: List of chunk information
            copy_streams: If True, copy streams without re-encoding (faster)

        Returns:
            List of output file paths
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        output_paths = []

        logger.info(f"Splitting {video_path.name} into {len(chunks)} chunks...")

        for chunk in chunks:
            output_path = output_dir / chunk.output_path

            # Build ffmpeg command
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-ss', str(chunk.start_time),
                '-t', str(chunk.duration),
                '-y'  # Overwrite output files
            ]

            if copy_streams:
                # Fast copy without re-encoding
                cmd.extend(['-c', 'copy'])
            else:
                # Re-encode (slower but more precise)
                cmd.extend(['-c:v', 'libx264', '-c:a', 'aac'])

            cmd.append(str(output_path))

            try:
                logger.info(f"  Creating chunk {chunk.index + 1}/{len(chunks)}: {chunk.output_path.name}")
                logger.info(f"    Time: {self._format_time(chunk.start_time)} → {self._format_time(chunk.end_time)}")

                subprocess.run(
                    cmd,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )

                output_paths.append(output_path)
                logger.info(f"    ✓ Created: {output_path}")

            except subprocess.CalledProcessError as e:
                logger.error(f"    ✗ Failed to create chunk {chunk.index}: {e}")
                raise

        return output_paths

    @staticmethod
    def _format_time(seconds: float) -> str:
        """Format seconds to HH:MM:SS"""
        return str(timedelta(seconds=int(seconds)))

    def create_manifest(
        self,
        video_info: VideoInfo,
        chunks: List[ChunkInfo],
        output_dir: Path
    ) -> Path:
        """
        Create JSON manifest for batch processing

        Args:
            video_info: Original video information
            chunks: List of chunks
            output_dir: Output directory

        Returns:
            Path to manifest file
        """
        from datetime import datetime

        # Update chunk paths to include output directory
        chunks_with_paths = []
        for chunk in chunks:
            chunk_copy = ChunkInfo(
                index=chunk.index,
                start_time=chunk.start_time,
                end_time=chunk.end_time,
                duration=chunk.duration,
                output_path=output_dir / chunk.output_path
            )
            chunks_with_paths.append(chunk_copy)

        manifest = SplitManifest(
            source_video=video_info.path,
            total_duration=video_info.duration,
            chunk_duration=self.max_chunk_duration,
            chunks=chunks_with_paths,
            timestamp=datetime.now().isoformat()
        )

        manifest_path = output_dir / f"{video_info.path.stem}_manifest.json"

        # Convert to dict for JSON serialization
        manifest_dict = {
            'source_video': str(manifest.source_video),
            'total_duration': manifest.total_duration,
            'chunk_duration': manifest.chunk_duration,
            'chunks': [
                {
                    'index': c.index,
                    'start_time': c.start_time,
                    'end_time': c.end_time,
                    'duration': c.duration,
                    'output_path': str(c.output_path)
                }
                for c in manifest.chunks
            ],
            'timestamp': manifest.timestamp
        }

        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest_dict, f, indent=2, ensure_ascii=False)

        logger.info(f"✓ Manifest created: {manifest_path}")
        return manifest_path


# ======================== CLI INTERFACE ========================

def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Split long videos into manageable chunks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Split video into 1-hour chunks
  python scripts/split_video.py video.mp4

  # Split into 30-minute chunks
  python scripts/split_video.py video.mp4 --max-duration 1800

  # Specify output directory and create manifest
  python scripts/split_video.py video.mp4 -o chunks/ --manifest

  # Re-encode chunks (slower but more precise)
  python scripts/split_video.py video.mp4 --no-copy
        """
    )

    parser.add_argument(
        'video',
        type=Path,
        help='Input video file'
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=None,
        help='Output directory (default: <video_name>_chunks/)'
    )

    parser.add_argument(
        '--max-duration',
        type=int,
        default=3600,
        help='Maximum chunk duration in seconds (default: 3600 = 1 hour)'
    )

    parser.add_argument(
        '--overlap',
        type=int,
        default=0,
        help='Overlap between chunks in seconds (default: 0)'
    )

    parser.add_argument(
        '--manifest',
        action='store_true',
        help='Create JSON manifest for batch processing'
    )

    parser.add_argument(
        '--no-copy',
        action='store_true',
        help='Re-encode chunks instead of stream copy (slower but precise)'
    )

    parser.add_argument(
        '--info-only',
        action='store_true',
        help='Show video info and exit without splitting'
    )

    args = parser.parse_args()

    try:
        # Validate video file
        video_path = args.video
        if not video_path.exists():
            logger.error(f"Video file not found: {video_path}")
            sys.exit(1)

        # Setup output directory
        if args.output:
            output_dir = args.output
        else:
            output_dir = Path(f"{video_path.stem}_chunks")

        # Initialize components
        analyzer = VideoAnalyzer()
        splitter = VideoSplitter(max_chunk_duration=args.max_duration)

        # Get video info
        logger.info("=" * 60)
        logger.info("Video Splitter")
        logger.info("=" * 60)
        logger.info(f"\nAnalyzing: {video_path.name}")

        video_info = analyzer.get_video_info(video_path)

        logger.info(f"\nVideo Information:")
        logger.info(f"  Duration: {splitter._format_time(video_info.duration)}")
        logger.info(f"  Resolution: {video_info.width}x{video_info.height}")
        logger.info(f"  FPS: {video_info.fps:.2f}")
        logger.info(f"  Video codec: {video_info.codec}")
        logger.info(f"  Audio codec: {video_info.audio_codec}")
        logger.info(f"  Bitrate: {video_info.bitrate / 1000:.0f} kbps")
        logger.info(f"  File size: {video_info.size_mb:.2f} MB")

        # Exit if info-only mode
        if args.info_only:
            sys.exit(0)

        # Calculate chunks
        chunks = splitter.calculate_chunks(video_info, overlap=args.overlap)

        logger.info(f"\nChunk Plan:")
        logger.info(f"  Total chunks: {len(chunks)}")
        logger.info(f"  Max duration: {args.max_duration}s ({args.max_duration / 60:.1f} min)")
        logger.info(f"  Overlap: {args.overlap}s")

        for chunk in chunks:
            logger.info(f"  Chunk {chunk.index + 1}: {splitter._format_time(chunk.start_time)} → {splitter._format_time(chunk.end_time)}")

        # Confirm before proceeding
        logger.info(f"\nOutput directory: {output_dir}")

        # Split video
        output_paths = splitter.split_video(
            video_path=video_path,
            output_dir=output_dir,
            chunks=chunks,
            copy_streams=not args.no_copy
        )

        # Create manifest if requested
        if args.manifest:
            manifest_path = splitter.create_manifest(
                video_info=video_info,
                chunks=chunks,
                output_dir=output_dir
            )

        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("SPLIT COMPLETE")
        logger.info("=" * 60)
        logger.info(f"✓ Created {len(output_paths)} chunks")
        logger.info(f"✓ Output directory: {output_dir}")
        if args.manifest:
            logger.info(f"✓ Manifest: {manifest_path}")

        logger.info(f"\nNext steps:")
        logger.info(f"  # Process chunks with batch processor:")
        if args.manifest:
            logger.info(f"  python scripts/batch_process.py {manifest_path}")
        else:
            logger.info(f"  python scripts/batch_process.py {output_dir}")

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
