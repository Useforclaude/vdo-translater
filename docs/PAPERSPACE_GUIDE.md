# 🚀 คู่มือการใช้งานใน Paperspace - ฉบับละเอียดทุกขั้นตอน

> **คู่มือนี้เขียนสำหรับผู้ที่ไม่เคยใช้ Paperspace มาก่อน**
> บอกทุกขั้นตอนว่า: **อยู่ที่ไหน → ทำอะไร → ใส่คำสั่งอะไร → ผลลัพธ์ที่ได้**

---

## 📋 สารบัญ

1. [เริ่มต้นใช้งาน Paperspace](#1-เริ่มต้นใช้งาน-paperspace)
2. [ติดตั้งและเตรียมสภาพแวดล้อม](#2-ติดตั้งและเตรียมสภาพแวดล้อม)
3. [การถอดเสียงครั้งแรก (ทดสอบ)](#3-การถอดเสียงครั้งแรก-ทดสอบ)
4. [การใช้งาน tmux (รันเบื้องหลัง)](#4-การใช้งาน-tmux-รันเบื้องหลัง)
5. [การ Resume จาก Checkpoint](#5-การ-resume-จาก-checkpoint)
6. [Best Practices: Paperspace + tmux + Checkpoint](#6-best-practices-paperspace--tmux--checkpoint-system)
7. [การตรวจสอบความคืบหน้า](#7-การตรวจสอบความคืบหน้า)
8. [การถอดเสียงแบบแบ่งช่วง](#8-การถอดเสียงแบบแบ่งช่วง)
9. [การดาวน์โหลดผลลัพธ์](#9-การดาวน์โหลดผลลัพธ์)
10. [แก้ปัญหาที่พบบ่อย](#10-แก้ปัญหาที่พบบ่อย)
11. [คำสั่งที่ใช้บ่อย (Quick Reference)](#11-คำสั่งที่ใช้บ่อย-quick-reference)

---

## 1. เริ่มต้นใช้งาน Paperspace

### 1.1 เข้าสู่ Paperspace

**ตอนนี้คุณอยู่ที่:** คอมพิวเตอร์ของคุณ (บ้าน/ออฟฟิศ)

**ขั้นตอน:**

1. **เปิด browser**
   - Chrome, Firefox, Safari, หรือ Edge อะไรก็ได้

2. **พิมพ์ URL:** `https://console.paperspace.com/`
   - กด Enter

3. **หน้า Login จะปรากฏขึ้น**
   - ถ้ายังไม่มี account: คลิก "Sign Up" (สมัครฟรี)
   - ถ้ามี account แล้ว: ใส่ email และ password → คลิก "Login"

4. **หลัง Login สำเร็จ → จะเห็นหน้า Console**
   - มุมซ้าย: เมนู (Projects, Notebooks, etc.)
   - กลาง: รายการ Projects ของคุณ

**ตอนนี้คุณอยู่ที่:** Paperspace Console (หน้าเว็บ)

---

### 1.2 เปิด Notebook ของคุณ

**ตอนนี้คุณอยู่ที่:** Paperspace Console (หน้าเว็บ)

**ขั้นตอน:**

1. **มองหาโฟลเดอร์ "Projects" ทางซ้ายมือ**
   - คลิกที่ "Projects" ถ้ายังไม่เปิด

2. **คลิกที่ project ของคุณ**
   - ชื่อ project เช่น: "video-translater" หรือชื่ออื่นที่คุณตั้งไว้
   - ถ้ายังไม่มี project: คลิก "Create Project" → ตั้งชื่อ → Create

3. **ใน project จะเห็น Notebooks**
   - หาชื่อ Notebook ของคุณ (เช่น: "My Notebook")
   - ดูว่า status เป็น "Stopped" หรือ "Running"

4. **ถ้า status = "Stopped":**
   - คลิกปุ่ม "Start" (สีเขียว)
   - รอ 30-90 วินาที ให้ machine boot (จะเห็นข้อความ "Starting...")
   - เมื่อเปลี่ยนเป็น "Running" → ✅ พร้อมใช้งาน

5. **คลิกปุ่ม "Open" หรือ "Open in JupyterLab"**
   - Tab ใหม่จะเปิดขึ้น → แสดงหน้า JupyterLab

**ตอนนี้คุณอยู่ที่:** JupyterLab (UI สีน้ำเงิน-ส้ม)

**หน้าตา JupyterLab:**
- ซ้ายมือ: File Browser (รายการไฟล์/โฟลเดอร์)
- กลาง: Launcher (ปุ่มสำหรับเปิดสิ่งต่างๆ)
- บน: Menu bar (File, Edit, View, etc.)

---

### 1.3 เปิด Terminal

**ตอนนี้คุณอยู่ที่:** JupyterLab (หน้าเว็บ)

**ขั้นตอน:**

1. **มองหา "Launcher" tab ตรงกลางหน้าจอ**
   - ถ้าไม่มี: คลิกเมนู **File → New Launcher** (มุมซ้ายบนสุด)

2. **ใน Launcher จะเห็นหลาย sections:**
   - Notebook (Python, R, etc.)
   - Console
   - **Other** ← หา section นี้

3. **ใน section "Other" จะมี icon "Terminal"**
   - icon รูป command prompt สีดำ มีข้อความ "$" หรือ ">"
   - **คลิกที่ icon "Terminal"**

4. **Tab ใหม่จะเปิดขึ้น → แสดง Terminal**
   - พื้นหลังสีดำ (หรือสีเทาเข้ม)
   - มีข้อความประมาณ:
     ```
     paperspace@ps-xxxxx:~$
     ```
   - เครื่องหมาย `$` คือ prompt (รอรับคำสั่ง)

**ตอนนี้คุณอยู่ที่:** Terminal (command line ของ Linux)

**ความหมายของ prompt:**
```
paperspace@ps-xxxxx:~$
│         │        │ │
│         │        │ └─ prompt (รอรับคำสั่ง)
│         │        └─ ~ = home directory (/notebooks หรือ /home/paperspace)
│         └─ machine ID
└─ username
```

---

### 1.4 ตรวจสอบตำแหน่งปัจจุบัน

**ตอนนี้คุณอยู่ที่:** Terminal

**พิมพ์คำสั่ง:**

```bash
pwd
```

**วิธีพิมพ์:**
1. พิมพ์ตัวอักษร `p` `w` `d` (lowercase)
2. กด Enter

**Output ที่คาดว่าจะเห็น:**
```
/notebooks
```

หรือ

```
/home/paperspace
```

**ความหมาย:**
- `pwd` = Print Working Directory (แสดงว่าตอนนี้อยู่โฟลเดอร์ไหน)
- `/notebooks` = home directory ปกติของ Paperspace

**ตอนนี้คุณอยู่ที่:** Terminal (ยังคงอยู่ที่เดิม), ตำแหน่ง `/notebooks`

---

### 1.5 ดูไฟล์และโฟลเดอร์ที่มีอยู่

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks`

**พิมพ์คำสั่ง:**

```bash
ls -lh
```

**วิธีพิมพ์:**
1. พิมพ์ `ls` (lowercase L, lowercase S)
2. เว้นวรรค (spacebar)
3. พิมพ์ `-lh` (ขีด, lowercase L, lowercase H)
4. กด Enter

**Output ที่คาดว่าจะเห็น:**
```
total 4.0K
drwxr-xr-x 5 paperspace paperspace 4.0K Oct  8 10:30 video-translater
drwxr-xr-x 2 paperspace paperspace 4.0K Oct  1 09:15 some-other-folder
-rw-r--r-- 1 paperspace paperspace  123 Oct  1 09:15 README.md
```

**ความหมาย:**
- `ls -lh` = แสดงรายการไฟล์/โฟลเดอร์ (แบบละเอียด)
- บรรทัดที่ขึ้นต้นด้วย `d` = โฟลเดอร์ (directory)
- บรรทัดที่ขึ้นต้นด้วย `-` = ไฟล์ (file)
- `video-translater` = โฟลเดอร์ของโปรเจกต์คุณ

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks` (ยังคงอยู่ที่เดิม)

---

## 2. ติดตั้งและเตรียมสภาพแวดล้อม

### 2.1 ไปยังโฟลเดอร์ project

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks`

**พิมพ์คำสั่ง:**

```bash
cd video-translater
```

**วิธีพิมพ์:**
1. พิมพ์ `cd` (lowercase)
2. เว้นวรรค
3. พิมพ์ `video-translater` (ชื่อโฟลเดอร์ของคุณ, ตัวพิมพ์เล็ก-ใหญ่ต้องถูกต้อง)
4. กด Enter

**ความหมาย:**
- `cd` = Change Directory (เปลี่ยนโฟลเดอร์)
- `video-translater` = ชื่อโฟลเดอร์ที่ต้องการเข้าไป

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater`

**ตรวจสอบว่าเข้ามาแล้ว:**

```bash
pwd
```

**Output ที่ต้องเห็น:**
```
/notebooks/video-translater
```

✅ ถูกต้อง! ตอนนี้อยู่ในโฟลเดอร์ project แล้ว

---

### 2.2 ดูไฟล์ใน project

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater`

**พิมพ์คำสั่ง:**

```bash
ls -lh
```

**Output ที่ควรเห็น:**
```
drwxr-xr-x 2 paperspace paperspace 4.0K Oct  8 10:30 scripts
drwxr-xr-x 2 paperspace paperspace 4.0K Oct  8 10:30 workflow
drwxr-xr-x 2 paperspace paperspace 4.0K Oct  8 10:30 input
drwxr-xr-x 5 paperspace paperspace 4.0K Oct  8 10:30 .venv
drwxr-xr-x 2 paperspace paperspace 4.0K Oct  8 10:30 docs
-rw-r--r-- 1 paperspace paperspace  15K Oct  8 10:30 CLAUDE.md
-rw-r--r-- 1 paperspace paperspace  10K Oct  8 10:30 SESSION_RESUME.md
```

**ความหมาย:**
- `scripts/` = สคริปต์ Python สำหรับถอดเสียง
- `workflow/` = ไฟล์ transcript และผลลัพธ์
- `input/` = วิดีโอที่จะถอดเสียง
- `.venv/` = Python virtual environment
- `docs/` = คู่มือ (รวมไฟล์นี้ที่คุณกำลังอ่าน)

**ถ้าไม่มี `.venv/`** → ต้องสร้างใหม่ (ดูขั้นตอนถัดไป)

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater` (ยังคงอยู่ที่เดิม)

---

### 2.3 ตรวจสอบ Python และติดตั้ง dependencies

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater`

#### ขั้นตอน 1: ตรวจสอบว่ามี `.venv` หรือยัง

**พิมพ์คำสั่ง:**

```bash
ls .venv/bin/python
```

**ถ้าเห็น:**
```
.venv/bin/python
```
→ ✅ มี virtual environment แล้ว ข้ามไป 2.4

**ถ้าเห็น:**
```
ls: cannot access '.venv/bin/python': No such file or directory
```
→ ❌ ยังไม่มี ต้องสร้างใหม่

---

#### ขั้นตอน 2: สร้าง virtual environment (ถ้ายังไม่มี)

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater`

**พิมพ์คำสั่ง:**

```bash
python3 -m venv .venv
```

**ความหมาย:**
- `python3` = ใช้ Python version 3
- `-m venv` = module venv (สร้าง virtual environment)
- `.venv` = ชื่อโฟลเดอร์ที่จะสร้าง

**รอให้ทำงานเสร็จ** (ประมาณ 10-30 วินาที)

**Output:** ไม่มีข้อความอะไร (เงียบ) = ✅ สำเร็จ

---

#### ขั้นตอน 3: ติดตั้ง Whisper และ dependencies

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater` (ยังคงอยู่ที่เดิม)

**พิมพ์คำสั่ง:**

```bash
.venv/bin/pip install openai-whisper torch torchaudio tqdm
```

**ความหมาย:**
- `.venv/bin/pip` = ใช้ pip ใน virtual environment (ไม่ใช่ pip ของระบบ)
- `install` = ติดตั้ง package
- `openai-whisper` = Whisper (ตัวถอดเสียง)
- `torch torchaudio` = PyTorch (สำหรับ deep learning)
- `tqdm` = Progress bar (แสดงความคืบหน้า)

**รอให้ติดตั้งเสร็จ** (อาจใช้เวลา 3-7 นาที ขึ้นอยู่กับความเร็ว internet)

**Output ที่จะเห็น:**
```
Collecting openai-whisper
  Downloading openai_whisper-...
Collecting torch
  Downloading torch-...
Installing collected packages: ...
Successfully installed openai-whisper-... torch-... torchaudio-... tqdm-...
```

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater` (ยังคงอยู่ที่เดิม)

---

### 2.4 ตรวจสอบว่า Whisper ติดตั้งสำเร็จ

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater`

**พิมพ์คำสั่ง:**

```bash
.venv/bin/python -c "import whisper; print('Whisper installed successfully!')"
```

**Output ที่ต้องเห็น:**
```
Whisper installed successfully!
```

✅ สำเร็จ! Whisper พร้อมใช้งานแล้ว

**ถ้าเห็น error:**
```
ModuleNotFoundError: No module named 'whisper'
```
→ กลับไปทำขั้นตอน 2.3 ใหม่

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater` (ยังคงอยู่ที่เดิม)

---

### 2.5 สร้างโฟลเดอร์สำหรับเก็บข้อมูล

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater`

**สำคัญ:** เราจะเก็บข้อมูลใน `/storage/` เพราะข้อมูลที่นี่ **ไม่หายเมื่อ machine restart**

**พิมพ์คำสั่งทีละบรรทัด:**

```bash
mkdir -p /storage/videos
```

กด Enter แล้วพิมพ์บรรทัดถัดไป:

```bash
mkdir -p /storage/output
```

กด Enter แล้วพิมพ์บรรทัดถัดไป:

```bash
mkdir -p /storage/logs
```

กด Enter แล้วพิมพ์บรรทัดถัดไป:

```bash
mkdir -p /storage/whisper_checkpoints
```

กด Enter

**ความหมาย:**
- `mkdir` = Make Directory (สร้างโฟลเดอร์)
- `-p` = สร้างโฟลเดอร์แม่ถ้ายังไม่มี (Parent directories)
- `/storage/` = ตำแหน่งที่ข้อมูลไม่หาย (persistent storage)

**ตรวจสอบว่าสร้างสำเร็จ:**

```bash
ls -lh /storage/
```

**Output ที่ต้องเห็น:**
```
drwxr-xr-x 2 paperspace paperspace 4.0K Oct  8 11:00 videos
drwxr-xr-x 2 paperspace paperspace 4.0K Oct  8 11:00 output
drwxr-xr-x 2 paperspace paperspace 4.0K Oct  8 11:00 logs
drwxr-xr-x 2 paperspace paperspace 4.0K Oct  8 11:00 whisper_checkpoints
```

✅ สร้างโฟลเดอร์สำเร็จทั้ง 4 โฟลเดอร์!

**📌 หมายเหตุสำคัญ:**
- ข้อมูลใน `/storage/` **ไม่หาย** เมื่อ machine restart
- ข้อมูลใน `/notebooks/` **อาจหาย** (ขึ้นอยู่กับ plan)
- **เก็บไฟล์สำคัญใน /storage/ เสมอ!**

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater` (ยังคงอยู่ที่เดิม)

---

### 2.6 คัดลอกวิดีโอไปยัง /storage/

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater`

**สมมติว่า:** วิดีโออยู่ที่ `input/ep-05271024.mp4`

#### ขั้นตอน 1: ตรวจสอบว่ามีวิดีโออยู่จริง

**พิมพ์คำสั่ง:**

```bash
ls -lh input/ep-05271024.mp4
```

**Output ที่ต้องเห็น:**
```
-rw-r--r-- 1 paperspace paperspace 850M Oct  8 09:00 input/ep-05271024.mp4
```

**ความหมาย:**
- ไฟล์มีขนาด 850MB
- เป็นไฟล์ที่มีอยู่จริง ✅

**ถ้าเห็น error:**
```
ls: cannot access 'input/ep-05271024.mp4': No such file or directory
```
→ ไฟล์ไม่อยู่ที่นี่ ต้องอัปโหลดก่อน (ดูวิธีใน section 9)

---

#### ขั้นตอน 2: คัดลอกไปยัง /storage/

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater` (ยังคงอยู่ที่เดิม)

**พิมพ์คำสั่ง:**

```bash
cp input/ep-05271024.mp4 /storage/videos/
```

**ความหมาย:**
- `cp` = Copy (คัดลอก)
- `input/ep-05271024.mp4` = ไฟล์ต้นทาง
- `/storage/videos/` = ปลายทาง

**รอให้ copy เสร็จ** (ไฟล์ขนาด 850MB อาจใช้เวลา 10-60 วินาที)

**ตรวจสอบว่า copy สำเร็จ:**

```bash
ls -lh /storage/videos/
```

**Output ที่ต้องเห็น:**
```
-rw-r--r-- 1 paperspace paperspace 850M Oct  8 11:01 ep-05271024.mp4
```

✅ คัดลอกสำเร็จ! วิดีโออยู่ใน /storage/ แล้ว

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater` (ยังคงอยู่ที่เดิม)

---

## 3. การถอดเสียงครั้งแรก (ทดสอบ)

### 3.1 ทดสอบสคริปต์ (ดู help)

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater`

**พิมพ์คำสั่ง:**

```bash
.venv/bin/python scripts/whisper_transcribe.py --help
```

**ความหมาย:**
- `.venv/bin/python` = ใช้ Python ใน virtual environment
- `scripts/whisper_transcribe.py` = สคริปต์ที่จะรัน
- `--help` = แสดงคำแนะนำการใช้งาน

**Output ที่ต้องเห็น:**
```
usage: whisper_transcribe.py [-h] [-o OUTPUT] [-m MODEL] [--device DEVICE]
                             [--checkpoint-dir CHECKPOINT_DIR]
                             [--checkpoint-interval CHECKPOINT_INTERVAL]
                             [--start-time START_TIME] [--end-time END_TIME]
                             [--resume] [--force-restart] [--status]
                             [input]

Transcribe Thai audio/video with Whisper (with checkpoint support)

positional arguments:
  input                 Input audio/video file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory (default: output/)
  -m MODEL, --model MODEL
                        Whisper model (default: large-v3)
  --device DEVICE       Device (default: cpu, use cuda for GPU)
  --checkpoint-dir CHECKPOINT_DIR
                        Checkpoint directory
  --checkpoint-interval CHECKPOINT_INTERVAL
                        Save checkpoint every N segments (default: 10)
  --start-time START_TIME
                        Start time in seconds
  --end-time END_TIME   End time in seconds
  --resume              Auto-resume from checkpoint if found
  --force-restart       Delete checkpoint and start from beginning
  --status              Show status of active transcriptions

Examples:
  # Basic transcription
  python scripts/whisper_transcribe.py video.mp4

  # With checkpoint (recommended for long videos)
  python scripts/whisper_transcribe.py video.mp4 \
    --checkpoint-dir /storage/whisper_checkpoints

  # Resume from checkpoint
  python scripts/whisper_transcribe.py video.mp4 --resume

  # Transcribe specific time range (10-20 minutes)
  python scripts/whisper_transcribe.py video.mp4 \
    --start-time 600 --end-time 1200

...
```

✅ สคริปต์ทำงานได้! พร้อมใช้งาน

**ถ้าเห็น error:**
```
python: can't open file 'scripts/whisper_transcribe.py': [Errno 2] No such file or directory
```
→ ตรวจสอบว่าอยู่ที่ `/notebooks/video-translater` หรือยัง (ใช้คำสั่ง `pwd`)

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater` (ยังคงอยู่ที่เดิม)

---

### 3.2 ทดสอบถอดเสียง 1 นาทีแรก

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater`

**เราจะทดสอบถอดเสียงเพียง 60 วินาทีแรก (เพื่อประหยัดเวลา)**

**พิมพ์คำสั่ง:** (คัดลอกทั้งหมดแล้ววางได้เลย)

```bash
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/ep-05271024.mp4 \
  -o /storage/output/ \
  --model large-v3 \
  --device cuda \
  --end-time 60 \
  --no-checkpoint
```

**อธิบายแต่ละส่วน:**
- `/storage/videos/ep-05271024.mp4` = ไฟล์ input (วิดีโอของคุณ)
- `-o /storage/output/` = เก็บผลลัพธ์ที่นี่
- `--model large-v3` = ใช้ model ขนาดใหญ่สุด (แม่นที่สุด)
- `--device cuda` = ใช้ GPU (เร็วกว่า CPU มาก)
- `--end-time 60` = ถอดแค่ 60 วินาทีแรก (ทดสอบ)
- `--no-checkpoint` = ไม่ใช้ checkpoint (เพราะแค่ทดสอบ)

**กด Enter แล้วรอ...**

**Output ที่จะเห็น:**
```
======================================================================
Whisper Transcriber (Thai-Optimized) - WITH CHECKPOINT
======================================================================
Model: large-v3
Device: cuda
Checkpoint: Disabled

Loading Whisper model...
(ครั้งแรกจะโหลด model จาก internet ประมาณ 2-3 GB, ใช้เวลา 2-5 นาที)
✓ Model loaded successfully

Extracting audio segment...
  Start: 0:00:00
  End: 0:01:00
✓ Audio segment extracted

Transcribing: ep-05271024.mp4
Settings:
  - Word-level timestamps: ✓
  - Multi-temperature: ✓
  - Beam search: ✓
  - Thai optimization: ✓
  - Time offset: 0:00:00

Processing...
Transcribing: 100%|██████████| 60.0/60.0 [00:15<00:00, 3.9s/s]

✓ Transcription complete:
  - Duration: 0:01:00
  - Segments: 15
  - Words: 180
  - Avg confidence: 94.2%
  - Processing time: 0:00:15
  - Speed: 4.0x realtime

✓ JSON saved: /storage/output/ep-05271024_transcript.json
✓ Thai SRT saved: /storage/output/ep-05271024_thai.srt

======================================================================
TRANSCRIPTION COMPLETE
======================================================================
Input: ep-05271024.mp4
Duration: 0:01:00
Processing time: 0:00:15
Speed: 4.0x realtime

Outputs:
  - JSON: /storage/output/ep-05271024_transcript.json
  - Thai SRT: /storage/output/ep-05271024_thai.srt

Next steps:
  1. Create translation batch:
     python scripts/create_translation_batch.py /storage/output/ep-05271024_transcript.json
  2. Translate with Claude Code
  3. Convert to English SRT:
     python scripts/batch_to_srt.py /storage/output/ep-05271024_transcript.json translated.txt
```

✅ **สำเร็จ!** ถอดเสียง 1 นาทีได้แล้ว ใช้เวลาประมาณ 15 วินาที (เร็วกว่า realtime 4 เท่า)

**ถ้าเจอ error ดูที่:** [แก้ปัญหาที่พบบ่อย](#9-แก้ปัญหาที่พบบ่อย)

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater` (ยังคงอยู่ที่เดิม)

---

## 4. การใช้งาน tmux (รันเบื้องหลัง)

### 4.1 ทำไมต้องใช้ tmux?

**ปัญหา:**
- ถ้าถอดเสียงใน Terminal ปกติ → **ต้องเปิด browser ตลอด**
- ปิด browser → งานหยุด → ข้อมูลหาย ❌

**วิธีแก้: ใช้ tmux**
- รันงานใน tmux session → **ปิด browser ได้**
- งานยังทำงานต่อบน server ✅
- Reconnect มาดูได้ตลอดเวลา ✅

---

### 4.2 ติดตั้ง tmux (ถ้ายังไม่มี)

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater`

#### ขั้นตอน 1: ตรวจสอบว่ามี tmux หรือยัง

**พิมพ์คำสั่ง:**

```bash
tmux -V
```

**ถ้าเห็น:**
```
tmux 3.2a
```
→ ✅ มีแล้ว ข้ามไป [4.3](#43-สร้าง-tmux-session)

**ถ้าเห็น:**
```
command not found: tmux
```
→ ❌ ยังไม่มี ต้องติดตั้ง

---

#### ขั้นตอน 2: ติดตั้ง tmux

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater` (ยังคงอยู่ที่เดิม)

**พิมพ์คำสั่ง:**

```bash
sudo apt-get update && sudo apt-get install -y tmux
```

**ความหมาย:**
- `sudo` = ใช้สิทธิ์ administrator
- `apt-get update` = อัปเดตรายการ package
- `apt-get install -y tmux` = ติดตั้ง tmux

**จะถามรหัสผ่าน:** (ถ้าถาม)
- พิมพ์รหัสผ่าน Paperspace ของคุณ
- (ตอนพิมพ์จะไม่เห็นตัวอักษร เป็นเรื่องปกติ)
- กด Enter

**รอให้ติดตั้งเสร็จ** (ประมาณ 30-90 วินาที)

**Output:**
```
...
Setting up tmux (3.2a-4) ...
```

✅ ติดตั้งเสร็จแล้ว!

**ตรวจสอบอีกครั้ง:**

```bash
tmux -V
```

**ต้องเห็น:**
```
tmux 3.2a
```

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater` (ยังคงอยู่ที่เดิม)

---

### 4.3 สร้าง tmux session

**ตอนนี้คุณอยู่ที่:** Terminal ปกติ, ตำแหน่ง `/notebooks/video-translater`

**พิมพ์คำสั่ง:**

```bash
tmux new -s whisper-ep05
```

**ความหมาย:**
- `tmux new` = สร้าง session ใหม่
- `-s whisper-ep05` = ตั้งชื่อ session ว่า "whisper-ep05" (ตั้งชื่ออะไรก็ได้)

**หน้าจอจะเปลี่ยน:**

**ก่อนกด Enter:**
- Terminal ปกติ
- ข้างล่างไม่มีอะไร

**หลังกด Enter:**
- Terminal ยังคงเป็น Terminal
- **แต่ล่างสุดจะมีแถบสีเขียว:**
  ```
  [whisper-ep05] 0:bash*                    paperspace@ps-xxxxx
  ```
- นี่คือ **tmux session** (สภาพแวดล้อมแยกต่างหาก)

**ตอนนี้คุณอยู่ที่:** tmux session "whisper-ep05" (ข้างในเป็น Terminal)

---

#### ตรวจสอบตำแหน่ง (ใน tmux)

**พิมพ์คำสั่ง:**

```bash
pwd
```

**ถ้าไม่ได้อยู่ที่ `/notebooks/video-translater`:**

```bash
cd /notebooks/video-translater
```

**ตอนนี้คุณอยู่ที่:** tmux session "whisper-ep05", ตำแหน่ง `/notebooks/video-translater`

---

### 4.4 รันการถอดเสียงใน tmux (เต็มไฟล์)

**ตอนนี้คุณอยู่ที่:** tmux session "whisper-ep05", ตำแหน่ง `/notebooks/video-translater`

**ตอนนี้เราจะถอดเสียงเต็มไฟล์ (ไม่ใช่แค่ 60 วินาที) และใช้ checkpoint**

**พิมพ์คำสั่ง:** (คัดลอกทั้งหมดแล้ววาง)

```bash
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/ep-05271024.mp4 \
  -o /storage/output/ \
  --model large-v3 \
  --device cuda \
  --checkpoint-dir /storage/whisper_checkpoints \
  --checkpoint-interval 10 \
  --resume
```

**อธิบายแต่ละส่วน:**
- `/storage/videos/ep-05271024.mp4` = วิดีโอของคุณ
- `-o /storage/output/` = เก็บผลลัพธ์
- `--model large-v3` = model ขนาดใหญ่
- `--device cuda` = ใช้ GPU
- `--checkpoint-dir /storage/whisper_checkpoints` = **เก็บ checkpoint ที่นี่**
- `--checkpoint-interval 10` = **บันทึกทุก 10 segments**
- `--resume` = **ถ้ามี checkpoint จะถามว่าจะ resume ไหม**

**กด Enter**

**งานจะเริ่มทำงาน:**

```
======================================================================
Whisper Transcriber (Thai-Optimized) - WITH CHECKPOINT
======================================================================
Model: large-v3
Device: cuda
Checkpoint: Enabled (/storage/whisper_checkpoints)
Checkpoint interval: Every 10 segments

Loading Whisper model...
✓ Model loaded successfully

Transcribing: ep-05271024.mp4
Settings:
  - Word-level timestamps: ✓
  - Multi-temperature: ✓
  - Beam search: ✓
  - Thai optimization: ✓

Processing...
Transcribing: 100%|████████░░░░░░░░░░| 20% (90/450 segments)
Speed: 8.5x realtime | ETA: 12m 30s | Elapsed: 3m 15s
Last checkpoint: 25s ago (segment 80)
```

**ตอนนี้งานกำลังรัน** ✅

**ตอนนี้คุณอยู่ที่:** tmux session "whisper-ep05" (งานกำลังทำอยู่)

---

### 4.5 Detach จาก tmux (ปล่อยให้รันต่อ)

**ตอนนี้คุณอยู่ที่:** tmux session "whisper-ep05" (งานกำลังรัน)

**วิธี Detach:**

1. **กดปุ่ม** `Ctrl` และ `B` **พร้อมกัน** (กดค้าง)
2. **ปล่อยทั้งสองปุ่ม**
3. **กดปุ่ม** `D` (ตัวเดียว)

**คำสั่งสั้นๆ:** `Ctrl+B` แล้วกด `D`

**หน้าจอจะกลับมาเป็น Terminal ปกติ:**

```
[detached (from session whisper-ep05)]
paperspace@ps-xxxxx:~/video-translater$
```

**ตอนนี้คุณอยู่ที่:** Terminal ปกติ (นอก tmux)

**งานยังทำงานอยู่ใน tmux เบื้องหลัง** ✅

**📌 สิ่งสำคัญ:**
- งานยังทำงานต่อใน tmux
- คุณสามารถ:
  - ✅ ปิด Terminal
  - ✅ ปิด browser
  - ✅ ปิดคอมพิวเตอร์
  - ✅ งานยังรันต่อบน Paperspace server

---

### 4.6 ตรวจสอบ tmux sessions

**ตอนนี้คุณอยู่ที่:** Terminal ปกติ (นอก tmux)

**พิมพ์คำสั่ง:**

```bash
tmux ls
```

**ความหมาย:**
- `tmux ls` = แสดงรายการ sessions ทั้งหมด

**Output ที่ต้องเห็น:**
```
whisper-ep05: 1 windows (created Wed Oct  8 11:30:15 2025)
```

**ความหมาย:**
- มี session ชื่อ "whisper-ep05" ยังทำงานอยู่ ✅

**ตอนนี้คุณอยู่ที่:** Terminal ปกติ (นอก tmux, ยังคงอยู่ที่เดิม)

---

### 4.7 กลับเข้าไปดู tmux session

**ตอนนี้คุณอยู่ที่:** Terminal ปกติ (นอก tmux)

**พิมพ์คำสั่ง:**

```bash
tmux attach -t whisper-ep05
```

**ความหมาย:**
- `tmux attach` = เข้าไปดู session
- `-t whisper-ep05` = ชื่อ session ที่ต้องการ

**หน้าจอจะเปลี่ยนกลับเข้าไปใน tmux:**

```
Transcribing: 100%|████████████░░░░░░| 60% (270/450 segments)
Speed: 8.5x realtime | ETA: 8m 15s | Elapsed: 12m 45s
Last checkpoint: 18s ago (segment 260)
```

**ตอนนี้คุณอยู่ที่:** tmux session "whisper-ep05" (กลับมาดูงาน)

**เห็นความคืบหน้าแบบ realtime** ✅

**ต้องการ detach อีกครั้ง:**
- กด `Ctrl+B` แล้วกด `D`

---

## 5. การ Resume จาก Checkpoint

### 5.1 สถานการณ์: Session หมดเวลากลางคัน

**สมมติว่า:**
- คุณกำลังถอดเสียงอยู่ segment 250/450 (55%)
- Paperspace timeout หรือ internet ขาด
- งานหยุดไป

**ไม่ต้องกังวล! Checkpoint ถูกบันทึกไว้ที่ /storage/ แล้ว** ✅

---

### 5.2 เข้า Paperspace ใหม่

**ตอนนี้คุณอยู่ที่:** คอมพิวเตอร์ของคุณ

**ขั้นตอน:**

1. **เปิด browser**
2. **ไปที่:** `https://console.paperspace.com/`
3. **Login** ด้วย account ของคุณ
4. **คลิกที่ project ของคุณ**
5. **Start machine** (ถ้าไม่ได้รันอยู่)
   - คลิกปุ่ม "Start"
   - รอ 30-90 วินาที
6. **คลิก "Open" → เปิด JupyterLab**
7. **เปิด Terminal ใหม่**
   - File → New Launcher → Terminal

**ตอนนี้คุณอยู่ที่:** Terminal ใหม่ (น่าจะอยู่ที่ `/notebooks`)

---

### 5.3 ไปยังโฟลเดอร์ project

**ตอนนี้คุณอยู่ที่:** Terminal

**พิมพ์คำสั่ง:**

```bash
cd /notebooks/video-translater
```

**ตรวจสอบ:**

```bash
pwd
```

**ต้องเห็น:**
```
/notebooks/video-translater
```

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater`

---

### 5.4 ตรวจสอบ tmux sessions เก่า

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater`

**พิมพ์คำสั่ง:**

```bash
tmux ls
```

**กรณีที่ 1: มี session เก่าอยู่**
```
whisper-ep05: 1 windows (created Wed Oct  8 11:30:15 2025)
```

**ทำอย่างนี้:**

```bash
tmux attach -t whisper-ep05
```

→ เข้าไปดู session → จะเห็นว่างานหยุดไป หรือ error

**กรณีที่ 2: ไม่มี session**
```
no sessions
```

→ **ไม่เป็นไร! Checkpoint ยังอยู่ที่ /storage/ อยู่**

---

### 5.5 Resume จาก checkpoint

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater`

**สร้าง tmux session ใหม่:**

```bash
tmux new -s whisper-ep05-resume
```

**ตอนนี้คุณอยู่ที่:** tmux session "whisper-ep05-resume"

**ไปยังโฟลเดอร์ project:**

```bash
cd /notebooks/video-translater
```

**รันคำสั่งเดิม (มี --resume):**

```bash
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/ep-05271024.mp4 \
  -o /storage/output/ \
  --model large-v3 \
  --device cuda \
  --checkpoint-dir /storage/whisper_checkpoints \
  --checkpoint-interval 10 \
  --resume
```

**จะเห็นข้อความ:**

```
======================================================================
CHECKPOINT FOUND
======================================================================
Video: ep-05271024.mp4
Hash: a3f2e1b9
Last checkpoint: 2025-10-08 12:45:30 (15 minutes ago)

Progress: 250/450 segments (55.6%)
Last saved: segment 250
Duration processed: 25m 00s
Model: large-v3
Device: cuda

Resume from checkpoint? [Y/n]:
```

**พิมพ์:** `Y` แล้วกด Enter

**จะเริ่มต่อจาก segment 250:**

```
✓ Resuming from checkpoint...
✓ Loaded 250 previous segments
✓ Resuming from segment 250

Resuming from segment 250...
Re-transcribing segment 249 (overlap safety)...
Progress: |████████████░░░░░░| 56% (252/450 segments)
Speed: 8.5x realtime | ETA: 7m 30s
```

**งานทำต่อจากที่หยุด!** ไม่เสียเวลา ✅

**ตอนนี้คุณอยู่ที่:** tmux session "whisper-ep05-resume" (งานกำลังรัน)

---

### 5.6 Detach และปล่อยให้ทำต่อ

**ตอนนี้คุณอยู่ที่:** tmux session "whisper-ep05-resume"

**กด:** `Ctrl+B` แล้วกด `D`

**ปิด browser ได้เลย** ✅ งานยังทำต่อ

---

## 6. Best Practices: Paperspace + tmux + Checkpoint System

### 6.1 ✅ ทำไมทำต่อได้หลัง Paperspace Restart?

**สิ่งสำคัญที่ทำให้ระบบทำต่อได้:**

1. **Checkpoint System ใน Whisper**
   - บันทึกความคืบหน้าทุก 10 segments
   - เก็บไว้ที่ `/storage/whisper_checkpoints/`

2. **Persistent Storage (/storage/)**
   - ข้อมูลใน `/storage/` **ไม่หาย** หลัง machine restart
   - Checkpoint, วิดีโอ, ผลลัพธ์ → เก็บใน `/storage/` เสมอ

3. **Resume Flag (--resume)**
   - Script ตรวจหา checkpoint อัตโนมัติ
   - ถามว่าจะทำต่อหรือไม่

4. **tmux Session (แม้จะหาย แต่ไม่สำคัญ!)**
   - tmux session หายหลัง restart → **ไม่เป็นไร!**
   - สร้าง session ใหม่ → รันคำสั่งเดิม → resume จาก checkpoint

---

### 6.2 📋 Checklist: ก่อนเริ่มถอดเสียง

**เพื่อให้ resume ได้หลัง timeout:**

- [ ] ✅ ใช้ `/storage/` สำหรับวิดีโอ input
  ```bash
  cp input/video.mp4 /storage/videos/
  ```

- [ ] ✅ ใช้ `/storage/` สำหรับ output
  ```bash
  -o /storage/output/
  ```

- [ ] ✅ เปิดใช้ checkpoint
  ```bash
  --checkpoint-dir /storage/whisper_checkpoints
  ```

- [ ] ✅ เปิดใช้ resume flag
  ```bash
  --resume
  ```

- [ ] ✅ รันใน tmux session
  ```bash
  tmux new -s whisper-session
  ```

**ถ้าทำครบทั้ง 5 ข้อ → งานไม่หายแม้ Paperspace restart!** 🎉

---

### 6.3 🔄 ขั้นตอน Resume หลัง Paperspace Timeout

**สถานการณ์:** Paperspace timeout ขณะถอดเสียง segment 250/450

#### Step 1: เริ่ม Paperspace Machine อีกครั้ง

1. เปิด browser → ไปที่ `https://console.paperspace.com/`
2. Login → เข้า project
3. คลิก "Start" machine
4. รอ 30-90 วินาที → status เป็น "Running"
5. คลิก "Open" → เปิด JupyterLab

---

#### Step 2: เปิด Terminal ใหม่

1. ใน JupyterLab: File → New Launcher
2. คลิก "Terminal"

---

#### Step 3: ตรวจสอบ Checkpoint (เพื่อความมั่นใจ)

```bash
# เช็คว่ามี checkpoint หรือไม่
ls -lh /storage/whisper_checkpoints/
```

**Output ที่ต้องเห็น:**
```
drwxr-xr-x 2 paperspace paperspace 4.0K Oct  8 12:45 a3f2e1b9
```

→ ✅ มี checkpoint อยู่! (a3f2e1b9 = hash ของวิดีโอ)

**ดูรายละเอียด checkpoint:**
```bash
ls -lh /storage/whisper_checkpoints/a3f2e1b9/
```

**Output:**
```
-rw-r--r-- 1 paperspace paperspace  45K Oct  8 12:45 checkpoint_250.json
-rw-r--r-- 1 paperspace paperspace  38K Oct  8 12:45 metadata.json
```

→ ✅ Checkpoint บันทึกไว้ที่ segment 250

---

#### Step 4: สร้าง tmux Session ใหม่

```bash
cd /notebooks/video-translater
tmux new -s whisper-resume
```

---

#### Step 5: รันคำสั่งเดิม (มี --resume)

```bash
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/ep-05271024.mp4 \
  -o /storage/output/ \
  --model large-v3 \
  --device cuda \
  --checkpoint-dir /storage/whisper_checkpoints \
  --checkpoint-interval 10 \
  --resume
```

**Script จะถาม:**
```
======================================================================
CHECKPOINT FOUND
======================================================================
Video: ep-05271024.mp4
Hash: a3f2e1b9
Last checkpoint: 2025-10-08 12:45:30 (15 minutes ago)

Progress: 250/450 segments (55.6%)
Last saved: segment 250
Duration processed: 25m 00s
Model: large-v3
Device: cuda

Resume from checkpoint? [Y/n]:
```

**พิมพ์:** `Y` แล้วกด Enter

→ ✅ **ทำต่อจาก segment 250!** ไม่ต้องเริ่มใหม่

---

#### Step 6: Detach และปล่อยให้ทำต่อ

กด `Ctrl+B` แล้วกด `D`

→ ✅ งานทำต่อ, ปิด browser ได้

---

### 6.4 ⚡ Quick Commands: Resume After Timeout

**คัดลอกวางได้เลย:**

```bash
# 1. เปิด Paperspace → Start machine → Open JupyterLab → Terminal

# 2. เช็ค checkpoint (optional, เพื่อความมั่นใจ)
ls -lh /storage/whisper_checkpoints/

# 3. ไป project directory
cd /notebooks/video-translater

# 4. สร้าง tmux session ใหม่
tmux new -s whisper-resume

# 5. รันคำสั่งเดิม (ต้องมี --resume)
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/YOUR_VIDEO.mp4 \
  -o /storage/output/ \
  --device cuda \
  --checkpoint-dir /storage/whisper_checkpoints \
  --checkpoint-interval 10 \
  --resume

# 6. เมื่อถาม "Resume from checkpoint? [Y/n]:" → กด Y

# 7. Detach (ปล่อยให้รัน)
# กด Ctrl+B แล้วกด D
```

---

### 6.5 🚨 สิ่งที่ต้องระวัง

**❌ อย่าทำ:**

1. **อย่าเก็บวิดีโอใน `/notebooks/`**
   - อาจหายหลัง restart (ขึ้นอยู่กับ Paperspace plan)
   - ✅ เก็บใน `/storage/` เสมอ

2. **อย่าลืม `--resume` flag**
   - ถ้าไม่มี → script ไม่ถามว่าจะ resume
   - จะเริ่มถอดเสียงใหม่ทั้งหมด (เสียเวลา!)

3. **อย่าลบ checkpoint ก่อนเสร็จ**
   - Checkpoint ใน `/storage/whisper_checkpoints/` → **อย่าลบ!**
   - ลบแล้วจะ resume ไม่ได้

4. **อย่าใช้ `--force-restart` โดยไม่รู้**
   - Flag นี้จะ**ลบ checkpoint และเริ่มใหม่**
   - ใช้เฉพาะเมื่อต้องการเริ่มใหม่จริงๆ

**✅ ต้องทำ:**

1. ✅ เก็บทุกอย่างใน `/storage/`
2. ✅ ใช้ `--resume` เสมอ
3. ✅ รันใน tmux session เสมอ
4. ✅ Detach ก่อนปิด browser
5. ✅ เช็ค checkpoint ก่อน resume (เพื่อความมั่นใจ)

---

### 6.6 💡 Pro Tips

**1. ใช้ชื่อ tmux session ที่จำง่าย**
```bash
# ดี: ใช้ชื่อบอกว่าเป็นวิดีโออะไร
tmux new -s ss1.5-ep01

# ไม่ดี: ชื่อทั่วไป ๆ
tmux new -s whisper
```

**2. Detach ทุกครั้งก่อนปิด browser**
```bash
# ในขณะที่อยู่ใน tmux (เห็นแถบเขียวด้านล่าง):
Ctrl+B แล้วกด D

# ตรวจสอบว่า detach แล้ว:
tmux ls
# ต้องเห็น session ที่สร้างไว้
```

**3. เช็คความคืบหน้าโดยไม่เข้า tmux**
```bash
# ดูสถานะโดยไม่ต้องเข้า tmux
.venv/bin/python scripts/whisper_status.py
```

**4. Backup checkpoint สำคัญ**
```bash
# สำหรับวิดีโอสำคัญมาก:
cp -r /storage/whisper_checkpoints/ /storage/whisper_checkpoints_backup/
```

---

### 6.7 📊 ตัวอย่างการใช้งานจริง

**สถานการณ์:** ถอดเสียง SS1.5 ทั้ง 6 episodes

#### วันที่ 1: เริ่มถอดเสียง

```bash
# 1. เข้า Paperspace
# 2. เปิด Terminal
cd /notebooks/video-translater

# 3. สร้าง tmux session
tmux new -s ss1.5-transcribe

# 4. รันสคริปต์
bash paperspace/transcribe_ss1.5_all.sh

# 5. Detach
Ctrl+B แล้วกด D

# 6. ปิด browser ได้เลย
```

---

#### วันที่ 2: Paperspace timeout กลางคัน

```bash
# Paperspace หมดเวลา (หรือ internet ขาด)
# งานหยุดที่ EP-03 segment 120/300
```

---

#### วันที่ 3: Resume งาน

```bash
# 1. เข้า Paperspace อีกครั้ง → Start machine → Terminal

# 2. เช็ค checkpoint
ls -lh /storage/whisper_checkpoints/

# Output:
# drwxr-xr-x 2 ... SS-1.5-Ep03_a3f2e1b9

# → ✅ มี checkpoint EP-03 อยู่

# 3. สร้าง tmux session ใหม่
cd /notebooks/video-translater
tmux new -s ss1.5-resume

# 4. รันสคริปต์เดิม
bash paperspace/transcribe_ss1.5_all.sh

# Script จะตรวจหา checkpoint และ resume EP-03 จาก segment 120
# จากนั้นทำ EP-04, EP-05, EP-06 ต่อ

# 5. Detach
Ctrl+B แล้วกด D
```

---

**ผลลัพธ์:**
- ✅ EP-01, EP-02 เสร็จแล้ว (ไม่ทำซ้ำ)
- ✅ EP-03 ทำต่อจาก segment 120 (ไม่เริ่มใหม่)
- ✅ EP-04, EP-05, EP-06 ทำต่อตามปกติ
- ✅ ไม่เสียเวลาเลย!

---

### 6.8 ✅ Checklist: ก่อนปิด Paperspace

**ก่อนปิด browser หรือปิด machine:**

- [ ] ✅ งานทำเสร็จแล้วหรือยัง?
  - ใช้: `.venv/bin/python scripts/whisper_status.py`
  - ถ้ายังไม่เสร็จ → ต้อง detach จาก tmux ก่อน

- [ ] ✅ Detach จาก tmux แล้ว?
  - กด `Ctrl+B` แล้ว `D`
  - ตรวจสอบ: `tmux ls` (ต้องเห็น session)

- [ ] ✅ Checkpoint ถูกบันทึกแล้ว?
  - เช็ค: `ls -lh /storage/whisper_checkpoints/`

- [ ] ✅ ไฟล์ผลลัพธ์อยู่ใน `/storage/`?
  - เช็ค: `ls -lh /storage/output/`

**ถ้าทุกข้อ ✅ → ปิด browser ได้เลย! งานยังรันต่อบน server** 🚀

---

## 7. การตรวจสอบความคืบหน้า

### 7.1 เช็คสถานะแบบรวดเร็ว (ไม่ต้องเข้า tmux)

**ตอนนี้คุณอยู่ที่:** Terminal ปกติ (นอก tmux)

**ไปที่ project:**

```bash
cd /notebooks/video-translater
```

**พิมพ์คำสั่ง:**

```bash
.venv/bin/python scripts/whisper_status.py
```

**Output:**
```
======================================================================
WHISPER TRANSCRIPTION STATUS
======================================================================
Active transcriptions: 1

[1] ep-05271024.mp4
    Hash: a3f2e1b9
    Model: large-v3 (cuda)

    Progress: 310/450 segments (68.9%)
    [███████████████████████████░░░░░░░░░░░░░░░░░░░░░]

    Elapsed: 18m 30s
    Speed: 8.5x realtime
    ETA: 6m 15s

    Created: 2025-10-08T11:30:00.000000
    Last updated: 2025-10-08T11:48:30.000000
    Checkpoint: /storage/whisper_checkpoints/a3f2e1b9

======================================================================

Commands:
  Resume: python scripts/whisper_transcribe.py <video> --resume
  Stop: Ctrl+C (checkpoint will be saved)
======================================================================
```

**ไม่ต้องเข้า tmux ก็ดูได้** ✅

**ตอนนี้คุณอยู่ที่:** Terminal ปกติ (ยังคงอยู่ที่เดิม)

---

### 7.2 Watch mode (auto-refresh ทุก 5 วินาที)

**ตอนนี้คุณอยู่ที่:** Terminal ปกติ, ตำแหน่ง `/notebooks/video-translater`

**พิมพ์คำสั่ง:**

```bash
.venv/bin/python scripts/whisper_status.py --watch
```

**หน้าจอจะ refresh ทุก 5 วินาที:**

```
======================================================================
WHISPER TRANSCRIPTION STATUS
======================================================================
Active transcriptions: 1

[1] ep-05271024.mp4
    Hash: a3f2e1b9
    Progress: 312/450 segments (69.3%)
    [████████████████████████████░░░░░░░░░░░░░░░░░░░░]
    Speed: 8.5x realtime | ETA: 6m 00s

Refreshing every 5s... (Ctrl+C to exit)
```

**กด Ctrl+C เพื่อหยุด**

**ตอนนี้คุณอยู่ที่:** Terminal ปกติ (ยังคงอยู่ที่เดิม)

---

## 8. การถอดเสียงแบบแบ่งช่วง

### 8.1 ทำไมต้องแบ่งช่วง?

**กรณีที่ควรแบ่งช่วง:**
- วิดีโอยาวมาก (เช่น 2-3 ชั่วโมง)
- GPU timeout (Paperspace มีข้อจำกัดเวลาใช้ GPU)
- ต้องการแบ่งงาน (ถอดเสียงทีละช่วง)

**วิธีการ:**
- แบ่งวิดีโอออกเป็น 4 ช่วง (เช่น 0-30, 30-60, 60-90, 90-120 นาที)
- ถอดแต่ละช่วงแยกกัน
- รวมกลับมาเป็นไฟล์เดียว

---

### 8.2 ตัวอย่าง: วิดีโอ 2 ชั่วโมง แบ่งเป็น 4 ช่วง

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater`

**สมมติ:** วิดีโอ `long_video.mp4` ยาว 2 ชั่วโมง (7200 วินาที)

#### ช่วงที่ 1: 0-30 นาที (0-1800 วินาที)

```bash
tmux new -s whisper-part1
```

(ตอนนี้อยู่ใน tmux)

```bash
cd /notebooks/video-translater

.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/long_video.mp4 \
  -o /storage/output/ \
  --model large-v3 \
  --device cuda \
  --start-time 0 \
  --end-time 1800 \
  --checkpoint-dir /storage/whisper_checkpoints
```

กด `Ctrl+B` แล้วกด `D` (detach)

---

#### ช่วงที่ 2: 30-60 นาที (1800-3600 วินาที)

```bash
tmux new -s whisper-part2
```

```bash
cd /notebooks/video-translater

.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/long_video.mp4 \
  -o /storage/output/ \
  --model large-v3 \
  --device cuda \
  --start-time 1800 \
  --end-time 3600 \
  --checkpoint-dir /storage/whisper_checkpoints
```

กด `Ctrl+B` แล้วกด `D` (detach)

---

#### ช่วงที่ 3: 60-90 นาที (3600-5400 วินาที)

```bash
tmux new -s whisper-part3
```

```bash
cd /notebooks/video-translater

.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/long_video.mp4 \
  -o /storage/output/ \
  --model large-v3 \
  --device cuda \
  --start-time 3600 \
  --end-time 5400 \
  --checkpoint-dir /storage/whisper_checkpoints
```

กด `Ctrl+B` แล้วกด `D` (detach)

---

#### ช่วงที่ 4: 90-120 นาที (5400-7200 วินาที)

```bash
tmux new -s whisper-part4
```

```bash
cd /notebooks/video-translater

.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/long_video.mp4 \
  -o /storage/output/ \
  --model large-v3 \
  --device cuda \
  --start-time 5400 \
  --end-time 7200 \
  --checkpoint-dir /storage/whisper_checkpoints
```

กด `Ctrl+B` แล้วกด `D` (detach)

---

#### ดูทุก sessions

```bash
tmux ls
```

**Output:**
```
whisper-part1: 1 windows (created ...)
whisper-part2: 1 windows (created ...)
whisper-part3: 1 windows (created ...)
whisper-part4: 1 windows (created ...)
```

**ทั้ง 4 ช่วงกำลังถอดเสียงพร้อมกัน!**

---

### 8.3 รวม transcripts ทั้ง 4 ช่วง

**เมื่อทุกช่วงเสร็จแล้ว** (ใช้คำสั่ง `whisper_status.py` เช็ค)

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater`

**พิมพ์คำสั่ง:**

```bash
.venv/bin/python scripts/merge_transcripts.py \
  /storage/output/long_video_transcript.json \
  --pattern "long_video*_transcript.json" \
  -o /storage/output/long_video_full_transcript.json \
  --srt /storage/output/long_video_full_thai.srt
```

**ความหมาย:**
- `--pattern "long_video*_transcript.json"` = หาไฟล์ที่ขึ้นต้นด้วย "long_video" ทั้งหมด
- `-o long_video_full_transcript.json` = ไฟล์ผลลัพธ์ที่รวมแล้ว
- `--srt long_video_full_thai.srt` = SRT ที่รวมแล้ว

**Output:**
```
======================================================================
MERGE TRANSCRIPTS
======================================================================
Input files: 4
  - long_video_0-1800_transcript.json
  - long_video_1800-3600_transcript.json
  - long_video_3600-5400_transcript.json
  - long_video_5400-7200_transcript.json

✓ Loaded: long_video_0-1800_transcript.json
  Segments: 180
  Duration: 0:30:00

✓ Loaded: long_video_1800-3600_transcript.json
  Segments: 180
  Duration: 0:30:00

(... และอีก 2 ไฟล์)

Validating transcripts...
  ⚠️  Gap detected: 2.5s between transcript 1 and 2

Continue with warnings? [y/N]: y

Merging 4 transcripts...
✓ Merge complete:
  - Total segments: 720
  - Total duration: 2:00:00
  - Total words: 21600
  - Avg confidence: 93.5%

✓ Merged JSON saved: /storage/output/long_video_full_transcript.json
✓ Merged SRT saved: /storage/output/long_video_full_thai.srt

======================================================================
MERGE COMPLETE
======================================================================
```

✅ รวมเสร็จแล้ว! ได้ transcript เต็มทั้ง 2 ชั่วโมง

---

## 9. การดาวน์โหลดผลลัพธ์

### 9.1 ตรวจสอบว่าเสร็จแล้ว

**ตอนนี้คุณอยู่ที่:** Terminal

```bash
cd /notebooks/video-translater
.venv/bin/python scripts/whisper_status.py
```

**ถ้าเห็น:**
```
No active transcriptions found
```

→ ✅ เสร็จแล้ว!

---

### 9.2 ตรวจสอบไฟล์ผลลัพธ์

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater`

**พิมพ์คำสั่ง:**

```bash
ls -lh /storage/output/
```

**Output ที่ต้องเห็น:**
```
-rw-r--r-- 1 paperspace paperspace  45K Oct  8 13:15 ep-05271024_transcript.json
-rw-r--r-- 1 paperspace paperspace  38K Oct  8 13:15 ep-05271024_thai.srt
```

✅ ไฟล์ผลลัพธ์พร้อมแล้ว!

---

### 9.3 คัดลอกไปยัง /notebooks/ (เพื่อดาวน์โหลด)

**ตอนนี้คุณอยู่ที่:** Terminal, ตำแหน่ง `/notebooks/video-translater`

**เหตุผล:** ไฟล์ใน `/storage/` ดาวน์โหลดยาก → คัดลอกไปยัง `/notebooks/` ก่อน

**พิมพ์คำสั่ง:**

```bash
mkdir -p output
```

แล้วพิมพ์:

```bash
cp /storage/output/ep-05271024_transcript.json output/
cp /storage/output/ep-05271024_thai.srt output/
```

**ตรวจสอบ:**

```bash
ls -lh output/
```

**Output:**
```
-rw-r--r-- 1 paperspace paperspace  45K Oct  8 13:15 ep-05271024_transcript.json
-rw-r--r-- 1 paperspace paperspace  38K Oct  8 13:15 ep-05271024_thai.srt
```

---

### 9.4 ดาวน์โหลดผ่าน JupyterLab

**ตอนนี้คุณอยู่ที่:** Terminal (แต่จะใช้ JupyterLab UI)

**ขั้นตอน:**

1. **กลับไปที่แท็บ JupyterLab** (browser tab ที่เปิด JupyterLab อยู่)

2. **คลิกที่ File Browser icon** (ทางซ้ายสุด, icon รูปโฟลเดอร์)

3. **ดับเบิลคลิกที่โฟลเดอร์ "video-translater"**

4. **ดับเบิลคลิกที่โฟลเดอร์ "output"**

5. **เห็นไฟล์:**
   - `ep-05271024_transcript.json`
   - `ep-05271024_thai.srt`

6. **คลิกขวาที่ไฟล์** → เลือก **"Download"**

7. **ไฟล์จะถูกดาวน์โหลดไปยังคอมพิวเตอร์ของคุณ** ✅

---

## 10. แก้ปัญหาที่พบบ่อย

### 10.1 Error: CUDA out of memory

**อาการ:**
```
RuntimeError: CUDA out of memory
```

**สาเหตุ:** GPU memory เต็ม

**วิธีแก้ที่ 1: ใช้ model เล็กลง**

```bash
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/video.mp4 \
  --model medium \
  --device cuda
```

(เปลี่ยนจาก `large-v3` เป็น `medium`)

**วิธีแก้ที่ 2: ใช้ CPU แทน**

```bash
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/video.mp4 \
  --model large-v3 \
  --device cpu
```

(ช้ากว่า แต่ไม่มีปัญหา memory)

---

### 10.2 Error: Checkpoint file corrupt

**อาการ:**
```
Error: Failed to load checkpoint (corrupt file)
```

**วิธีแก้: ลบ checkpoint และเริ่มใหม่**

```bash
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/video.mp4 \
  --force-restart
```

---

### 10.3 tmux session หาย

**อาการ:**
```bash
tmux ls
# no sessions
```

**สาเหตุ:** Machine restart

**วิธีแก้:**

Checkpoint ยังอยู่! ทำตาม [5.5 Resume จาก checkpoint](#55-resume-จาก-checkpoint)

---

### 10.4 ไฟล์วิดีโอหาย

**อาการ:**
```
ls: cannot access 'input/video.mp4': No such file or directory
```

**วิธีอัปโหลดวิดีโอ:**

1. **ใน JupyterLab → คลิก File Browser (ซ้ายมือ)**
2. **เข้าไปใน `video-translater/input/`**
3. **คลิกปุ่ม Upload** (icon รูปลูกศรขึ้น, ทางบนของ File Browser)
4. **เลือกไฟล์วิดีโอจากคอมพิวเตอร์**
5. **รอให้อัปโหลดเสร็จ** (อาจใช้เวลานานถ้าไฟล์ใหญ่)
6. **คัดลอกไปยัง /storage/**

```bash
cp input/video.mp4 /storage/videos/
```

---

## 11. คำสั่งที่ใช้บ่อย (Quick Reference)

### การใช้ tmux

| คำสั่ง | ทำอะไร |
|--------|---------|
| `tmux new -s NAME` | สร้าง session ชื่อ NAME |
| `tmux ls` | แสดง sessions ทั้งหมด |
| `tmux attach -t NAME` | เข้าไปดู session ชื่อ NAME |
| `Ctrl+B` แล้ว `D` | Detach (ออกแต่ยังรัน) |
| `Ctrl+B` แล้ว `C` | สร้าง window ใหม่ |
| `Ctrl+B` แล้ว `[` | Scroll mode (เลื่อนดูได้) |
| `tmux kill-session -t NAME` | ฆ่า session ชื่อ NAME |

---

### การถอดเสียง

**ถอดเสียงปกติ:**
```bash
.venv/bin/python scripts/whisper_transcribe.py video.mp4
```

**ถอดเสียงด้วย checkpoint:**
```bash
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/video.mp4 \
  -o /storage/output/ \
  --device cuda \
  --checkpoint-dir /storage/whisper_checkpoints \
  --resume
```

**ถอดเสียงช่วงเวลา:**
```bash
.venv/bin/python scripts/whisper_transcribe.py video.mp4 \
  --start-time 600 --end-time 1200
```

**เช็คสถานะ:**
```bash
.venv/bin/python scripts/whisper_status.py
```

**รวม transcripts:**
```bash
.venv/bin/python scripts/merge_transcripts.py \
  part1.json part2.json part3.json \
  -o merged.json
```

---

### ไฟล์และโฟลเดอร์

| คำสั่ง | ทำอะไร |
|--------|---------|
| `pwd` | แสดงตำแหน่งปัจจุบัน |
| `cd FOLDER` | เข้าไปในโฟลเดอร์ |
| `cd ..` | ขึ้นไป 1 ระดับ |
| `ls -lh` | แสดงรายการไฟล์ |
| `cp SRC DST` | คัดลอกไฟล์ |
| `mkdir NAME` | สร้างโฟลเดอร์ |

---

## 🎉 สรุป

คุณได้เรียนรู้:
✅ วิธีใช้ Paperspace และ JupyterLab
✅ วิธีติดตั้ง Whisper และ dependencies
✅ วิธีใช้ tmux (รันเบื้องหลัง)
✅ วิธีถอดเสียงด้วย checkpoint
✅ วิธี resume จากที่หยุด
✅ วิธีแบ่งช่วงถอดเสียง
✅ วิธีดาวน์โหลดผลลัพธ์

**ตอนนี้คุณพร้อมถอดเสียงวิดีโอยาวๆ โดยไม่กลัว session หมดเวลาแล้ว!** 🚀

---

**หมายเหตุ:**
- คู่มือนี้เขียนละเอียดเพื่อผู้เริ่มต้น
- ถ้ามีปัญหาที่ไม่ได้กล่าวถึง โปรดดูที่ [TMUX_CHEATSHEET.md](TMUX_CHEATSHEET.md)
- หรือถามใน GitHub Issues

---

**เขียนโดย:** Claude Code
**วันที่:** October 2025
**เวอร์ชัน:** 1.0
