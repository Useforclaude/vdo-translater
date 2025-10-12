#!/usr/bin/env python3
"""
Thai Transcriber - Optimized Whisper-based Thai Audio Transcription
====================================================================
Version: 1.0.0
Description: High-accuracy Thai transcription using Whisper large-v3
             with Thai-specific optimizations

Features:
- Word-level timestamps
- Multi-temperature ensemble for accuracy
- Thai-specific prompt conditioning
- Forex terminology awareness
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import json

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to import whisper
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    logger.warning("OpenAI Whisper not installed. Install with: pip install openai-whisper")
    WHISPER_AVAILABLE = False


# ======================== DATA STRUCTURES ========================

@dataclass
class TranscriptionSegment:
    """Single transcription segment with timing"""
    id: int
    start: float
    end: float
    text: str
    words: List[Dict[str, Any]]
    confidence: float = 0.0
    no_speech_prob: float = 0.0


@dataclass
class TranscriptionResult:
    """Complete transcription result"""
    segments: List[TranscriptionSegment]
    language: str
    duration: float
    text: str
    word_count: int
    average_confidence: float


# ======================== THAI TRANSCRIBER ========================

class ThaiTranscriber:
    """
    Optimized Thai transcription using Whisper
    """

    # Thai-specific Whisper settings
    THAI_SETTINGS = {
        "language": "th",
        "task": "transcribe",
        "word_timestamps": True,

        # Multi-temperature ensemble for accuracy
        "temperature": (0.0, 0.2, 0.4, 0.6, 0.8),

        # Beam search
        "beam_size": 5,
        "best_of": 5,

        # Thai-specific thresholds
        "compression_ratio_threshold": 2.4,
        "logprob_threshold": -1.0,
        "no_speech_threshold": 0.6,

        # Context priming
        "condition_on_previous_text": True,
        "initial_prompt": "นี่คือการสอนเทรด Forex และการลงทุน ใช้คำศัพท์ทางการเงินและการวิเคราะห์ทางเทคนิค"
    }

    def __init__(self, model_name: str = "large-v3", device: str = "cpu"):
        """
        Initialize Thai transcriber

        Args:
            model_name: Whisper model to use (large-v3 recommended)
            device: Device to use ('cpu' or 'cuda')
        """
        if not WHISPER_AVAILABLE:
            raise ImportError("Whisper not installed. Please install with: pip install openai-whisper")

        self.model_name = model_name
        self.device = device
        self.model = None

        logger.info(f"Initializing Thai Transcriber with model: {model_name}")
        self._load_model()

    def _load_model(self):
        """Load Whisper model"""
        try:
            logger.info(f"Loading Whisper model: {self.model_name}...")
            self.model = whisper.load_model(self.model_name, device=self.device)
            logger.info("✓ Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def transcribe_file(
        self,
        audio_path: Path,
        **kwargs
    ) -> TranscriptionResult:
        """
        Transcribe audio file to Thai text

        Args:
            audio_path: Path to audio/video file
            **kwargs: Additional Whisper parameters to override

        Returns:
            TranscriptionResult with segments and metadata
        """
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        logger.info(f"Transcribing: {audio_path}")

        # Merge settings
        settings = {**self.THAI_SETTINGS, **kwargs}

        try:
            # Run Whisper transcription
            result = self.model.transcribe(
                str(audio_path),
                **settings
            )

            # Process results
            transcription = self._process_whisper_result(result)

            logger.info(f"✓ Transcription complete:")
            logger.info(f"  - Duration: {transcription.duration:.2f}s")
            logger.info(f"  - Segments: {len(transcription.segments)}")
            logger.info(f"  - Words: {transcription.word_count}")
            logger.info(f"  - Avg confidence: {transcription.average_confidence:.2%}")

            return transcription

        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise

    def _process_whisper_result(self, result: Dict) -> TranscriptionResult:
        """Process Whisper output into structured format"""
        segments = []
        total_confidence = 0
        word_count = 0

        for i, seg in enumerate(result.get("segments", []), 1):
            # Extract word-level timestamps if available
            words = []
            if "words" in seg:
                words = [
                    {
                        "word": w.get("word", ""),
                        "start": w.get("start", 0.0),
                        "end": w.get("end", 0.0),
                        "probability": w.get("probability", 0.0)
                    }
                    for w in seg["words"]
                ]
                word_count += len(words)

            # Calculate confidence from word probabilities
            if words:
                avg_prob = sum(w["probability"] for w in words) / len(words)
            else:
                avg_prob = 0.8  # Default confidence

            total_confidence += avg_prob

            segment = TranscriptionSegment(
                id=i,
                start=seg.get("start", 0.0),
                end=seg.get("end", 0.0),
                text=seg.get("text", "").strip(),
                words=words,
                confidence=avg_prob,
                no_speech_prob=seg.get("no_speech_prob", 0.0)
            )

            segments.append(segment)

        # Calculate average confidence
        avg_confidence = total_confidence / len(segments) if segments else 0.0

        return TranscriptionResult(
            segments=segments,
            language=result.get("language", "th"),
            duration=result.get("duration", 0.0),
            text=result.get("text", ""),
            word_count=word_count,
            average_confidence=avg_confidence
        )

    def save_srt(self, transcription: TranscriptionResult, output_path: Path):
        """Save transcription as SRT file"""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        srt_content = []
        for seg in transcription.segments:
            # Format timestamps
            start = self._format_srt_timestamp(seg.start)
            end = self._format_srt_timestamp(seg.end)

            # Create SRT entry
            srt_entry = f"{seg.id}\n{start} --> {end}\n{seg.text}\n"
            srt_content.append(srt_entry)

        # Write file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(srt_content))

        logger.info(f"✓ SRT saved: {output_path}")

    def save_json(self, transcription: TranscriptionResult, output_path: Path):
        """Save transcription as JSON"""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "language": transcription.language,
            "duration": transcription.duration,
            "word_count": transcription.word_count,
            "average_confidence": transcription.average_confidence,
            "text": transcription.text,
            "segments": [
                {
                    "id": seg.id,
                    "start": seg.start,
                    "end": seg.end,
                    "text": seg.text,
                    "confidence": seg.confidence,
                    "words": seg.words
                }
                for seg in transcription.segments
            ]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"✓ JSON saved: {output_path}")

    def save_txt(self, transcription: TranscriptionResult, output_path: Path):
        """Save plain text transcription"""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transcription.text)

        logger.info(f"✓ TXT saved: {output_path}")

    @staticmethod
    def _format_srt_timestamp(seconds: float) -> str:
        """Convert seconds to SRT timestamp format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"


