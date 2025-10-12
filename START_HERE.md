# 🎬 Video Translater - START HERE

**Last Updated:** 2025-10-11
**Current Status:** ✅ Production Ready (Paperspace Verified)
**Purpose:** Thai Video → English Subtitles (Transcription + Translation)

---

## 🎯 โปรเจคนี้คืออะไร?

**Video Translater** คือระบบแปลงวิดีโอ Forex ภาษาไทยเป็นซับไตเติ้ลภาษาอังกฤษ

### ความสามารถหลัก:
- ✅ **Thai Audio Transcription** - ใช้ Whisper large-v3 (95%+ accuracy)
- ✅ **Context-Aware Translation** - ใช้ Claude/GPT (Thai → English)
- ✅ **Checkpoint/Resume System** - ต่องานได้เมื่อ Paperspace timeout
- ✅ **Cost Optimization** - ~$1.50-2.50 ต่อชั่วโมงวิดีโอ
- ✅ **Forex Terminology** - Dictionary สำหรับคำศัพท์ Forex 50+ terms
- ✅ **Thai Idioms** - รองรับสำนวนไทย 105+ expressions

---

## 📂 โครงสร้างโปรเจค

```
video-translater/
│
├── 📜 START_HERE.md              ← ไฟล์นี้! เริ่มต้นที่นี่
├── 📜 README.md                   ← Complete documentation
├── 📜 QUICKSTART.md               ← Fast reference guide
├── 📜 CLAUDE.md                   ← Technical handover (for AI)
├── 📜 SESSION_RESUME.md           ← Session continuity guide
│
├── 🔧 scripts/                    ← Main scripts
│   ├── whisper_transcribe.py     ← Transcribe audio (with checkpoints)
│   ├── whisper_status.py         ← Check progress
│   ├── merge_transcripts.py      ← Merge chunks
│   ├── create_translation_batch.py ← Prepare for translation
│   └── batch_to_srt.py           ← Convert to SRT
│
├── 📚 docs/                       ← Documentation
│   ├── PAPERSPACE_GUIDE.md       ← Paperspace workflow (1,600+ lines)
│   ├── TMUX_CHEATSHEET.md        ← tmux reference
│   └── UTILITIES_GUIDE.md        ← Utility scripts
│
├── 🧠 src/                        ← Core modules
│   ├── thai_transcriber.py       ← Thai-optimized Whisper
│   ├── translation_pipeline.py   ← Smart translation routing
│   └── context_analyzer.py       ← Two-pass context analysis
│
├── 📊 data/dictionaries/          ← External dictionaries
│   ├── forex_terms.json          ← 50+ Forex terms
│   ├── thai_idioms.json          ← 105 Thai idioms
│   └── thai_slang.json           ← 30 colloquialisms
│
└── 🔄 workflow/                   ← Working files
    ├── 01_transcripts/            ← Thai transcripts (JSON)
    ├── 02_for_translation/        ← Prepared batches
    ├── 03_translated/             ← Translated text
    └── 04_final_srt/              ← Final English SRT files
```

---

## 🔍 สถานะปัจจุบัน (2025-10-11)

### ✅ Production Features:

**Transcription System:**
- ✅ Whisper large-v3 model
- ✅ 95%+ accuracy for Thai speech
- ✅ GPU acceleration (8-10x faster)
- ✅ Checkpoint/Resume system
- ✅ Timestamp precision ±0.1s

**Translation System:**
- ✅ Context-aware translation
- ✅ Forex terminology preservation
- ✅ Thai idioms handling
- ✅ Two-pass context analysis
- ✅ Claude/GPT API support

**Paperspace Integration:**
- ✅ tmux session management
- ✅ Persistent checkpoint storage
- ✅ Auto-resume on timeout
- ✅ Progress monitoring

---

## 🚀 Quick Start (5 นาที)

### สำหรับ Paperspace (แนะนำ!):

```bash
# 1. เข้าไปที่โปรเจค
cd /notebooks/video-translater

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Start tmux session
tmux new -s whisper

# 4. Transcribe video (with checkpoint)
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/your-video.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --resume

# 5. Detach from tmux (let it run in background)
# Press: Ctrl+B then D

# 6. Check progress anytime
.venv/bin/python scripts/whisper_status.py --watch
```

### สำหรับ Local Development:

```bash
# 1. Setup
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 2. Configure API keys
cp .env.example .env
# Edit .env and add ANTHROPIC_API_KEY or OPENAI_API_KEY

# 3. Run transcription
.venv/bin/python scripts/whisper_transcribe.py input/video.mp4

# 4. Check output
cat workflow/01_transcripts/video_transcript.json
```

---

## 📚 เอกสารที่ต้องอ่าน

