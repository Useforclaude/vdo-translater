# ⚡ Paperspace Quick Start Guide

> Fast commands for video download and transcription in Paperspace

---

## 🎯 Quick Workflow (3 Steps)

### Step 1: Download Videos from Google Drive

```bash
# Download all videos
bash scripts/download_videos.sh

# Or download specific video (fuzzy matching)
bash scripts/download_videos.sh ep01        # Downloads ep01.mp4
bash scripts/download_videos.sh 01          # Fuzzy match → ep01
bash scripts/download_videos.sh part1       # Fuzzy match → ep-04-part-1
bash scripts/download_videos.sh ep05        # Downloads SS-1-5-ep05.mp4

# List available videos
bash scripts/download_videos.sh list
```

**Videos will be saved to:** `/storage/videos/`

---

### Step 2: Transcribe with Whisper (in tmux)

```bash
# Start transcription (auto-creates tmux session)
bash scripts/paperspace_transcribe.sh ep01

# Or fuzzy match
bash scripts/paperspace_transcribe.sh 01     # Matches ep01
bash scripts/paperspace_transcribe.sh part1  # Matches ep-04-part-1
```

**Features:**
- ✅ Runs in tmux (survives disconnect)
- ✅ Auto-checkpoint every 10 segments
- ✅ Auto-resume on restart
- ✅ GPU acceleration (if available)

**Session will auto-attach. To detach:** Press `Ctrl+B` then `D`

---

### Step 3: Monitor Progress (Optional)

```bash
# Watch progress (auto-refresh)
.venv/bin/python scripts/whisper_status.py --watch

# Or check manually
.venv/bin/python scripts/whisper_status.py
```

---

## 📋 Available Videos

| Fuzzy Key | Full Filename | Google Drive ID |
|-----------|---------------|-----------------|
| `ep01` or `01` | ep01.mp4 | 1G5IZEQhYAZLdVB6RIXjbofmWyG-BxDIL |
| `ep02` or `02` | ep02.mp4 | 1gQB_nh0WV5Ec_LgUQkKy1a3cRQfFf31D |
| `ep03` or `03` | Ep03.mp4 | 1N59eoYoMuu2wC7_sM-gihHiSxILfDv3j |
| `ep04-part1` or `part1` | ep-04-part-1.mp4 | 1Lx0Me6TshvxsK_Uck7RddawnEB4pKyjT |
| `ep04-part2` or `part2` | ep-04-part-2.mp4 | 10Q4UgtQlDQw1QzJfdgD6KVQjqnxTXyHt |
| `ep05` or `05` | SS-1-5-ep05.mp4 | 1PZUMnOfpOqwUEE9b07H0blEyM-1HezGu |

---

## 🔧 tmux Commands

### Basic tmux operations:

```bash
# List all sessions
tmux ls

# Attach to session
tmux attach -t whisper-ep01

# Detach from session (while inside)
Ctrl+B then D

# Kill session
tmux kill-session -t whisper-ep01

# Kill all sessions
tmux kill-server
```

---

## 📂 File Locations

```
/storage/
├── videos/                      ← Downloaded videos
│   ├── ep01.mp4
│   ├── ep02.mp4
│   └── ...
└── whisper_checkpoints/         ← Transcription checkpoints
    ├── ep01_checkpoint_0.json
    └── ...

/notebooks/video-translater/
└── workflow/
    └── 01_transcripts/          ← Completed transcripts
        ├── ep01_transcript.json
        └── ...
```

---

## 🚀 Complete Example Workflow

```bash
# 1. Connect to Paperspace
ssh paperspace@xxx.xxx.xxx.xxx

# 2. Navigate to project
cd /notebooks/video-translater

# 3. Download video
bash scripts/download_videos.sh ep01

# 4. Start transcription (creates tmux session)
bash scripts/paperspace_transcribe.sh ep01

# → Session auto-attaches
# → Work is running in background

# 5. Detach from session
# Press: Ctrl+B then D

# 6. Close SSH (transcription continues!)
exit

# 7. Later: Reconnect and check progress
ssh paperspace@xxx.xxx.xxx.xxx
cd /notebooks/video-translater
tmux attach -t whisper-ep01

# Or monitor without attaching
.venv/bin/python scripts/whisper_status.py --watch
```

---

## 💡 Pro Tips

### 1. Download Multiple Videos in Background
```bash
# Download all videos in tmux
tmux new -s download
bash scripts/download_videos.sh
# Ctrl+B D to detach
```

### 2. Transcribe Multiple Videos Sequentially
```bash
# Create script
cat > transcribe_all.sh << 'EOF'
#!/bin/bash
for VIDEO in ep01 ep02 ep03; do
    bash scripts/paperspace_transcribe.sh $VIDEO
    # Wait for completion before next
    sleep 10
done
EOF

chmod +x transcribe_all.sh

# Run in tmux
tmux new -s transcribe-all
./transcribe_all.sh
```

### 3. Check Disk Space
```bash
df -h /storage
du -sh /storage/videos/
```

### 4. Resume After Disconnect
```bash
# Your work is still running!
# Just reattach:
tmux ls                          # Find your session
tmux attach -t whisper-ep01      # Reattach
```

---

## ⚠️ Troubleshooting

### Issue: "gdown not found"
```bash
pip install gdown
# Or use .venv
.venv/bin/pip install gdown
```

### Issue: "tmux session already exists"
```bash
# Kill old session
tmux kill-session -t whisper-ep01

# Or attach to existing
tmux attach -t whisper-ep01
```

### Issue: "Out of storage space"
```bash
# Check space
df -h /storage

# Delete old videos
rm /storage/videos/ep01.mp4

# Delete old checkpoints
rm -rf /storage/whisper_checkpoints/ep01*
```

### Issue: "Transcription stopped"
```bash
# Check if session still running
tmux ls

# Attach and check logs
tmux attach -t whisper-ep01

# Restart if needed (will resume from checkpoint!)
bash scripts/paperspace_transcribe.sh ep01
```

---

## 📊 Expected Performance

| Hardware | Speed | Time for 60-min video |
|----------|-------|----------------------|
| CPU only | 1x | ~60 minutes |
| GPU (T4) | 8-10x | ~6-8 minutes |
| GPU (A100) | 15-20x | ~3-4 minutes |

**Checkpoint interval:** Every 10 segments (~30-60 seconds)

---

## ✅ Verification Commands

```bash
# Check downloaded videos
ls -lh /storage/videos/

# Check transcripts
ls -lh workflow/01_transcripts/

# Check checkpoints
ls -lh /storage/whisper_checkpoints/

# Count segments in transcript
cat workflow/01_transcripts/ep01_transcript.json | jq '.segments | length'

# Verify JSON format
cat workflow/01_transcripts/ep01_transcript.json | jq . | head -50
```

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Download video | `bash scripts/download_videos.sh ep01` |
| Start transcription | `bash scripts/paperspace_transcribe.sh ep01` |
| Detach from tmux | `Ctrl+B` then `D` |
| List tmux sessions | `tmux ls` |
| Reattach to session | `tmux attach -t whisper-ep01` |
| Monitor progress | `.venv/bin/python scripts/whisper_status.py --watch` |
| Check files | `ls -lh /storage/videos/` |
| Kill session | `tmux kill-session -t whisper-ep01` |

---

**Ready to transcribe!** 🚀

**Next:** See [docs/PAPERSPACE_GUIDE.md](docs/PAPERSPACE_GUIDE.md) for full documentation
