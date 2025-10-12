# 🎯 CLAUDE.md - Thai→English Video Translation Pipeline

> **Project Handover Document for Claude Code**
> Complete guide to continue development of Thai Forex video translation system

---

## 🔄 SESSION CONTINUITY PROTOCOL - ALWAYS READ THIS FIRST!

> **CRITICAL: Read this section at the START of EVERY new session!**
> This ensures seamless continuity even after power outages, disconnects, or days/weeks between sessions.

---

### 🎯 MANDATORY: First Actions on New Session

**EVERY TIME you start a new Claude Code session, perform these steps IN ORDER:**

#### Step 1: Read Session Resume File (5 seconds)
```bash
# Read this FIRST - it tells you exactly what to do
cat SESSION_RESUME.md
```

**What this tells you:**
- ✅ Current project status
- ✅ Last task completed
- ✅ Next task to do
- ✅ Files to read
- ✅ Context needed

#### Step 2: Read Translation Checkpoint (if exists)
```bash
# Check if translation work is in progress
cat workflow/.translation_checkpoint.txt 2>/dev/null
```

**What to look for:**
- Progress percentage (e.g., 100/277 = 36%)
- Last completed segment
- Next segment to do
- Translation style notes

#### Step 3: Check Last Modified Files
```bash
# See what was worked on recently
ls -lt workflow/03_translated/*.txt 2>/dev/null | head -5
ls -lt colab/*.ipynb 2>/dev/null | head -2
```

**This reveals:**
- Which video is being translated
- How recent the work is
- If work is in progress

#### Step 4: Announce Status
```
After reading the above, ALWAYS respond with:

📊 Session Status:
- Project: [project name]
- Last worked: [date from checkpoint]
- Progress: [X/Y done, Z%]
- Current task: [what's in progress]
- Next action: [what to do next]

Ready to continue? [Yes/No/Need more context]
```

---

### 🚨 NEVER Skip Session Resume

**DON'T:**
❌ Start working without reading SESSION_RESUME.md
❌ Ask user "what do you want to do?" (YOU should know from files!)
❌ Assume you remember context from "previous" sessions
❌ Start from scratch on an existing task

**DO:**
✅ Read SESSION_RESUME.md FIRST
✅ Read checkpoint files
✅ Announce current status
✅ Ask clarification ONLY if files are unclear
✅ Resume exactly where work stopped

---

### 📁 Critical State Files (Read These on Session Start)

**Priority 1 - Always Read:**
1. `SESSION_RESUME.md` - Master session guide
2. `workflow/.translation_checkpoint.txt` - Translation progress
3. `WORKFLOW_PROGRESS.md` - Overall project status

**Priority 2 - Read if Relevant:**
4. Last modified file in `workflow/03_translated/` - Current translation
5. Last modified file in `workflow/02_for_translation/` - Source material
6. `colab/hybrid_workflow.ipynb` - If doing transcription

**Priority 3 - Reference Only:**
7. `CLAUDE.md` (this file) - Full documentation
8. `UTILITIES_GUIDE.md` - Tool usage

---

### 🎯 How to Recognize Context from Files

#### Translation in Progress:
```bash
# If this shows segments < total (e.g., 100/277)
grep "Progress:" workflow/.translation_checkpoint.txt

# You should:
1. Read the checkpoint file
2. Note last completed segment
3. Continue from next segment
4. Maintain same translation style
```

#### Fresh Start:
```bash
# If checkpoint doesn't exist or shows "COMPLETED"
ls workflow/.translation_checkpoint.txt

# You should:
1. Check SESSION_RESUME.md for next task
2. Ask user to confirm direction
```

#### Colab Work:
```bash
# If notebook was recently modified
ls -lt colab/*.ipynb | head -1

# You should:
1. Check what improvements were made
2. Verify if testing is needed
3. Update documentation if needed
```

---

### 💾 Auto-Update Checkpoints

**ALWAYS update checkpoint files when:**

1. **Completing a translation batch** (every 20 segments):
```bash
# Update checkpoint with progress
echo "Last completed: Segment 120" >> workflow/.translation_checkpoint.txt
echo "Progress: 120/277 segments (43%)" >> workflow/.translation_checkpoint.txt
```

2. **Finishing a major task**:
```bash
# Mark as complete
echo "Status: COMPLETED - [date]" >> workflow/.translation_checkpoint.txt
```

3. **Switching tasks**:
```bash
# Document the switch
echo "Switched to: [new task] - [date]" >> SESSION_RESUME.md
```

---

### 🧠 Context Recovery Examples

#### Example 1: Power Outage During Translation

**User returns and says:** "Continue from last session"

**You should:**
```bash
# 1. Read session state
cat SESSION_RESUME.md
cat workflow/.translation_checkpoint.txt

# 2. Announce findings:
"I see translation was in progress:
- File: ep-01-19-12-24
- Completed: 100/277 segments (36%)
- Last: Segment 100
- Style: Casual teaching tone, context-aware
- Next: Continue from segment 101

Ready to resume translation?"
```

#### Example 2: Week Between Sessions

**User says:** "What was I working on?"

**You should:**
```bash
# 1. Check state files
cat SESSION_RESUME.md
ls -lt workflow/03_translated/ | head -3

# 2. Report:
"Last session (2025-10-04):
✅ Completed: Colab checkpoint system
✅ Completed: 100/277 segments translated
⏸️  Paused: Translation at segment 100
📋 Next: Translate segments 101-277

Would you like to continue translation or work on something else?"
```

---

### 🎓 User Intent Recognition

**When user says these, do this:**

| User Input | Your Action |
|------------|-------------|
| "Continue" / "Resume" / "ทำต่อ" | Read SESSION_RESUME.md → announce status → resume work |
| "What's next?" / "ต่อไปทำอะไร" | Read checkpoints → report status → suggest next steps |
| "Status?" / "ถึงไหนแล้ว" | Read progress files → report stats |
| "Start over" / "เริ่มใหม่" | ⚠️ CONFIRM before deleting progress! |
| [No context given] | ⚠️ READ SESSION_RESUME.md FIRST before asking! |

---

### ⚡ Quick Commands for Session Start

**Copy-paste these for fast context recovery:**

```bash
# Full context dump (use when totally lost)
echo "=== SESSION CONTEXT ===" && \
cat SESSION_RESUME.md && \
echo "\n=== TRANSLATION PROGRESS ===" && \
cat workflow/.translation_checkpoint.txt 2>/dev/null && \
echo "\n=== RECENT FILES ===" && \
ls -lt workflow/03_translated/ 2>/dev/null | head -3

# Quick status check
grep -E "(Progress|Status|Last completed)" workflow/.translation_checkpoint.txt

# Find what was worked on recently
find . -type f -mtime -7 -name "*.txt" -o -name "*.md" | head -10
```

---

### 🔒 Session Integrity Checklist

**Before EVERY work session, verify:**

- [ ] Read SESSION_RESUME.md
- [ ] Checked translation checkpoint
- [ ] Know current progress (X/Y segments)
- [ ] Know translation style to maintain
- [ ] Announced status to user
- [ ] Ready to continue seamlessly

**After completing work, verify:**

- [ ] Updated checkpoint file
- [ ] Saved all progress
- [ ] Documented what was done
- [ ] Ready for next session

---

### 🎯 Success Criteria

**You know you're doing it RIGHT when:**

✅ You can resume work within 30 seconds of session start
✅ User doesn't need to explain context again
✅ Translation style is consistent across sessions
✅ No duplicate work or starting from scratch
✅ Progress is never lost

**You know something is WRONG when:**

❌ You ask "what should I do?" (you should know from files!)
❌ User has to explain progress again
❌ You start translating from segment 1 (should resume from 101!)
❌ Translation tone changes between sessions
❌ You don't mention the checkpoint files

---

## 🚨 TRANSLATION PROTOCOL - MANDATORY READING BEFORE EVERY TRANSLATION

> **⚠️ CRITICAL: Read this ENTIRE section BEFORE starting ANY translation work!**
> Failure to follow this protocol will result in poor quality translations that must be redone.

---

### ❌ FORBIDDEN: Sequential Segment-by-Segment Translation

**YOU MUST NEVER DO THIS:**

```python
# ❌ WRONG - Translating segment-by-segment without full context
for segment in segments:
    translated = translate(segment)  # NO CONTEXT!
    output.append(translated)
```

**Why this is WRONG:**
- ❌ No understanding of overall topic
- ❌ Idioms translated literally (e.g., "พูดแต่เนื้อๆ" → "speak only meat")
- ❌ Missing context for slang/colloquialisms
- ❌ Inconsistent tone across segments
- ❌ Forex terms translated inconsistently
- ❌ Teaching flow becomes choppy

---

### ✅ REQUIRED: Strict Two-Pass Translation Method

**YOU MUST ALWAYS DO THIS:**

#### **Pass 1: FULL DOCUMENT ANALYSIS (No Translation Yet!)**

**Objective:** Understand EVERYTHING before translating ANYTHING

