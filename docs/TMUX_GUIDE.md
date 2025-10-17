# 🖥️ tmux Complete Guide for Paperspace

**Date:** 2025-10-17
**Purpose:** Master tmux for reliable long-running tasks on Paperspace
**Target:** Paperspace users running transcription/translation workflows

---

## 📖 Table of Contents

1. [What is tmux?](#what-is-tmux)
2. [Why Use tmux on Paperspace?](#why-use-tmux-on-paperspace)
3. [Installation](#installation)
4. [Basic Usage](#basic-usage)
5. [Essential Commands](#essential-commands)
6. [Practical Examples](#practical-examples)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)
9. [Advanced Usage](#advanced-usage)
10. [Quick Reference](#quick-reference)

---

## 🎯 What is tmux?

**tmux** (Terminal Multiplexer) is a tool that lets you:

- ✅ **Run processes in background** (even when you close browser)
- ✅ **Detach and reattach** to sessions anytime
- ✅ **Survive connection drops** (work continues)
- ✅ **Multiple terminal windows** in one screen
- ✅ **Session persistence** across disconnects

**In simple terms:** A virtual terminal that keeps running even when you're not looking at it!

---

## 🚀 Why Use tmux on Paperspace?

### Problems tmux Solves:

| Problem | Without tmux | With tmux |
|---------|-------------|-----------|
| **Close browser** | ❌ Work stops | ✅ Work continues |
| **Connection drops** | ❌ Work lost | ✅ Work continues |
| **Long tasks (hours)** | ❌ Must watch screen | ✅ Check later |
| **Machine timeout** | ❌ Start over | ✅ Resume from checkpoint |

### Real Example:

```
Task: Transcribe 6 videos (2 hours total)

WITHOUT tmux:
- Must keep browser open for 2 hours
- If connection drops → lose progress
- Can't do anything else

WITH tmux:
- Start transcription
- Detach (Ctrl+B D)
- Close browser
- Go have lunch
- Come back 2 hours later
- Reattach (tmux attach)
- See completed results!
```

---

## 🔧 Installation

### Check if tmux is installed:

```bash
tmux -V
```

**If you see:** `tmux 3.2a` (or any version) → ✅ Already installed!

**If you see:** `command not found` → Install:

```bash
# Ubuntu/Debian (Paperspace)
apt-get update && apt-get install -y tmux

# Verify installation
tmux -V
```

---

## 📖 Basic Usage

### 1. Create a New Session

```bash
# Create session (automatic name)
tmux

# Create session with custom name
tmux new -s my-session-name

# Example: Create session for transcription
tmux new -s transcribe
```

**You'll see:**
- Green status bar at bottom
- Session name in brackets: `[transcribe]`

---

### 2. Run Your Task

```bash
# Inside tmux session, run your task
bash paperspace/transcribe_ss1.5_all.sh

# Or any long-running command
python train.py
./long_script.sh
```

---

### 3. Detach (Leave session running)

**Method 1: Keyboard shortcut**
```
Press: Ctrl+B
Release both keys
Press: D
```

**You'll see:**
```
[detached (from session transcribe)]
```

**Method 2: Command**
```bash
# Inside tmux session
tmux detach
```

**What happens:**
- ✅ You exit tmux
- ✅ Session keeps running in background
- ✅ Task continues working
- ✅ Can close browser safely

---

### 4. List Sessions

```bash
# See all running sessions
tmux ls

# Example output:
# transcribe: 1 windows (created Fri Oct 17 02:44:11 2025)
# training: 1 windows (created Fri Oct 17 01:30:00 2025)
```

---

### 5. Reattach (Return to session)

```bash
# Attach to session by name
tmux attach -t transcribe

# Or shorter version
tmux a -t transcribe

# If only one session, just:
tmux attach
```

**You'll see:**
- Back in the session
- See current progress
- Continue where you left off

---

### 6. Kill Session

```bash
# Kill specific session
tmux kill-session -t transcribe

# Kill all sessions
tmux kill-server

# Inside session: Ctrl+D or type 'exit'
```

---

## 🎮 Essential Commands

### Keyboard Shortcuts

**All shortcuts start with Ctrl+B (called "prefix key")**

| Command | Keys | What it does |
|---------|------|--------------|
| **Detach** | `Ctrl+B` then `D` | Leave session (keeps running) |
| **List sessions** | `Ctrl+B` then `S` | Show all sessions |
| **Rename session** | `Ctrl+B` then `$` | Change session name |
| **New window** | `Ctrl+B` then `C` | Create new window in session |
| **Next window** | `Ctrl+B` then `N` | Switch to next window |
| **Previous window** | `Ctrl+B` then `P` | Switch to previous window |
| **Split horizontal** | `Ctrl+B` then `"` | Split screen horizontally |
| **Split vertical** | `Ctrl+B` then `%` | Split screen vertically |
| **Switch pane** | `Ctrl+B` then arrow keys | Move between panes |
| **Close pane** | `Ctrl+D` or `exit` | Close current pane |
| **Help** | `Ctrl+B` then `?` | Show all shortcuts |

---

### Command-line Commands

```bash
# Create sessions
tmux new -s name                # New session with name
tmux new -s name -d             # New session detached

# Attach to sessions
tmux attach -t name             # Attach to session
tmux attach                     # Attach to last session

# List and info
tmux ls                         # List all sessions
tmux info                       # Show tmux info

# Kill sessions
tmux kill-session -t name       # Kill specific session
tmux kill-session -a            # Kill all except current
tmux kill-server                # Kill tmux server (all sessions)

# Rename session
tmux rename-session -t old new  # Rename session
```

---

## 🎬 Practical Examples

### Example 1: Simple Transcription

```bash
# 1. Create session
tmux new -s transcribe

# 2. Start transcription
cd /notebooks/video-translater
bash paperspace/transcribe_ss1.5_all.sh

# 3. Detach
Press: Ctrl+B then D

# 4. Close browser, go do something else

# 5. Come back later
tmux attach -t transcribe

# 6. Check if done
# If done, exit normally: Ctrl+D
```

---

### Example 2: Multiple Videos (Parallel)

```bash
# Create session with multiple windows
tmux new -s batch

# Window 1: EP-01
python whisper_transcribe.py video1.mp4
Ctrl+B then C (create new window)

# Window 2: EP-02
python whisper_transcribe.py video2.mp4
Ctrl+B then C (create new window)

# Window 3: EP-03
python whisper_transcribe.py video3.mp4

# Switch between windows:
Ctrl+B then N (next)
Ctrl+B then P (previous)
Ctrl+B then 0-9 (window number)

# Detach all
Ctrl+B then D
```

---

### Example 3: Monitor Progress

```bash
# Create session with split screen
tmux new -s monitor

# Split horizontally
Ctrl+B then "

# Top pane: Run transcription
bash paperspace/transcribe_ss1.5_all.sh

# Switch to bottom pane
Ctrl+B then arrow keys

# Bottom pane: Monitor progress
watch -n 5 'ls -lh workflow/01_transcripts/'

# Now you can see both at once!
# Detach: Ctrl+B then D
```

---

### Example 4: Run and Detach Immediately

```bash
# Create detached session and run command
tmux new -s transcribe -d "bash paperspace/transcribe_ss1.5_all.sh"

# Session is created and running in background immediately!

# Check later
tmux attach -t transcribe
```

---

### Example 5: Keep Session Open After Command

```bash
# Problem: Session closes when script finishes
# Solution: Keep bash shell open

tmux new -s transcribe bash -c "
    bash paperspace/transcribe_ss1.5_all.sh;
    exec bash
"

# Now session stays open even after script finishes
# Good for checking results or errors
```

---

## 🐛 Troubleshooting

### Issue 1: "no server running on /tmp/tmux-xxx"

**Cause:** tmux server not started or crashed

**Solution:**
```bash
# Start new session (will start server)
tmux new -s test

# If persists, kill and restart
tmux kill-server
tmux new -s test
```

---

### Issue 2: "session not found"

**Cause:** Session doesn't exist or was killed

**Solution:**
```bash
# List all sessions
tmux ls

# If empty, create new session
tmux new -s transcribe
```

---

### Issue 3: Can't see green status bar

**Cause:** Not inside tmux session

**Solution:**
```bash
# Check if in tmux
echo $TMUX

# If empty, not in tmux
# Create or attach to session
tmux new -s test
```

---

### Issue 4: Ctrl+B doesn't work

**Cause:** Wrong key combination or timing

**Solution:**
```
Correct way:
1. Press Ctrl+B together
2. Release BOTH keys
3. Press next key (like D)

NOT:
1. Hold Ctrl+B+D all together (WRONG!)
```

**Test:**
```
Try: Ctrl+B then ?
Should show help menu
If works, Ctrl+B is working correctly
```

---

### Issue 5: Session closes immediately

**Cause:** Command finished or errored

**Solution:**
```bash
# Keep session open with exec bash
tmux new -s test bash -c "
    your-command;
    exec bash
"

# Or run interactively
tmux new -s test
# Then run commands inside
```

---

### Issue 6: "sessions should be nested with care"

**Cause:** Trying to run tmux inside tmux

**Solution:**
```bash
# Exit inner tmux first
exit
# Or Ctrl+D

# Then create new session
tmux new -s new-session
```

---

### Issue 7: Lost session name

**Solution:**
```bash
# List all sessions
tmux ls

# Attach by session number
tmux attach -t 0

# Rename inside session
Ctrl+B then $
# Type new name
```

---

### Issue 8: Too many dead sessions

**Solution:**
```bash
# List all sessions
tmux ls

# Kill specific session
tmux kill-session -t old-name

# Kill all except current
tmux kill-session -a

# Nuclear option (kill all)
tmux kill-server
```

---

## 💡 Best Practices

### 1. Always Name Your Sessions

```bash
# ❌ BAD (automatic names like 0, 1, 2)
tmux new

# ✅ GOOD (descriptive names)
tmux new -s transcribe-ep01
tmux new -s training-model
tmux new -s download-videos
```

---

### 2. One Task Per Session

```bash
# ✅ GOOD
tmux new -s transcribe  # For transcription only
tmux new -s translate   # For translation only

# ❌ AVOID (confusing)
tmux new -s everything  # Running many different tasks
```

---

### 3. Use Meaningful Names

```bash
# ✅ GOOD
tmux new -s ss1.5-transcribe
tmux new -s model-training-v2
tmux new -s data-download

# ❌ BAD
tmux new -s test
tmux new -s tmp
tmux new -s asdf
```

---

### 4. Clean Up Old Sessions

```bash
# Weekly cleanup
tmux ls  # See all sessions
tmux kill-session -t old-name  # Kill finished ones
```

---

### 5. Check Before Creating

```bash
# Before creating new session, check existing
tmux ls

# If session exists, attach instead of creating new
tmux attach -t transcribe
```

---

### 6. Use Detach, Not Close

```bash
# ✅ GOOD (task continues)
Ctrl+B then D  # Detach

# ❌ BAD (task stops!)
Ctrl+C  # Kill task
exit    # Exit session
```

---

### 7. Document Your Sessions

```bash
# Keep notes of what's running
tmux ls  # List sessions

# Example naming convention:
# project-task-date
tmux new -s video-transcribe-oct17
tmux new -s model-train-oct17
```

---

## 🚀 Advanced Usage

### Custom tmux Configuration

Create `~/.tmux.conf`:

```bash
# Better key bindings
unbind C-b
set -g prefix C-a  # Use Ctrl+A instead of Ctrl+B

# Mouse support
set -g mouse on

# Better colors
set -g default-terminal "screen-256color"

# Longer history
set -g history-limit 10000

# Start windows at 1 instead of 0
set -g base-index 1

# Reload config
bind r source-file ~/.tmux.conf \; display "Config reloaded!"
```

**Apply config:**
```bash
# Inside tmux
Ctrl+B then :
source-file ~/.tmux.conf
```

---

### Scripted Session Creation

Create `start-transcription.sh`:

```bash
#!/bin/bash

SESSION="transcribe-$(date +%Y%m%d)"

# Create session
tmux new-session -d -s "$SESSION"

# Rename window
tmux rename-window -t "$SESSION:0" "main"

# Run transcription
tmux send-keys -t "$SESSION:0" "cd /notebooks/video-translater" C-m
tmux send-keys -t "$SESSION:0" "bash paperspace/transcribe_ss1.5_all.sh" C-m

# Create monitoring window
tmux new-window -t "$SESSION:1" -n "monitor"
tmux send-keys -t "$SESSION:1" "watch -n 5 'ls -lh workflow/01_transcripts/'" C-m

# Attach to session
tmux attach -t "$SESSION"
```

**Usage:**
```bash
bash start-transcription.sh
```

---

### Session Management Script

```bash
#!/bin/bash
# save as: tmux-manager.sh

case "$1" in
    list)
        tmux ls
        ;;
    create)
        tmux new -s "$2"
        ;;
    attach)
        tmux attach -t "$2"
        ;;
    kill)
        tmux kill-session -t "$2"
        ;;
    cleanup)
        tmux kill-session -a
        echo "All sessions except current killed"
        ;;
    *)
        echo "Usage: $0 {list|create|attach|kill|cleanup} [session-name]"
        exit 1
        ;;
esac
```

**Usage:**
```bash
bash tmux-manager.sh list
bash tmux-manager.sh create transcribe
bash tmux-manager.sh attach transcribe
bash tmux-manager.sh kill transcribe
bash tmux-manager.sh cleanup
```

---

## 📋 Quick Reference

### Essential 5 Commands (Remember These!)

```bash
# 1. Create session
tmux new -s name

# 2. Detach
Ctrl+B then D

# 3. List sessions
tmux ls

# 4. Reattach
tmux attach -t name

# 5. Kill session
tmux kill-session -t name
```

---

### Keyboard Shortcuts Cheat Sheet

```
Ctrl+B D    → Detach
Ctrl+B C    → New window
Ctrl+B N    → Next window
Ctrl+B P    → Previous window
Ctrl+B "    → Split horizontal
Ctrl+B %    → Split vertical
Ctrl+B ←→↑↓ → Switch panes
Ctrl+B ?    → Help
```

---

### Command Cheat Sheet

```bash
# Sessions
tmux new -s name          # Create
tmux attach -t name       # Attach
tmux ls                   # List
tmux kill-session -t name # Kill

# Inside session
exit                      # Exit
Ctrl+D                    # Exit
tmux detach              # Detach
```

---

## 🎯 tmux for Paperspace Transcription

### Complete Workflow Example

```bash
# ===== Day 1: Start Work =====

# 1. SSH to Paperspace
ssh root@paperspace

# 2. Create tmux session
tmux new -s ss1.5-transcribe

# 3. Navigate to project
cd /notebooks/video-translater

# 4. Start transcription
bash paperspace/transcribe_ss1.5_all.sh

# 5. Detach and close browser
Press: Ctrl+B then D
# >>> Can now close browser safely! <<<

# ===== Hours Later: Check Progress =====

# 6. SSH back to Paperspace
ssh root@paperspace

# 7. List sessions
tmux ls

# 8. Reattach to session
tmux attach -t ss1.5-transcribe

# 9. See current progress
# [Watching progress bar...]

# 10. Detach again if not done
Press: Ctrl+B then D

# ===== Day 2: Retrieve Results =====

# 11. SSH to Paperspace
ssh root@paperspace

# 12. Reattach
tmux attach -t ss1.5-transcribe

# 13. If complete, exit normally
Press: Ctrl+D

# 14. Download results
scp paperspace:/notebooks/video-translater/workflow/01_transcripts/*.json ./local/
```

---

## 📊 tmux vs. No tmux Comparison

| Scenario | Without tmux | With tmux |
|----------|-------------|-----------|
| **5-hour transcription** | Must watch screen 5 hours | Detach, check once after 5 hours |
| **Connection drops** | Start over | Resume where left off |
| **Browser crash** | All work lost | No impact, work continues |
| **Check progress** | Can't, must wait | Reattach anytime to check |
| **Multiple tasks** | One at a time | Run many sessions in parallel |
| **Error occurred?** | Lost, no logs | Reattach to see error |

---

## ✅ Success Checklist

- [ ] tmux installed (`tmux -V`)
- [ ] Know how to create session (`tmux new -s name`)
- [ ] Know how to detach (`Ctrl+B D`)
- [ ] Know how to list sessions (`tmux ls`)
- [ ] Know how to reattach (`tmux attach -t name`)
- [ ] Practiced once with test session
- [ ] Understand when to use tmux (long tasks)
- [ ] Know how to kill session (`tmux kill-session -t name`)

---

## 🆘 Getting Help

### Inside tmux:
```
Press: Ctrl+B then ?
Shows all keyboard shortcuts
Press Q to exit help
```

### Command line:
```bash
man tmux           # Full manual
tmux --help        # Basic help
```

### Online Resources:
- tmux GitHub Wiki: https://github.com/tmux/tmux/wiki
- tmux Cheat Sheet: https://tmuxcheatsheet.com/

---

## 🎓 Learning Path

**Beginner (Day 1):**
- Install tmux
- Create session
- Run simple command
- Detach
- Reattach
- Kill session

**Intermediate (Week 1):**
- Multiple windows
- Split panes
- Named sessions
- Session management

**Advanced (Month 1):**
- Custom configuration
- Scripted sessions
- Complex layouts
- Automation

---

**Made with ❤️ for Paperspace users**

**Last Updated:** 2025-10-17

**Status:** ✅ Production Ready

---

**🚀 Ready to master tmux? Start with the Essential 5 Commands above!**
