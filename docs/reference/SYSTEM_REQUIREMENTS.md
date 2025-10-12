# 💻 System Requirements & Performance Analysis

**Date**: 2025-10-03
**Status**: Production Ready

---

## 📊 Resource Usage Breakdown

### 🔵 **LIGHT Components** (ทำงานบนเครื่องปกติได้)

| Component | RAM | CPU | Disk | Speed |
|-----------|-----|-----|------|-------|
| **Context Analyzer** | ~100 MB | Low | 5 MB | Very Fast |
| **Translation Pipeline** | ~200 MB | Low | - | Fast |
| **Dictionary System** | ~10 MB | Low | 2 MB | Instant |
| **Idiom Detection** | ~50 MB | Low | - | Fast |
| **SRT Generation** | ~50 MB | Low | - | Instant |

**Total Light**: **~500 MB RAM**, CPU minimal

✅ **ใช้สเปคน้อยมาก เครื่องธรรมดารันได้สบาย**

---

### 🔴 **HEAVY Component** (ต้องการสเปคสูง)

| Component | RAM | CPU | Disk | GPU | Speed |
|-----------|-----|-----|------|-----|-------|
| **Whisper large-v3** | **10-12 GB** | High | **6 GB** | Optional | 1-2x realtime |

**Detail:**
- Model Size: **6 GB** (download once)
- Runtime RAM: **10-12 GB** (during transcription)
- CPU: High usage (แนะนำ 4+ cores)
- GPU: **Optional** but **10x faster** with CUDA

⚠️ **Whisper ใช้สเปคเยอะ! แนะนำใช้ Colab**

---

## 🎯 Recommended Deployment Strategy

### ✅ **BEST APPROACH: Hybrid** (แนะนำที่สุด!)

**แยกงานตามความหนัก:**

```
┌─────────────────────────────────────────────┐
│  HEAVY WORK → Google Colab (FREE GPU)      │
│  ├─ Whisper Transcription (10 GB RAM)      │
│  └─ Output: Thai SRT + JSON                │
└─────────────────────────────────────────────┘
                    ↓ Download
┌─────────────────────────────────────────────┐
│  LIGHT WORK → Local Machine                │
│  ├─ Context Analysis (100 MB)              │
│  ├─ Translation (200 MB)                    │
│  ├─ Idiom Detection (50 MB)                │
│  └─ English SRT Generation                 │
└─────────────────────────────────────────────┘
```

**ประโยชน์:**
- ✅ Colab ให้ GPU **ฟรี** (NVIDIA T4/P100)
- ✅ Whisper เร็วขึ้น **10-15 เท่า** กับ GPU
- ✅ Local แปลได้เร็ว ไม่ต้องรอ Colab
- ✅ ประหยัดค่า API

---

## 💰 Cost Comparison

### Option A: All Local (เครื่องแรงพอ)
```
Requirements:
- RAM: 16 GB+ (สำหรับ Whisper)
- CPU: 8+ cores
- GPU: Optional (แต่ช้ามาก ถ้าไม่มี)

Cost: $0
Speed: 1-2x realtime (CPU only)
      10-20x realtime (with GPU)
```

### Option B: All Colab (ไม่ต้องติดตั้งอะไร)
```
Requirements:
- Google account
- Internet connection

Cost: $0 (Free tier)
      $10/month (Colab Pro - faster)
Speed: 10-20x realtime (GPU T4)
       30-50x realtime (Colab Pro - A100)
```

### Option C: Hybrid (แนะนำ!)
```
Requirements:
- Colab: Whisper only
- Local: RAM 4 GB+, CPU normal

Cost: $0 (Whisper free on Colab)
      API cost for translation only
Speed: Best of both worlds!
```

---

## 🚀 Step-by-Step Guide for Colab

### **Part 1: Whisper Transcription on Colab**

**Create Colab Notebook:**

```python
# ===== CELL 1: Install =====
!pip install openai-whisper

# ===== CELL 2: Upload Video =====
from google.colab import files
uploaded = files.upload()  # Upload your video
video_file = list(uploaded.keys())[0]

# ===== CELL 3: Transcribe =====
import whisper
import json

# Load model (first time downloads 6 GB)
print("Loading Whisper large-v3...")
model = whisper.load_model("large-v3")

# Transcribe
print("Transcribing...")
result = model.transcribe(
    video_file,
    language="th",
    task="transcribe",
    word_timestamps=True,
    temperature=(0.0, 0.2, 0.4, 0.6, 0.8),
    beam_size=5,
    best_of=5
)

# Save results
output_file = video_file.replace('.mp4', '_transcript.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"✓ Transcription saved: {output_file}")

# ===== CELL 4: Download Results =====
from google.colab import files
files.download(output_file)
```