1. **Read the ENTIRE document** (all segments, start to finish)
   - Do NOT start translating yet
   - Read as a continuous story
   - Understand the teaching flow

2. **Extract and document:**
   ```
   📊 Document Analysis Checklist:
   - [ ] Main topic identified (e.g., "Dow Theory - Part 3")
   - [ ] Speaker's teaching style noted (casual/formal/technical)
   - [ ] All forex terms listed (แนวโน้ม, แท่งเทียน, etc.)
   - [ ] All idioms/metaphors identified (สูสี, วิ่ง, etc.)
   - [ ] All particles counted (ครับ, นะ, เนี้ย frequency)
   - [ ] Teaching structure mapped (intro → concepts → examples → conclusion)
   - [ ] Context summary written (200-300 words)
   ```

3. **Load translation dictionaries:**
   ```python
   # MUST load these BEFORE Pass 2
   forex_terms = load_json('data/dictionaries/forex_terms.json')
   colloquialisms = load_json('data/dictionaries/colloquialisms.json')
   metaphors = load_json('data/dictionaries/metaphors.json')
   ```

4. **Create Context Summary:**
   ```
   Must include:
   - Topic: [what is being taught]
   - Teaching tone: [casual/formal/mixed]
   - Key terminology: [list top 10 terms]
   - Metaphor domains: [military/automotive/physics/nature]
   - Particles to remove: [list frequency]
   - Special instructions: [any unique aspects]
   ```

**⚠️ CHECKPOINT: Do NOT proceed to Pass 2 until ALL items checked**

---

#### **Pass 2: CONTEXT-AWARE TRANSLATION**

**Objective:** Translate with FULL understanding of context

1. **Before starting, verify:**
   - [ ] Pass 1 is 100% complete
   - [ ] Context summary is ready
   - [ ] Dictionaries are loaded
   - [ ] You understand the topic

2. **Translate each segment using:**
   - ✅ Context from Pass 1
   - ✅ Forex term mappings (แนวโน้ม → Trend, NOT tendency)
   - ✅ Idiom contextual translation (สูสี → evenly matched, NOT compete color)
   - ✅ Consistent teaching tone
   - ✅ Remove Thai particles (ครับ, นะ, เนี้ย)
   - ✅ Natural English flow (use contractions: we'll, let's)

3. **Segment translation format:**
   ```
   [Segment X] timestamp
   English translation here

   [Segment X+1] timestamp
   Next translation
   ```

4. **Quality check every 50 segments:**
   - Verify tone consistency
   - Check no literal idiom translations
   - Ensure forex terms use English equivalents
   - Confirm natural English flow

---

### 📋 Pre-Translation Checklist (MUST Complete Before Starting)

**Before you type a SINGLE translated word, verify:**

- [ ] I have read this TRANSLATION PROTOCOL section completely
- [ ] I have read CLAUDE.md Idiom & Slang Handling section
- [ ] I have loaded all 3 dictionaries (forex, colloquial, metaphors)
- [ ] I have read the ENTIRE source document (all segments)
- [ ] I have created a Context Summary (200+ words)
- [ ] I understand the topic being taught
- [ ] I know the speaker's tone/style
- [ ] I have identified all idioms and their contextual meanings
- [ ] I am ready to translate WITH CONTEXT, not segment-by-segment

**If ANY checkbox is unchecked → STOP and complete it first**

---

### 🎯 Translation Quality Standards

**Your translation MUST meet these criteria:**

1. **Idiom Translation: 100% Contextual**
   - ❌ WRONG: "พูดแต่เนื้อๆ" → "speak only meat"
   - ✅ RIGHT: "พูดแต่เนื้อๆ" → "get straight to the point"

2. **Forex Terms: 100% English Equivalents**
   - ❌ WRONG: "แนวโน้ม" → "tendency line"
   - ✅ RIGHT: "แนวโน้ม" → "trend"

3. **Particles: 100% Removed**
   - ❌ WRONG: "Good right polite-particle"
   - ✅ RIGHT: "Looks good"

4. **Tone: 100% Consistent**
   - If segment 1 is casual → all segments must be casual
   - Use contractions: "we'll" not "we will"
   - Keep teaching enthusiasm: "This is important!", "Check this out!"

5. **Natural English: 100% Readable**
   - ❌ WRONG: "Price it move up continue go"
   - ✅ RIGHT: "Price continues moving up"

---

### 🔍 Examples: WRONG vs RIGHT Approach

#### ❌ WRONG Approach (Sequential Translation)

```
Translator starts immediately without reading full document:

Segment 1: "สวัสดีครับ ก็มาถึงอีก Part 1"
Think: "Hello, we reach Part 1"
Translate: "Hello, we have reached Part 1 again"

Segment 2: "เรื่องของแท่งเทียน"
Think: "About candle bars"
Translate: "About candle bars"  ← WRONG! Should be "candlesticks"

Segment 50: "มันสูสีกัน"
Think: "They compete color each other"
Translate: "They compete with each other"  ← WRONG! No context for "สูสี"

Result: Poor quality, literal translations, missing context
```

#### ✅ RIGHT Approach (Two-Pass Method)

```
Pass 1: Read all 479 segments first
- Topic identified: Dow Theory (Part 3 of Price Action series)
- Tone: Casual teaching, friendly instructor
- Key terms found: แนวโน้ม (trend, 20x), แท่งเทียน (candlestick, 13x)
- Idioms found: สูสี (evenly matched, 5x)
- Particles: ครับ (137x), นะ (95x) → remove all
- Context: Teaching higher high/higher low concepts

Pass 2: Translate with context
Segment 1: "สวัสดีครับ ก็มาถึงอีก Part 1"
Context: Part 3 of series, casual tone
Translate: "Hello everyone, we've reached Part 3"  ✓

Segment 2: "เรื่องของแท่งเทียน"
Context: Forex teaching, standard term
Translate: "candlesticks"  ✓

Segment 50: "มันสูสีกัน"
Context: Bulls vs bears evenly matched (from Pass 1 analysis)
Translate: "They're evenly matched"  ✓

Result: High quality, contextual, natural English
```

---

### ⚠️ Common Mistakes to Avoid

1. **Starting translation before reading full document**
   - Consequence: Missing context, literal translations

2. **Not loading dictionaries**
   - Consequence: Inconsistent term usage

3. **Ignoring Thai idioms**
   - Consequence: "speak only meat" instead of "get to the point"

4. **Translating particles**
   - Consequence: "Good particle polite" instead of "Looks good"

5. **Inconsistent tone**
   - Consequence: Segment 1 casual, Segment 50 formal (confusing!)

6. **Not checking quality**
   - Consequence: Low quality output that must be redone

---

### 🎓 Mandatory Reading Before Translation

**EVERY TIME you are asked to translate, you MUST:**

