# 📂 Workflow Data Directory

> **Important**: This directory contains working files and may include large transcript files (27MB+)

---

## 📁 Directory Structure

```
workflow/
├── 01_transcripts/          ← Thai transcripts (JSON) - 27MB
├── 02_for_translation/      ← Prepared batches (TXT) - 696KB
├── 03_translated/           ← English translations (TXT) - 392KB
├── 04_subtitles/            ← Final SRT files (SRT) - 200KB
├── 04_final_srt/            ← Alternate SRT location - 32KB
├── 04_srt/                  ← Alternate SRT location - 224KB
└── .translation_checkpoint* ← Session checkpoints (hidden)
```

---

## ⚠️ Large Files Notice

### Files NOT included in Git:

**Transcripts (27MB):**
- `01_transcripts/*.json` - Original Thai transcripts

These files are excluded from Git to keep the repository small.

**Where to get transcripts:**
1. **Download from**: `/mnt/d/Downloads/claude-code-แปลSS1/`
2. **Or transcribe your own**: See [scripts/whisper_transcribe.py](../scripts/whisper_transcribe.py)

---

## ✅ Files Included in Git

### Small working files included:
- ✅ `03_translated/*.txt` - Translated English text (~392KB)
- ✅ `04_subtitles/*.srt` - Final SRT subtitles (~200KB)
- ✅ `.translation_checkpoint*.txt` - Session checkpoints
- ✅ `.context_summary*.txt` - Analysis summaries
- ✅ `README.md` - This file

---

## 🚀 Quick Setup

### First time setup:

```bash
# 1. Clone repository
git clone https://github.com/Useforclaude/vdo-translater.git
cd vdo-translater

# 2. Create workflow directories
mkdir -p workflow/{01_transcripts,02_for_translation,03_translated,04_subtitles}

# 3. Copy your transcript files
cp /path/to/transcripts/*.json workflow/01_transcripts/

# 4. Start translating!
.venv/bin/python scripts/create_translation_batch.py \
  workflow/01_transcripts/your-file_transcript.json
```

---

## 📊 Completed Episodes (Included)

**Available translated files:**

| Episode | Status | Files |
|---------|--------|-------|
| EP-01 | ✅ Complete | ep-01-19-12-24_translated.txt |
| EP-03 | ✅ Complete | ep-03-061024_translated.txt |
| EP-04 | ✅ Complete | ep-04-081024_translated.txt |
| EP-05 | ✅ Complete | EP-05-new-clip_translated.txt |
| EP-06 | ✅ Complete | EP-06-sub-12102024_translated.txt |
| EP-08 | ✅ Complete | EP08_translated.txt |

**Total:** 2,400+ segments translated (95-100% quality)

---

## 🔄 Checkpoint Files

Session continuity files (included for resume capability):

- `.translation_checkpoint.txt` - Main checkpoint
- `.translation_checkpoint_EP-*.txt` - Per-episode checkpoints
- `.context_summary_EP-*.txt` - Context analysis per episode

**Purpose:** Allow resuming translation work after disconnect/restart

---

## 💾 Storage Recommendations

### Local Development:
```
workflow/
  01_transcripts/    → Keep locally (27MB)
  02_for_translation → Can regenerate
  03_translated/     → Keep (work product!)
  04_subtitles/      → Keep (final output!)
```

### Production (Paperspace):
```
/storage/
  whisper_checkpoints/  → Transcription checkpoints
  videos/               → Source videos

/notebooks/video-translater/workflow/
  01_transcripts/       → Download or transcribe here
  03_translated/        → Generated translations
  04_subtitles/         → Final SRT files
```

---

## 📥 Download Transcripts

**Option 1: From source location**
```bash
# If you have access to original location
cp /mnt/d/Downloads/claude-code-แปลSS1/*_transcript.json \
   workflow/01_transcripts/
```

**Option 2: Transcribe yourself**
```bash
# Transcribe video to create transcript
.venv/bin/python scripts/whisper_transcribe.py \
  /path/to/video.mp4 \
  -o workflow/01_transcripts/video_transcript.json
```

**Option 3: Use checkpoint system**
```bash
# For long videos, use checkpoint/resume
.venv/bin/python scripts/whisper_transcribe.py \
  video.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --resume
```

---

## 🗂️ File Naming Convention

```
Episode naming:
- ep-01-19-12-24_transcript.json → 01_transcripts/
- ep-01-19-12-24_batch.txt → 02_for_translation/
- ep-01-19-12-24_translated.txt → 03_translated/
- ep-01-19-12-24_english.srt → 04_subtitles/

Checkpoint naming:
- .translation_checkpoint.txt (main)
- .translation_checkpoint_EP-01.txt (per episode)
- .context_summary_EP-01.txt (analysis)
```

---

## 🔍 What's in Each Directory?

### 01_transcripts/
```json
// Thai transcript with timestamps
{
  "segments": [
    {
      "id": 1,
      "start": 0.0,
      "end": 3.5,
      "text": "สวัสดีครับ วันนี้เราจะมาเรียนเรื่อง..."
    }
  ]
}
```

### 02_for_translation/
```
Prepared text for translation (with segment markers):

[Segment 1] 0.0 → 3.5
สวัสดีครับ วันนี้เราจะมาเรียนเรื่อง...

[Segment 2] 3.5 → 7.2
เรื่องของ Price Action นะครับ
```

### 03_translated/
```
English translations (with segment markers):

[Segment 1] 0.0 → 3.5
Hello everyone, today we'll learn about...

[Segment 2] 3.5 → 7.2
Price Action trading
```

### 04_subtitles/
```srt
// Standard SRT format
1
00:00:00,000 --> 00:00:03,500
Hello everyone, today we'll learn about...

2
00:00:03,500 --> 00:00:07,200
Price Action trading
```

---

## 💡 Tips

1. **Don't commit large transcripts to Git** (use .gitignore)
2. **Do commit translations and SRT files** (work products)
3. **Keep checkpoints** (enable session continuity)
4. **Use descriptive filenames** (ep-XX-DDMMYYYY format)
5. **Backup `/mnt/d/Downloads/` location** (source transcripts)

---

## 🚨 Important Notes

- **Transcripts are excluded from Git** (27MB is too large)
- **Translated files ARE included** (these are your work!)
- **SRT files ARE included** (final output)
- **Checkpoints ARE included** (enable resume)
- **Download transcripts separately** or transcribe yourself

---

**Need help?** See main [README.md](../README.md) or [QUICKSTART.md](../QUICKSTART.md)