**Time:**
- Upload video: 1-5 min (depends on size)
- First run: 5 min (download model)
- Transcribe: **10-20x realtime** (1 hour video = 3-6 minutes)
- Download: 1 min

**Total:** ~10 minutes for 1 hour video (first time)

---

### **Part 2: Translation on Local Machine**

**After downloading transcript from Colab:**

```bash
# 1. Put transcript in project folder
mv ~/Downloads/video_transcript.json input/

# 2. Run translation pipeline
.venv/bin/python src/translator_only.py \
  input/video_transcript.json \
  -o output/

# Output:
# - video_english.srt
# - video_context.json
# - video_stats.json
```

**Time:**
- Load idiom database: <1 sec
- Context analysis: 5-10 sec
- Translation: 30-60 sec (1 hour video)
- SRT generation: <1 sec

**Total:** ~1 minute for translation

---

## 📊 Performance Comparison

### 1 Hour Video Processing Time:

| Setup | Transcription | Translation | Total | Cost |
|-------|--------------|-------------|-------|------|
| **Local CPU only** | 60-120 min | 1 min | 61-121 min | $0 |
| **Local GPU (RTX)** | 3-6 min | 1 min | 4-7 min | $0 |
| **Colab Free** | 3-6 min | 1 min | 4-7 min | $0 |
| **Colab Pro** | 1-2 min | 1 min | 2-3 min | $10/mo |
| **Hybrid (Colab+Local)** | 3-6 min | 1 min | 4-7 min | $0 |

✅ **แนะนำ: Hybrid** - ฟรี และเร็ว!

---

## 💾 Disk Space Requirements

### Minimum:
```
Whisper model: 6 GB (download once)
Project code: 50 MB
Dictionaries: 2 MB
Python packages: 500 MB
Temp files: 1-2 GB (per video)
─────────────────────────
Total: ~8.5 GB
```

### Recommended:
```
Same as minimum: 8.5 GB
+ Cache space: 5 GB
+ Output space: 10 GB
─────────────────────────
Total: ~24 GB
```

**Colab:** ไม่ต้องกังวล มี storage ฟรี 15-100 GB

---

## 🎯 Which Option Should You Choose?

### ✅ **Use Colab If:**
- ✅ RAM < 16 GB
- ✅ No GPU
- ✅ Want maximum speed (10-20x)
- ✅ Don't want to install anything
- ✅ Occasional use

### ✅ **Use Local If:**
- ✅ RAM ≥ 16 GB
- ✅ Have GPU (NVIDIA)
- ✅ Frequent use (many videos)
- ✅ Privacy concerns
- ✅ No internet sometimes

### ✅ **Use Hybrid (BEST!) If:**
- ✅ Want best of both worlds
- ✅ Have internet
- ✅ Want to save local resources
- ✅ Need speed but don't have GPU

---

## 🛠️ Setup Guide for Each Option

### **Option A: Full Colab Setup**

**Colab Notebook (All-in-One):**

```python
# Cell 1: Clone Project
!git clone https://github.com/your-repo/video-translater.git
%cd video-translater

# Cell 2: Install
!pip install openai-whisper openai python-dotenv pyyaml

# Cell 3: Upload .env
from google.colab import files
uploaded = files.upload()  # Upload .env with API key

# Cell 4: Upload Video
uploaded = files.upload()
video_file = list(uploaded.keys())[0]

# Cell 5: Run Full Pipeline
!python src/orchestrator.py {video_file} \
  --model large-v3 \
  --mode production \
  --device cuda

# Cell 6: Download Results
from google.colab import files
import os
for f in os.listdir('output'):
    files.download(f'output/{f}')
```

**Pros:**
- ✅ Everything in one place
- ✅ Free GPU
- ✅ No local installation

**Cons:**
- ❌ Need internet
- ❌ Session timeout (12 hours max)
- ❌ Upload/download every time

---

### **Option B: Hybrid Setup (Recommended!)**

