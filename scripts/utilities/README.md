# 🔧 Utility Scripts

Advanced utility scripts for specialized tasks.

---

## 📚 Available Utilities

### batch_process.py
**Purpose:** Process multiple videos in batch mode

**Usage:**
```bash
.venv/bin/python scripts/utilities/batch_process.py \
  input/*.mp4 \
  --output-dir workflow/01_transcripts/
```

**Features:**
- Process multiple videos sequentially
- Progress tracking across all videos
- Resume capability for batch operations
- Summary statistics

**When to use:** When you have 5+ videos to process

---

### merge_srt_video.py
**Purpose:** Burn SRT subtitles directly into video

**Usage:**
```bash
.venv/bin/python scripts/utilities/merge_srt_video.py \
  video.mp4 \
  workflow/04_final_srt/video_english.srt \
  -o video_with_subs.mp4
```

**Features:**
- Hardcode subtitles into video
- Customizable font, size, position
- Multiple subtitle tracks
- Quality preservation

**Output:** Video with embedded subtitles (no separate SRT needed)

**When to use:**
- Sharing videos where SRT support isn't guaranteed
- YouTube/social media uploads
- Final distribution

---

### split_video.py
**Purpose:** Split long videos into smaller chunks

**Usage:**
```bash
# Split by time (30-minute chunks)
.venv/bin/python scripts/utilities/split_video.py \
  long_video.mp4 \
  --chunk-duration 1800 \
  -o chunks/

# Split by size (500MB chunks)
.venv/bin/python scripts/utilities/split_video.py \
  long_video.mp4 \
  --chunk-size 500 \
  -o chunks/
```

**Features:**
- Split by duration or file size
- Preserve quality (no re-encoding)
- Smart keyframe detection
- Automatic naming

**When to use:**
- Videos > 2 hours (easier to transcribe in chunks)
- File size limits (Colab, Paperspace uploads)
- Parallel processing

---

### fix_all_issues.py
**Purpose:** Automated project maintenance and fixes

**Usage:**
```bash
.venv/bin/python scripts/utilities/fix_all_issues.py
```

**What it fixes:**
- File permission issues
- Missing directories
- Corrupted JSON files
- Encoding problems
- Path inconsistencies

**When to use:**
- After git pull (fix permissions)
- After moving files
- When encountering weird errors
- Regular maintenance

---

### enhanced_forex_dictionary.py
**Purpose:** Manage and expand Forex terminology dictionary

**Usage:**
```bash
# Add new term
.venv/bin/python scripts/utilities/enhanced_forex_dictionary.py add \
  --thai "คำศัพท์ใหม่" \
  --english "new term" \
  --category "technical"

# Search terms
.venv/bin/python scripts/utilities/enhanced_forex_dictionary.py search "แนวโน้ม"

# Export dictionary
.venv/bin/python scripts/utilities/enhanced_forex_dictionary.py export \
  -o forex_terms_export.json
```

**Features:**
- Add/edit/delete terms
- Search and filter
- Export to various formats
- Validation and duplicates check

**When to use:**
- Adding new Forex terms
- Maintaining terminology consistency
- Creating custom dictionaries

---

### migration_script.py
**Purpose:** Migrate data between different storage formats

**Usage:**
```bash
.venv/bin/python scripts/utilities/migration_script.py \
  --from old_format/ \
  --to new_format/ \
  --format json
```

**Features:**
- Convert between formats (JSON, CSV, etc.)
- Batch migration
- Validation and error checking
- Rollback capability

**When to use:**
- Upgrading data format
- Migrating from old system
- Changing storage structure

---

## 🎯 Common Workflows

### Workflow 1: Process Long Video

```bash
# 1. Split video into 30-minute chunks
.venv/bin/python scripts/utilities/split_video.py \
  long_video.mp4 --chunk-duration 1800 -o chunks/

# 2. Transcribe each chunk
for chunk in chunks/*.mp4; do
  .venv/bin/python scripts/whisper_transcribe.py $chunk
done

# 3. Merge transcripts
.venv/bin/python scripts/merge_transcripts.py \
  workflow/01_transcripts/chunk*.json -o merged.json
```

### Workflow 2: Batch Process Multiple Videos

```bash
# 1. Process all videos
.venv/bin/python scripts/utilities/batch_process.py input/*.mp4

# 2. Create translation batches
for transcript in workflow/01_transcripts/*.json; do
  .venv/bin/python scripts/create_translation_batch.py $transcript
done
```

### Workflow 3: Create Final Videos with Subtitles

```bash
# Merge SRT with original videos
for video in input/*.mp4; do
  basename=$(basename $video .mp4)
  .venv/bin/python scripts/utilities/merge_srt_video.py \
    $video \
    workflow/04_final_srt/${basename}_english.srt \
    -o output/${basename}_final.mp4
done
```

---

## 🐛 Troubleshooting

### Issue: "Permission denied"
```bash
# Fix permissions
chmod +x scripts/utilities/*.py
# Or run fix script
.venv/bin/python scripts/utilities/fix_all_issues.py
```

### Issue: "FFmpeg not found" (split_video.py, merge_srt_video.py)
```bash
# Install FFmpeg
sudo apt-get install ffmpeg  # Ubuntu/Debian
brew install ffmpeg          # Mac
```

### Issue: "Invalid JSON" (enhanced_forex_dictionary.py)
```bash
# Validate JSON files
.venv/bin/python scripts/utilities/fix_all_issues.py
```

---

## 📊 Performance Tips

1. **Parallel Processing:** Use batch_process.py with `--parallel` flag for multiple CPUs
2. **Split Long Videos:** Always split videos > 2 hours before transcribing
3. **Use Chunks:** Process 30-minute chunks for better checkpoint granularity

---

## 🔗 Related Documentation

- **Main Scripts:** [../README.md](../README.md)
- **User Guides:** [../../docs/guides/](../../docs/guides/)
- **Reference:** [../../docs/reference/](../../docs/reference/)

---

**Back to [Scripts Documentation](../)**
