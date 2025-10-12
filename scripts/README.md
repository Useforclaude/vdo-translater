# 📜 Scripts Documentation

All executable scripts for video transcription and translation.

---

## 🎯 Main Scripts

### 1. whisper_transcribe.py
**Purpose**: Transcribe Thai audio to text using Whisper large-v3

**Features**:
- ✅ Checkpoint/resume system (survive timeouts)
- ✅ Time range support (split long videos)
- ✅ Word-level timestamps
- ✅ Thai-optimized settings
- ✅ Progress tracking with ETA
- ✅ Graceful shutdown (Ctrl+C saves checkpoint)

**Basic Usage**:
```bash
.venv/bin/python scripts/whisper_transcribe.py video.mp4
```

**With Checkpoint** (recommended):
```bash
.venv/bin/python scripts/whisper_transcribe.py video.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --resume
```

**Time Range** (0-30 minutes):
```bash
.venv/bin/python scripts/whisper_transcribe.py video.mp4 \
  --start-time 0 \
  --end-time 1800 \
  -o workflow/01_transcripts/part1.json
```

**All Parameters**:
```
video_file              Video/audio file path
-o, --output           Output JSON file (default: auto-generated)
--model                Whisper model (default: large-v3)
--device               Device: cuda/cpu (default: auto)
--checkpoint-dir       Checkpoint directory (default: .cache/checkpoints)
--checkpoint-interval  Save every N segments (default: 10)
--resume               Resume from checkpoint if exists
--force-restart        Ignore checkpoint, start fresh
--start-time           Start time in seconds
--end-time             End time in seconds
--status               Show checkpoint status and exit
```

**Output Format** (JSON):
```json
{
  "metadata": {
    "video_file": "video.mp4",
    "duration": 3600.5,
    "model_name": "large-v3",
    "language": "th"
  },
  "text": "Full transcript text...",
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 5.2,
      "text": "สวัสดีครับ",
      "confidence": 0.95
    }
  ]
}
```

**Exit Codes**:
- 0: Success
- 1: Error
- 130: Interrupted by user (Ctrl+C)

---

### 2. whisper_status.py
**Purpose**: Check transcription progress without loading Whisper model

**Features**:
- ✅ Fast status check (no heavy model loading)
- ✅ Watch mode (auto-refresh)
- ✅ JSON output (for automation)
- ✅ Multiple checkpoints support
- ✅ ETA calculation
- ✅ Progress bar visualization

**Basic Usage**:
```bash
.venv/bin/python scripts/whisper_status.py
```

**Watch Mode** (auto-refresh every 5 seconds):
```bash
.venv/bin/python scripts/whisper_status.py --watch
```

**Custom Checkpoint Directory**:
```bash
.venv/bin/python scripts/whisper_status.py \
  --checkpoint-dir /storage/whisper_checkpoints
```

**JSON Output** (for scripts):
```bash
.venv/bin/python scripts/whisper_status.py --json
```

**Parameters**:
```
--checkpoint-dir    Checkpoint directory (default: /storage/whisper_checkpoints)
--json              Output in JSON format
--watch             Watch mode (auto-refresh)
--interval          Refresh interval in seconds (default: 5)
```

**Sample Output**:
```
================================================================================
WHISPER TRANSCRIPTION STATUS
================================================================================
Active transcriptions: 2

[1] /storage/videos/ep-06.mp4
    Hash: a1b2c3d4
    Model: large-v3 (cuda)
    Time range: 0s - 1800s

    Progress: 150/300 segments (50.0%)
    [█████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░]

    Elapsed: 15m 30s
    Speed: 8.5x realtime
    ETA: 8m 45s

    Created: 2025-10-08 14:00:00
    Last updated: 2025-10-08 14:15:30
    Checkpoint: /storage/whisper_checkpoints/a1b2c3d4

[2] /storage/videos/ep-07.mp4
    ...
================================================================================
```

---

### 3. merge_transcripts.py
**Purpose**: Merge multiple transcript chunks into one complete file

**Use Case**: You transcribed a 2-hour video in 4x 30-minute chunks, now merge them into one.

**Features**:
- ✅ Merge multiple JSON transcripts
- ✅ Sort segments by timestamp
- ✅ Re-index segment IDs
- ✅ Detect gaps/overlaps
- ✅ Validation checks
- ✅ Output merged JSON + SRT

**Basic Usage**:
```bash
.venv/bin/python scripts/merge_transcripts.py \
  part1.json part2.json part3.json \
  -o merged.json
```

**Auto-Find with Pattern**:
```bash
.venv/bin/python scripts/merge_transcripts.py \
  --pattern "video_part*_transcript.json" \
  -o merged.json
```

