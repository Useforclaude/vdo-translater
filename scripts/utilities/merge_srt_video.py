#!/usr/bin/env python3
"""
SRT-Video Merger - Burn subtitles into video files
==================================================
Burns SRT subtitle files directly into video files (hardcoded subtitles).

Features:
- Hard-code SRT subtitles into video using FFmpeg
- Support for Thai fonts (Sarabun, Noto Sans Thai)
- Customizable subtitle styling (font, size, color, position)
- Batch processing support
- Preserve video quality or optimize

Usage:
    python scripts/merge_srt_video.py video.mp4 subtitles.srt
    python scripts/merge_srt_video.py video.mp4 subtitles.srt -o output.mp4
    python scripts/merge_srt_video.py video.mp4 --thai thai.srt --english en.srt
"""

import os
import sys
import logging
import argparse
import subprocess
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ======================== DATA STRUCTURES ========================

@dataclass
class SubtitleStyle:
    """Subtitle styling configuration"""
    font_name: str = "Sarabun"
    font_size: int = 24
    primary_color: str = "&H00FFFFFF"  # White
    outline_color: str = "&H00000000"  # Black
    back_color: str = "&H80000000"  # Semi-transparent black
    outline_width: int = 2
    shadow_offset: int = 1
    alignment: int = 2  # Bottom center (1=left, 2=center, 3=right)
    margin_v: int = 30  # Vertical margin from bottom
    margin_h: int = 20  # Horizontal margin
    bold: bool = False
    italic: bool = False


@dataclass
class MergeConfig:
    """Video-subtitle merge configuration"""
    video_path: Path
    subtitle_path: Path
    output_path: Path
    style: SubtitleStyle
    video_codec: str = "libx264"
    audio_codec: str = "aac"
    preset: str = "medium"
    crf: int = 23  # Quality (lower = better, 18-28 recommended)
    copy_streams: bool = False  # If True, copy streams (faster but may have issues)


# ======================== SUBTITLE MERGER ========================

