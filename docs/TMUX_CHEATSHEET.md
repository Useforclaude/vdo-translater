# 🖥️ tmux Cheat Sheet - คำสั่งที่ใช้บ่อย

> Quick reference สำหรับ tmux commands ที่ใช้กับ Paperspace

---

## 🚀 พื้นฐาน (Basic Commands)

### สร้าง Session
```bash
# สร้าง session ใหม่
tmux

# สร้าง session พร้อมตั้งชื่อ
tmux new -s whisper

# สร้าง session ชื่อ "whisper-ep05"
tmux new -s whisper-ep05
```

---

### ดู Sessions ทั้งหมด
```bash
# แสดงรายการ sessions ทั้งหมด
tmux ls

# หรือ
tmux list-sessions
```

**Output ตัวอย่าง:**
```
whisper-ep05: 1 windows (created Wed Oct  8 11:30:15 2025)
whisper-ep06: 1 windows (created Wed Oct  8 12:45:00 2025)
```

---

### เข้าไปดู Session (Attach)
```bash
# Attach session ชื่อ "whisper-ep05"
tmux attach -t whisper-ep05

# หรือแบบสั้น
tmux a -t whisper-ep05

# Attach session ล่าสุด
tmux attach
```

---

### ออกจาก Session (Detach)

**วิธีที่ 1: Detach (ออกแต่ยังรันต่อ)**
- กด `Ctrl+B` (กดค้าง)
- ปล่อย แล้วกด `D`

**วิธีที่ 2: ใช้คำสั่ง**
```bash
# (พิมพ์ใน tmux)
tmux detach
```

**ผลลัพธ์:**
```
[detached (from session whisper-ep05)]
```

→ งานยังทำงานต่อเบื้องหลัง ✅

---

### ฆ่า Session (Kill)
```bash
# ฆ่า session ชื่อ "whisper-ep05"
tmux kill-session -t whisper-ep05

# ฆ่า session ปัจจุบัน (ในขณะที่อยู่ใน session)
# กด Ctrl+B แล้วพิมพ์:
:kill-session
```

---

## ⌨️ Keyboard Shortcuts (ใน tmux)

> **Prefix Key: `Ctrl+B`**
> ทุกคำสั่งเริ่มด้วยการกด `Ctrl+B` ก่อน แล้วจึงกดปุ่มอื่น

### การจัดการ Session

| คีย์ | คำสั่ง |
|------|--------|
| `Ctrl+B` แล้ว `D` | Detach (ออกจาก session) |
| `Ctrl+B` แล้ว `$` | เปลี่ยนชื่อ session |
| `Ctrl+B` แล้ว `:kill-session` | ฆ่า session ปัจจุบัน |

---

### การจัดการ Windows

| คีย์ | คำสั่ง |
|------|--------|
| `Ctrl+B` แล้ว `C` | สร้าง window ใหม่ |
| `Ctrl+B` แล้ว `N` | ไป window ถัดไป (Next) |
| `Ctrl+B` แล้ว `P` | ไป window ก่อนหน้า (Previous) |
| `Ctrl+B` แล้ว `0-9` | ไป window ที่ 0-9 |
| `Ctrl+B` แล้ว `,` | เปลี่ยนชื่อ window |
| `Ctrl+B` แล้ว `&` | ปิด window ปัจจุบัน |
| `Ctrl+B` แล้ว `W` | แสดงรายการ windows |

---

### การแบ่ง Panes

| คีย์ | คำสั่ง |
|------|--------|
| `Ctrl+B` แล้ว `%` | แบ่ง pane แนวตั้ง (ซ้าย-ขวา) |
| `Ctrl+B` แล้ว `"` | แบ่ง pane แนวนอน (บน-ล่าง) |
| `Ctrl+B` แล้ว `Arrow` | สลับระหว่าง panes (ลูกศร ←↑↓→) |
| `Ctrl+B` แล้ว `X` | ปิด pane ปัจจุบัน |
| `Ctrl+B` แล้ว `{` | สลับ pane กับซ้ายมือ |
| `Ctrl+B` แล้ว `}` | สลับ pane กับขวามือ |
| `Ctrl+B` แล้ว `Z` | Zoom pane (เต็มจอ/ย่อกลับ) |

---

### Scroll Mode (เลื่อนดู output)

| คีย์ | คำสั่ง |
|------|--------|
| `Ctrl+B` แล้ว `[` | เข้า scroll mode |
| ลูกศร `↑↓` | เลื่อนขึ้น-ลง (ทีละบรรทัด) |
| `Page Up/Down` | เลื่อนเร็ว (ทีละหน้า) |
| `Q` | ออกจาก scroll mode |

**วิธีใช้:**
1. กด `Ctrl+B` แล้วกด `[`
2. ใช้ลูกศรหรือ Page Up/Down เลื่อนดู
3. กด `Q` เพื่อออก

---

### Copy Mode (คัดลอก text)

| คีย์ | คำสั่ง |
|------|--------|
| `Ctrl+B` แล้ว `[` | เข้า copy mode |
| `Space` | เริ่มเลือก (selection start) |
| ลูกศร | เลื่อนเคอร์เซอร์ |
| `Enter` | คัดลอกและออก |
| `Ctrl+B` แล้ว `]` | วาง (paste) |

