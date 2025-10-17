# 📥 SS1.5 Episodes - Download & Transcription Guide

**Date:** 2025-10-17
**Purpose:** Download SS1.5 episodes from Google Drive and transcribe on Paperspace
**Target Location:** `/notebooks/thai-whisper/videos/`

---

## 🎬 Episode List (6 Videos)

| Episode | File Name | Google Drive ID | Size Est. |
|---------|-----------|-----------------|-----------|
| EP-01 | SS-1.5-ep01.mp4 | `1G5IZEQhYAZLdVB6RIXjbofmWyG-BxDIL` | ~? MB |
| EP-02 | SS-1.5-ep02.mp4 | `1gQB_nh0WV5Ec_LgUQkKy1a3cRQfFf31D` | ~? MB |
| EP-03 | SS-1.5-Ep03.mp4 | `1N59eoYoMuu2wC7_sM-gihHiSxILfDv3j` | ~? MB |
| EP-04 Part 1 | SS1.5-ep-04-part-1.mp4 | `1Lx0Me6TshvxsK_Uck7RddawnEB4pKyjT` | ~? MB |
| EP-04 Part 2 | SS-1.5-ep-04-part-2.mp4 | `10Q4UgtQlDQw1QzJfdgD6KVQjqnxTXyHt` | ~? MB |
| EP-05 | SS-1.5-ep05.mp4 | `1PZUMnOfpOqwUEE9b07H0blEyM-1HezGu` | ~? MB |

**Original URLs:**
```
https://drive.google.com/file/d/1G5IZEQhYAZLdVB6RIXjbofmWyG-BxDIL/view?usp=sharing  # EP-01
https://drive.google.com/file/d/1gQB_nh0WV5Ec_LgUQkKy1a3cRQfFf31D/view?usp=sharing  # EP-02
https://drive.google.com/file/d/1N59eoYoMuu2wC7_sM-gihHiSxILfDv3j/view?usp=sharing  # EP-03
https://drive.google.com/file/d/1Lx0Me6TshvxsK_Uck7RddawnEB4pKyjT/view?usp=sharing  # EP-04-part-1
https://drive.google.com/file/d/10Q4UgtQlDQw1QzJfdgD6KVQjqnxTXyHt/view?usp=sharing  # EP-04-part-2
https://drive.google.com/file/d/1PZUMnOfpOqwUEE9b07H0blEyM-1HezGu/view?usp=sharing  # EP-05
```

---

## 🚀 Quick Start (Copy-Paste Ready!)

### Step 1: Setup Paperspace

```bash
# 1. SSH to Paperspace or open Jupyter Terminal
# 2. Navigate to target directory
cd /notebooks
mkdir -p thai-whisper/videos
cd thai-whisper/videos

# 3. Install gdown (if not already installed)
pip install -U gdown

# 4. Verify installation
gdown --version
```

---

## 📥 Download All Episodes (Automated Script)

### Method 1: One-Command Download (Recommended)