class SubtitleMerger:
    """Merge SRT subtitles with video using FFmpeg"""

    DEFAULT_THAI_STYLE = SubtitleStyle(
        font_name="Sarabun",
        font_size=28,
        outline_width=3,
        margin_v=40,
        bold=True
    )

    DEFAULT_ENGLISH_STYLE = SubtitleStyle(
        font_name="Arial",
        font_size=24,
        outline_width=2,
        margin_v=30
    )

    @staticmethod
    def create_ass_style(style: SubtitleStyle) -> str:
        """
        Create ASS subtitle style string

        Args:
            style: SubtitleStyle configuration

        Returns:
            ASS style format string
        """
        bold = "-1" if style.bold else "0"
        italic = "-1" if style.italic else "0"

        return (
            f"FontName={style.font_name},"
            f"FontSize={style.font_size},"
            f"PrimaryColour={style.primary_color},"
            f"OutlineColour={style.outline_color},"
            f"BackColour={style.back_color},"
            f"Outline={style.outline_width},"
            f"Shadow={style.shadow_offset},"
            f"Alignment={style.alignment},"
            f"MarginV={style.margin_v},"
            f"MarginL={style.margin_h},"
            f"MarginR={style.margin_h},"
            f"Bold={bold},"
            f"Italic={italic}"
        )

    def merge_single_subtitle(
        self,
        video_path: Path,
        subtitle_path: Path,
        output_path: Path,
        style: Optional[SubtitleStyle] = None,
        **kwargs
    ) -> Path:
        """
        Merge single SRT file into video

        Args:
            video_path: Input video file
            subtitle_path: SRT subtitle file
            output_path: Output video file
            style: Subtitle styling (None = use default)
            **kwargs: Additional FFmpeg parameters

        Returns:
            Path to output video
        """
        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")
        if not subtitle_path.exists():
            raise FileNotFoundError(f"Subtitle not found: {subtitle_path}")

        # Use default style if not provided
        if style is None:
            # Auto-detect Thai or English
            if self._is_thai_subtitle(subtitle_path):
                style = self.DEFAULT_THAI_STYLE
            else:
                style = self.DEFAULT_ENGLISH_STYLE

        # Create ASS style
        ass_style = self.create_ass_style(style)

        # Build FFmpeg command
        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-vf', f"subtitles={subtitle_path}:force_style='{ass_style}'",
            '-c:v', kwargs.get('video_codec', 'libx264'),
            '-preset', kwargs.get('preset', 'medium'),
            '-crf', str(kwargs.get('crf', 23)),
            '-c:a', kwargs.get('audio_codec', 'copy'),
            '-y',  # Overwrite output
            str(output_path)
        ]

        try:
            logger.info(f"Merging subtitles...")
            logger.info(f"  Video: {video_path.name}")
            logger.info(f"  Subtitle: {subtitle_path.name}")
            logger.info(f"  Output: {output_path.name}")
            logger.info(f"  Style: {style.font_name} {style.font_size}px")

            # Run FFmpeg
            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            logger.info(f"✓ Successfully created: {output_path}")
            return output_path

        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg failed: {e}")
            logger.error(f"Error output: {e.stderr}")
            raise

    def merge_dual_subtitles(
        self,
        video_path: Path,
        top_subtitle_path: Path,
        bottom_subtitle_path: Path,
        output_path: Path,
        top_style: Optional[SubtitleStyle] = None,
        bottom_style: Optional[SubtitleStyle] = None,
        **kwargs
    ) -> Path:
        """
        Merge two SRT files (e.g., Thai + English) into video

        Args:
            video_path: Input video file
            top_subtitle_path: Top subtitle file (usually original language)
            bottom_subtitle_path: Bottom subtitle file (usually translation)
            output_path: Output video file
            top_style: Top subtitle style
            bottom_style: Bottom subtitle style
            **kwargs: Additional FFmpeg parameters

        Returns:
            Path to output video
        """
        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")
        if not top_subtitle_path.exists():
            raise FileNotFoundError(f"Top subtitle not found: {top_subtitle_path}")
        if not bottom_subtitle_path.exists():
            raise FileNotFoundError(f"Bottom subtitle not found: {bottom_subtitle_path}")

        # Auto-detect styles
        if top_style is None:
            top_style = self.DEFAULT_THAI_STYLE if self._is_thai_subtitle(top_subtitle_path) else self.DEFAULT_ENGLISH_STYLE

        if bottom_style is None:
            bottom_style = self.DEFAULT_ENGLISH_STYLE

        # Adjust positions for dual subtitles
        top_style.margin_v = 80  # Higher position
        bottom_style.margin_v = 30  # Lower position

        # Create ASS styles
        top_ass_style = self.create_ass_style(top_style)
        bottom_ass_style = self.create_ass_style(bottom_style)

        # Build complex filter for dual subtitles
        filter_complex = (
            f"subtitles={top_subtitle_path}:force_style='{top_ass_style}',"
            f"subtitles={bottom_subtitle_path}:force_style='{bottom_ass_style}'"
        )

        cmd = [
            'ffmpeg',
            '-i', str(video_path),
            '-vf', filter_complex,
            '-c:v', kwargs.get('video_codec', 'libx264'),
            '-preset', kwargs.get('preset', 'medium'),
            '-crf', str(kwargs.get('crf', 23)),
            '-c:a', kwargs.get('audio_codec', 'copy'),
            '-y',
            str(output_path)
        ]

        try:
            logger.info(f"Merging dual subtitles...")
            logger.info(f"  Video: {video_path.name}")
            logger.info(f"  Top subtitle: {top_subtitle_path.name}")
            logger.info(f"  Bottom subtitle: {bottom_subtitle_path.name}")
            logger.info(f"  Output: {output_path.name}")

            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            logger.info(f"✓ Successfully created: {output_path}")
            return output_path

        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg failed: {e}")
            logger.error(f"Error output: {e.stderr}")
            raise

    def batch_merge(
        self,
        video_subtitle_pairs: List[tuple],
        output_dir: Path,
        **kwargs
    ) -> List[Path]:
        """
        Batch merge multiple video-subtitle pairs

        Args:
            video_subtitle_pairs: List of (video_path, subtitle_path) tuples
            output_dir: Output directory
            **kwargs: Additional FFmpeg parameters

        Returns:
            List of output video paths
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        output_paths = []

        logger.info(f"Batch merging {len(video_subtitle_pairs)} videos...")

        for i, (video_path, subtitle_path) in enumerate(video_subtitle_pairs, 1):
            video_path = Path(video_path)
            subtitle_path = Path(subtitle_path)

            output_name = f"{video_path.stem}_subtitled{video_path.suffix}"
            output_path = output_dir / output_name

            logger.info(f"\n[{i}/{len(video_subtitle_pairs)}]")

            try:
                self.merge_single_subtitle(
                    video_path=video_path,
                    subtitle_path=subtitle_path,
                    output_path=output_path,
                    **kwargs
                )
                output_paths.append(output_path)

            except Exception as e:
                logger.error(f"Failed to merge {video_path.name}: {e}")
                continue

        return output_paths

    @staticmethod
    def _is_thai_subtitle(subtitle_path: Path) -> bool:
        """
        Detect if subtitle file contains Thai text

        Args:
            subtitle_path: Path to SRT file

        Returns:
            True if Thai characters detected
        """
        try:
            with open(subtitle_path, 'r', encoding='utf-8') as f:
                content = f.read(1000)  # Check first 1000 chars
                # Thai Unicode range: 0E00-0E7F
                return any('\u0e00' <= char <= '\u0e7f' for char in content)
        except Exception:
            return False


# ======================== CLI INTERFACE ========================

def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Burn SRT subtitles into video files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Merge single subtitle
  python scripts/merge_srt_video.py video.mp4 subtitle.srt

  # Specify output file
  python scripts/merge_srt_video.py video.mp4 subtitle.srt -o output.mp4

  # Merge dual subtitles (Thai + English)
  python scripts/merge_srt_video.py video.mp4 --thai thai.srt --english en.srt

  # Custom font size
  python scripts/merge_srt_video.py video.mp4 subtitle.srt --font-size 32

  # High quality output
  python scripts/merge_srt_video.py video.mp4 subtitle.srt --crf 18 --preset slow

  # Batch mode (auto-match video-srt pairs)
  python scripts/merge_srt_video.py --batch input_dir/
        """
    )

    parser.add_argument(
        'video',
        type=Path,
        nargs='?',
        help='Input video file'
    )

    parser.add_argument(
        'subtitle',
        type=Path,
        nargs='?',
        help='SRT subtitle file'
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output video file (default: <video>_subtitled.mp4)'
    )

    parser.add_argument(
        '--thai',
        type=Path,
        help='Thai subtitle file (for dual subtitle mode)'
    )

    parser.add_argument(
        '--english',
        type=Path,
        help='English subtitle file (for dual subtitle mode)'
    )

    parser.add_argument(
        '--font',
        type=str,
        default=None,
        help='Font name (default: Sarabun for Thai, Arial for English)'
    )

    parser.add_argument(
        '--font-size',
        type=int,
        default=None,
        help='Font size in pixels (default: 28 for Thai, 24 for English)'
    )

    parser.add_argument(
        '--margin',
        type=int,
        default=None,
        help='Vertical margin from bottom in pixels (default: 30)'
    )

    parser.add_argument(
        '--crf',
        type=int,
        default=23,
        help='Video quality (18-28, lower=better, default: 23)'
    )

    parser.add_argument(
        '--preset',
        type=str,
        default='medium',
        choices=['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'],
        help='Encoding preset (default: medium)'
    )

    parser.add_argument(
        '--batch',
        type=Path,
        help='Batch mode: directory with video-srt pairs'
    )

    args = parser.parse_args()

    try:
        merger = SubtitleMerger()

        # ==================== BATCH MODE ====================
        if args.batch:
            batch_dir = args.batch
            if not batch_dir.exists() or not batch_dir.is_dir():
                logger.error(f"Batch directory not found: {batch_dir}")
                sys.exit(1)

            # Find video-srt pairs
            video_exts = {'.mp4', '.avi', '.mkv', '.mov', '.webm'}
            videos = [f for f in batch_dir.glob('*') if f.suffix.lower() in video_exts]

            pairs = []
            for video in videos:
                srt = batch_dir / f"{video.stem}.srt"
                if srt.exists():
                    pairs.append((video, srt))

            if not pairs:
                logger.error(f"No video-srt pairs found in {batch_dir}")
                sys.exit(1)

            output_dir = batch_dir / "subtitled"
            output_paths = merger.batch_merge(
                video_subtitle_pairs=pairs,
                output_dir=output_dir,
                crf=args.crf,
                preset=args.preset
            )

            logger.info(f"\n✓ Batch complete: {len(output_paths)} videos created")
            sys.exit(0)

        # ==================== DUAL SUBTITLE MODE ====================
        if args.thai and args.english:
            if not args.video:
                logger.error("Video file required for dual subtitle mode")
                sys.exit(1)

            video_path = args.video
            output_path = args.output or video_path.parent / f"{video_path.stem}_dual_sub{video_path.suffix}"

            # Custom styles if specified
            thai_style = SubtitleMerger.DEFAULT_THAI_STYLE
            english_style = SubtitleMerger.DEFAULT_ENGLISH_STYLE

            if args.font:
                thai_style.font_name = args.font
                english_style.font_name = args.font

            if args.font_size:
                thai_style.font_size = args.font_size
                english_style.font_size = args.font_size

            if args.margin:
                english_style.margin_v = args.margin
                thai_style.margin_v = args.margin + 50

            merger.merge_dual_subtitles(
                video_path=video_path,
                top_subtitle_path=args.thai,
                bottom_subtitle_path=args.english,
                output_path=output_path,
                top_style=thai_style,
                bottom_style=english_style,
                crf=args.crf,
                preset=args.preset
            )

            logger.info(f"\n✓ Dual subtitle merge complete")
            sys.exit(0)

        # ==================== SINGLE SUBTITLE MODE ====================
        if not args.video or not args.subtitle:
            parser.print_help()
            sys.exit(1)

        video_path = args.video
        subtitle_path = args.subtitle
        output_path = args.output or video_path.parent / f"{video_path.stem}_subtitled{video_path.suffix}"

        # Custom style if specified
        style = None
        if args.font or args.font_size or args.margin:
            is_thai = merger._is_thai_subtitle(subtitle_path)
            style = SubtitleMerger.DEFAULT_THAI_STYLE if is_thai else SubtitleMerger.DEFAULT_ENGLISH_STYLE

            if args.font:
                style.font_name = args.font
            if args.font_size:
                style.font_size = args.font_size
            if args.margin:
                style.margin_v = args.margin

        merger.merge_single_subtitle(
            video_path=video_path,
            subtitle_path=subtitle_path,
            output_path=output_path,
            style=style,
            crf=args.crf,
            preset=args.preset
        )

        logger.info(f"\n✓ Merge complete")
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
