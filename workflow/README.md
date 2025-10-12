# 🔄 Workflow Directory

Working files for the translation pipeline - organized by stage.

---

## 📁 Directory Structure

```
workflow/
├── 01_transcripts/         ← Stage 1: Thai transcripts (JSON)
├── 02_for_translation/     ← Stage 2: Prepared translation batches (TXT)
├── 03_translated/          ← Stage 3: English translations (TXT)
├── 04_final_srt/           ← Stage 4: Final SRT subtitle files
└── .translation_checkpoint.txt  ← Translation progress tracker
```

---

## 📊 Stage-by-Stage Workflow

### Stage 1: Transcription (01_transcripts/)

**Purpose**: Store Thai audio transcripts in JSON format

**Input**: Video/audio files
**Output**: JSON transcripts with timestamps

**Files**:
```
01_transcripts/
├── ep-01-19-12-24_transcript.json
├── ep-02_transcript.json
├── ep-06_part1_transcript.json
├── ep-06_part2_transcript.json
└── ...
```

**JSON Format**:
```json
{
  "metadata": {
    "video_file": "ep-01-19-12-24.mp4",
    "duration": 5720.5,
    "language": "th",
    "model_name": "large-v3",
    "timestamp": "2025-10-08T14:30:00"
  },
  "text": "Full Thai transcript text...",
  "segments": [
    {
      "id": 0,
      "start": 0.0,
      "end": 5.2,
      "text": "สวัสดีครับ ก็มาถึง Part 3 แล้วนะครับ",
      "confidence": 0.95
    }
  ]
}
```

**Commands to Create**:

**Method A: Colab (Recommended - FREE GPU, 100% Reliable)**
```bash
# 1. Open colab/hybrid_workflow.ipynb in Google Colab
# 2. Enable GPU (Runtime → Change runtime → GPU T4)
# 3. Mount Google Drive (for checkpoint storage)
# 4. Upload video OR use from Drive
# 5. Run transcription cell
# 6. Download transcript JSON
# 7. Move to workflow/01_transcripts/

# Features:
# ✓ FREE GPU (3-6 min for 1 hour video)
# ✓ Checkpoint saved to Google Drive
# ✓ 100% disconnect-proof (resume capability)
# ✓ CPU fallback if GPU quota exhausted
```

**Method B: Local/Paperspace (Slower but works offline)**
```bash
# Simple transcription
.venv/bin/python scripts/whisper_transcribe.py video.mp4

# With checkpoint (Paperspace)
.venv/bin/python scripts/whisper_transcribe.py video.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --resume

# Split into chunks (long videos)
.venv/bin/python scripts/whisper_transcribe.py video.mp4 \
  --start-time 0 --end-time 1800 \
  -o workflow/01_transcripts/video_part1.json
```

---

### Stage 2: Translation Preparation (02_for_translation/)

**Purpose**: Format Thai text for translation (manual or API)

**Input**: Transcript JSON files
**Output**: Text files ready for translation

**Files**:
```
02_for_translation/
├── ep-01-19-12-24_batch.txt
├── ep-02_batch.txt
└── ...
```

**Batch Format**:
```
# Translation Batch
# Source: ep-01-19-12-24_transcript.json
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
เริ่มจาก ไพรซ์แอคชั่น

...
```

**Commands to Create**:
```bash
.venv/bin/python scripts/create_translation_batch.py \
  workflow/01_transcripts/ep-01-19-12-24_transcript.json

# Output: workflow/02_for_translation/ep-01-19-12-24_batch.txt
```

**What to Do Next**:
1. Open the batch file in text editor
2. Translate using:
   - Claude Pro web (manual, free)
   - Claude API (automated, $0.50-1/hr)
   - OpenAI API (automated, $1.50-2.50/hr)
3. Save translated version to Stage 3

---

### Stage 3: Translated Text (03_translated/)

**Purpose**: Store English translations

**Input**: Translation batch files (manual/API)
**Output**: Translated text files with same segment format

