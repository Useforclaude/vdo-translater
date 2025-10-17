# ⚡ Quick Start Guide

> Fast reference for common tasks - no explanations, just commands

---

## 🎬 Transcribe Video

### Simple (1 command)
```bash
.venv/bin/python scripts/whisper_transcribe.py video.mp4
```

### With Checkpoint (recommended for Paperspace)
```bash
.venv/bin/python scripts/whisper_transcribe.py video.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --resume
```

### In Background (tmux)
```bash
tmux new -s whisper
.venv/bin/python scripts/whisper_transcribe.py video.mp4 --resume
# Press: Ctrl+B then D
```

---

## 📊 Check Progress

### Quick Check
```bash
.venv/bin/python scripts/whisper_status.py
```

### Watch Mode (auto-refresh)
```bash
.venv/bin/python scripts/whisper_status.py --watch
```

---

## 🔄 Resume Transcription

### After Timeout/Crash
```bash
.venv/bin/python scripts/whisper_transcribe.py video.mp4 --resume
```

### Force Restart (ignore checkpoint)
```bash
.venv/bin/python scripts/whisper_transcribe.py video.mp4 --force-restart
```

---

## ✂️ Split Long Videos

### Transcribe 0-30 minutes
```bash
.venv/bin/python scripts/whisper_transcribe.py video.mp4 \
  --start-time 0 --end-time 1800 \
  -o workflow/01_transcripts/part1.json
```

### Transcribe 30-60 minutes
```bash
.venv/bin/python scripts/whisper_transcribe.py video.mp4 \
  --start-time 1800 --end-time 3600 \
  -o workflow/01_transcripts/part2.json
```

### Merge Parts
```bash
.venv/bin/python scripts/merge_transcripts.py \
  workflow/01_transcripts/part*.json \
  -o workflow/01_transcripts/full.json
```

---

## 🌐 Translate to English

### Step 1: Create Batch
```bash
.venv/bin/python scripts/create_translation_batch.py \
  workflow/01_transcripts/video_transcript.json
```

### Step 2: Translate
```
→ Use Claude Pro web or API
→ Save to: workflow/03_translated/video_translated.txt
```

### Step 3: Generate SRT
```bash
.venv/bin/python scripts/batch_to_srt.py \
  workflow/01_transcripts/video_transcript.json \
  workflow/03_translated/video_translated.txt
```

---

## 🔧 tmux Basics

### Create Session
```bash
tmux new -s name
```

### List Sessions
```bash
tmux ls
```

### Attach to Session
```bash
tmux attach -t name
```

### Detach (keep running)
```
Press: Ctrl+B then D
```

### Kill Session
```bash
tmux kill-session -t name
```

---

## 📦 Installation

### First Time Setup
```bash
cd /notebooks
git clone <repo> video-translater
cd video-translater
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### Download Whisper Model
```bash
.venv/bin/python -c "import whisper; whisper.load_model('large-v3')"
```

---

## 🐛 Quick Fixes

### "No module named 'whisper'"
```bash
.venv/bin/pip install -U openai-whisper
```

### "FFmpeg not found"
```bash
# Ubuntu/Paperspace
sudo apt-get install ffmpeg
```

### "CUDA out of memory"
```bash
.venv/bin/python scripts/whisper_transcribe.py video.mp4 --device cpu
```

---

## 📁 File Locations

| Type | Location |
|------|----------|
| Videos | `input/` or `/storage/videos/` |
| Transcripts (Thai) | `workflow/01_transcripts/` |
| Translation batches | `workflow/02_for_translation/` |
| Translations (English) | `workflow/03_translated/` |
| Final SRT files | `workflow/04_final_srt/` |
| Checkpoints | `/storage/whisper_checkpoints/` |

---

## 🎯 Complete Workflow (Copy-Paste)

### Paperspace Production Workflow

```bash
# 1. Start tmux session
tmux new -s ep06

# 2. Transcribe with checkpoint
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/ep-06.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --checkpoint-interval 10 \
  --resume

# 3. Detach (Ctrl+B D)
# Can close browser now ✓

# 4. Later: Check progress
tmux attach -t ep06
# or
.venv/bin/python scripts/whisper_status.py --watch

# 5. Create translation batch
.venv/bin/python scripts/create_translation_batch.py \
  workflow/01_transcripts/ep-06_transcript.json

# 6. Translate (manual via Claude Pro)
# Open: workflow/02_for_translation/ep-06_batch.txt
# Save translated to: workflow/03_translated/ep-06_translated.txt

# 7. Generate English SRT
.venv/bin/python scripts/batch_to_srt.py \
  workflow/01_transcripts/ep-06_transcript.json \
  workflow/03_translated/ep-06_translated.txt

# 8. Download result
# File: workflow/04_final_srt/ep-06_english.srt
```

---

## 💡 Pro Tips

### 1. Always Use tmux on Paperspace
```bash
tmux new -s whisper  # Before any long task
```

### 2. Always Enable Checkpoints
```bash
--checkpoint-dir /storage/whisper_checkpoints --resume
```

### 3. Check Progress Without Entering tmux
```bash
.venv/bin/python scripts/whisper_status.py --watch
```

### 4. Split Long Videos
```bash
# 2-hour video → 4x 30-min chunks
# Faster + safer (can resume individual chunks)
```

### 5. Use Persistent Storage
```bash
/storage/  # Survives Paperspace restarts
/notebooks/  # Temporary, may be deleted
```

---

## 📞 Need More Details?

- **Full Guide**: [README.md](README.md)
- **Paperspace**: [docs/PAPERSPACE_GUIDE.md](docs/PAPERSPACE_GUIDE.md)
- **tmux Commands**: [docs/TMUX_CHEATSHEET.md](docs/TMUX_CHEATSHEET.md)
- **All Scripts**: [scripts/README.md](scripts/README.md)

---

**Last updated: October 17, 2025**