1. **Read this TRANSLATION PROTOCOL section** (this section you're reading now)
2. **Read CLAUDE.md "Thai Idiom & Slang Handling" section** (line ~400-600)
3. **Read CLAUDE.md "Translation Tone & Style Rules" section** (line ~100-200)
4. **Load all dictionaries from `data/dictionaries/`**

**If you skip ANY of these → your translation WILL be wrong**

---

### ✅ Translation Approval Criteria

**Before submitting translation, verify:**

- [ ] All segments translated (none skipped)
- [ ] All idioms translated contextually (none literal)
- [ ] All forex terms in English (none in Thai phonetic)
- [ ] All particles removed (no ครับ, นะ, เนี้ย in English)
- [ ] Tone consistent throughout
- [ ] Natural English (readable by native speaker)
- [ ] Context maintained from Pass 1
- [ ] Timestamps preserved exactly

**If ANY item fails → fix before submitting**

---

## ⚠️ CRITICAL RULES - READ FIRST

### 🐍 Virtual Environment Rule

**ALWAYS use the project's virtual environment for ALL Python operations:**

```bash
# CORRECT - Use .venv for this project
.venv/bin/python script.py
.venv/bin/pip install package

# WRONG - Never use system Python
python script.py          # ❌ WRONG
pip install package       # ❌ WRONG
```

**Why this matters:**
- Prevents dependency conflicts
- Ensures correct package versions
- Isolates project environment
- Avoids permission issues

**Before ANY Python command:**
1. Check if .venv exists: `ls .venv/bin/python`
2. Use `.venv/bin/python` or `.venv/bin/pip`
3. NEVER use bare `python` or `pip`

### 🔄 Auto-Checkpoint System

**Automatic backups every 15 minutes to prevent data loss:**

```bash
# Start auto-checkpoint (runs in background)
.venv/bin/python src/auto_checkpoint.py start

# Create manual checkpoint before risky changes
.venv/bin/python src/auto_checkpoint.py create --desc "Before refactoring"

# List available checkpoints
.venv/bin/python src/auto_checkpoint.py list

# Restore from checkpoint if something breaks
.venv/bin/python src/auto_checkpoint.py restore checkpoint_20250103_143000
```

**Checkpoints are stored in `.checkpoints/` directory**

### 🎯 Thai Idiom & Slang Handling - CRITICAL FOR QUALITY

**The #1 rule for Thai translation: NEVER translate idioms word-by-word!**

This system now includes **105 Thai idioms + 30 slang expressions** with context-aware translation.

#### 🎭 Translation Tone & Style Rules

**IMPORTANT: Match the speaker's tone and style!**

1. **Casual/Conversational Tone (มันส์ๆ, เป็นกันเอง)**
   - Keep it natural and friendly
   - Use contractions: "we'll" not "we will", "let's" not "let us"
   - Preserve casual expressions: "you know", "right?", "okay?"
   - Example: "มาเริ่มกันเลยดีกว่า" → "Let's just get started" (NOT "Let us commence")

2. **Teaching/Instructional Tone**
   - Use "you" for direct address
   - Keep it engaging: "Now let's look at...", "Here's what..."
   - Preserve enthusiasm: "This is important!", "Check this out!"

3. **Technical Terms - Keep Accurate**
   - Forex terms stay in English: "Price Action", "Candlestick", "Support/Resistance"
   - Thai phonetic terms → English equivalents: "แท่งเทียน" → "candlestick"
   - Pattern names: "Engulfing", "Pinbar", "Doji" (standard names)

4. **Common Transcription Errors to Fix**
   - "Prize Action" → "Price Action"
   - "Priority Action" → "Price Action"
   - "Indictor" → "Indicator"
   - "ชาร์จ" → "Chart"
   - "Engruffing" → "Engulfing"

5. **Context Over Literal Translation**
   - If transcription seems off, use context to infer correct meaning
   - Example: "มันวิ่ง" (literally "it runs") → "the price moves" (in trading context)

6. **Particles Handling (นะ, ครับ, ค่ะ, ละ, ซะ, เลย, แหละ)**
   - **Remove** particles in final translation (they add politeness/emphasis in Thai)
   - ❌ Wrong: "ดีนะครับ" → "good particle polite-male"
   - ✅ Right: "ดีนะครับ" → "looks good"
   - Exception: Keep meaning if particle changes intent
     - "ดีนะ" (suggesting) → "looks good" / "should be good"
     - "ดีแหละ" (emphatic) → "definitely good"

7. **Filler Words (อ่า, เอ่อ, แบบว่า, ก็คือ)**
   - **Remove** most filler words for clarity
   - ❌ Wrong: "แบบว่า เราต้องดู" → "Like, we need to see"
   - ✅ Right: "แบบว่า เราต้องดู" → "We need to see"
   - Exception: Keep for natural flow in long explanations
     - "ก็คือว่า... มันเป็นแบบนี้" → "So basically... it works like this"

8. **Repetition/Stuttering (เนี้ยๆ, อยู่ๆ, เล็กๆ)**
   - Thai uses repetition for emphasis/description
   - ❌ Wrong: "เล็กๆ" → "small small"
   - ✅ Right: "เล็กๆ" → "very small" / "quite small"
   - ❌ Wrong: "อยู่ๆ" → "suddenly suddenly"
   - ✅ Right: "อยู่ๆ" → "suddenly" / "out of nowhere"

9. **Mixed Thai-English Terms**
   - Keep English technical terms as-is (don't re-translate)
   - "Price Action" → "Price Action" (NOT "การเคลื่อนไหวของราคา")
   - "Candlestick" → "Candlestick" (can use lowercase: "candlestick")
   - "Momentum Analysis" → "Momentum Analysis"
   - Thai pronunciation → Standard English:
     - "ไพรซ์ แอคชั่น" → "Price Action"
     - "แคนเดิลสติ๊ก" → "Candlestick"

10. **Numbers and Quantities**
    - Convert Thai number format to English
    - "สองร้อย" → "200" or "two hundred"
    - "หนึ่งพัน" → "1,000" or "one thousand"
    - "สิบเปอร์เซ็นต์" → "10%" or "ten percent"
    - Keep context: "200 กม./ชม." → "200 km/h" (in metaphor context)

11. **Time Expressions**
    - "สักพัก" → "for a while"
    - "ตอนนี้" → "now" / "at this point"
    - "ก่อนหน้านี้" → "earlier" / "before"
    - "ต่อไป" → "next" / "going forward"

12. **Demonstratives (นี่, นั่น, โน่น, นี้)**
    - Context-dependent translation
    - "อันนี้" → "this one" / "this" / "here"
    - "แท่งนี้" → "this candle" / "this bar"
    - "ตรงนี้" → "at this point" / "here" / "this level"

#### ❌ **WRONG - Literal Translation**
```
Thai: "วันนี้เราจะพูดแต่เนื้อๆ ไม่มีน้ำนะครับ"
BAD:  "Today we speak only meat no water"  ← WRONG!
```

#### ✅ **CORRECT - Contextual Translation**
```
Thai: "วันนี้เราจะพูดแต่เนื้อๆ ไม่มีน้ำนะครับ"
GOOD: "Today we'll get straight to the point, no fluff"  ← RIGHT!
```

#### 📊 Idiom Database Coverage

**Location:** `data/dictionaries/`
- **thai_idioms.json** - 105 idioms with context
  - General idioms (50): พูดแต่เนื้อๆ, ไฟแดงกระพริบ, etc.
  - Forex-specific (40): กระทิงชนหมี, แรงเหวี่ยง, etc.
  - Teaching phrases (15): เข้าเนื้อกันดีกว่า, etc.

- **thai_slang.json** - 30 modern slang
  - Casual speech: มันจะ, แบบว่า
  - Modern slang: ไม่ฟิน, เท่ห์, โดน, ปัง
  - Particles: นะ, ซะ, เลย, แหละ

#### 🔍 How Idiom Detection Works

**Two-Pass System:**

1. **Pass 1: Document Analysis**
   ```python
   # System analyzes ENTIRE document first
   - Detects all idioms using regex patterns
   - Understands document context
   - Identifies metaphor domains (military, automotive, physics)
   ```

2. **Pass 2: Context-Aware Translation**
   ```python
   # Translates each segment WITH full context
   - Knows what idioms are present
   - Understands figurative vs literal usage
   - Applies correct English equivalent
   ```

#### 📝 **Idiom Translation Examples**

| Thai Idiom | ❌ Literal (WRONG) | ✅ Contextual (RIGHT) |
|------------|-------------------|----------------------|
| พูดแต่เนื้อๆ ไม่มีน้ำ | speak meat no water | get straight to the point |
| ไฟแดงกระพริบ | red light blinking | warning signs flashing |
| ฝั่งไหนครองเกมอยู่ | which side owns game | which side is dominating |
| น้ำท่วมถึงหัว | water flood to head | in over your head |
| เหวี่ยงลูกตุ้ม | swing pendulum | oscillating like a pendulum |
| ยูเทิร์นกลับ | U-turn back | reversing direction |
| หมดกำลัง | out of power | running out of steam |
| กองทัพซะมากกว่า | army very more | more like an army |
| สูสี | compete color | evenly matched / neck and neck |

#### 🚫 **Common Translation Mistakes to AVOID**

1. **Word-by-word translation**
   - ❌ "มันจะขึ้น" → "it will rise" (too literal)
   - ✅ "มันจะขึ้น" → "price will rise" (natural)

2. **Ignoring context**
   - ❌ "แรงเหวี่ยง" → "swing force" (literal)
   - ✅ "แรงเหวี่ยง" → "momentum" (contextual)

3. **Over-translating particles**
   - ❌ "ดีนะครับ" → "good particle polite-male"
   - ✅ "ดีนะครับ" → "looks good" (remove particles)

4. **Missing metaphors**
   - ❌ "กระทิงชนหมี" → "bull hits bear"
   - ✅ "กระทิงชนหมี" → "bulls versus bears battle"

5. **Misunderstanding Thai idioms**
   - ❌ "สูสี" → "compete color" (literal!)
   - ✅ "สูสี" → "evenly matched" / "neck and neck" (contextual!)
   - Context: กำลังของทั้งสองฝ่ายพอๆ กัน ไม่รู้ฝ่ายไหนจะชนะ

#### 🎓 **Translation Guidelines**

**For General Idioms:**
1. Detect the idiom pattern
2. Understand the meaning in context
3. Choose appropriate English equivalent
4. Maintain tone and formality

**For Casual Speech:**
```python
# Remove filler words but keep naturalness
"แบบว่า เราต้องดู" → "We need to see"  (not "Like we need to see")
"มันจะขึ้นนะ" → "It will rise"  (not "It particle will rise particle")
```

**For Forex Metaphors:**
```python
# Maintain metaphor domain
"กองทัพซะมากกว่า" → "more like an army"  ✓
"เหวี่ยงลูกตุ้ม" → "like a swinging pendulum"  ✓
"ยูเทิร์นกลับ" → "making a U-turn"  ✓

# Evenly matched battle
"สูสีกัน" → "evenly matched" / "neck and neck"  ✓
"สูสีมาก" → "closely contested"  ✓
Context: ฝั่งซื้อและฝั่งขายสูสีกัน → "Bulls and bears are evenly matched"
```

#### 📚 **Idiom Categories**

**1. Teaching/Transitions (15)**
- เข้าเนื้อกันดีกว่า → let's dive into details
- พูดแต่เนื้อๆ → straight to the point
- ยกตัวอย่าง → for example

**2. Market Analysis (25)**
- ฝั่งไหนครองเกม → which side dominates
- แรงซื้อแรงขาย → buying/selling pressure
- กระทิงชนหมี → bulls vs bears

**3. Price Movement (20)**
- ผงาดขึ้น → surge up
- ดิ่งลง → plunge down
- แกว่งตัว → oscillating

**4. Risk/Warning (15)**
- ไฟแดงกระพริบ → warning signs
- เล่นไฟ → playing with fire
- น้ำท่วมถึงหัว → in over your head

**5. Trading Actions (15)**
- เข้าเกม → enter trade
- ออกจากเกม → exit trade
- ตามกระแส → follow the trend

**6. Casual/Slang (15)**
- ไม่ฟิน → doesn't feel right
- โดน → got hit
- ของจริง → the real deal

#### 🔧 **For Developers**

**Adding New Idioms:**
```json
{
  "id": 106,
  "thai": "your_idiom_here",
  "literal": "word_by_word_translation",
  "meaning": "actual_meaning_in_context",
  "english_equivalents": ["option1", "option2"],
  "category": "general/forex/teaching",
  "detection_patterns": ["regex_pattern"],
  "examples": [...],
  "priority": 1
}
```

**Testing Idiom Detection:**
```bash
# Test with sample text
.venv/bin/python -c "
from src.context_analyzer import ContextAnalyzer
analyzer = ContextAnalyzer()
result = analyzer.analyze_document('พูดแต่เนื้อๆ ไม่มีน้ำ')
print(result.colloquialisms)
"
```

#### ✅ **Quality Checks**

Before releasing translation, verify:
- [ ] No literal idiom translations
- [ ] All idioms translated contextually
- [ ] Metaphors preserved naturally
- [ ] Casual particles removed appropriately
- [ ] Tone and formality maintained
- [ ] Context makes sense in English

#### 📈 **Success Metrics**

**Target:**
- 95%+ idiom detection rate
- 98%+ correct idiom translation
- 100% zero literal translations
- Natural English flow

**Current:**
- 105 idioms in database
- 30 slang expressions
- Context-aware detection ✓
- Two-pass translation ✓

---

## 📋 Executive Summary

**Mission**: Build a production-ready system to translate Thai Forex/Trading videos to English SRT subtitles with 95%+ accuracy and $1.50-2.50/hour cost.

**Status**: 60% Complete - Core modules ready, need integration and Thai transcription optimization

**Critical**: This project ONLY generates SRT files. Voice synthesis is handled by existing Quantum-SyncV5 system.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    INPUT: Thai Video                     │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│  STAGE 1: Transcription (thai_transcriber.py)           │
│  - Whisper large-v3 (local, FREE)                       │
│  - Word-level timestamps                                │
│  - Thai-specific optimization                           │
│  - 95%+ accuracy target                                 │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│  STAGE 2: Context Analysis (context_analyzer.py) ✅     │
│  - Two-pass analysis                                    │
│  - Document-level understanding                         │
│  - Forex terminology detection                          │
│  - Colloquialism identification                         │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│  STAGE 3: Translation (translation_pipeline.py) ✅      │
│  - Smart model routing (GPT-3.5/4 or Claude)           │
│  - Context-aware translation                            │
│  - Aggressive caching (60-70% hit rate)                 │
│  - Cost optimization                                    │
└─────────────────────────────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│  OUTPUT: English SRT + Statistics                        │
│  → Ready for Quantum-SyncV5 voice synthesis             │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Project Status

### ✅ Completed Modules (6/10)

| Module | File | Status | Features |
|--------|------|--------|----------|
| **Context Analyzer** | `context_analyzer.py` | ✅ Complete | Two-pass analysis, colloquialism detection |
| **Data Management** | `data_management_system.py` | ✅ Complete | External JSON dictionaries, hot-reload |
| **Configuration** | `config.py` | ✅ Complete | 5 preset modes, cost estimation |
| **Data Migration** | `migrate_to_json.py` | ✅ Complete | Extract hardcoded → JSON |
| **Translation Pipeline** | `translation_pipeline.py` | ✅ Complete | Smart routing, caching, mock mode |
| **Thai Transcriber** | `thai_transcriber.py` | ✅ NEW! | Whisper optimization, word timestamps |

### ⏳ TODO Modules (4/10)

| Module | Priority | Description |
|--------|----------|-------------|
| **Orchestrator** | 🔥 HIGH | Complete pipeline controller (50% done) |
| **Cache Manager** | 🔥 HIGH | Redis integration for cost savings |
| **Quality Validator** | MEDIUM | SRT quality checks, accuracy metrics |
| **CLI Interface** | LOW | User-friendly command-line tool |

---

## 🎯 Key Design Decisions

### 1. **External Configuration (NOT Hardcoded)** ✅
```
data/
├── dictionaries/
│   ├── forex_terms.json      # 50+ Forex terms
│   ├── colloquialisms.json   # 20+ Thai phrases
│   ├── metaphors.json        # 5 metaphor domains
│   └── custom_terms.json     # User-defined
└── patterns/
    └── speech_patterns.yaml
```

**Why**: Maintainability, user can add terms without code changes

### 2. **Two-Pass Translation** ✅
```python
# Pass 1: Analyze entire document
document_context = analyze_document(full_text)

# Pass 2: Translate segments with context
for segment in segments:
    translated = translate_with_context(segment, document_context)
```

**Why**: Thai spoken language needs full context understanding

### 3. **Smart Model Routing** ✅
```python
if complexity < 0.3:
    model = "gpt-3.5-turbo"  # $0.002/1K
elif complexity < 0.7:
    model = "gpt-3.5-turbo"  # $0.002/1K
else:
    model = "gpt-4"          # $0.03/1K
```

**Why**: Cost optimization - save 50-70% on API costs

### 4. **Translation Provider Options** 💡

#### Option A: OpenAI (Current, Recommended)
```
Cost: $1.50-2.50/hour
Setup: Requires OPENAI_API_KEY
Pros: Proven, automated, cost-effective
Cons: Quality good but not best
```

#### Option B: Claude API (Higher Quality)
```
Cost: $0.50-1.00/hour
Setup: Requires ANTHROPIC_API_KEY
Pros: Better Thai understanding, higher quality
Cons: Need to implement adapter
```

#### Option C: Claude Pro Web (Manual)
```
Cost: $0 (included in $20/month subscription)
Setup: Manual via web interface
Pros: Free, highest quality
Cons: Not automated, rate limited
```

**Recommendation**: Use Hybrid approach
- Development: Mock mode (free)
- Small batches: Claude Pro web (free, manual)
- Production: OpenAI API (automated, $1.50-2.50/hr)

---

## 💾 File Structure

```
thai-video-translator/
├── src/
│   ├── config.py                    ✅ Complete
│   ├── context_analyzer.py          ✅ Complete
│   ├── data_management_system.py    ✅ Complete
│   ├── migrate_to_json.py           ✅ Complete
│   ├── translation_pipeline.py      ✅ Complete
│   ├── thai_transcriber.py          ✅ NEW - Complete
│   ├── orchestrator.py              ⏳ 50% done
│   ├── cache_manager.py             📋 TODO
│   ├── quality_validator.py         📋 TODO
│   └── cli.py                       📋 TODO
│
├── data/
│   ├── dictionaries/
│   │   ├── forex_terms.json
│   │   ├── colloquialisms.json
│   │   ├── metaphors.json
│   │   └── custom_terms.json
│   └── patterns/
│       └── speech_patterns.yaml
│
├── tests/
│   ├── test_simple.py               ✅ Works
│   ├── test_mock_mode.py            ✅ Works
│   └── Test_Script_ep02.py          📋 Update needed
│
├── output/
│   └── [generated SRT files]
│
├── .env                             ⚠️ Create this!
├── requirements.txt                 ✅ Complete
└── README.md                        📋 TODO
```

---

## 🚀 Quick Start Guide

### Step 1: Environment Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# Key packages:
# - openai-whisper (transcription)
# - openai>=1.0.0 (translation API)
# - anthropic (optional, for Claude)
# - python-dotenv
# - pyyaml
# - watchdog

# 2. Create .env file
cat > .env << EOF
OPENAI_API_KEY=sk-your-key-here
# Optional:
# ANTHROPIC_API_KEY=sk-ant-your-key-here
# REDIS_URL=redis://localhost:6379
EOF

# 3. Run data migration (create JSON files)
python src/migrate_to_json.py
```

### Step 2: Test Components

```bash
# Test 1: Mock mode (no API needed)
python tests/test_mock_mode.py

# Test 2: Thai transcription (requires audio file)
python src/thai_transcriber.py sample.mp4 -o output/

# Test 3: Full pipeline (requires API key)
python tests/Test_Script_ep02.py
```

### Step 3: Run Production Pipeline

```bash
# Option A: Command-line
python src/orchestrator.py input_video.mp4 \
  --model large-v3 \
  --provider openai \
  --output ./output

# Option B: Python script
from orchestrator import VideoTranslationOrchestrator

orch = VideoTranslationOrchestrator(
    whisper_model="large-v3",
    translation_provider="openai"
)

result = orch.process_video("input_video.mp4")
print(f"Output SRT: {result.output_files['english_srt']}")
```

---

## 📝 Sample Input/Output

### Input: Thai Audio Transcript (ep-02.txt)
```
ที่นี่ อย่างเช่น โมเมนตัมนะครับ แสดงถึงการที่ราคามันมีแรงเหวี่ยง
เหมือนกับเวลาที่เราเหวี่ยงลูกตุ้ม ลูกตุ้มมันจะมีแรงเหวี่ยง
พอมันเหวี่ยงไปถึงจุดสูงสุด มันก็จะเริ่มหมดแรง แล้วก็เหวี่ยงกลับ
```

### Output: English SRT
```srt
1
00:00:00,000 --> 00:00:05,200
Here, for example, momentum represents the swing force of price movement

2
00:00:05,200 --> 00:00:10,500
Like when we swing a pendulum, it has momentum

3
00:00:10,500 --> 00:00:15,800
When it swings to the highest point, it loses force and swings back
```

### Key Features:
- ✅ Forex terms preserved correctly ("momentum" = technical term)
- ✅ Metaphors translated naturally (pendulum analogy)
- ✅ Timestamps preserved perfectly (±0.1s accuracy)
- ✅ Natural English phrasing

---

## 🔧 Critical Configuration

### config.py - Preset Modes

```python
# 1. DEVELOPMENT (testing, mock mode)
config = Config(mode=ConfigMode.DEVELOPMENT)

# 2. PRODUCTION (optimized for cost/quality)
config = Config(mode=ConfigMode.PRODUCTION)

# 3. HIGH_QUALITY (best accuracy, higher cost)
config = Config(mode=ConfigMode.HIGH_QUALITY)

# 4. COST_OPTIMIZED (minimum cost)
config = Config(mode=ConfigMode.COST_OPTIMIZED)

# 5. MOCK (no API, for testing)
config = Config(mode=ConfigMode.MOCK)
```

### Whisper Settings (thai_transcriber.py)

```python
THAI_SETTINGS = {
    "language": "th",
    "task": "transcribe",
    "word_timestamps": True,
    
    # Multi-temperature ensemble for accuracy
    "temperature": (0.0, 0.2, 0.4, 0.6, 0.8),
    
    # Beam search
    "beam_size": 5,
    "best_of": 5,
    
    # Thai-specific thresholds
    "compression_ratio_threshold": 2.4,
    "logprob_threshold": -1.0,
    "no_speech_threshold": 0.6,
    
    # Context priming
    "condition_on_previous_text": True,
    "initial_prompt": "นี่คือการสอนเทรด Forex และการลงทุน"
}
```

### Translation Settings

```python
# Smart routing rules
ROUTING_RULES = {
    "simple": {
        "max_complexity": 0.3,
        "model": "gpt-3.5-turbo",
        "cost_per_1k": 0.002
    },
    "medium": {
        "max_complexity": 0.7,
        "model": "gpt-3.5-turbo",
        "cost_per_1k": 0.002
    },
    "complex": {
        "max_complexity": 1.0,
        "model": "gpt-4",
        "cost_per_1k": 0.03
    }
}

# Caching strategy
CACHE_STRATEGY = {
    "forex_terms": "permanent",      # Never expires
    "common_phrases": "6_months",    # Long cache
    "translations": "30_days",       # Medium cache
    "temp_results": "7_days"         # Short cache
}
```

---

## 🎯 Success Criteria

The project is successful when:

1. ✅ **Thai Transcription**: 95%+ accuracy for Forex content
2. ✅ **Terminology**: 100% Forex terms correctly preserved
3. ✅ **Translation Quality**: 92%+ accuracy (human evaluation)
4. ✅ **Timing Accuracy**: 100% timestamp preservation (±0.1s)
5. ✅ **Cost Efficiency**: < $2.50 per hour of video
6. ✅ **Processing Speed**: > 10x realtime
7. ✅ **Reliability**: Zero runtime errors in production
8. ✅ **Integration**: SRT works perfectly with Quantum-SyncV5

---

## 🔄 Current Performance Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| **Cost per hour** | $1.50-2.50 | ~$2.00 | ✅ |
| **Cache hit rate** | 60-70% | 0% (new) | ⏳ Need Redis |
| **Translation accuracy** | 92%+ | TBD | ⏳ Need eval |
| **Processing speed** | 10x realtime | ~8x | ⏳ Optimize |
| **Thai accuracy** | 95%+ | TBD | ⏳ Test needed |

---

## 📋 TODO List (Priority Order)

### HIGH Priority 🔥

1. **Complete orchestrator.py**
   ```python
   # File: src/orchestrator.py (50% done)
   # Need to finish:
   - Stage 4: Quality validation
   - Stage 5: Statistics reporting
   - Error handling for all stages
   - Batch processing support
   ```

2. **Create cache_manager.py**
   ```python
   # File: src/cache_manager.py (NEW)
   # Features needed:
   - Redis integration
   - Multi-tier caching (memory + Redis)
   - Cache key generation
   - TTL management
   - Hit rate tracking
   ```

3. **Test with real video**
   ```bash
   # Use ep-02.txt or actual video file
   # Validate:
   - Transcription accuracy
   - Translation quality
   - Timing preservation
   - Cost tracking
   ```

### MEDIUM Priority

4. **Create quality_validator.py**
   ```python
   # File: src/quality_validator.py (NEW)
   # Features needed:
   - SRT format validation
   - Timestamp gap detection
   - Translation quality checks
   - Forex term verification
   - Confidence scoring
   ```

5. **Optimize performance**
   ```python
   # Areas to optimize:
   - Parallel processing for multiple files
   - GPU acceleration for Whisper
   - Batch API calls (reduce overhead)
   - Memory management for long videos
   ```

### LOW Priority

6. **Create CLI interface**
   ```python
   # File: src/cli.py (NEW)
   # Features:
   - User-friendly commands
   - Progress bars (rich/tqdm)
   - Interactive mode
   - Batch processing
   - Config management
   ```

7. **Documentation**
   ```markdown
   # Files needed:
   - README.md (user guide)
   - API.md (developer docs)
   - CONTRIBUTING.md (for contributors)
   - CHANGELOG.md (version history)
   ```

---

## 🐛 Known Issues & Solutions

### Issue 1: OPENAI_API_KEY Error
```python
# Problem: KeyError when API key not set
# Solution: Create .env file
echo "OPENAI_API_KEY=sk-your-key" > .env

# Or use mock mode for testing:
config = Config(mode=ConfigMode.MOCK)
```

### Issue 2: Whisper Model Download
```python
# Problem: Large model (>2GB) download on first run
# Solution: Download manually
import whisper
whisper.load_model("large-v3")  # One-time download
```

### Issue 3: Missing Modules (Graceful Degradation)
```python
# Problem: Some modules not yet created
# Solution: Pipeline uses mock mode automatically
# Check logs for: "Using mock mode for missing component"
```

### Issue 4: SRT Timestamp Format
```python
# Problem: Timestamps must be exact format
# Solution: Use built-in formatter
def to_srt_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"
```

---

## 💰 Cost Optimization Strategies

### 1. Aggressive Caching
```python
# Cache everything possible:
- Transcriptions (by audio hash)
- Translations (by segment + context)
- Forex term lookups
- API responses

# Expected savings: 60-70% of API costs
```

### 2. Smart Model Routing
```python
# Route by complexity:
Simple segments → GPT-3.5 ($0.002/1K)
Complex segments → GPT-4 ($0.03/1K)

# Expected savings: 50% vs all GPT-4
```

### 3. Batch Processing
```python
# Process multiple segments in one API call:
batch_size = 10
combined_prompt = "\n".join(segments[:batch_size])

# Expected savings: 30-40% API overhead
```

### 4. Local Whisper
```python
# Use local Whisper (not API):
model = whisper.load_model("large-v3")
result = model.transcribe(audio)

# Savings: $0.006/min = FREE vs $360/hour
```

---

## 🔐 Environment Variables

```bash
# .env file (create this!)

# Required for OpenAI
OPENAI_API_KEY=sk-your-openai-key-here

# Optional: Claude API (higher quality)
ANTHROPIC_API_KEY=sk-ant-your-claude-key-here

# Optional: Redis caching
REDIS_URL=redis://localhost:6379

# Optional: Custom paths
WHISPER_MODEL_PATH=/models/whisper-large-v3
CACHE_DIR=.cache
OUTPUT_DIR=./output

# Optional: Performance tuning
MAX_WORKERS=4
BATCH_SIZE=10
LOG_LEVEL=INFO

# Optional: Cost limits
MAX_COST_PER_VIDEO=10.00
ENABLE_COST_ALERTS=true
```

---

## 🧪 Testing Guide

### Unit Tests
```bash
# Test individual modules
pytest tests/test_context_analyzer.py
pytest tests/test_translation_pipeline.py
pytest tests/test_thai_transcriber.py
```

### Integration Tests
```bash
# Test full pipeline
python tests/test_integration.py

# Test with sample video
python src/orchestrator.py tests/samples/sample.mp4
```

### Quality Validation
```bash
# Manual quality check
1. Process test video
2. Compare Thai SRT with original audio
3. Compare English SRT with Thai meaning
4. Verify Forex terms are correct
5. Check timestamp accuracy
```

---

## 📚 Key Forex Terms (Examples)

```json
{
  "โมเมนตัม": {
    "thai": "โมเมนตัม",
    "english": "momentum",
    "category": "technical_analysis",
    "explanation": "แรงเหวี่ยงของราคา"
  },
  "กระทิง": {
    "thai": "กระทิง",
    "english": "bull",
    "category": "market_sentiment",
    "explanation": "ฝั่งซื้อ ราคาขึ้น"
  },
  "หมี": {
    "thai": "หมี",
    "english": "bear",
    "category": "market_sentiment",
    "explanation": "ฝั่งขาย ราคาลง"
  },
  "เทรนด์": {
    "thai": "เทรนด์",
    "english": "trend",
    "category": "technical_analysis"
  }
}
```

---

## 🎓 Thai Colloquialisms (Examples)

```json
{
  "แบบว่า": {
    "thai": "แบบว่า",
    "english": "I mean",
    "type": "filler",
    "usage": "conversational"
  },
  "พี่ชาย": {
    "thai": "พี่ชาย",
    "english": "this trader",
    "context": "ใช้เรียกเทรดเดอร์ที่พูดถึง",
    "translate_as": "this trader/this person"
  },
  "มันจะ": {
    "thai": "มันจะ",
    "english": "it will",
    "note": "informal, conversational Thai"
  }
}
```

---

## 🔗 Integration with Quantum-SyncV5

```python
# Our output → Quantum-SyncV5 input
our_output = "output/video_english.srt"

# Quantum-SyncV5 process:
from quantum_sync import process_srt_file

result = process_srt_file(
    srt_file=our_output,
    voice='Matthew',  # AWS Polly voice
    batch_size=100
)

# Final output: Synchronized voice audio
```

---

## 🚨 Critical Reminders

### DO:
✅ Always use external JSON files for dictionaries  
✅ Run two-pass analysis for context  
✅ Cache aggressively (60-70% hit rate target)  
✅ Use smart model routing for cost optimization  
✅ Validate SRT format before output  
✅ Test with real Forex content  
✅ Monitor API costs closely  

### DON'T:
❌ Hardcode any terminology in code  
❌ Skip context analysis (single-pass fails)  
❌ Use GPT-4 for everything (too expensive)  
❌ Translate word-by-word (need context)  
❌ Forget timestamp preservation  
❌ Build voice synthesis (Quantum-SyncV5 exists)  
❌ Ignore cache hits (major cost savings)  

---

## 🤖 For Claude Code: Next Steps

### Immediate Actions (Start Here!)

1. **Complete orchestrator.py**
   ```
   Current file is 50% done. Need to:
   - Finish Stage 4: Quality validation
   - Add Stage 5: Statistics and reporting
   - Implement batch processing
   - Add comprehensive error handling
   - Test end-to-end flow
   ```

2. **Create cache_manager.py**
   ```
   Redis-based caching system:
   - Multi-tier: Memory (fast) + Redis (persistent)
   - Smart key generation (hash-based)
   - TTL management by data type
   - Hit rate tracking and reporting
   - Cost savings calculation
   ```

3. **Test complete pipeline**
   ```
   - Use ep-02.txt as test input
   - Validate transcription accuracy
   - Check translation quality
   - Verify cost tracking
   - Ensure SRT format correctness
   ```

### File Locations

```
✅ Already created (reference these):
- src/config.py
- src/context_analyzer.py
- src/data_management_system.py
- src/translation_pipeline.py
- src/thai_transcriber.py

⏳ Partially done (complete these):
- src/orchestrator.py (50% done)

📋 Need to create:
- src/cache_manager.py
- src/quality_validator.py
- src/cli.py
- tests/test_integration.py
- README.md
```

### Testing Commands

```bash
# After completing modules:

# 1. Unit test each module
pytest tests/

# 2. Test full pipeline
python src/orchestrator.py tests/sample.mp4

# 3. Validate output
python src/quality_validator.py output/sample_english.srt

# 4. Check costs
python -c "
from orchestrator import VideoTranslationOrchestrator
orch = VideoTranslationOrchestrator()
result = orch.process_video('sample.mp4')
print(f'Cost: ${result.stats[\"total_cost\"]:.4f}')
"
```

---

## 📞 Contact & Resources

### Documentation
- **Claude Code Docs**: https://docs.claude.com/en/docs/claude-code
- **Whisper Docs**: https://github.com/openai/whisper
- **OpenAI API**: https://platform.openai.com/docs

### Key Files in Project Knowledge
1. `Project Handover Document - Thai→English SRT Generator.md`
2. `Thai-English Video Translation Pipeline - Complete Project Summary.md`
3. `ep-02.txt` (sample transcript)
4. `Forex Terminology Guide.md`
5. All completed .py files

### Support
- Check `/help` in Claude Code
- Review error logs in `.cache/logs/`
- Test with mock mode first: `Config(mode=ConfigMode.MOCK)`

---

## ✅ Success Checklist

Before considering project complete:

- [ ] All modules implemented and tested
- [ ] Pipeline processes video end-to-end
- [ ] Thai transcription accuracy > 95%
- [ ] Translation quality > 92%
- [ ] Timestamp accuracy ±0.1s
- [ ] Cost < $2.50 per hour
- [ ] Cache hit rate > 60%
- [ ] Processing speed > 10x realtime
- [ ] SRT format validated
- [ ] Integration with Quantum-SyncV5 confirmed
- [ ] Documentation complete
- [ ] Error handling comprehensive

---

## 🎯 Final Notes

This project is **60% complete**. The core architecture is solid and proven. Main work remaining:

1. **Finish orchestrator** (2-3 hours)
2. **Add caching** (2-3 hours)  
3. **Quality validation** (1-2 hours)
4. **Testing & optimization** (2-4 hours)

**Estimated time to completion: 7-12 hours**

The foundation is strong. Focus on integration, testing, and optimization.

---

**Ready for Claude Code! 🚀**

*Generated: 2025-10-03*  
*Project: Thai→English Video Translation Pipeline*  
*Version: 2.0*## 🔬 การ Debug และแก้ไขปัญหา (Codex Methodology)

**สำคัญ:** เมื่อเจอ bug หรือ unexpected behavior ต้องทำตามขั้นตอนนี้ **ทุกครั้ง**

### 1. **Trace Execution Flow** 🔍

❌ **อย่า assume ว่ารู้ปัญหาทันที!**

✅ **ต้องทำ:**
- ติดตาม code path ทีละขั้นตอน
- ใช้ `sed -n 'line_start,line_end p' file.py` เพื่ออ่าน code sections
- ใช้ `grep -n "function_name" file.py` เพื่อหา call sites
- ใช้ `python -c "import module; print(module.__file__)"` เพื่อยืนยัน import path

**ตัวอย่าง:**
```bash
# หา function ที่เรียกใช้
grep -n "process_chunk" chunk_processor.py

# อ่าน code section
sed -n '200,250p' chunk_processor.py

# ตรวจสอบ import path
python -c "import chunk_processor; print(chunk_processor.__file__)"
```

---

### 2. **Calculate Expected Values** 📐

**ต้องคำนวณ expected output ด้วย math เสมอ!**

```python
# Expected: 1189s (SRT target)
# Actual: 1396s (จาก ffprobe)
# Difference: +207s

# คำถาม: +207s มาจากไหน?
# → Trace backward เพื่อหา source
```

**Checklist:**
- [ ] คำนวณ expected result
- [ ] เปรียบเทียบ actual vs expected
- [ ] ถ้าต่างกัน → backtrack เพื่อหา root cause
- [ ] Validate ทุก intermediate value

---

### 3. **Validate Assumptions** ✓

❌ **อย่า assume code ทำงานถูกต้อง!**

✅ **ต้องทำ:**
- ตรวจสอบ return values
- ตรวจสอบ data flow
- ตรวจสอบ loop iterations
- ยืนยัน variable values

**ตัวอย่าง:**
```bash
# ตรวจสอบว่า loop ทำงานกี่รอบ
sed -n '658,678p' chunk_processor.py

# ตรวจสอบ indentation (spaces vs tabs)
cat -A chunk_processor.py | sed -n '660,665p'

# ตรวจสอบ return type
grep -A 5 "def process_chunk" chunk_processor.py
```

---

### 4. **Systematic Debugging Checklist** 📋

```bash
# ======================================
# Step 1: Understand the Problem
# ======================================
# - Expected result คืออะไร?
# - Actual result คืออะไร?
# - ต่างกันอย่างไร? เท่าไหร่?

# ======================================
# Step 2: Locate Code Path
# ======================================
grep -n "function_name" file.py
sed -n 'start,end p' file.py

# ======================================
# Step 3: Trace Execution
# ======================================
# - อ่าน code line by line
# - Track variable values
# - คำนวณ intermediate results

# ======================================
# Step 4: Identify Root Cause
# ======================================
# - อย่าหยุดที่ surface issues!
# - หา source ของ unexpected values
# - Validate ด้วย math

# ======================================
# Step 5: Verify Fix
# ======================================
# - คำนวณ expected result หลัง fix
# - Test กับ actual data
# - Confirm ว่า drift/values ตรง
```

---

### 5. **Common Pitfalls to Avoid** ⚠️

| ❌ **อย่าทำ** | ✅ **ต้องทำ** |
|---------------|---------------|
| คิดว่ารู้ปัญหาทันที | Trace complete flow |
| แก้ surface symptoms | Calculate expected values |
| Skip math validation | Validate every assumption |
| Assume code ถูกต้อง | Test with real data |
| Pattern matching alone | Deep analysis + math |
| Quick fix without understanding | Root cause analysis |

---

### 6. **Case Study #1: Double TimelineAwareMerger Bug** 📚

#### **ปัญหา:**
- Expected: 1189.9s
- Actual: 1396.6s
- Drift: **+206.7s (+17%)**

#### **❌ Bad Approach (Claude - ฉัน):**
```python
# 1. ดู code → เจอ indentation ที่ดูแปลก
# 2. คิดว่า: "อ้อ! process_chunk() นอก loop!"
# 3. แก้ indentation
# 4. คิดว่าเสร็จแล้ว ❌

# ปัญหา: วินิจฉัยผิด! ไม่ได้เจอ root cause
```

#### **✅ Good Approach (Codex):**
```python
# 1. Math analysis:
#    segments: 1031s
#    final: 1396s
#    silence: 1396 - 1031 = 365s ← มากเกินไป!

# 2. Trace flow:
#    - ChunkProcessor: ใส่ silence ที่ไหน?
#    - MasterProcessor: ใส่ silence ที่ไหน?

# 3. Discover:
#    merger1 = TimelineAwareMerger()  # ใน ChunkProcessor
#    merger1.add_segment() → ใส่ silence
#
#    merger2 = TimelineAwareMerger()  # ใน MasterProcessor
#    merger2.add_segment() → ใส่ silence อีกรอบ!

# 4. Root cause: Double merging!
#    - Chunk level: +182s
#    - Final level: +182s (ซ้ำ!)
#    - Total: ~365s ✓

# 5. Fix: ลบ chunk-level merger
#    → ใช้แค่ final merger ครั้งเดียว
```

#### **ผลลัพธ์:**
- Claude: แก้ indentation (ผิด!) → ยังมี bug
- Codex: แก้ double merger (ถูก!) → drift = 0%

---

### 7. **Case Study #2: Timeline Target Misunderstanding** 🚨

#### **ปัญหา:**
หลังแก้ double merger แล้ว เห็น output:
```
Target (timeline): 1396.6s
Target (segments): 1189.9s
Final drift: +0ms (+0.00%)
```

Claude คิดว่า: "1396.6s ≠ 1189.9s → เป็น bug!"

#### **❌ Bad Approach (Claude - ฉันอีกครั้ง!):**
```python
# 1. เห็นตัวเลขต่างกัน → คิดว่าเป็น bug ทันที
# 2. ไม่ได้ทำความเข้าใจ domain ก่อน
# 3. เกือบแก้ timeline_target_ms ให้ใช้ segment.end_ms
# 4. เกือบ commit fix ที่ผิด! ❌

# ปัญหา:
# - Pattern matching alone (เห็นเลขต่าง → assume bug)
# - ไม่เข้าใจว่า SRT มี timeline span vs segments duration
# - ไม่ได้คำนวณ expected behavior
```

#### **✅ Good Approach (Codex + User):**
```python
# Step 0: Understand the Domain (สำคัญที่สุด!)
# - SRT มี 2 ค่า:
#   1. Segments duration: 1189.9s (เวลาที่มีเสียงพูดจริง)
#   2. Timeline span: 1396.6s (first_start → last_end, รวมช่องว่าง)
#
# - Difference: 1396.6 - 1189.9 = 206.7s
# - นี่คือ gaps ระหว่าง segments ที่ต้องใส่กลับเข้าไปเพื่อซิงค์กับวิดีโอ!

# Step 1: Calculate Expected Behavior
# Synthesized segments: 1031.1s (เสียงจริง)
# Timeline span:         1396.6s (absolute time)
# Expected gaps:         1396.6 - 1031.1 = 365.5s
#
# TimelineAwareMerger ควรจะ:
#   - เอาเสียง 1031.1s
#   - ใส่ gaps 365.5s
#   - ได้ final 1396.6s

# Step 2: Validate with ffprobe
# ffprobe result: 1372.8s
# Actual gaps: 1372.8 - 1031.1 = 341.7s
# Missing: 365.5 - 341.7 = 23.8s ← MP3 encoding overhead (ยอมรับได้!)

# Step 3: Check Final Drift
# Final drift: +0ms (+0.00%) ✅
# Timeline alignment ทำงานสมบูรณ์!

# Step 4: Conclusion
# timeline_target_ms = 1396.6s ← ถูกต้องแล้ว!
# segment_target_ms  = 1189.9s ← ถูกต้องแล้ว!
# ไม่ต้องแก้อะไร! Don't fix what isn't broken!
```

#### **ผลลัพธ์:**
- Claude: เกือบแก้ timeline calculation (ผิด!) → จะทำให้ระบบพัง
- Codex: Validate ว่าถูกต้องแล้ว (ถูก!) → ไม่ต้องแก้!

#### **บทเรียนสำคัญ:**

**กฎใหม่ที่ต้องเพิ่ม:**
```
Step 0: UNDERSTAND THE DOMAIN FIRST! 🎯
======================================
ก่อนสรุปว่าเป็น bug ต้องถามตัวเองก่อน:

1. ค่าเหล่านี้หมายถึงอะไร?
   - Timeline span vs Segments duration แตกต่างกันอย่างไร?
   - มี semantic ที่แตกต่างกันหรือไม่?

2. ความต่างนี้เป็นไปตาม design หรือไม่?
   - ระบบออกแบบมาให้แตกต่างกันหรือเปล่า?
   - มีเหตุผลทางเทคนิคที่ต้องแตกต่างหรือไม่?

3. คำนวณ expected behavior
   - ถ้าระบบทำงานถูกต้อง ควรได้ค่าเท่าไหร่?
   - Math ออกมาตรงกับที่เห็นหรือไม่?

4. Validate against specification
   - Output ตรงกับ spec หรือไม่?
   - Final drift เป็น 0% หรือไม่?

❌ Different values ≠ Bug!
✅ Understand first, calculate second, then decide!
```

**ข้อผิดพลาดที่ต้องหลีกเลี่ยง:**
- ❌ เห็นเลขต่างกัน → สรุปเป็น bug ทันที
- ❌ ไม่เข้าใจ domain semantics
- ❌ ไม่คำนวณ expected behavior ก่อน assume
- ❌ แก้ code ที่ทำงานถูกต้องอยู่แล้ว
- ❌ Pattern matching โดยไม่ deep analysis

**สิ่งที่ต้องทำ:**
- ✅ Understand domain และ data model ก่อนเสมอ
- ✅ คำนวณ expected values ตาม specification
- ✅ Validate ว่า code ทำงานตรงตาม design หรือไม่
- ✅ ถ้าทำงานถูกต้องแล้ว → **Don't fix it!**

---

### 7. **Case Study #3: Codex WAV Pipeline Collaboration** 🤝

#### **สถานการณ์:**
หลังจาก Codex แก้ double merger bug แล้ว Timeline alignment ทำงาน (drift +0ms) แต่ผู้ใช้พบว่าเสียงไม่ตรงกับวิดีโอ:

```
Video duration: 1396.846s
Audio (MP3 mode): 1372.82s
Difference: -24.04s

ปัญหา: วิดีโอมี silent 24s ตอนท้าย
สาเหตุ: MP3 encoding frame rounding overhead
```

#### **Codex เสนอ Solution: WAV Pipeline**
```python
# Idea: แปลงเป็น WAV ก่อน concat → convert MP3 ทีเดียวตอนท้าย

Step 1: Convert all segments/silence to WAV
Step 2: Concat WAV files (no frame overhead)
Step 3: Convert final WAV → MP3 once
Result: Overhead reduced from 24s to ~0.024s (99% improvement!)
```

#### **❌ Bug แรก: Mixed Codec Problem**

Codex implementation แรก (commit f75037e):
```python
# TimelineAwareMerger in WAV mode:
silence_files = [silence_001.wav, silence_002.wav, ...]  # WAV format
segment_files = [seg0001.mp3, seg0002.mp3, ...]         # MP3 format ❌

# ffmpeg concat file:
file 'silence_001.wav'
file 'seg0001.mp3'  # ← Different codec!
file 'silence_002.wav'
file 'seg0002.mp3'  # ← Different codec!

# Result: ffmpeg concat demuxer ไม่สามารถ mix codecs → skip MP3 files
# Output: เฉพาะ silence (no segments!) → Duration 1031s instead of 1396s
```

#### **✅ Codex ซ้อมมือแก้: Segment Conversion**

Codex ทำการวินิจฉัยและแก้ไข (commit b7a722f):
```python
def _ensure_wav_copy(self, source_path: Path) -> Path:
    """
    Convert MP3 segments to WAV for consistent codec during concat.
    """
    if source_path.suffix.lower() == ".wav":
        return source_path  # Already WAV

    # Convert MP3 → WAV
    wav_path = source_path.with_suffix(".wav")
    subprocess.run([
        'ffmpeg', '-i', str(source_path),
        '-ar', '44100',  # 44.1kHz
        '-ac', '2',      # Stereo
        '-c:a', 'pcm_s16le',  # WAV codec
        '-y', str(wav_path)
    ], capture_output=True, check=True)

    return wav_path

def add_segment(self, audio_path, segment, actual_duration_ms):
    if self.output_format == "wav_then_mp3":
        # Convert MP3 segments to WAV BEFORE adding to list
        audio_path = self._ensure_wav_copy(audio_path)

    self.segment_files.append(audio_path)
    ...
```

**ผลลัพธ์:**
```
Test 1: MP3 mode (default)
  Duration: 1372.82s
  Timeline drift: +0ms ✅
  Backwards compatible: YES ✅

Test 2: WAV mode (after fix)
  Duration: 1396.61s
  Timeline drift: +0ms ✅
  Video sync: -0.24s (perfect!) ✅
```

#### **บทเรียนสำคัญ:**

**1. Trust But Verify** 🔍
```python
# Codex implementation ดูดี แต่ต้อง test ก่อนใช้งานจริง

Codex said: "WAV pipeline will work"
Reality: First version had bug (mixed codecs)
Codex response: Diagnosed and fixed quickly (commit b7a722f)

Key: Test thoroughly, even expert implementations!
```

**2. Backwards Compatibility First** 🛡️
```python
# Codex design ที่ดี:
def __init__(self, output_format: str = "mp3"):  # ← Default unchanged
    self.output_format = output_format

if self.output_format == "wav_then_mp3":
    # New feature (opt-in)
    ...
else:
    # Original behavior (default)
    ...

Result:
- Existing code works unchanged ✅
- New feature available if needed ✅
- Easy rollback if issues ✅
```

**3. Git Safety Procedures** 🔐
```bash
# ก่อนให้ Codex แก้ไข:
git checkout -b v11-codex-timeline-fix-backup
git push origin v11-codex-timeline-fix-backup

# ถ้า Codex แก้พัง:
git reset --hard origin/v11-codex-timeline-fix-backup

Result: ไม่กลัว Codex พังโค้ด เพราะมี backup เสมอ!
```

**4. Collaborative Debugging** 🤝
```
Codex Strengths:
✅ Quick implementation
✅ Systematic approach
✅ Self-correcting (found and fixed own bug)
✅ Good architecture (backwards compatible)

Claude Role:
✅ Test implementation
✅ Identify bugs (mixed codec issue)
✅ Provide diagnostic data (ls temp_v11/)
✅ Verify fixes work

Result: Faster than either working alone!
```

**5. Domain-Specific Knowledge Matters** 🎓
```
Why mixed codec failed:
- ffmpeg concat demuxer requires uniform format
- MP3 uses frames, WAV uses raw samples
- Cannot concat different codecs without re-encoding

Codex knew: WAV eliminates overhead
Codex missed: Segments were still MP3 (not converted)
Claude caught: Check temp files → found mixed formats

Lesson: Even experts need domain validation!
```

#### **ผลสรุป:**

**Before Codex collaboration:**
- Timeline alignment broken (double merger)
- Video sync poor (-24s)

**After Codex collaboration:**
- ✅ Timeline alignment perfect (0ms drift)
- ✅ Video sync perfect (-0.24s)
- ✅ Backwards compatible
- ✅ Production ready

**Success factors:**
1. Codex systematic approach
2. Claude thorough testing
3. Git safety procedures
4. Quick iteration (found bug → fixed in 1 commit)
5. Good communication (Claude provided diagnostic data)

**Time saved:**
- Manual debug: ~2-3 hours estimated
- With Codex: ~30 minutes (including bug fix)
- 75% time reduction! 🚀

---

### 7. **Case Study #4: Paperspace Production Success** 🎬

#### **สถานการณ์:**
ทำงานมาหลายวันไม่สำเร็จ วันนี้ใช้ Codex methodology แล้วสำเร็จใน Paperspace

**ปัญหาที่พบ:**
1. `bc: command not found` (Paperspace ไม่มี bc)
2. Path ไม่ตรง (คาดหวัง subfolder แต่จริงๆ อยู่ root)
3. Filename pattern ไม่ match (หา `*_agents.mp3` แต่ได้ `*_v11.mp3`)

#### **❌ Claude's Previous Approach (หลายวัน ไม่สำเร็จ):**
```python
# 1. พบ error → แก้แบบ quick fix
# 2. ไม่ได้ test environment ก่อน
# 3. Assume path structure เหมือน local
# 4. Hardcode filename patterns
# 5. ไม่มี error handling ที่ดี

Result: ใช้ไม่ได้ใน Paperspace ❌
```

#### **✅ Codex Methodology (วันนี้สำเร็จ):**

**Step 1: Understand Environment**
```bash
# ตรวจสอบว่า bc มีไหม
which bc  # ไม่มี!

# เช็ค Python (มีแน่นอน)
which python3  # มี!

Solution: ใช้ Python แทน bc ทุกที่
```

**Step 2: Validate Path Structure**
```bash
# เช็คว่าไฟล์อยู่ที่ไหนจริง
ls -la /notebooks/quantum-sync-v5/

# พบว่า: ไฟล์อยู่ root ไม่ใช่ subfolder!
# Local: /notebooks/quantum-sync-v5/quantum-sync-v11-production/
# Paperspace: /notebooks/quantum-sync-v5/  # ไม่มี subfolder

Solution: แก้ WORK_DIR และ OUTPUT_DIR
```

**Step 3: Debug Filename Pattern**
```bash
# Error: "Audio synthesis failed"
# แต่เห็น output: "✅ SUCCESS! Output saved to: .../Matthew_v11.mp3"

# เช็คจริง
ls output/

# พบ: ep-04-081024_english_Matthew_v11.mp3
# Pattern เดิม: *_${VOICE}_v11_agents.mp3  ❌
# Pattern ใหม่: *_${VOICE}_v11*.mp3  ✅

Solution: ใช้ wildcard ที่ยืดหยุ่นกว่า
```

**Step 4: Systematic Fixes**
```bash
# Fix 1: Replace bc with Python
DURATION_DIFF=$(python3 -c "print($SRT_DURATION - $VIDEO_DURATION)")

# Fix 2: Correct paths
WORK_DIR="${PROJECT_DIR}"  # Not subfolder in Paperspace
OUTPUT_DIR="${PROJECT_DIR}/output"

# Fix 3: Flexible pattern
OUTPUT_AUDIO=$(find output/ -name "*_${VOICE}_v11*.mp3" | head -1)

# Fix 4: Better error handling
if [ -z "$OUTPUT_AUDIO" ]; then
    echo "ERROR: No MP3 file found"
    ls -lh output/  # Show what's actually there
    exit 1
fi
```

**ผลลัพธ์:**
```
BEFORE (หลายวัน):
- bc errors ❌
- Path errors ❌
- File not found ❌
- ไม่รู้ว่าปัญหาอะไร

AFTER (วันนี้ - Codex method):
- ✅ Replace bc → Python
- ✅ Fix paths for Paperspace
- ✅ Flexible filename matching
- ✅ Production success!

Final Video:
- Video: 2567.807s
- Audio: 2567.784s
- Sync: -0.023s (PERFECT!)
- File: 902MB
```

#### **บทเรียนสำคัญ:**

**1. Test Environment First** 🧪
```bash
# ก่อนเขียน script ต้องเช็ค:
which bc          # มีหรือเปล่า?
which python3     # ทางเลือกอื่น?
pwd               # Path structure?
ls -la            # File locations?

Don't assume! Verify everything!
```

**2. Flexible Patterns** 🎯
```bash
# ❌ Rigid pattern
OUTPUT_AUDIO=$(find output/ -name "*_${VOICE}_v11_agents.mp3")

# ✅ Flexible pattern
OUTPUT_AUDIO=$(find output/ -name "*_${VOICE}_v11*.mp3" | head -1)

# ✅ With error handling
if [ -z "$OUTPUT_AUDIO" ]; then
    ls -lh output/  # Show what exists
    exit 1
fi
```

**3. Environment-Specific Code** 🔧
```bash
# Local structure:
WORK_DIR="${PROJECT_DIR}/quantum-sync-v11-production"

# Paperspace structure:
WORK_DIR="${PROJECT_DIR}"  # Files in root

Solution: Detect or document environment differences!
```
