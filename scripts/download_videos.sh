#!/bin/bash
# ========================================
# Download Videos from Google Drive
# For Paperspace/Remote Environment
# ========================================

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Storage directory (Paperspace persistent storage)
STORAGE_DIR="${STORAGE_DIR:-/storage/videos}"
mkdir -p "$STORAGE_DIR"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Video Downloader (Google Drive)${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if gdown is installed
if ! command -v gdown &> /dev/null; then
    echo -e "${YELLOW}Installing gdown...${NC}"
    pip install gdown
fi

# Video files with Google Drive IDs
declare -A VIDEOS=(
    ["ep01"]="1G5IZEQhYAZLdVB6RIXjbofmWyG-BxDIL"
    ["ep02"]="1gQB_nh0WV5Ec_LgUQkKy1a3cRQfFf31D"
    ["ep03"]="1N59eoYoMuu2wC7_sM-gihHiSxILfDv3j"
    ["ep04-part1"]="1Lx0Me6TshvxsK_Uck7RddawnEB4pKyjT"
    ["ep04-part2"]="10Q4UgtQlDQw1QzJfdgD6KVQjqnxTXyHt"
    ["ep05"]="1PZUMnOfpOqwUEE9b07H0blEyM-1HezGu"
)

declare -A FILENAMES=(
    ["ep01"]="ep01.mp4"
    ["ep02"]="ep02.mp4"
    ["ep03"]="Ep03.mp4"
    ["ep04-part1"]="ep-04-part-1.mp4"
    ["ep04-part2"]="ep-04-part-2.mp4"
    ["ep05"]="SS-1-5-ep05.mp4"
)

# Function: Download single video
download_video() {
    local KEY="$1"
    local FILE_ID="${VIDEOS[$KEY]}"
    local FILENAME="${FILENAMES[$KEY]}"
    local OUTPUT_PATH="$STORAGE_DIR/$FILENAME"

    echo -e "${YELLOW}Downloading: $FILENAME${NC}"
    echo -e "Target: $OUTPUT_PATH"

    # Check if already exists
    if [ -f "$OUTPUT_PATH" ]; then
        echo -e "${GREEN}✓ File already exists, skipping.${NC}"
        echo ""
        return 0
    fi

    # Download with gdown
    gdown "https://drive.google.com/uc?id=$FILE_ID" -O "$OUTPUT_PATH"

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Downloaded successfully!${NC}"
        ls -lh "$OUTPUT_PATH"
    else
        echo -e "${RED}✗ Download failed!${NC}"
    fi
    echo ""
}

# Function: Fuzzy search
fuzzy_search() {
    local QUERY=$(echo "$1" | tr '[:upper:]' '[:lower:]')

    for KEY in "${!VIDEOS[@]}"; do
        if [[ "$KEY" == *"$QUERY"* ]]; then
            echo "$KEY"
            return 0
        fi
    done

    return 1
}

# Main logic
if [ $# -eq 0 ]; then
    # No arguments: Download all videos
    echo -e "${YELLOW}No arguments provided. Downloading ALL videos...${NC}"
    echo ""

    for KEY in "${!VIDEOS[@]}"; do
        download_video "$KEY"
    done

elif [ "$1" == "list" ]; then
    # List available videos
    echo -e "${YELLOW}Available videos:${NC}"
    echo ""
    for KEY in "${!VIDEOS[@]}"; do
        echo "  - $KEY → ${FILENAMES[$KEY]}"
    done
    echo ""
    echo -e "${YELLOW}Usage:${NC}"
    echo "  bash download_videos.sh           # Download all"
    echo "  bash download_videos.sh ep01      # Download ep01"
    echo "  bash download_videos.sh 01        # Fuzzy match (ep01)"
    echo "  bash download_videos.sh part1     # Fuzzy match (ep04-part1)"

else
    # Download specific video (with fuzzy matching)
    QUERY="$1"

    # Try exact match first
    if [ -n "${VIDEOS[$QUERY]}" ]; then
        download_video "$QUERY"
    else
        # Try fuzzy search
        MATCH=$(fuzzy_search "$QUERY")
        if [ -n "$MATCH" ]; then
            echo -e "${YELLOW}Fuzzy match: '$QUERY' → '$MATCH'${NC}"
            echo ""
            download_video "$MATCH"
        else
            echo -e "${RED}No match found for: '$QUERY'${NC}"
            echo ""
            echo -e "${YELLOW}Try: bash download_videos.sh list${NC}"
            exit 1
        fi
    fi
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Downloaded files:${NC}"
ls -lh "$STORAGE_DIR/"*.mp4 2>/dev/null || echo "No files yet"
echo -e "${GREEN}========================================${NC}"