**With SRT Output**:
```bash
.venv/bin/python scripts/merge_transcripts.py \
  part*.json \
  -o merged.json \
  --srt merged_thai.srt
```

**Force Merge** (ignore warnings):
```bash
.venv/bin/python scripts/merge_transcripts.py \
  part*.json \
  -o merged.json \
  --force
```

**Parameters**:
```
inputs              Input transcript JSON files
--pattern           Glob pattern to find files
-o, --output        Output merged JSON file (required)
--srt               Output Thai SRT file (optional)
--force             Force merge even with warnings
```

**Validation**:
- Checks for gaps > 5 seconds between chunks
- Checks for overlaps > 5 seconds
- Warns but allows merge (unless validation fails)

**Example Output**:
```
======================================================================
MERGE TRANSCRIPTS
======================================================================
Input files: 4
  - video_part1_transcript.json
  - video_part2_transcript.json
  - video_part3_transcript.json
  - video_part4_transcript.json

✓ Loaded: video_part1_transcript.json
  Segments: 200
  Duration: 0:30:00

✓ Loaded: video_part2_transcript.json
  Segments: 195
  Duration: 0:29:30

Validating transcripts...
⚠️  Gap detected: 0:00:02 between transcript 2 and transcript 3

Continue with warnings? [y/N]: y

Merging 4 transcripts...
✓ Merge complete:
  - Total segments: 779
  - Total duration: 1:59:45
  - Total words: 15,432
  - Avg confidence: 94.5%

✓ Merged JSON saved: merged.json
✓ Merged SRT saved: merged_thai.srt

======================================================================
MERGE COMPLETE
======================================================================
Output JSON: merged.json
Output SRT: merged_thai.srt

Next steps:
  1. Create translation batch:
     python scripts/create_translation_batch.py merged.json
  2. Translate with Claude Code
  3. Convert to English SRT:
     python scripts/batch_to_srt.py merged.json translated.txt
```

---

### 4. create_translation_batch.py
**Purpose**: Prepare Thai transcript for translation (format for Claude/GPT)

**Features**:
- ✅ Extract Thai text from transcript JSON
- ✅ Format as numbered segments
- ✅ Include context headers
- ✅ Preserve segment IDs
- ✅ Add translation instructions

**Basic Usage**:
```bash
.venv/bin/python scripts/create_translation_batch.py \
  workflow/01_transcripts/video_transcript.json
```

**Custom Output**:
```bash
.venv/bin/python scripts/create_translation_batch.py \
  input.json \
  -o custom_batch.txt
```

**Parameters**:
```
transcript_file     Input transcript JSON file
-o, --output        Output batch file (default: auto-generated)
```

**Output Format**:
```
# Translation Batch
# Source: video_transcript.json
# Segments: 479
# Duration: 1:35:20
# Language: Thai → English

Instructions:
- Translate Thai to natural English
- Preserve Forex terminology
- Remove Thai particles (ครับ, นะ, etc.)
- Keep timestamp references

---

[Segment 0]
สวัสดีครับ ก็มาถึง Part 3 แล้วนะครับ

[Segment 1]
เรื่องของแท่งเทียน และการอ่านแท่งเทียน

[Segment 2]
...
```

---

### 5. batch_to_srt.py
**Purpose**: Convert translated text to English SRT subtitle file

**Features**:
- ✅ Parse translated batch file
- ✅ Match with original timestamps
- ✅ Generate SRT format
- ✅ Validate segment count
- ✅ Handle missing translations

**Basic Usage**:
```bash
.venv/bin/python scripts/batch_to_srt.py \
  workflow/01_transcripts/video_transcript.json \
  workflow/03_translated/video_translated.txt
```

**Custom Output**:
```bash
.venv/bin/python scripts/batch_to_srt.py \
  transcript.json \
  translated.txt \
  -o custom_output.srt
```

**Parameters**:
```
transcript_file     Original transcript JSON (for timestamps)
translated_file     Translated batch file
-o, --output        Output SRT file (default: auto-generated)
```

**Input Format** (translated.txt):
```
[Segment 0]
Hello everyone, we've reached Part 3

[Segment 1]
About candlesticks and how to read them

[Segment 2]
...
```

**Output Format** (SRT):
```srt
1
00:00:00,000 --> 00:00:03,500
Hello everyone, we've reached Part 3

2
00:00:03,500 --> 00:00:07,200
About candlesticks and how to read them

3
00:00:07,200 --> 00:00:12,800
...
```

---

## 🔄 Complete Workflow

### Workflow 1: Simple (No Chunks)