```bash
# Create and run download script
cat > /notebooks/thai-whisper/download_ss1.5.sh << 'EOF'
#!/bin/bash

# SS1.5 Episode Download Script
# Date: 2025-10-17
# Target: /notebooks/thai-whisper/videos/

set -e  # Exit on error

DOWNLOAD_DIR="/notebooks/thai-whisper/videos"
cd "$DOWNLOAD_DIR" || exit 1

echo "================================================"
echo "SS1.5 Episode Downloader"
echo "Target: $DOWNLOAD_DIR"
echo "================================================"

# EP-01
echo ""
echo "[1/6] Downloading SS-1.5-ep01.mp4..."
gdown 1G5IZEQhYAZLdVB6RIXjbofmWyG-BxDIL -O SS-1.5-ep01.mp4
echo "✅ EP-01 complete"

# EP-02
echo ""
echo "[2/6] Downloading SS-1.5-ep02.mp4..."
gdown 1gQB_nh0WV5Ec_LgUQkKy1a3cRQfFf31D -O SS-1.5-ep02.mp4
echo "✅ EP-02 complete"

# EP-03
echo ""
echo "[3/6] Downloading SS-1.5-Ep03.mp4..."
gdown 1N59eoYoMuu2wC7_sM-gihHiSxILfDv3j -O SS-1.5-Ep03.mp4
echo "✅ EP-03 complete"

# EP-04 Part 1
echo ""
echo "[4/6] Downloading SS1.5-ep-04-part-1.mp4..."
gdown 1Lx0Me6TshvxsK_Uck7RddawnEB4pKyjT -O SS1.5-ep-04-part-1.mp4
echo "✅ EP-04 Part 1 complete"

# EP-04 Part 2
echo ""
echo "[5/6] Downloading SS-1.5-ep-04-part-2.mp4..."
gdown 10Q4UgtQlDQw1QzJfdgD6KVQjqnxTXyHt -O SS-1.5-ep-04-part-2.mp4
echo "✅ EP-04 Part 2 complete"

# EP-05
echo ""
echo "[6/6] Downloading SS-1.5-ep05.mp4..."
gdown 1PZUMnOfpOqwUEE9b07H0blEyM-1HezGu -O SS-1.5-ep05.mp4
echo "✅ EP-05 complete"

echo ""
echo "================================================"
echo "✅ All downloads complete!"
echo "================================================"

# List files
ls -lh

echo ""
echo "Total size:"
du -sh .
EOF

# Make executable
chmod +x /notebooks/thai-whisper/download_ss1.5.sh

# Run the script
/notebooks/thai-whisper/download_ss1.5.sh
```

---

## 📥 Method 2: Manual Download (One-by-One)

```bash
# Navigate to videos directory
cd /notebooks/thai-whisper/videos

# Download EP-01
gdown 1G5IZEQhYAZLdVB6RIXjbofmWyG-BxDIL -O SS-1.5-ep01.mp4

# Download EP-02
gdown 1gQB_nh0WV5Ec_LgUQkKy1a3cRQfFf31D -O SS-1.5-ep02.mp4

# Download EP-03
gdown 1N59eoYoMuu2wC7_sM-gihHiSxILfDv3j -O SS-1.5-Ep03.mp4

# Download EP-04 Part 1
gdown 1Lx0Me6TshvxsK_Uck7RddawnEB4pKyjT -O SS1.5-ep-04-part-1.mp4

# Download EP-04 Part 2
gdown 10Q4UgtQlDQw1QzJfdgD6KVQjqnxTXyHt -O SS-1.5-ep-04-part-2.mp4

# Download EP-05
gdown 1PZUMnOfpOqwUEE9b07H0blEyM-1HezGu -O SS-1.5-ep05.mp4

# Verify downloads
ls -lh
```

---

## 🎙️ Transcription Workflow

### Step 1: Start tmux Session

**⭐ What is tmux?**
- Terminal multiplexer that keeps tasks running
- Works even when browser closes or connection drops
- Essential for long-running tasks on Paperspace!

**📖 Full tmux guide:** [docs/TMUX_GUIDE.md](../docs/TMUX_GUIDE.md)

```bash
# Create persistent session
tmux new -s ss1.5-transcribe
```

**Quick tmux commands:**
- **Detach:** `Ctrl+B` then `D` (keeps running in background)
- **Reattach:** `tmux attach -t ss1.5-transcribe`
- **List sessions:** `tmux ls`

### Step 2: Setup Python Environment

```bash
# Navigate to project
cd /notebooks/video-translater

# Activate virtual environment (if exists)
source .venv/bin/activate

# Or install dependencies
pip install -U openai-whisper ffmpeg-python tqdm
```

### Step 3: Transcribe Episodes

#### Option A: Transcribe All (Sequential)

