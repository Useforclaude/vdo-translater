# ⚡ SS1.5 Quick Commands - Copy & Paste Ready!

**Date:** 2025-10-17
**Purpose:** Ultra-fast command reference for Paperspace SS1.5 workflow

---

## 🚀 Complete Workflow (3 Commands)

### 1️⃣ Download All Videos (One Command)

```bash
cd /notebooks && \
git clone https://github.com/Useforclaude/vdo-translater.git video-translater 2>/dev/null || cd video-translater && \
git pull && \
bash paperspace/download_ss1.5_videos.sh
```

**What this does:**
- Clones/updates project
- Runs download script
- Downloads all 6 SS1.5 videos to `/notebooks/thai-whisper/videos/`

---

### 2️⃣ Transcribe All Videos (One Command)

```bash
tmux new -s ss1.5 "cd /notebooks/video-translater && bash paperspace/transcribe_ss1.5_all.sh"
```

**What this does:**
- Creates tmux session `ss1.5`
- Transcribes all 6 videos
- Merges EP-04 parts automatically
- Runs in background (safe from timeout!)

**To detach:** Press `Ctrl+B` then `D`
**To reattach:** `tmux attach -t ss1.5`

---

### 3️⃣ Monitor Progress (Real-time)

```bash
cd /notebooks/video-translater && \
.venv/bin/python scripts/whisper_status.py --watch
```

---

## 📥 Download Only (Detailed)

### Method A: Automated Script (Recommended)

```bash
# Clone/update project
cd /notebooks
git clone https://github.com/Useforclaude/vdo-translater.git video-translater 2>/dev/null || cd video-translater && git pull

# Run download script
bash paperspace/download_ss1.5_videos.sh
```

### Method B: Manual (One-by-One)

```bash
# Setup
cd /notebooks
mkdir -p thai-whisper/videos
cd thai-whisper/videos
pip install -U gdown

# Download
gdown 1G5IZEQhYAZLdVB6RIXjbofmWyG-BxDIL -O SS-1.5-ep01.mp4  # EP-01
gdown 1gQB_nh0WV5Ec_LgUQkKy1a3cRQfFf31D -O SS-1.5-ep02.mp4  # EP-02
gdown 1N59eoYoMuu2wC7_sM-gihHiSxILfDv3j -O SS-1.5-Ep03.mp4  # EP-03
gdown 1Lx0Me6TshvxsK_Uck7RddawnEB4pKyjT -O SS1.5-ep-04-part-1.mp4  # EP-04 Part 1
gdown 10Q4UgtQlDQw1QzJfdgD6KVQjqnxTXyHt -O SS-1.5-ep-04-part-2.mp4  # EP-04 Part 2
gdown 1PZUMnOfpOqwUEE9b07H0blEyM-1HezGu -O SS-1.5-ep05.mp4  # EP-05
```

---

## 🎙️ Transcribe Only

### Method A: Automated Script (All at Once)

```bash
cd /notebooks/video-translater

# In tmux (recommended)
tmux new -s ss1.5
bash paperspace/transcribe_ss1.5_all.sh
# Press Ctrl+B D to detach

# Or without tmux (not recommended - will stop if connection lost)
bash paperspace/transcribe_ss1.5_all.sh
```

### Method B: One Episode at a Time

```bash
cd /notebooks/video-translater

# EP-01
.venv/bin/python scripts/whisper_transcribe.py \
  /notebooks/thai-whisper/videos/SS-1.5-ep01.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --resume

# EP-02
.venv/bin/python scripts/whisper_transcribe.py \
  /notebooks/thai-whisper/videos/SS-1.5-ep02.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --resume

# ... (repeat for other episodes)
```

---

## 🔍 Check & Verify

### Check Downloads
```bash
ls -lh /notebooks/thai-whisper/videos/SS*.mp4
du -sh /notebooks/thai-whisper/videos/
```

### Check Transcripts
```bash
ls -lh /notebooks/video-translater/workflow/01_transcripts/SS-1.5-*.json
du -sh /notebooks/video-translater/workflow/01_transcripts/
```

### Monitor Transcription
```bash
# Watch progress (auto-refresh)
cd /notebooks/video-translater
.venv/bin/python scripts/whisper_status.py --watch

# Check once
.venv/bin/python scripts/whisper_status.py
```

### Check tmux Session
```bash
tmux ls                    # List all sessions
tmux attach -t ss1.5       # Attach to ss1.5 session
# Ctrl+B D to detach
```

---

## 🔄 Resume After Interruption

### If Download Stopped
```bash
# gdown auto-resumes, just run again
cd /notebooks/thai-whisper/videos
gdown [FILE_ID] -O output.mp4
```

### If Transcription Stopped
```bash
cd /notebooks/video-translater

# Just add --resume flag
.venv/bin/python scripts/whisper_transcribe.py \
  /notebooks/thai-whisper/videos/SS-1.5-ep01.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --resume  # ← This will continue from last checkpoint
```

---

## 📊 File Locations Quick Reference

| Type | Location |
|------|----------|
| **Videos** | `/notebooks/thai-whisper/videos/` |
| **Transcripts (output)** | `/notebooks/video-translater/workflow/01_transcripts/` |
| **Checkpoints** | `/storage/whisper_checkpoints/` |
| **Scripts** | `/notebooks/video-translater/paperspace/` |
| **Project** | `/notebooks/video-translater/` |

---

## 🐛 Quick Fixes

### gdown not found
```bash
pip install -U gdown
```

### No space left
```bash
# Check space
df -h /notebooks

# Clear cache
rm -rf /notebooks/.cache/*
```

### tmux session lost
```bash
# List sessions
tmux ls

# Attach to existing
tmux attach -t ss1.5
```

### Python module not found
```bash
cd /notebooks/video-translater
.venv/bin/pip install -r requirements.txt
```

---

## ⏱️ Time Estimates

| Task | Duration |
|------|----------|
| Download 6 videos | ~10-30 min (depends on internet speed) |
| Transcribe 6 videos (with GPU) | ~20-40 min |
| Merge EP-04 parts | ~10 seconds |
| **Total** | **~30-70 minutes** |

---

## ✅ Success Criteria

After completion, you should have:

```
/notebooks/thai-whisper/videos/
├── SS-1.5-ep01.mp4
├── SS-1.5-ep02.mp4
├── SS-1.5-Ep03.mp4
├── SS1.5-ep-04-part-1.mp4
├── SS-1.5-ep-04-part-2.mp4
└── SS-1.5-ep05.mp4

/notebooks/video-translater/workflow/01_transcripts/
├── SS-1.5-ep01_transcript.json
├── SS-1.5-ep02_transcript.json
├── SS-1.5-ep03_transcript.json
├── SS-1.5-ep04_transcript.json  ← Merged from part1+part2
└── SS-1.5-ep05_transcript.json
```

**Total:** 6 videos → 5 transcripts (EP-04 merged)

---

## 💡 Pro Tips

1. **Always use tmux** for long-running tasks
2. **Use --resume flag** for checkpoints
3. **Don't close browser** while downloading (unless using tmux)
4. **Check disk space** before starting (`df -h`)
5. **Stop machine when done** to save costs!

---

## 📞 Need More Details?

See complete guide: `paperspace/SS1.5_DOWNLOAD_GUIDE.md`

---

**Ready? Copy the 3-command workflow above and paste into Paperspace! 🚀**

**Created:** 2025-10-17