```bash
# Step 1: Transcribe
.venv/bin/python scripts/whisper_transcribe.py video.mp4

# Step 2: Create translation batch
.venv/bin/python scripts/create_translation_batch.py \
  workflow/01_transcripts/video_transcript.json

# Step 3: Translate manually
# Open: workflow/02_for_translation/video_batch.txt
# Translate using Claude Pro or API
# Save: workflow/03_translated/video_translated.txt

# Step 4: Generate SRT
.venv/bin/python scripts/batch_to_srt.py \
  workflow/01_transcripts/video_transcript.json \
  workflow/03_translated/video_translated.txt

# Done! → workflow/04_final_srt/video_english.srt
```

### Workflow 2: Long Video (With Chunks)

```bash
# Step 1: Transcribe chunks (in tmux sessions)
tmux new -s part1
.venv/bin/python scripts/whisper_transcribe.py video.mp4 \
  --start-time 0 --end-time 1800 \
  -o workflow/01_transcripts/video_part1.json
# Ctrl+B D

tmux new -s part2
.venv/bin/python scripts/whisper_transcribe.py video.mp4 \
  --start-time 1800 --end-time 3600 \
  -o workflow/01_transcripts/video_part2.json
# Ctrl+B D

# Step 2: Check progress
.venv/bin/python scripts/whisper_status.py --watch

# Step 3: Merge when done
.venv/bin/python scripts/merge_transcripts.py \
  workflow/01_transcripts/video_part*.json \
  -o workflow/01_transcripts/video_full.json

# Step 4-6: Same as Workflow 1
```

### Workflow 3: Paperspace Production

```bash
# Use tmux + checkpoints for safety
tmux new -s whisper

.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/ep-06.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --checkpoint-interval 10 \
  --resume

# Detach: Ctrl+B D
# Check: python scripts/whisper_status.py --watch
# Resume if needed: --resume flag handles it automatically
```

---

## 📊 Performance Tips

### 1. Use GPU for Faster Transcription
```bash
# Auto-detect (uses GPU if available)
.venv/bin/python scripts/whisper_transcribe.py video.mp4

# Force CPU (if GPU memory issues)
.venv/bin/python scripts/whisper_transcribe.py video.mp4 --device cpu
```

### 2. Split Long Videos
```bash
# Instead of 2-hour video → 4x 30-min chunks
# Pros: Faster, safer, can resume chunks independently
```

### 3. Use Persistent Storage (Paperspace)
```bash
# Save checkpoints to /storage/ (survives restarts)
--checkpoint-dir /storage/whisper_checkpoints
```

### 4. Save Checkpoints Frequently
```bash
# Save every 10 segments (default)
--checkpoint-interval 10

# For unstable connections, save more often
--checkpoint-interval 5
```

---

## 🐛 Troubleshooting

### Issue: "No module named 'whisper'"
```bash
.venv/bin/pip install -U openai-whisper
```

### Issue: "FFmpeg not found"
```bash
sudo apt-get install ffmpeg
```

### Issue: "CUDA out of memory"
```bash
# Use CPU or smaller model
.venv/bin/python scripts/whisper_transcribe.py video.mp4 --device cpu
# or
.venv/bin/python scripts/whisper_transcribe.py video.mp4 --model medium
```

### Issue: Transcription stopped midway
```bash
# Just resume!
.venv/bin/python scripts/whisper_transcribe.py video.mp4 --resume
```

### Issue: Checkpoint file corrupted
```bash
# Force restart (ignore checkpoint)
.venv/bin/python scripts/whisper_transcribe.py video.mp4 --force-restart
```

### Issue: Merge fails with "gaps detected"
```bash
# Force merge (ignore warnings)
.venv/bin/python scripts/merge_transcripts.py part*.json -o full.json --force
```

---

## 📁 Output File Locations

| Script | Default Output |
|--------|----------------|
| whisper_transcribe.py | `workflow/01_transcripts/{video}_transcript.json` |
| create_translation_batch.py | `workflow/02_for_translation/{video}_batch.txt` |
| batch_to_srt.py | `workflow/04_final_srt/{video}_english.srt` |
| merge_transcripts.py | Custom (must specify with -o) |

---

## 🎯 Quick Reference

```bash
# Transcribe
.venv/bin/python scripts/whisper_transcribe.py video.mp4

# Transcribe with checkpoint
.venv/bin/python scripts/whisper_transcribe.py video.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints --resume

# Check status
.venv/bin/python scripts/whisper_status.py --watch

# Merge chunks
.venv/bin/python scripts/merge_transcripts.py part*.json -o full.json

# Create translation batch
.venv/bin/python scripts/create_translation_batch.py transcript.json

# Generate SRT
.venv/bin/python scripts/batch_to_srt.py transcript.json translated.txt
```

---

**For more details, see [Main README](../README.md)**