# ======================== CLI INTERFACE ========================

def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Thai Audio Transcriber using Whisper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Transcribe video with default settings
  python thai_transcriber.py input.mp4

  # Specify output directory
  python thai_transcriber.py input.mp4 -o output/

  # Use different model
  python thai_transcriber.py input.mp4 -m medium

  # Save all formats
  python thai_transcriber.py input.mp4 --srt --json --txt
        """
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input audio/video file"
    )

    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("output"),
        help="Output directory (default: output/)"
    )

    parser.add_argument(
        "-m", "--model",
        type=str,
        default="large-v3",
        choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
        help="Whisper model to use (default: large-v3)"
    )

    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        choices=["cpu", "cuda"],
        help="Device to use (default: cpu)"
    )

    parser.add_argument(
        "--srt",
        action="store_true",
        help="Save SRT file"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Save JSON file"
    )

    parser.add_argument(
        "--txt",
        action="store_true",
        help="Save TXT file"
    )

    args = parser.parse_args()

    # If no format specified, save all
    if not (args.srt or args.json or args.txt):
        args.srt = args.json = args.txt = True

    try:
        # Initialize transcriber
        transcriber = ThaiTranscriber(model_name=args.model, device=args.device)

        # Transcribe
        result = transcriber.transcribe_file(args.input)

        # Generate output filename base
        output_base = args.output / args.input.stem

        # Save requested formats
        if args.srt:
            transcriber.save_srt(result, output_base.with_suffix(".srt"))

        if args.json:
            transcriber.save_json(result, output_base.with_suffix(".json"))

        if args.txt:
            transcriber.save_txt(result, output_base.with_suffix(".txt"))

        logger.info("✓ All done!")

    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
