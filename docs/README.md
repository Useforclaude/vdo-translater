# 📚 Documentation Index

Complete documentation for the Thai Video Translation Pipeline.

---

## 🎯 Start Here

**New to the project?**
1. Read [../README.md](../README.md) - Project overview
2. Read [../QUICKSTART.md](../QUICKSTART.md) - Quick commands
3. Choose your guide below

---

## 📖 Documentation Categories

### 📚 [User Guides](guides/)
Step-by-step guides for using the system.

**Available guides:**
- **[PAPERSPACE_GUIDE.md](PAPERSPACE_GUIDE.md)** - Complete Paperspace workflow (1,600+ lines)
- **[TMUX_CHEATSHEET.md](TMUX_CHEATSHEET.md)** - tmux command reference (300+ lines)
- **[UTILITIES_GUIDE.md](guides/UTILITIES_GUIDE.md)** - Advanced utility scripts

**When to use:** Learning how to use the system

---

### 📖 [Reference Materials](reference/)
Technical reference and terminology.

**Available references:**
- **[Forex_Terminology_Guide.md](reference/Forex_Terminology_Guide.md)** - 50+ Forex terms (73KB)
- **[IDIOM_SYSTEM_IMPLEMENTATION.md](reference/IDIOM_SYSTEM_IMPLEMENTATION.md)** - 105 Thai idioms + 30 slang
- **[SYSTEM_REQUIREMENTS.md](reference/SYSTEM_REQUIREMENTS.md)** - Technical requirements

**When to use:** Looking up terminology, understanding system design

**Quick stats:**
- Forex terms: 50+
- Thai idioms: 105
- Thai slang: 30
- Total coverage: 185+ expressions

---

### 🤝 [Handover Documents](handover/)
Complete project context for developers.

**Available documents:**
- **[Project_Handover_Document.md](handover/Project_Handover_Document.md)** - Original project vision
- **[PROJECT_COMPLETE_SUMMARY.md](handover/PROJECT_COMPLETE_SUMMARY.md)** - Current status (60% complete)
- **[WORKFLOW_PROGRESS.md](handover/WORKFLOW_PROGRESS.md)** - Translation progress tracking
- **[RECOVERY_REPORT.md](handover/RECOVERY_REPORT.md)** - System resilience
- **[claude_handover_complete.md](handover/claude_handover_complete.md)** - Claude-specific handover
- **[CLAUDE_CODE_WORKFLOW.md](handover/CLAUDE_CODE_WORKFLOW.md)** - Development workflow

**When to use:**
- Starting new development session
- Understanding project architecture
- Maintaining the system

**Project status:**
- ✅ Core modules: 6/10 complete
- ⏳ Integration: In progress
- 📋 TODO: 4 modules remaining

---

## 🗂️ Other Documentation

### [../scripts/README.md](../scripts/README.md)
Complete scripts documentation.

**Main scripts:**
- whisper_transcribe.py - Transcribe audio
- whisper_status.py - Check progress
- merge_transcripts.py - Merge chunks
- create_translation_batch.py - Prepare translation
- batch_to_srt.py - Generate SRT

**Utilities:** [../scripts/utilities/](../scripts/utilities/)

---

### [../src/README.md](../src/README.md)
Core modules documentation.

**Modules:**
- config.py - Configuration management
- context_analyzer.py - Two-pass analysis
- translation_pipeline.py - Smart translation
- thai_transcriber.py - Thai-optimized Whisper
- data_management_system.py - Dictionary management

---

### [../workflow/README.md](../workflow/README.md)
Workflow directory guide.

**Stages:**
1. 01_transcripts/ - Thai transcripts
2. 02_for_translation/ - Translation batches
3. 03_translated/ - English translations
4. 04_final_srt/ - Final SRT files

---

## 🎯 Quick Navigation

### By Task

| I want to... | Go to... |
|-------------|----------|
| **Start using the system** | [../README.md](../README.md) → [../QUICKSTART.md](../QUICKSTART.md) |
| **Use Paperspace** | [PAPERSPACE_GUIDE.md](PAPERSPACE_GUIDE.md) |
| **Learn tmux** | [TMUX_CHEATSHEET.md](TMUX_CHEATSHEET.md) |
| **Look up Forex terms** | [reference/Forex_Terminology_Guide.md](reference/Forex_Terminology_Guide.md) |
| **Understand idioms** | [reference/IDIOM_SYSTEM_IMPLEMENTATION.md](reference/IDIOM_SYSTEM_IMPLEMENTATION.md) |
| **Start development** | [handover/](handover/) |
| **Use utility scripts** | [guides/UTILITIES_GUIDE.md](guides/UTILITIES_GUIDE.md) |
| **Understand modules** | [../src/README.md](../src/README.md) |

### By Role

| I am a... | Start here... |
|-----------|--------------|
| **New user** | [../README.md](../README.md) |
| **Paperspace user** | [PAPERSPACE_GUIDE.md](PAPERSPACE_GUIDE.md) |
| **Translator** | [reference/](reference/) → Terminology guides |
| **Developer** | [handover/](handover/) → [../src/README.md](../src/README.md) |
| **Maintainer** | [handover/RECOVERY_REPORT.md](handover/RECOVERY_REPORT.md) |

---

## 📊 Documentation Statistics

| Category | Files | Lines | Key Info |
|----------|-------|-------|----------|
| **User Guides** | 3 | 2,200+ | Complete workflows |
| **Reference** | 3 | 100+ pages | 185+ terms/idioms |
| **Handover** | 6 | 500+ | 60% complete |
| **Scripts** | 10+ | 3,000+ | 10 scripts |
| **Core Modules** | 5 | 2,000+ | 5 modules |
| **Total** | 30+ | 8,000+ | Complete system |

---

## 🔍 Search Tips

**Looking for specific info?**

```bash
# Search all documentation
grep -r "your search term" docs/

# Search specific category
grep -r "Forex" docs/reference/
grep -r "tmux" docs/guides/
grep -r "checkpoint" docs/handover/
```

---

## 📞 Still Can't Find It?

1. **Check [../README.md](../README.md)** - Main overview
2. **Check [../CLAUDE.md](../CLAUDE.md)** - Complete project context
3. **Check [../SESSION_RESUME.md](../SESSION_RESUME.md)** - Session continuity

---

## 🔄 Document Updates

**Last major reorganization:** October 8, 2025

**Changes:**
- ✅ Organized into categories (guides, reference, handover)
- ✅ Created README in each directory
- ✅ Removed duplicate documents
- ✅ Updated cross-references
- ✅ Cleaned up root directory

**Previous location:** Many docs were in project root

---

**Back to [Project Root](../)**