---

## 📝 Use Cases สำหรับ Paperspace

### Case 1: ถอดเสียงแบบไม่กลัวหลุด

```bash
# เข้า Paperspace → เปิด Terminal

# สร้าง tmux session
tmux new -s whisper

# รันการถอดเสียง
cd /notebooks/video-translater
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/video.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --resume

# Detach (ปล่อยให้รันต่อ)
Ctrl+B แล้วกด D

# ปิด browser ได้เลย ✅
```

---

### Case 2: ถอดเสียงหลายไฟล์พร้อมกัน

```bash
# Session 1: วิดีโอ ep-05
tmux new -s ep05
cd /notebooks/video-translater
.venv/bin/python scripts/whisper_transcribe.py /storage/videos/ep-05.mp4
# Detach: Ctrl+B D

# Session 2: วิดีโอ ep-06
tmux new -s ep06
cd /notebooks/video-translater
.venv/bin/python scripts/whisper_transcribe.py /storage/videos/ep-06.mp4
# Detach: Ctrl+B D

# Session 3: วิดีโอ ep-07
tmux new -s ep07
cd /notebooks/video-translater
.venv/bin/python scripts/whisper_transcribe.py /storage/videos/ep-07.mp4
# Detach: Ctrl+B D

# ดู sessions ทั้งหมด
tmux ls

# ทั้ง 3 sessions กำลังทำงานพร้อมกัน!
```

---

### Case 3: กลับมาดูความคืบหน้า

```bash
# เข้า Paperspace ใหม่ → เปิด Terminal

# ดู sessions ที่ทำงานอยู่
tmux ls

# Attach กลับเข้าไปดู
tmux attach -t ep05

# เห็นความคืบหน้า realtime ✅

# Detach อีกครั้ง
Ctrl+B แล้วกด D
```

---

### Case 4: Session หลุด (Resume จาก checkpoint)

```bash
# เข้า Paperspace ใหม่

# ตรวจสอบ sessions
tmux ls
# Output: no sessions (หลุดหมด)

# ไม่เป็นไร! Checkpoint ยังอยู่

# สร้าง session ใหม่
tmux new -s resume

# รันคำสั่งเดิม + --resume
cd /notebooks/video-translater
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/video.mp4 \
  --checkpoint-dir /storage/whisper_checkpoints \
  --resume

# จะถาม: Resume from checkpoint? [Y/n]
# พิมพ์: Y

# ทำงานต่อจากที่หยุด ✅
```

---

## 🎯 Tips & Tricks

### 1. ตั้งชื่อ session ให้เข้าใจง่าย
```bash
# ไม่ดี
tmux new -s s1

# ดี
tmux new -s whisper-ep05-large-v3
```

### 2. ใช้ windows แยกงาน
```bash
# เข้า session
tmux attach -t whisper

# สร้าง window ใหม่: Ctrl+B C
# Window 0: ถอดเสียง
# Window 1: เช็คสถานะ (whisper_status.py)
# Window 2: ดู logs

# สลับระหว่าง windows: Ctrl+B 0, Ctrl+B 1, Ctrl+B 2
```

### 3. แบ่ง panes ดูพร้อมกัน
```bash
# ใน tmux
# แบ่ง pane แนวนอน: Ctrl+B "

# บน: ถอดเสียง (กำลังรัน)
# ล่าง: เช็คสถานะ (whisper_status.py --watch)

# เห็นทั้งสองอย่างพร้อมกัน!
```

---

## 🔧 Config (Advanced)

### เปลี่ยน Prefix Key (ถ้าไม่ชอบ Ctrl+B)

สร้างไฟล์ `~/.tmux.conf`:

```bash
# เปลี่ยน prefix เป็น Ctrl+A
unbind C-b
set-option -g prefix C-a
bind-key C-a send-prefix

# เปิด mouse support
set -g mouse on

# เพิ่มสี
set -g default-terminal "screen-256color"
```

Reload config:
```bash
tmux source-file ~/.tmux.conf
```

---

## 📚 เพิ่มเติม

### Official Docs
- https://github.com/tmux/tmux/wiki

### คีย์ลัดทั้งหมด
```bash
# พิมพ์ใน tmux
Ctrl+B ?

# แสดงรายการคีย์ลัดทั้งหมด
# กด Q เพื่อออก
```

---

## 🎉 สรุป

**ที่ใช้บ่อยที่สุด:**
- `tmux new -s NAME` - สร้าง session
- `tmux ls` - ดู sessions
- `tmux attach -t NAME` - เข้าไปดู session
- `Ctrl+B` แล้ว `D` - Detach (ออกแต่ยังรัน)
- `Ctrl+B` แล้ว `[` - Scroll mode (เลื่อนดู)

**จำง่ายๆ:**
- `Ctrl+B` = Prefix (ต้องกดก่อนเสมอ)
- `D` = Detach (ออก)
- `C` = Create window (สร้าง)
- `[` = Browse/Scroll (เลื่อน)

---

**เขียนโดย:** Claude Code
**วันที่:** October 2025
**สำหรับ:** Paperspace Whisper Transcription Project
