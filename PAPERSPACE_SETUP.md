# 🛠️ Paperspace Setup Guide

> Complete setup instructions for first-time Paperspace users

---

## 📋 Prerequisites

- Paperspace account with GPU machine
- Internet connection
- Basic terminal knowledge

---

## 🚀 Complete Setup (Step-by-Step)

### Step 1: Connect to Paperspace

```bash
# Connect via web terminal or SSH
# Web: https://console.paperspace.com/
# SSH: ssh paperspace@your-machine-ip
```

---

### Step 2: Install gdown (Required for Video Download)

```bash
# Method 1: Global install (recommended)
pip install --upgrade gdown

# Method 2: User install (if permission denied)
pip install --user --upgrade gdown

# Method 3: Latest from GitHub
pip install --upgrade git+https://github.com/wkentaro/gdown.git

# Verify installation
gdown --version
which gdown
# Should output: gdown, version X.X.X
```

**Common Issues:**
```bash
# If "command not found" after install:
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

### Step 3: Clone Project from GitHub

```bash
# Navigate to notebooks directory
cd /notebooks

# Clone repository
git clone https://github.com/Useforclaude/vdo-translater.git

# Enter project directory
cd vdo-translater

# Verify structure
ls -lh
# Should see: scripts/, workflow/, README.md, etc.
```

---

### Step 4: Setup Python Virtual Environment

```bash
cd /notebooks/vdo-translater

# Create virtual environment
python3 -m venv .venv

# Activate (optional for manual commands)
source .venv/bin/activate

# Install dependencies
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

# Install gdown in venv (optional)
.venv/bin/pip install gdown

# Verify Whisper installation
.venv/bin/python -c "import whisper; print('Whisper OK')"
```

---

### Step 5: Fix Script Line Endings (Important!)

```bash
cd /notebooks/vdo-translater

# Convert Windows CRLF to Unix LF
sed -i 's/\r$//' scripts/download_videos.sh
sed -i 's/\r$//' scripts/paperspace_transcribe.sh