**Files**:
```
03_translated/
├── ep-01-19-12-24_translated.txt
├── ep-02_translated.txt
└── ...
```

**Translation Format**:
```
[Segment 0]
Hello everyone, we've reached Part 3

[Segment 1]
About candlesticks and how to read them

[Segment 2]
Starting with Price Action

...
```

**How to Create**:

**Option A: Manual (Claude Pro Web)**
1. Copy text from `02_for_translation/ep-XX_batch.txt`
2. Paste into Claude Pro web interface
3. Ask: "Translate this Thai text to natural English, preserve Forex terms"
4. Copy result
5. Save to `03_translated/ep-XX_translated.txt`

**Option B: API (Automated)**
```python
# Coming soon - automated API translation
# For now, use manual method
```

**Quality Checklist**:
- [ ] All segments translated (none skipped)
- [ ] Forex terms in English (not Thai phonetic)
- [ ] No literal idiom translations
- [ ] Thai particles removed (ครับ, นะ, etc.)
- [ ] Natural English flow
- [ ] Segment IDs match original

---

### Stage 4: Final SRT Files (04_final_srt/)

**Purpose**: Generate English SRT subtitle files

**Input**: Original transcript JSON + translated text
**Output**: SRT files ready for video

**Files**:
```
04_final_srt/
├── ep-01-19-12-24_english.srt
├── ep-02_english.srt
└── ...
```

**SRT Format**:
```srt
1
00:00:00,000 --> 00:00:05,200
Hello everyone, we've reached Part 3

2
00:00:05,200 --> 00:00:10,400
About candlesticks and how to read them

3
00:00:10,400 --> 00:00:15,600
Starting with Price Action
```

**Commands to Create**:
```bash
.venv/bin/python scripts/batch_to_srt.py \
  workflow/01_transcripts/ep-01-19-12-24_transcript.json \
  workflow/03_translated/ep-01-19-12-24_translated.txt

# Output: workflow/04_final_srt/ep-01-19-12-24_english.srt
```

**What to Do Next**:
1. Download SRT file
2. Add to video using:
   - Video editor (Premiere, DaVinci Resolve)
   - YouTube/Vimeo upload
   - Quantum-SyncV5 (for voice synthesis)

---

## 🎯 Complete Workflow Example

### Example: Processing ep-06.mp4

```bash
# ===== STAGE 1: TRANSCRIBE =====
# Method A: Colab (Recommended)
# - Open colab/hybrid_workflow.ipynb
# - Run transcription with GPU
# - Download JSON to workflow/01_transcripts/

# Method B: Paperspace
tmux new -s ep06
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/ep-06.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --resume
# Ctrl+B D to detach

# Result: workflow/01_transcripts/ep-06_transcript.json


# ===== STAGE 2: PREPARE TRANSLATION =====
.venv/bin/python scripts/create_translation_batch.py \
  workflow/01_transcripts/ep-06_transcript.json

# Result: workflow/02_for_translation/ep-06_batch.txt


# ===== STAGE 3: TRANSLATE (MANUAL) =====
# 1. Open: workflow/02_for_translation/ep-06_batch.txt
# 2. Copy content
# 3. Paste into Claude Pro
# 4. Ask: "Translate Thai to English, preserve Forex terms"
# 5. Copy result
# 6. Save to: workflow/03_translated/ep-06_translated.txt


# ===== STAGE 4: GENERATE SRT =====
.venv/bin/python scripts/batch_to_srt.py \
  workflow/01_transcripts/ep-06_transcript.json \
  workflow/03_translated/ep-06_translated.txt

# Result: workflow/04_final_srt/ep-06_english.srt


# ===== DONE! =====
# Download: workflow/04_final_srt/ep-06_english.srt
```

---

## 📋 File Naming Convention

### Recommended Format