```bash
# Create transcription script
cat > /notebooks/thai-whisper/transcribe_all_ss1.5.sh << 'EOF'
#!/bin/bash

set -e

VIDEOS_DIR="/notebooks/thai-whisper/videos"
OUTPUT_DIR="/notebooks/video-translater/workflow/01_transcripts"
CHECKPOINT_DIR="/storage/whisper_checkpoints"

cd /notebooks/video-translater

echo "Starting SS1.5 transcription batch..."

# EP-01
echo "[1/6] Transcribing SS-1.5-ep01.mp4..."
.venv/bin/python scripts/whisper_transcribe.py \
  "$VIDEOS_DIR/SS-1.5-ep01.mp4" \
  --checkpoint-dir "$CHECKPOINT_DIR" \
  --checkpoint-interval 10 \
  --resume \
  -o "$OUTPUT_DIR/SS-1.5-ep01_transcript.json"

# EP-02
echo "[2/6] Transcribing SS-1.5-ep02.mp4..."
.venv/bin/python scripts/whisper_transcribe.py \
  "$VIDEOS_DIR/SS-1.5-ep02.mp4" \
  --checkpoint-dir "$CHECKPOINT_DIR" \
  --checkpoint-interval 10 \
  --resume \
  -o "$OUTPUT_DIR/SS-1.5-ep02_transcript.json"

# EP-03
echo "[3/6] Transcribing SS-1.5-Ep03.mp4..."
.venv/bin/python scripts/whisper_transcribe.py \
  "$VIDEOS_DIR/SS-1.5-Ep03.mp4" \
  --checkpoint-dir "$CHECKPOINT_DIR" \
  --checkpoint-interval 10 \
  --resume \
  -o "$OUTPUT_DIR/SS-1.5-ep03_transcript.json"

# EP-04 Part 1
echo "[4/6] Transcribing SS1.5-ep-04-part-1.mp4..."
.venv/bin/python scripts/whisper_transcribe.py \
  "$VIDEOS_DIR/SS1.5-ep-04-part-1.mp4" \
  --checkpoint-dir "$CHECKPOINT_DIR" \
  --checkpoint-interval 10 \
  --resume \
  -o "$OUTPUT_DIR/SS-1.5-ep04-part1_transcript.json"

# EP-04 Part 2
echo "[5/6] Transcribing SS-1.5-ep-04-part-2.mp4..."
.venv/bin/python scripts/whisper_transcribe.py \
  "$VIDEOS_DIR/SS-1.5-ep-04-part-2.mp4" \
  --checkpoint-dir "$CHECKPOINT_DIR" \
  --checkpoint-interval 10 \
  --resume \
  -o "$OUTPUT_DIR/SS-1.5-ep04-part2_transcript.json"

# EP-05
echo "[6/6] Transcribing SS-1.5-ep05.mp4..."
.venv/bin/python scripts/whisper_transcribe.py \
  "$VIDEOS_DIR/SS-1.5-ep05.mp4" \
  --checkpoint-dir "$CHECKPOINT_DIR" \
  --checkpoint-interval 10 \
  --resume \
  -o "$OUTPUT_DIR/SS-1.5-ep05_transcript.json"

echo "✅ All transcriptions complete!"
ls -lh "$OUTPUT_DIR"/SS-1.5-*.json
EOF

chmod +x /notebooks/thai-whisper/transcribe_all_ss1.5.sh
/notebooks/thai-whisper/transcribe_all_ss1.5.sh
```

#### Option B: Transcribe One-by-One

```bash
cd /notebooks/video-translater

# EP-01
.venv/bin/python scripts/whisper_transcribe.py \
  /notebooks/thai-whisper/videos/SS-1.5-ep01.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --checkpoint-interval 10 \
  --resume

# Press Ctrl+B D to detach from tmux
# Check progress: python scripts/whisper_status.py --watch
```

### Step 4: Monitor Progress

```bash
# In new terminal (or reattach to tmux)
cd /notebooks/video-translater
.venv/bin/python scripts/whisper_status.py --watch
```

---

## 🔄 Merge EP-04 Parts (After Transcription)

```bash
cd /notebooks/video-translater

# Merge EP-04 Part 1 + Part 2
.venv/bin/python scripts/merge_transcripts.py \
  workflow/01_transcripts/SS-1.5-ep04-part1_transcript.json \
  workflow/01_transcripts/SS-1.5-ep04-part2_transcript.json \
  -o workflow/01_transcripts/SS-1.5-ep04_transcript.json

# Verify merged file
ls -lh workflow/01_transcripts/SS-1.5-ep04_transcript.json
```

---

## 📊 Expected Output

After completion, you should have:

