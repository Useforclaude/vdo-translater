#!/bin/bash

################################################################################
# SS1.5 Episodes Transcription Script
# Date: 2025-10-17
# Purpose: Transcribe all SS1.5 videos using Whisper large-v3
# Requires: video-translater project installed on Paperspace
################################################################################

set -e

# Configuration
VIDEOS_DIR="/notebooks/thai-whisper/videos"
PROJECT_DIR="/notebooks/video-translater"
OUTPUT_DIR="$PROJECT_DIR/workflow/01_transcripts"
CHECKPOINT_DIR="/storage/whisper_checkpoints"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

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

transcribe_video() {
    local video_file="$1"
    local output_file="$2"
    local episode_label="$3"

    print_header "$episode_label"

    echo "Input:  $video_file"
    echo "Output: $output_file"
    echo "Started: $(date)"

    if [ ! -f "$video_file" ]; then
        print_error "Video not found: $video_file"
        return 1
    fi

    # Run transcription
    "$PROJECT_DIR/.venv/bin/python" "$PROJECT_DIR/scripts/whisper_transcribe.py" \
        "$video_file" \
        --checkpoint-dir "$CHECKPOINT_DIR" \
        --checkpoint-interval 10 \
        --resume \
        -o "$output_file"

    if [ -f "$output_file" ]; then
        local size=$(ls -lh "$output_file" | awk '{print $5}')
        print_success "Completed: $output_file ($size)"
    else
        print_error "Failed to create: $output_file"
        return 1
    fi
}

main() {
    print_header "SS1.5 Transcription Batch Process"
    echo "Videos: $VIDEOS_DIR"
    echo "Output: $OUTPUT_DIR"
    echo "Started: $(date)"

    # Check project exists
    if [ ! -d "$PROJECT_DIR" ]; then
        print_error "Project not found: $PROJECT_DIR"
        exit 1
    fi

    # Check videos directory
    if [ ! -d "$VIDEOS_DIR" ]; then
        print_error "Videos directory not found: $VIDEOS_DIR"
        exit 1
    fi

    # Create output and checkpoint directories
    mkdir -p "$OUTPUT_DIR"
    mkdir -p "$CHECKPOINT_DIR"

    cd "$PROJECT_DIR"

    # Transcribe all episodes
    transcribe_video \
        "$VIDEOS_DIR/SS-1.5-ep01.mp4" \
        "$OUTPUT_DIR/SS-1.5-ep01_transcript.json" \
        "[1/6] Transcribing EP-01"

    transcribe_video \
        "$VIDEOS_DIR/SS-1.5-ep02.mp4" \
        "$OUTPUT_DIR/SS-1.5-ep02_transcript.json" \
        "[2/6] Transcribing EP-02"

    transcribe_video \
        "$VIDEOS_DIR/SS-1.5-Ep03.mp4" \
        "$OUTPUT_DIR/SS-1.5-ep03_transcript.json" \
        "[3/6] Transcribing EP-03"

    transcribe_video \
        "$VIDEOS_DIR/SS1.5-ep-04-part-1.mp4" \
        "$OUTPUT_DIR/SS-1.5-ep04-part1_transcript.json" \
        "[4/6] Transcribing EP-04 Part 1"

    transcribe_video \
        "$VIDEOS_DIR/SS-1.5-ep-04-part-2.mp4" \
        "$OUTPUT_DIR/SS-1.5-ep04-part2_transcript.json" \
        "[5/6] Transcribing EP-04 Part 2"

    transcribe_video \
        "$VIDEOS_DIR/SS-1.5-ep05.mp4" \
        "$OUTPUT_DIR/SS-1.5-ep05_transcript.json" \
        "[6/6] Transcribing EP-05"

    print_header "Merging EP-04 Parts"

    "$PROJECT_DIR/.venv/bin/python" "$PROJECT_DIR/scripts/merge_transcripts.py" \
        "$OUTPUT_DIR/SS-1.5-ep04-part1_transcript.json" \
        "$OUTPUT_DIR/SS-1.5-ep04-part2_transcript.json" \
        -o "$OUTPUT_DIR/SS-1.5-ep04_transcript.json"

    print_success "EP-04 merged successfully"

    print_header "Transcription Summary"
    echo "Output directory: $OUTPUT_DIR"
    ls -lh "$OUTPUT_DIR"/SS-1.5-*.json

    echo ""
    echo "Total size:"
    du -sh "$OUTPUT_DIR"

    echo ""
    print_success "All transcriptions complete!"
    echo ""
    echo "Final transcripts:"
    echo "  - SS-1.5-ep01_transcript.json"
    echo "  - SS-1.5-ep02_transcript.json"
    echo "  - SS-1.5-ep03_transcript.json"
    echo "  - SS-1.5-ep04_transcript.json (merged)"
    echo "  - SS-1.5-ep05_transcript.json"
    echo ""
    echo "Completed: $(date)"
}

main