### อันดับความสำคัญ:

| # | ไฟล์ | ขนาด | จุดประสงค์ | ใครควรอ่าน |
|---|------|------|-----------|------------|
| 1️⃣ | **START_HERE.md** | - | ไฟล์นี้! เริ่มต้นที่นี่ | ทุกคน |
| 2️⃣ | **QUICKSTART.md** | 5.4K | Fast reference | Developer |
| 3️⃣ | **README.md** | 13K | Complete guide | Developer |
| 4️⃣ | **docs/PAPERSPACE_GUIDE.md** | 1,600+ lines | Production workflow | Paperspace users |
| 5️⃣ | **CLAUDE.md** | 71K | Technical handover | AI assistants |
| 6️⃣ | **SESSION_RESUME.md** | 4K | Session continuity | Claude Code |

---

## 🎯 Common Workflows

### Workflow 1: Simple Transcription (Local)

```bash
# Input: video.mp4
# Output: workflow/01_transcripts/video_transcript.json

.venv/bin/python scripts/whisper_transcribe.py video.mp4
```

**ใช้เวลา:** 1 hour video = 6-8 minutes (with GPU)

### Workflow 2: Paperspace Production

```bash
# Step 1: Start persistent session
tmux new -s ep06

# Step 2: Transcribe with checkpoint
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/ep-06.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --checkpoint-interval 10 \
  --resume

# Step 3: Detach (Ctrl+B D)
# → Work continues even if browser closes!

# Step 4: Check progress later
.venv/bin/python scripts/whisper_status.py --watch
```

**ใช้เวลา:** 1 hour video = 6-8 minutes

### Workflow 3: Long Video (Split & Merge)

```bash
# Chunk 1: 0-30 min
.venv/bin/python scripts/whisper_transcribe.py video.mp4 \
  --start-time 0 --end-time 1800 \
  -o workflow/01_transcripts/part1.json

# Chunk 2: 30-60 min
.venv/bin/python scripts/whisper_transcribe.py video.mp4 \
  --start-time 1800 --end-time 3600 \
  -o workflow/01_transcripts/part2.json

# Merge
.venv/bin/python scripts/merge_transcripts.py \
  workflow/01_transcripts/part*.json \
  -o workflow/01_transcripts/full.json
```

### Workflow 4: Translation Pipeline

```bash
# Step 1: Create translation batch
.venv/bin/python scripts/create_translation_batch.py \
  workflow/01_transcripts/video_transcript.json

# Output: workflow/02_for_translation/video_batch.txt

# Step 2: Translate
# → Use Claude Pro web interface or API
# → Save to workflow/03_translated/video_translated.txt

# Step 3: Convert to SRT
.venv/bin/python scripts/batch_to_srt.py \
  workflow/01_transcripts/video_transcript.json \
  workflow/03_translated/video_translated.txt
```

**Output:** `workflow/04_final_srt/video_english.srt`

---

## 🔧 Key Features อธิบายง่ายๆ

### 1. Checkpoint/Resume System
```python
# ปัญหา: Paperspace timeout → transcription หาย!
# Solution: Auto-checkpoint ทุก 10 segments
# → Resume จากจุดที่หยุดได้ทันที!

python scripts/whisper_transcribe.py video.mp4 \
  --checkpoint-dir /storage/checkpoints \
  --resume  # ← Magic!
```

### 2. Context-Aware Translation
```python
# ไม่ใช่แค่แปลตรงตัว แต่เข้าใจ context:
# - Two-pass analysis (หา topics ก่อน)
# - Forex terminology preservation
# - Thai idioms → English equivalent
# - Maintain conversation flow

# Result: Natural English, not word-by-word translation!
```

### 3. tmux Integration
```bash
# ปัญหา: ปิด browser → terminal ปิด → transcription หยุด!
# Solution: tmux session persistence

tmux new -s whisper        # Create session
python script.py           # Start work
Ctrl+B D                   # Detach
# → Close browser, work continues!

tmux attach -t whisper     # Reattach later
```

---

## 💰 Cost Estimation

| Task | Method | Cost (per hour of video) |
|------|--------|--------------------------|
| **Transcription** | Whisper (local) | **FREE** |
| **Translation** | GPT-3.5 Turbo | $1.50-2.00 |
| **Translation** | GPT-4 | $3.00-5.00 |
| **Translation** | Claude API | $0.50-1.00 |
| **Translation** | Claude Pro (manual) | **FREE** ($20/month unlimited) |

**แนะนำ:** Local Whisper + Claude Pro = Best quality at lowest cost

---

## 📊 Performance

### Transcription Speed:

