# 🎬 Thai Video Translation Pipeline

> Complete system for transcribing Thai Forex videos and translating to English subtitles

---

## 📋 Quick Overview

This project provides:
- **Thai Audio Transcription** using Whisper large-v3 (95%+ accuracy)
- **Context-Aware Translation** using Claude/GPT (Thai → English)
- **Checkpoint/Resume System** for long videos and Paperspace sessions
- **Cost Optimization** (~$1.50-2.50 per hour of video)

---

## 🚀 Quick Start

### For Paperspace Users (Most Common)

```bash
# 1. Clone and setup
cd /notebooks
git clone <repo-url> video-translater
cd video-translater
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 2. Start a tmux session (prevents timeout)
tmux new -s whisper

# 3. Transcribe video
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/your-video.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --resume

# 4. Detach from tmux (work continues in background)
# Press: Ctrl+B then D

# 5. Check progress anytime
.venv/bin/python scripts/whisper_status.py --watch
```

**📖 Full Paperspace Guide**: [docs/PAPERSPACE_GUIDE.md](docs/PAPERSPACE_GUIDE.md)

### For Local Development

```bash
# 1. Setup
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 2. Configure API keys
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY or ANTHROPIC_API_KEY

# 3. Run full pipeline
.venv/bin/python scripts/run_pipeline.py input/video.mp4
```

---

## 📁 Project Structure

```
video-translater/
│
├── 📜 README.md                    ← You are here
├── 📜 QUICKSTART.md                ← Fast reference guide
├── 📜 CLAUDE.md                    ← Project handover doc (for Claude Code)
├── 📜 SESSION_RESUME.md            ← Session continuity guide
│
├── 🔧 scripts/                     ← Main scripts
│   ├── whisper_transcribe.py      ← Transcribe audio (with checkpoints)
│   ├── whisper_status.py          ← Check transcription progress
│   ├── merge_transcripts.py       ← Merge multiple transcript chunks
│   ├── create_translation_batch.py ← Prepare Thai text for translation
│   ├── batch_to_srt.py            ← Convert translations to SRT
│   └── README.md                  ← Scripts documentation
│
├── 📚 docs/                        ← Documentation
│   ├── PAPERSPACE_GUIDE.md        ← Detailed Paperspace workflow (1,600+ lines)
│   ├── TMUX_CHEATSHEET.md         ← tmux commands reference
│   └── UTILITIES_GUIDE.md         ← Utility scripts guide
│
├── 🧠 src/                         ← Core translation modules
│   ├── config.py                  ← Configuration management
│   ├── context_analyzer.py        ← Two-pass context analysis
│   ├── translation_pipeline.py    ← Smart translation routing
│   ├── thai_transcriber.py        ← Thai-optimized Whisper wrapper
│   └── README.md                  ← Core modules documentation
│
├── 📊 data/                        ← External dictionaries
│   └── dictionaries/
│       ├── forex_terms.json       ← 50+ Forex terms
│       ├── thai_idioms.json       ← 105 Thai idioms
│       └── thai_slang.json        ← 30 colloquialisms
│
├── 🔄 workflow/                    ← Working files
│   ├── 01_transcripts/            ← Thai transcripts (JSON)
│   ├── 02_for_translation/        ← Prepared batches
│   ├── 03_translated/             ← Translated text
│   └── 04_final_srt/              ← Final English SRT files
│
├── 📥 input/                       ← Input videos
├── 📤 output/                      ← Output files
└── 🐍 .venv/                       ← Python virtual environment
```

---

## 🎯 Common Workflows

### 1. Transcribe Video (Simple)

```bash
.venv/bin/python scripts/whisper_transcribe.py video.mp4
```

**Output**: `workflow/01_transcripts/video_transcript.json`

### 2. Transcribe with Checkpoint (Paperspace)

```bash
# Start in tmux
tmux new -s whisper

# Transcribe with resume capability
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/video.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --resume

# Detach: Ctrl+B D
# Check status: python scripts/whisper_status.py
```

### 3. Transcribe Long Video (Split into Chunks)

