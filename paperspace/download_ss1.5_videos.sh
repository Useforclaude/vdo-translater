#!/bin/bash

################################################################################
# SS1.5 Episodes Download Script
# Date: 2025-10-17
# Purpose: Download all SS1.5 videos from Google Drive to Paperspace
# Target: /notebooks/thai-whisper/videos/
################################################################################

set -e  # Exit on error

# Configuration
DOWNLOAD_DIR="/notebooks/thai-whisper/videos"
REQUIRED_SPACE_GB=10  # Minimum GB required

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo ""
    echo "================================================================"
    echo "$1"
    echo "================================================================"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  WARNING: $1${NC}"
}

check_requirements() {
    print_header "Checking Requirements"

    # Check gdown
    if ! command -v gdown &> /dev/null; then
        print_error "gdown not found. Installing..."
        pip install -U gdown
        print_success "gdown installed"
    else
        print_success "gdown found: $(gdown --version)"
    fi

    # Check storage space
    available_gb=$(df -BG "$DOWNLOAD_DIR" 2>/dev/null | awk 'NR==2 {print $4}' | sed 's/G//' || echo "0")
    if [ "$available_gb" -lt "$REQUIRED_SPACE_GB" ]; then
        print_warning "Low disk space: ${available_gb}GB available (recommended: ${REQUIRED_SPACE_GB}GB)"
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_error "Aborted by user"
            exit 1
        fi
    else
        print_success "Storage OK: ${available_gb}GB available"
    fi

    # Create directory
    mkdir -p "$DOWNLOAD_DIR"
    cd "$DOWNLOAD_DIR" || exit 1
    print_success "Working directory: $DOWNLOAD_DIR"
}

download_file() {
    local file_id="$1"
    local output_name="$2"
    local episode_label="$3"

    echo ""
    echo "------------------------------------------------"
    echo "$episode_label: $output_name"
    echo "------------------------------------------------"

    # Check if file already exists
    if [ -f "$output_name" ]; then
        print_warning "File already exists: $output_name"
        read -p "Skip download? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_success "Skipped: $output_name"
            return 0
        fi
        rm -f "$output_name"
    fi

    # Download with progress
    if gdown "$file_id" -O "$output_name"; then
        local size=$(ls -lh "$output_name" | awk '{print $5}')
        print_success "Downloaded: $output_name ($size)"
    else
        print_error "Failed to download: $output_name"
        return 1
    fi
}

################################################################################
# Main Download Process
################################################################################

main() {
    print_header "SS1.5 Episodes Download Script"
    echo "Target: $DOWNLOAD_DIR"
    echo "Date: $(date)"

    check_requirements

    print_header "Starting Downloads (6 files)"

    # Download all episodes
    download_file "1G5IZEQhYAZLdVB6RIXjbofmWyG-BxDIL" "SS-1.5-ep01.mp4" "[1/6] EP-01"
    download_file "1gQB_nh0WV5Ec_LgUQkKy1a3cRQfFf31D" "SS-1.5-ep02.mp4" "[2/6] EP-02"
    download_file "1N59eoYoMuu2wC7_sM-gihHiSxILfDv3j" "SS-1.5-Ep03.mp4" "[3/6] EP-03"
    download_file "1Lx0Me6TshvxsK_Uck7RddawnEB4pKyjT" "SS1.5-ep-04-part-1.mp4" "[4/6] EP-04 Part 1"
    download_file "10Q4UgtQlDQw1QzJfdgD6KVQjqnxTXyHt" "SS-1.5-ep-04-part-2.mp4" "[5/6] EP-04 Part 2"
    download_file "1PZUMnOfpOqwUEE9b07H0blEyM-1HezGu" "SS-1.5-ep05.mp4" "[6/6] EP-05"

    print_header "Download Summary"
    echo "Files in $DOWNLOAD_DIR:"
    ls -lh SS-*.mp4

    echo ""
    echo "Total size:"
    du -sh .

    echo ""
    print_success "All downloads complete!"
    echo ""
    echo "Next steps:"
    echo "1. Start tmux session: tmux new -s transcribe"
    echo "2. Run transcription script"
    echo "3. See: SS1.5_DOWNLOAD_GUIDE.md for details"
}

# Run main function
main