**Step 1: Colab (Transcription Only)**

```python
# Simple transcription notebook
!pip install openai-whisper

from google.colab import files
uploaded = files.upload()
video = list(uploaded.keys())[0]

import whisper
model = whisper.load_model("large-v3")
result = model.transcribe(video, language="th", word_timestamps=True)

import json
with open('transcript.json', 'w') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

files.download('transcript.json')
```

**Step 2: Local (Translation Only)**

```bash
# Fast translation on local machine
.venv/bin/python scripts/translate_from_transcript.py \
  transcript.json \
  -o output/
```

**Pros:**
- ✅ Best speed (GPU transcription)
- ✅ Best flexibility (local translation)
- ✅ Save Colab session time
- ✅ Can tweak translation locally

**Cons:**
- ❌ Need 2 steps
- ❌ Need to download/upload transcript

---

## 📱 Minimum System Requirements

### For Transcription:
| Spec | Minimum | Recommended | Colab |
|------|---------|-------------|-------|
| RAM | 16 GB | 32 GB | 12 GB (free) |
| CPU | 4 cores | 8+ cores | 2-4 cores |
| GPU | None | NVIDIA 8GB+ | T4 16GB (free) |
| Disk | 10 GB | 30 GB | Unlimited |

### For Translation Only:
| Spec | Minimum | Recommended |
|------|---------|-------------|
| RAM | 2 GB | 4 GB |
| CPU | 2 cores | 4 cores |
| Disk | 1 GB | 5 GB |

---

## 🎓 Quick Decision Guide

**คำถาม: คอมของคุณมี RAM เท่าไร?**

- **< 8 GB** → ใช้ Colab เต็มรูปแบบ (All Colab)
- **8-16 GB** → ใช้ Hybrid (Colab + Local)
- **16+ GB + GPU** → ใช้ Local ทั้งหมด
- **16+ GB ไม่มี GPU** → ใช้ Hybrid (เร็วกว่า)

---

## 💡 Pro Tips

### Speed Up Colab:
```python
# Use GPU runtime
# Runtime → Change runtime type → GPU → Save

# Check GPU
import torch
print(f"GPU: {torch.cuda.is_available()}")
print(f"GPU Name: {torch.cuda.get_device_name(0)}")
```

### Save Colab Session:
```python
# Mount Google Drive to save model
from google.colab import drive
drive.mount('/content/drive')

# Save model there (won't need to redownload)
import whisper
model = whisper.load_model("large-v3",
    download_root="/content/drive/MyDrive/whisper_models")
```

### Batch Processing:
```python
# Process multiple videos in one session
videos = ['video1.mp4', 'video2.mp4', 'video3.mp4']

for video in videos:
    result = model.transcribe(video, ...)
    # Save each result
```

---

## ✅ Final Recommendation

**สำหรับคนทั่วไป (เครื่องปกติ):**
```
🥇 BEST: Hybrid Approach
   - Whisper on Colab (ฟรี, เร็ว 10-20x)
   - Translation on Local (เร็ว, ปรับแต่งง่าย)
   - Total time: 4-7 min per hour video
   - Cost: $0 (transcription) + $1.50-2.50 (translation API)
```

**สำหรับคนที่มีเครื่องแรง (16GB+ RAM + GPU):**
```
🥈 GOOD: Full Local
   - Everything on local machine
   - No internet dependency
   - Privacy
   - One-time setup
```

**สำหรับคนที่ไม่อยากติดตั้งอะไร:**
```
🥉 OK: Full Colab
   - Zero installation
   - Everything online
   - Need good internet
   - 12 hour session limit
```

---

## 📞 Need Help?

**Colab Setup Issues:**
- Check GPU is enabled
- Check CUDA is available
- Try restarting runtime

**Local Setup Issues:**
- Make sure use .venv
- Check RAM usage
- Try smaller Whisper model (medium/small)

**Performance Issues:**
- Use GPU if available
- Reduce Whisper model size
- Process shorter clips
- Use batch processing

---

**สรุป: ระบบส่วนใหญ่เบามาก ใช้สเปคน้อย แต่ Whisper ใช้เยอะ แนะนำให้รัน Whisper บน Colab (ฟรี + เร็ว) แล้วแปลภาษาบนเครื่องตัวเอง!**

---

*Last Updated: 2025-10-03*
*Version: 1.0*