# Make scripts executable
chmod +x scripts/*.sh

# Verify fix
file scripts/download_videos.sh
# Should see: "UTF-8 text executable" (NO "CRLF"!)
```

---

### Step 6: Create Persistent Storage Directories

```bash
# Create directories in /storage (persistent across sessions)
mkdir -p /storage/videos
mkdir -p /storage/whisper_checkpoints
mkdir -p /storage/transcripts

# Verify
ls -lh /storage/
```

---

### Step 7: Install tmux (For Background Processes)

```bash
# Check if tmux exists
which tmux

# If not installed:
apt-get update
apt-get install -y tmux

# Verify
tmux -V
# Should output: tmux X.X
```

---

### Step 8: Test Setup

```bash
cd /notebooks/vdo-translater

# Test 1: Check scripts exist
ls -lh scripts/download_videos.sh
ls -lh scripts/paperspace_transcribe.sh

# Test 2: Test download script
bash scripts/download_videos.sh list
# Should show available videos

# Test 3: Test gdown directly
gdown --help
# Should show gdown help

# Test 4: Test Whisper
.venv/bin/python -c "
import whisper
print('Whisper version:', whisper.__version__)
model = whisper.load_model('base')
print('Model loaded successfully!')
"
```

---

## ✅ Quick Setup Script (All-in-One)

Copy-paste this entire block:

```bash
#!/bin/bash
# ========================================
# Paperspace Complete Setup
# ========================================

echo "Step 1: Installing gdown..."
pip install --upgrade gdown

echo "Step 2: Cloning repository..."
cd /notebooks
[ ! -d "vdo-translater" ] && git clone https://github.com/Useforclaude/vdo-translater.git
cd vdo-translater

echo "Step 3: Pulling latest code..."
git pull origin main

echo "Step 4: Fixing line endings..."
sed -i 's/\r$//' scripts/download_videos.sh scripts/paperspace_transcribe.sh
chmod +x scripts/*.sh

echo "Step 5: Setting up Python environment..."
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install gdown

echo "Step 6: Creating storage directories..."
mkdir -p /storage/videos
mkdir -p /storage/whisper_checkpoints

echo "Step 7: Testing setup..."
gdown --version
.venv/bin/python -c "import whisper; print('Whisper OK')"
bash scripts/download_videos.sh list

echo "========================================
✅ Setup Complete!
========================================

Next steps:
1. Download video: bash scripts/download_videos.sh 01
2. Transcribe: bash scripts/paperspace_transcribe.sh 01
3. Detach: Ctrl+B then D

For help: cat PAPERSPACE_QUICKSTART.md
"
```

---

## 🔍 Verification Checklist

After setup, verify everything works:

- [ ] `gdown --version` → Shows version number
- [ ] `which gdown` → Shows path (e.g., `/usr/local/bin/gdown`)
- [ ] `ls scripts/download_videos.sh` → File exists
- [ ] `file scripts/download_videos.sh` → No "CRLF" in output
- [ ] `bash scripts/download_videos.sh list` → Shows video list
- [ ] `.venv/bin/python -c "import whisper"` → No errors
- [ ] `tmux -V` → Shows tmux version
- [ ] `ls /storage/videos/` → Directory exists

---

## ⚠️ Common Issues & Solutions

### Issue 1: `gdown: command not found`

**Solution:**
```bash
# Add to PATH
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Or reinstall globally
sudo pip install --upgrade gdown
```

### Issue 2: `$'\r': command not found`

**Solution:**
```bash
# Fix line endings
cd /notebooks/vdo-translater
sed -i 's/\r$//' scripts/*.sh
chmod +x scripts/*.sh
```

### Issue 3: `Permission denied`

**Solution:**
```bash
# Make scripts executable
chmod +x scripts/download_videos.sh scripts/paperspace_transcribe.sh

# Or run with bash
bash scripts/download_videos.sh 01
```

### Issue 4: `CUDA out of memory`

**Solution:**
```bash
# Use CPU mode
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/ep01.mp4 \
  --device cpu

# Or use smaller model
.venv/bin/python scripts/whisper_transcribe.py \
  /storage/videos/ep01.mp4 \
  --model medium
```

### Issue 5: `git pull` fails

**Solution:**
```bash
cd /notebooks/vdo-translater

# Reset local changes
git reset --hard origin/main
git pull origin main
```

---

## 📊 Storage Recommendations

| Path | Purpose | Size Needed | Persistent? |
|------|---------|-------------|-------------|
| `/storage/videos/` | Downloaded videos | ~10-20GB | ✅ Yes |
| `/storage/whisper_checkpoints/` | Transcription checkpoints | ~100MB | ✅ Yes |
| `/notebooks/vdo-translater/` | Project code | ~50MB | ❌ No (use git) |
| `/notebooks/vdo-translater/.venv/` | Python packages | ~2GB | ❌ No (reinstall) |

**Important:** Only `/storage/` persists across Paperspace sessions!

---

## 🚀 Ready to Use!

After setup, start transcribing:

```bash
cd /notebooks/vdo-translater

# Download video
bash scripts/download_videos.sh 01

# Start transcription (auto-tmux)
bash scripts/paperspace_transcribe.sh 01

# Detach: Ctrl+B then D
# Check progress: .venv/bin/python scripts/whisper_status.py --watch
```

---

## 📚 Next Steps

- **Quick Commands:** See [PAPERSPACE_COMMANDS.txt](PAPERSPACE_COMMANDS.txt)
- **Quick Start:** See [PAPERSPACE_QUICKSTART.md](PAPERSPACE_QUICKSTART.md)
- **Full Guide:** See [docs/PAPERSPACE_GUIDE.md](docs/PAPERSPACE_GUIDE.md)

---

**Setup Time:** ~5-10 minutes
**Status:** Ready for production use
**Last Updated:** 2025-10-12
