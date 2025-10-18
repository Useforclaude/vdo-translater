#!/usr/bin/env python3
"""
Subtitle Words-Per-Minute Validator
===================================

ตรวจสอบไฟล์ .srt ที่ได้จากการแปลว่าแต่ละ segment มีความยาวคำ/เวลา
สอดคล้องกับเกณฑ์ เพื่อป้องกันปัญหาเสียงสังเคราะห์พูดไม่ทันหรือ timing เพี้ยน

Features:
- รองรับทั้งไฟล์เดี่ยวและไดเรกทอรี (ค้นหา *.srt แบบ recursive)
- คำนวณ duration, word count, WPM ต่อ segment
- สรุปสถิติภาพรวม และไฮไลต์ segment ที่เกิน target WPM หรือสั้นผิดปกติ
- เลือก export รายงานเป็น JSON สำหรับประสานงานกับ agent อื่นได้

Usage:
    python scripts/check_subtitle_wpm.py workflow/04_final_srt/
    python scripts/check_subtitle_wpm.py path/to/file.srt --target-wpm 130 --top 10
    python scripts/check_subtitle_wpm.py workflow/04_final_srt --export report.json
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence


DEFAULT_TARGET_WPM = 140.0
DEFAULT_MIN_DURATION = 1.5  # seconds


@dataclass
class SubtitleSegment:
    """Subtitle segment with helper metrics."""

    index: int
    start: float
    end: float
    text: str

    @property
    def duration(self) -> float:
        return round(self.end - self.start, 3)

    @property
    def words(self) -> int:
        # split on whitespace, ignore empty tokens
        return len([w for w in self.text.replace("\n", " ").split(" ") if w])

    @property
    def wpm(self) -> float:
        if self.duration <= 0:
            return float("inf")
        return (self.words / self.duration) * 60.0


TIME_PATTERN = re.compile(r"(\d{2}):(\d{2}):(\d{2})[.,](\d{3})")
TIMELINE_PATTERN = re.compile(
    r"(\d{2}:\d{2}:\d{2}[.,]\d{3}) --> (\d{2}:\d{2}:\d{2}[.,]\d{3})"
)


def to_seconds(timestamp: str) -> float:
    match = TIME_PATTERN.fullmatch(timestamp.strip())
    if not match:
        raise ValueError(f"Invalid timestamp format: '{timestamp}'")
    hours, minutes, seconds, millis = map(int, match.groups())
    return hours * 3600 + minutes * 60 + seconds + millis / 1000


def load_srt(srt_path: Path) -> List[SubtitleSegment]:
    """
    Load SRT file and convert to SubtitleSegment list.

    Args:
        srt_path: Path to .srt file
    """
    segments: List[SubtitleSegment] = []
    contents = srt_path.read_text(encoding="utf-8", errors="replace").strip()
    blocks = re.split(r"\n\s*\n", contents)

    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if len(lines) < 3:
            continue

        index_line = lines[0]
        if not index_line.isdigit():
            continue
        index = int(index_line)

        time_line = lines[1]
        time_match = TIMELINE_PATTERN.fullmatch(time_line)
        if not time_match:
            continue
        start = to_seconds(time_match.group(1))
        end = to_seconds(time_match.group(2))

        text = " ".join(lines[2:])
        segments.append(SubtitleSegment(index=index, start=start, end=end, text=text))

    return segments


def gather_srt_files(inputs: Sequence[Path]) -> List[Path]:
    """Expand input paths into a unique list of .srt files."""
    srt_files: List[Path] = []
    for path in inputs:
        if path.is_file() and path.suffix.lower() == ".srt":
            srt_files.append(path)
        elif path.is_dir():
            srt_files.extend(sorted(path.rglob("*.srt")))
    # Remove duplicates while preserving order
    seen = set()
    unique: List[Path] = []
    for file_path in srt_files:
        if file_path not in seen:
            seen.add(file_path)
            unique.append(file_path)
    return unique


def summarize_segments(segments: Sequence[SubtitleSegment]):
    """Return aggregate statistics for a sequence of segments."""
    durations = [seg.duration for seg in segments if seg.duration > 0]
    wpm_values = [seg.wpm for seg in segments if seg.duration > 0]
    total_words = sum(seg.words for seg in segments)
    total_time = sum(seg.duration for seg in segments if seg.duration > 0)

    return {
        "segment_count": len(segments),
        "total_words": total_words,
        "total_time_sec": total_time,
        "avg_duration_sec": statistics.mean(durations) if durations else 0.0,
        "avg_wpm": statistics.mean(wpm_values) if wpm_values else 0.0,
        "p90_wpm": statistics.quantiles(wpm_values, n=10)[-1] if len(wpm_values) >= 10 else 0.0,
        "max_wpm": max(wpm_values) if wpm_values else 0.0,
    }


def find_violations(
    segments: Sequence[SubtitleSegment],
    target_wpm: float,
    min_duration: float,
) -> List[SubtitleSegment]:
    """Return segments that exceed WPM target or are shorter than min_duration."""
    violations: List[SubtitleSegment] = []
    for segment in segments:
        if segment.duration <= 0 or segment.duration < min_duration:
            violations.append(segment)
        elif segment.wpm > target_wpm:
            violations.append(segment)
    return violations


def format_seconds(seconds: float) -> str:
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(int(minutes), 60)
    return f"{hours:02d}:{minutes:02d}:{sec:06.3f}"


def build_report_entry(
    srt_path: Path,
    segments: Sequence[SubtitleSegment],
    violations: Sequence[SubtitleSegment],
) -> dict:
    summary = summarize_segments(segments)
    payload = {
        "file": str(srt_path),
        "summary": summary,
        "violations": [
            {
                "index": seg.index,
                "start": format_seconds(seg.start),
                "end": format_seconds(seg.end),
                "duration_sec": seg.duration,
                "word_count": seg.words,
                "wpm": seg.wpm,
                "text": seg.text,
            }
            for seg in violations
        ],
    }
    return payload


def print_report_entry(report: dict, top_n: int):
    summary = report["summary"]
    file_name = report["file"]
    violations = report["violations"]
    print("=" * 80)
    print(file_name)
    print("- Summary -")
    print(
        f"Segments: {summary['segment_count']} | "
        f"Total Duration: {summary['total_time_sec']:.1f}s | "
        f"Avg WPM: {summary['avg_wpm']:.1f} | "
        f"P90 WPM: {summary['p90_wpm']:.1f} | "
        f"Max WPM: {summary['max_wpm']:.1f}"
    )
    print(f"Violations: {len(violations)} segment(s)")
    if not violations:
        return

    print("- Top Violations -")
    for entry in violations[:top_n]:
        print(
            f"#{entry['index']:04d} "
            f"{entry['start']} → {entry['end']} "
            f"(dur {entry['duration_sec']:.2f}s, words {entry['word_count']}, "
            f"WPM {entry['wpm']:.1f})"
        )
        print(f"  {entry['text']}")


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate subtitle speed (WPM)")
    parser.add_argument(
        "inputs",
        nargs="+",
        help="ไฟล์หรือโฟลเดอร์ที่มี .srt (ค้นหาแบบ recursive)",
    )
    parser.add_argument(
        "--target-wpm",
        type=float,
        default=DEFAULT_TARGET_WPM,
        help="เกณฑ์ WPM สูงสุดต่อ segment (default: 140)",
    )
    parser.add_argument(
        "--min-duration",
        type=float,
        default=DEFAULT_MIN_DURATION,
        help="ความยาวขั้นต่ำของ segment (วินาที) default: 1.5",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="จำนวน violation ที่จะแสดง (default: 5)",
    )
    parser.add_argument(
        "--export",
        type=Path,
        help="บันทึกรายงานเป็น JSON ไฟล์ (optional)",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    input_paths = [Path(p) for p in args.inputs]
    srt_files = gather_srt_files(input_paths)

    if not srt_files:
        print("⚠️  ไม่พบไฟล์ .srt ตามเส้นทางที่ระบุ")
        return 1

    reports = []
    for srt_path in srt_files:
        segments = load_srt(srt_path)
        violations = find_violations(
            segments=segments,
            target_wpm=args.target_wpm,
            min_duration=args.min_duration,
        )
        report = build_report_entry(srt_path, segments, violations)
        print_report_entry(report, top_n=args.top)
        reports.append(report)

    if args.export:
        args.export.parent.mkdir(parents=True, exist_ok=True)
        args.export.write_text(
            json.dumps(reports, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"\nรายงานถูกบันทึกไว้ที่: {args.export}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