```bash
# Chunk 1: 0-30 minutes
.venv/bin/python scripts/whisper_transcribe.py video.mp4 \
  --start-time 0 --end-time 1800 \
  -o workflow/01_transcripts/video_part1.json

# Chunk 2: 30-60 minutes
.venv/bin/python scripts/whisper_transcribe.py video.mp4 \
  --start-time 1800 --end-time 3600 \
  -o workflow/01_transcripts/video_part2.json

# Merge chunks
.venv/bin/python scripts/merge_transcripts.py \
  workflow/01_transcripts/video_part*.json \
  -o workflow/01_transcripts/video_full.json
```

### 4. Translate to English

```bash
# Step 1: Create translation batch
.venv/bin/python scripts/create_translation_batch.py \
  workflow/01_transcripts/video_transcript.json

# Output: workflow/02_for_translation/video_batch.txt

# Step 2: Translate (manual via Claude Pro or API)
# → Save to workflow/03_translated/video_translated.txt

# Step 3: Convert to SRT
.venv/bin/python scripts/batch_to_srt.py \
  workflow/01_transcripts/video_transcript.json \
  workflow/03_translated/video_translated.txt
```

---

## 📖 Documentation

### Getting Started
- **[QUICKSTART.md](QUICKSTART.md)** - Fast reference for common tasks
- **[docs/PAPERSPACE_GUIDE.md](docs/PAPERSPACE_GUIDE.md)** - Complete Paperspace workflow

### Reference Guides
- **[docs/TMUX_CHEATSHEET.md](docs/TMUX_CHEATSHEET.md)** - tmux commands
- **[scripts/README.md](scripts/README.md)** - All scripts explained
- **[src/README.md](src/README.md)** - Core modules documentation

### For Developers
- **[CLAUDE.md](CLAUDE.md)** - Complete project handover document
- **[SESSION_RESUME.md](SESSION_RESUME.md)** - Session continuity protocol

---

## 🔧 Installation

### System Requirements

- **Python**: 3.8+
- **FFmpeg**: For audio processing
- **GPU**: Optional but recommended (10x faster transcription)

### Install Dependencies

```bash
# Create virtual environment
python3 -m venv .venv

# Activate (Linux/Mac)
source .venv/bin/activate

# Or on Windows
.venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Key Dependencies

```
openai-whisper      # Thai transcription
torch               # ML framework
ffmpeg-python       # Audio processing
openai>=1.0.0       # Translation API (optional)
anthropic           # Claude API (optional)
tqdm                # Progress bars
```

---

## ⚙️ Configuration

### API Keys (Optional - for translation)

```bash
# Create .env file
cat > .env << EOF
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-claude-key
EOF
```

### Whisper Model Download

```bash
# Download large-v3 model (first time only, ~3GB)
.venv/bin/python -c "
import whisper
whisper.load_model('large-v3')
"
```

---

## 💰 Cost Estimation

| Task | Method | Cost |
|------|--------|------|
| **Transcription** | Whisper (local) | **FREE** |
| **Translation** | GPT-3.5 Turbo | $1.50-2.00/hour |
| **Translation** | GPT-4 | $3.00-5.00/hour |
| **Translation** | Claude API | $0.50-1.00/hour |
| **Translation** | Claude Pro (manual) | **FREE** ($20/month subscription) |

**Recommended**: Use local Whisper + Claude Pro for best quality at lowest cost.

---

## 🎓 Examples

### Example 1: Quick Test

```bash
# Transcribe 1-minute sample
.venv/bin/python scripts/whisper_transcribe.py sample.mp4

# Check output
cat workflow/01_transcripts/sample_transcript.json
```

### Example 2: Production Workflow (Paperspace)

```bash
# Step 1: Start persistent session
tmux new -s ep06

# Step 2: Transcribe with checkpoint
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/ep-06.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --checkpoint-interval 10 \
  --resume

# Step 3: Detach and close browser
# Press: Ctrl+B then D
# → Can safely close browser, transcription continues