```
{video_name}_{stage}.{extension}

Examples:
- ep-01-19-12-24_transcript.json        (Stage 1)
- ep-01-19-12-24_batch.txt              (Stage 2)
- ep-01-19-12-24_translated.txt         (Stage 3)
- ep-01-19-12-24_english.srt            (Stage 4)

For chunks:
- ep-06_part1_transcript.json
- ep-06_part2_transcript.json
- ep-06_full_transcript.json            (merged)
```

### Naming Tips

✅ **Good**:
```
ep-01-19-12-24_transcript.json
forex-basics_part1_transcript.json
dow-theory-03_translated.txt
```

❌ **Bad**:
```
transcript.json                    (too generic)
video1.json                        (not descriptive)
ep01_final_final_v2.txt           (messy versions)
```

---

## 🔍 Checking Progress

### Current Status

```bash
# List all transcripts
ls -lh workflow/01_transcripts/

# Count segments in transcript
jq '.segments | length' workflow/01_transcripts/ep-01_transcript.json

# Check translation progress
cat workflow/.translation_checkpoint.txt

# List completed translations
ls -lh workflow/03_translated/

# List final SRT files
ls -lh workflow/04_final_srt/
```

### Translation Checkpoint File

**Location**: `workflow/.translation_checkpoint.txt`

**Purpose**: Track manual translation progress

**Format**:
```
Project: Thai Video Translation
Episode: ep-01-19-12-24
Status: IN_PROGRESS

Progress: 100/479 segments (20.9%)
Last completed: Segment 100
Last updated: 2025-10-08 15:30:00

Style notes:
- Casual teaching tone
- Using contractions (we'll, let's)
- Forex terms in English
- Context-aware idiom translation

Next: Continue from segment 101
```

**Commands**:
```bash
# Create checkpoint
cat > workflow/.translation_checkpoint.txt << EOF
Episode: ep-06
Progress: 50/300 segments (16.7%)
Last completed: Segment 50
EOF

# Update checkpoint
echo "Progress: 100/300 segments (33.3%)" >> workflow/.translation_checkpoint.txt

# Check checkpoint
cat workflow/.translation_checkpoint.txt
```

---

## 💡 Tips

### For Better Translations

1. **Read the context guide** in `*_batch.txt`
2. **Check idiom list** - don't translate literally!
3. **Keep forex terms accurate** (กระทิง = bull, หมี = bear)
4. **Maintain conversational tone**
5. **Preserve meaning, not words**

### For Faster Workflow

1. **🆕 Use Colab for transcription**: 3-6 min for 1hr video (vs 15-30 min local)
2. **🆕 Mount Google Drive in Colab**: Checkpoint saves even if disconnected
3. **Batch translate** multiple segments at once in Claude Code
4. **Use template file** for quicker format
5. **Save checkpoints** while translating

### 🆕 Colab-Specific Tips

1. **Enable GPU first**: Runtime → Change runtime → T4 GPU
2. **Mount Drive early**: Saves checkpoint to Drive automatically
3. **Use Drive for large videos**: Faster than local upload (2GB instant vs 15 min)
4. **Check checkpoint folder**: `/content/drive/MyDrive/.whisper_checkpoints/`
5. **If GPU exhausted**: Use CPU fallback cell (slower but works)
6. **Session disconnected?**: Just reconnect, mount Drive, re-run → resumes automatically

### Quality Checks

1. **Verify segment count** matches
2. **Check coverage percentage**
3. **Review [MISSING] markers**
4. **Test SRT** in video player before merging

---

## 🧹 Cleanup

### Remove Temporary Files

```bash
# Remove all transcripts (careful!)
rm workflow/01_transcripts/*.json

# Remove specific episode
rm workflow/01_transcripts/ep-01*.json
rm workflow/02_for_translation/ep-01*.txt
rm workflow/03_translated/ep-01*.txt
rm workflow/04_final_srt/ep-01*.srt

# Keep only final SRT files
rm workflow/01_transcripts/*.json
rm workflow/02_for_translation/*.txt
rm workflow/03_translated/*.txt
# Keep: workflow/04_final_srt/*.srt
```