| Hardware | Speed | Time for 1h video |
|----------|-------|-------------------|
| CPU | 1x realtime | 1 hour |
| GPU (T4) | 8-10x | 6-8 minutes |
| GPU (A100) | 15-20x | 3-4 minutes |

### Accuracy:

- **Thai Speech:** 95%+ word accuracy
- **Forex Terms:** 98%+ preservation
- **Timestamps:** ±0.1 second precision
- **Translation:** Context-aware, natural English

---

## 🐛 Troubleshooting

### Issue: "No module named 'whisper'"
```bash
.venv/bin/pip install -U openai-whisper
```

### Issue: "FFmpeg not found"
```bash
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# Mac:
brew install ffmpeg
```

### Issue: "CUDA out of memory"
```bash
# Use CPU
.venv/bin/python scripts/whisper_transcribe.py video.mp4 --device cpu

# Or smaller model
.venv/bin/python scripts/whisper_transcribe.py video.mp4 --model medium
```

### Issue: Transcription stopped midway
```bash
# Just resume!
.venv/bin/python scripts/whisper_transcribe.py video.mp4 --resume
```

### Issue: tmux session lost
```bash
# List all sessions
tmux ls

# Attach to your session
tmux attach -t whisper
```

---

## ✅ Common Mistakes (ต้องหลีกเลี่ยง!)

### ❌ Don't: Use system Python
```bash
python scripts/whisper_transcribe.py  # WRONG
```

### ✅ Do: Use virtual environment
```bash
.venv/bin/python scripts/whisper_transcribe.py  # CORRECT
```

---

### ❌ Don't: Run without tmux on Paperspace
```bash
# Terminal closes → transcription stops!
python scripts/whisper_transcribe.py video.mp4
```

### ✅ Do: Always use tmux
```bash
tmux new -s whisper
python scripts/whisper_transcribe.py video.mp4
# Press Ctrl+B D to detach
```

---

### ❌ Don't: Ignore checkpoints
```bash
# No checkpoint → lose progress!
python scripts/whisper_transcribe.py video.mp4
```

### ✅ Do: Always use checkpoints
```bash
python scripts/whisper_transcribe.py video.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --resume
```

---

## 💡 Pro Tips

1. **Always test with small file first** (1-2 minutes)
2. **Use tmux on Paperspace** (prevents timeout issues)
3. **Enable checkpoints** (can resume anytime)
4. **Use Claude Pro for translation** (best quality + free)
5. **Check transcripts before translating** (verify accuracy)

---

## 📈 Next Steps

### สำหรับคนใหม่:

1. ✅ อ่านไฟล์นี้แล้ว
2. ⏩ อ่าน **QUICKSTART.md** (fast reference)
3. ⏩ อ่าน **README.md** (complete guide)
4. ⏩ รัน Quick Start commands
5. ⏩ ถ้าใช้ Paperspace → อ่าน **docs/PAPERSPACE_GUIDE.md**

### สำหรับ Paperspace Users:

1. ⏩ อ่าน **docs/PAPERSPACE_GUIDE.md** (1,600+ lines)
2. ⏩ Setup tmux session
3. ⏩ Configure checkpoint directory
4. ⏩ Start transcription
5. ⏩ Monitor with `whisper_status.py`

### สำหรับ Production:

1. ⏩ Test with small video first
2. ⏩ Verify accuracy
3. ⏩ Setup checkpoint system
4. ⏩ Run full pipeline
5. ⏩ Verify SRT output

---

## 🆘 Need Help?

### Documentation:
- **This file** - Overview and quick start
- **QUICKSTART.md** - Fast reference
- **README.md** - Complete guide
- **docs/PAPERSPACE_GUIDE.md** - Production workflow
- **CLAUDE.md** - Technical details

### Common Commands:
```bash
# Transcribe
.venv/bin/python scripts/whisper_transcribe.py video.mp4

# Check status
.venv/bin/python scripts/whisper_status.py

# Watch progress
.venv/bin/python scripts/whisper_status.py --watch

# tmux
tmux ls                # List sessions
tmux attach -t name    # Attach
Ctrl+B D               # Detach
```

---

## 📊 Related Projects

โปรเจคนี้ทำงานคู่กับ:

- **quantum-sync-v5** - SRT → MP3 synthesis (timeline sync)
- **video-translation-platform** - Unified platform (combines both)

**Complete Video Localization Pipeline:**
```
Video (Thai)
  → [video-translater] → SRT (English)
  → [quantum-sync-v5] → MP3 (English voice)
  → [ffmpeg] → Video (English dub)
```

---

**Version:** Production
**Status:** ✅ Production Ready
**Last Updated:** 2025-10-11

**Made with ❤️ for Thai Forex content creators**

---

**🚀 Ready to start? Read QUICKSTART.md next!**