# Step 4: Check progress (later)
tmux attach -t ep06
# or
.venv/bin/python scripts/whisper_status.py --watch
```

### Example 3: Recover from Timeout

```bash
# Your session timed out? No problem!

# 1. Check if transcription exists
.venv/bin/python scripts/whisper_status.py

# 2. Resume from checkpoint
tmux new -s resume
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/ep-06.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --resume

# → Continues from where it stopped!
```

---

## 🐛 Troubleshooting

### Issue: "No module named 'whisper'"

```bash
# Install Whisper
.venv/bin/pip install -U openai-whisper
```

### Issue: "FFmpeg not found"

```bash
# Install FFmpeg
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# Mac:
brew install ffmpeg
```

### Issue: "CUDA out of memory"

```bash
# Use CPU instead
.venv/bin/python scripts/whisper_transcribe.py video.mp4 --device cpu

# Or use smaller model
.venv/bin/python scripts/whisper_transcribe.py video.mp4 --model medium
```

### Issue: Transcription stopped midway

```bash
# Just resume!
.venv/bin/python scripts/whisper_transcribe.py video.mp4 --resume
```

---

## 🚨 Common Mistakes

❌ **Don't**: Use system Python
```bash
python scripts/whisper_transcribe.py  # WRONG
```

✅ **Do**: Use virtual environment
```bash
.venv/bin/python scripts/whisper_transcribe.py  # CORRECT
```

---

❌ **Don't**: Transcribe in Paperspace terminal without tmux
```bash
# Terminal closes → transcription stops!
python scripts/whisper_transcribe.py video.mp4
```

✅ **Do**: Use tmux for background execution
```bash
tmux new -s whisper
python scripts/whisper_transcribe.py video.mp4
# Press Ctrl+B D to detach
```

---

❌ **Don't**: Ignore checkpoints
```bash
# No checkpoint → lose progress on timeout!
python scripts/whisper_transcribe.py video.mp4
```

✅ **Do**: Always use checkpoints on Paperspace
```bash
python scripts/whisper_transcribe.py video.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --resume
```

---

## 📊 Performance

### Transcription Speed

| Hardware | Model | Speed |
|----------|-------|-------|
| **CPU** | large-v3 | 1x realtime (1 hour = 1 hour) |
| **GPU (T4)** | large-v3 | 8-10x realtime (1 hour = 6-8 minutes) |
| **GPU (A100)** | large-v3 | 15-20x realtime (1 hour = 3-4 minutes) |

### Accuracy

- **Thai Speech**: 95%+ word accuracy
- **Forex Terms**: 98%+ term preservation
- **Timestamps**: ±0.1 second precision

---

## 🤝 Contributing

This project uses:
- **Black** for code formatting
- **pytest** for testing
- **Type hints** for documentation

```bash
# Run tests
.venv/bin/pytest tests/

# Format code
.venv/bin/black src/ scripts/
```

---

## 📜 License

MIT License - See LICENSE file for details

---

## 📞 Support

### Documentation
- [Full Documentation](docs/)
- [Paperspace Guide](docs/PAPERSPACE_GUIDE.md)
- [Scripts Reference](scripts/README.md)

### Issues
- Check [Troubleshooting](#-troubleshooting) section
- Review error logs in `.cache/logs/`
- Test with mock mode: `Config(mode=ConfigMode.MOCK)`

---

## ✅ Quick Reference

### Most Used Commands

```bash
# Transcribe (simple)
.venv/bin/python scripts/whisper_transcribe.py video.mp4

# Transcribe (with checkpoint)
.venv/bin/python scripts/whisper_transcribe.py video.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints --resume

# Check status
.venv/bin/python scripts/whisper_status.py

# Watch progress (auto-refresh)
.venv/bin/python scripts/whisper_status.py --watch

# Merge transcripts
.venv/bin/python scripts/merge_transcripts.py part*.json -o full.json

# tmux basics
tmux new -s name        # Create session
tmux ls                 # List sessions
tmux attach -t name     # Attach to session
Ctrl+B D                # Detach from session
```

---

**Made with ❤️ for Thai Forex content creators**

*Last updated: October 2025*