### Archive Completed Work

```bash
# Create archive
mkdir -p archives/ep-01
cp workflow/01_transcripts/ep-01*.json archives/ep-01/
cp workflow/04_final_srt/ep-01*.srt archives/ep-01/

# Or zip it
zip -r ep-01-archive.zip \
  workflow/01_transcripts/ep-01*.json \
  workflow/04_final_srt/ep-01*.srt
```

---

## 📊 Statistics

### Calculate Progress

```bash
# Count total segments
find workflow/01_transcripts -name "*.json" -exec jq '.segments | length' {} \; | paste -sd+ | bc

# Count translated files
ls workflow/03_translated/*.txt | wc -l

# Count final SRT files
ls workflow/04_final_srt/*.srt | wc -l

# Calculate completion rate
echo "scale=2; $(ls workflow/04_final_srt/*.srt | wc -l) / $(ls workflow/01_transcripts/*.json | wc -l) * 100" | bc
```

---

## 🐛 Troubleshooting

### Issue: Missing translations

**Symptom**: `batch_to_srt.py` shows [MISSING] segments

**Solution**:
1. Check translated file has all segment IDs
2. Verify format: `[001]`, `[002]`, etc.
3. Make sure EN: lines have text

### Issue: Wrong timestamps

**Symptom**: Subtitles appear at wrong time

**Solution**:
1. Check you're using correct `transcript.json`
2. Don't modify timestamps in translated file
3. Re-run `batch_to_srt.py` with correct files

### Issue: Encoding errors

**Symptom**: Thai text shows as ??????

**Solution**:
1. Save all files as UTF-8
2. Use text editor that supports UTF-8
3. Check terminal encoding

### Issue: Segment count mismatch

```bash
# Check segment counts
echo "Transcript segments:"
jq '.segments | length' workflow/01_transcripts/ep-XX_transcript.json

echo "Translation segments:"
grep -c "^\[Segment " workflow/03_translated/ep-XX_translated.txt

# Should match!
```

### Issue: Corrupted JSON

```bash
# Validate JSON
jq empty workflow/01_transcripts/ep-XX_transcript.json

# If corrupted, re-transcribe
.venv/bin/python scripts/whisper_transcribe.py video.mp4 --force-restart
```

---

## 📊 Cost Comparison

### Old Method (API)
```
Transcription (Whisper): FREE
Translation (GPT API):   $1.50-2.50 per hour
Total:                   $1.50-2.50 per hour
```

### New Method (Claude Code)
```
Transcription (Whisper): FREE
Translation (Claude Code): FREE (manual)
Total:                   $0
```

**Savings**: 100% on translation costs! 💰

**Time**: +10-20 minutes manual work, but much higher quality

---

## ✅ Quick Reference

### One-Line Commands

```bash
# 1. Transcribe
.venv/bin/python scripts/whisper_transcribe.py video.mp4

# 2. Create batch
.venv/bin/python scripts/create_translation_batch.py \
  workflow/01_transcripts/video_transcript.json

# 3. Translate manually (Claude Code) ← YOU DO THIS

# 4. Convert to SRT
.venv/bin/python scripts/batch_to_srt.py \
  workflow/01_transcripts/video_transcript.json \
  workflow/03_translated/video_translated.txt

# 5. Merge (optional)
.venv/bin/python scripts/merge_srt_video.py \
  video.mp4 workflow/04_final_srt/video_english.srt
```

---

## 📞 Need Help?

- **Workflow Issues**: See [Main README](../README.md)
- **Script Usage**: See [scripts/README.md](../scripts/README.md)
- **Paperspace**: See [docs/PAPERSPACE_GUIDE.md](../docs/PAPERSPACE_GUIDE.md)
- **Colab**: See [colab/hybrid_workflow.ipynb](../colab/hybrid_workflow.ipynb)

---

**Keep your workflow organized for efficient translation! 📁**