```
workflow/01_transcripts/
├── SS-1.5-ep01_transcript.json
├── SS-1.5-ep02_transcript.json
├── SS-1.5-ep03_transcript.json
├── SS-1.5-ep04_transcript.json  (merged from part1 + part2)
└── SS-1.5-ep05_transcript.json
```

**Total:** 5 episodes (EP-04 merged)

---

## ⏱️ Time Estimates

| Episode | Estimated Duration | Transcription Time (GPU) |
|---------|-------------------|--------------------------|
| EP-01 | ~30-60 min | ~3-8 minutes |
| EP-02 | ~30-60 min | ~3-8 minutes |
| EP-03 | ~30-60 min | ~3-8 minutes |
| EP-04 (combined) | ~60-90 min | ~6-12 minutes |
| EP-05 | ~30-60 min | ~3-8 minutes |

**Total:** ~3-5 hours video → ~18-44 minutes transcription (with GPU)

---

## 🐛 Troubleshooting

### Issue: gdown fails with "Access denied"

**Solution 1: Use cookies.txt**
```bash
# Export cookies from browser (Google account logged in)
# Save as /notebooks/cookies.txt
gdown --fuzzy --cookies /notebooks/cookies.txt [FILE_ID] -O output.mp4
```

**Solution 2: Make files public**
- Right-click file in Google Drive → Share → Anyone with link

### Issue: Download stops midway

```bash
# Resume download (gdown auto-resumes)
gdown [FILE_ID] -O output.mp4  # Will continue from where it stopped
```

### Issue: Out of storage space

```bash
# Check available space
df -h /notebooks

# Clear unnecessary files
rm -rf /notebooks/.cache/*
```

---

## 📝 Next Steps After Transcription

1. **Download transcripts to local**
   ```bash
   # On local machine
   scp paperspace:/notebooks/video-translater/workflow/01_transcripts/SS-1.5-*.json \
       ./workflow/01_transcripts/
   ```

2. **Start translation pipeline**
   ```bash
   # For each episode
   .venv/bin/python scripts/create_translation_batch.py \
     workflow/01_transcripts/SS-1.5-ep01_transcript.json

   # Then translate manually or via API
   ```

3. **Generate SRT files**
   ```bash
   .venv/bin/python scripts/batch_to_srt.py \
     workflow/01_transcripts/SS-1.5-ep01_transcript.json \
     workflow/03_translated/SS-1.5-ep01_translated.txt
   ```

---

## ✅ Checklist

**Pre-Download:**
- [ ] Paperspace machine started
- [ ] Sufficient storage space (check `df -h`)
- [ ] gdown installed (`pip install gdown`)
- [ ] Target directory created (`/notebooks/thai-whisper/videos/`)

**Download Phase:**
- [ ] EP-01 downloaded
- [ ] EP-02 downloaded
- [ ] EP-03 downloaded
- [ ] EP-04 Part 1 downloaded
- [ ] EP-04 Part 2 downloaded
- [ ] EP-05 downloaded
- [ ] All files verified (`ls -lh`)

**Transcription Phase:**
- [ ] tmux session started
- [ ] Virtual environment activated
- [ ] Checkpoint directory exists
- [ ] EP-01 transcribed
- [ ] EP-02 transcribed
- [ ] EP-03 transcribed
- [ ] EP-04 Part 1 transcribed
- [ ] EP-04 Part 2 transcribed
- [ ] EP-04 parts merged
- [ ] EP-05 transcribed

**Post-Transcription:**
- [ ] All JSON files verified
- [ ] Transcripts downloaded to local
- [ ] Translation batches created
- [ ] Paperspace machine stopped (to save costs!)

---

## 💡 Pro Tips

1. **Always use tmux** - Prevents loss if connection drops
2. **Enable checkpoints** - Can resume if GPU timeout
3. **Merge EP-04 parts** - Easier to translate as one file
4. **Download in batches** - Don't download all at once if storage limited
5. **Monitor progress** - Use `whisper_status.py --watch`
6. **Stop machine when done** - Save money on Paperspace!

---

**Created:** 2025-10-17
**Project:** Thai Video Translation Pipeline
**Status:** Ready for execution

---

**🚀 Ready to start? Copy the commands above and paste into Paperspace!**
