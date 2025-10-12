#!/bin/bash
# ========================================
# Paperspace Whisper Transcription Script
# With tmux, checkpoint, and fuzzy matching
# ========================================

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Default paths
STORAGE_DIR="${STORAGE_DIR:-/storage/videos}"
CHECKPOINT_DIR="${CHECKPOINT_DIR:-/storage/whisper_checkpoints}"
PROJECT_DIR="${PROJECT_DIR:-/notebooks/video-translater}"
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python"

mkdir -p "$CHECKPOINT_DIR"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Paperspace Whisper Transcription${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Function: List available videos
list_videos() {
    echo -e "${YELLOW}Available videos in $STORAGE_DIR:${NC}"
    echo ""

    if ls "$STORAGE_DIR"/*.mp4 1> /dev/null 2>&1; then
        ls -lh "$STORAGE_DIR"/*.mp4 | awk '{print "  - " $9 " (" $5 ")"}'
    else
        echo -e "${RED}No videos found. Run download_videos.sh first!${NC}"
        exit 1
    fi
    echo ""
}

# Function: Fuzzy match video file
fuzzy_match() {
    local QUERY=$(echo "$1" | tr '[:upper:]' '[:lower:]')
    local MATCHES=()

    # Search for matching files
    for FILE in "$STORAGE_DIR"/*.mp4; do
        BASENAME=$(basename "$FILE" .mp4 | tr '[:upper:]' '[:lower:]')
        if [[ "$BASENAME" == *"$QUERY"* ]]; then
            MATCHES+=("$FILE")
        fi
    done

    # Return result
    if [ ${#MATCHES[@]} -eq 0 ]; then
        return 1
    elif [ ${#MATCHES[@]} -eq 1 ]; then
        echo "${MATCHES[0]}"
        return 0
    else
        # Multiple matches: show options
        echo -e "${YELLOW}Multiple matches found:${NC}" >&2
        for i in "${!MATCHES[@]}"; do
            echo "  $((i+1)). $(basename ${MATCHES[$i]})" >&2
        done
        echo "${MATCHES[0]}" # Return first match
        return 0
    fi
}

# Function: Start transcription in tmux
start_transcription() {
    local VIDEO_PATH="$1"
    local VIDEO_NAME=$(basename "$VIDEO_PATH" .mp4)
    local SESSION_NAME="whisper-$VIDEO_NAME"

    echo -e "${BLUE}Video: $(basename $VIDEO_PATH)${NC}"
    echo -e "${BLUE}Session: $SESSION_NAME${NC}"
    echo -e "${BLUE}Checkpoint: $CHECKPOINT_DIR${NC}"
    echo ""

    # Check if session exists
    if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
        echo -e "${YELLOW}Session '$SESSION_NAME' already exists!${NC}"
        echo -e "${YELLOW}Options:${NC}"
        echo "  1. Attach to existing session: tmux attach -t $SESSION_NAME"
        echo "  2. Kill and restart: tmux kill-session -t $SESSION_NAME"
        exit 1
    fi

    # Create tmux session with transcription command
    echo -e "${GREEN}Creating tmux session: $SESSION_NAME${NC}"
    echo ""

    tmux new-session -d -s "$SESSION_NAME" "
        cd $PROJECT_DIR && \
        echo '========================================' && \
        echo 'Whisper Transcription Started' && \
        echo 'Video: $VIDEO_PATH' && \
        echo 'Checkpoint: $CHECKPOINT_DIR' && \
        echo '========================================' && \
        echo '' && \
        $VENV_PYTHON scripts/whisper_transcribe.py \
            '$VIDEO_PATH' \
            --checkpoint-dir '$CHECKPOINT_DIR' \
            --checkpoint-interval 10 \
            --resume \
            --device auto && \
        echo '' && \
        echo '========================================' && \
        echo '✓ Transcription Complete!' && \
        echo '========================================' && \
        echo 'Press Enter to close this session...' && \
        read
    "

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ tmux session created successfully!${NC}"
        echo ""
        echo -e "${YELLOW}Commands:${NC}"
        echo "  Attach to session:  tmux attach -t $SESSION_NAME"
        echo "  Detach from session: Ctrl+B then D"
        echo "  Kill session:       tmux kill-session -t $SESSION_NAME"
        echo ""
        echo -e "${YELLOW}Monitor progress (in another terminal):${NC}"
        echo "  $VENV_PYTHON scripts/whisper_status.py --watch"
        echo ""
        echo -e "${BLUE}Auto-attaching in 3 seconds...${NC}"
        sleep 3
        tmux attach -t "$SESSION_NAME"
    else
        echo -e "${RED}✗ Failed to create tmux session${NC}"
        exit 1
    fi
}

# Main logic
if [ $# -eq 0 ]; then
    # No arguments: show help
    list_videos
    echo -e "${YELLOW}Usage:${NC}"
    echo "  bash paperspace_transcribe.sh <video-name-or-pattern>"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo "  bash paperspace_transcribe.sh ep01         # Exact or fuzzy match"
    echo "  bash paperspace_transcribe.sh 01           # Fuzzy match"
    echo "  bash paperspace_transcribe.sh part1        # Match 'ep-04-part-1'"
    echo "  bash paperspace_transcribe.sh ep05         # Match 'SS-1-5-ep05'"
    exit 0
fi

# Get query
QUERY="$1"

# Try exact file path first
if [ -f "$QUERY" ]; then
    VIDEO_PATH="$QUERY"
# Try file in storage directory
elif [ -f "$STORAGE_DIR/$QUERY" ]; then
    VIDEO_PATH="$STORAGE_DIR/$QUERY"
# Try fuzzy matching
else
    VIDEO_PATH=$(fuzzy_match "$QUERY")
    if [ $? -ne 0 ]; then
        echo -e "${RED}No match found for: '$QUERY'${NC}"
        echo ""
        list_videos
        exit 1
    fi
    echo -e "${GREEN}Fuzzy match: '$QUERY' → $(basename $VIDEO_PATH)${NC}"
    echo ""
fi

# Verify file exists
if [ ! -f "$VIDEO_PATH" ]; then
    echo -e "${RED}File not found: $VIDEO_PATH${NC}"
    exit 1
fi

# Start transcription
start_transcription "$VIDEO_PATH"
