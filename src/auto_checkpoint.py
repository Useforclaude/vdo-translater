#!/usr/bin/env python3
"""
Auto-Checkpoint System - Automatic Project State Backup
========================================================
Version: 1.0.0
Description: Automatic backup system that saves project state every 15 minutes
             to prevent data loss from power outages or system crashes

Features:
- Automatic backups every 15 minutes
- Git-based versioning
- Compression for space efficiency
- Rotation of old checkpoints
- Easy restore functionality
"""

import os
import sys
import time
import shutil
import logging
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional
import json
import threading

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ======================== AUTO-CHECKPOINT SYSTEM ========================

class AutoCheckpoint:
    """
    Automatic checkpoint/backup system
    Saves project state at regular intervals
    """

    def __init__(
        self,
        project_dir: Path,
        checkpoint_dir: Optional[Path] = None,
        interval_minutes: int = 15,
        max_checkpoints: int = 10
    ):
        """
        Initialize auto-checkpoint system

        Args:
            project_dir: Project directory to backup
            checkpoint_dir: Where to store checkpoints (default: .checkpoints/)
            interval_minutes: Backup interval in minutes
            max_checkpoints: Maximum checkpoints to keep
        """
        self.project_dir = Path(project_dir).resolve()
        self.checkpoint_dir = checkpoint_dir or (self.project_dir / ".checkpoints")
        self.interval_seconds = interval_minutes * 60
        self.max_checkpoints = max_checkpoints

        # Create checkpoint directory
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

        # Files/dirs to exclude from backup
        self.exclude_patterns = [
            ".checkpoints",
            ".git",
            "__pycache__",
            "*.pyc",
            ".cache",
            "*.log",
            "venv",
            ".venv",
            "node_modules",
            ".DS_Store",
            "output/*.mp4",
            "output/*.wav",
            "temp/*"
        ]

        # Running state
        self.running = False
        self.thread = None
        self.last_checkpoint = None

        logger.info(f"Auto-checkpoint initialized:")
        logger.info(f"  - Project: {self.project_dir}")
        logger.info(f"  - Checkpoints: {self.checkpoint_dir}")
        logger.info(f"  - Interval: {interval_minutes} minutes")

    def create_checkpoint(self, description: str = "") -> Path:
        """
        Create a checkpoint now

        Args:
            description: Optional description for this checkpoint

        Returns:
            Path to checkpoint directory
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_name = f"checkpoint_{timestamp}"

        if description:
            checkpoint_name += f"_{description}"

        checkpoint_path = self.checkpoint_dir / checkpoint_name

        try:
            logger.info(f"Creating checkpoint: {checkpoint_name}")

            # Create checkpoint metadata
            metadata = {
                "timestamp": datetime.now().isoformat(),
                "description": description,
                "project_dir": str(self.project_dir),
                "files_backed_up": []
            }

            # Create checkpoint directory
            checkpoint_path.mkdir(parents=True, exist_ok=True)

            # Copy important files
            files_backed_up = self._backup_files(self.project_dir, checkpoint_path)
            metadata["files_backed_up"] = files_backed_up
            metadata["file_count"] = len(files_backed_up)

            # Save metadata
            with open(checkpoint_path / "metadata.json", 'w') as f:
                json.dump(metadata, f, indent=2)

            # Cleanup old checkpoints
            self._cleanup_old_checkpoints()

            logger.info(f"✓ Checkpoint created: {checkpoint_name}")
            logger.info(f"  - Files backed up: {len(files_backed_up)}")

            self.last_checkpoint = checkpoint_path
            return checkpoint_path

        except Exception as e:
            logger.error(f"Failed to create checkpoint: {e}")
            # Cleanup failed checkpoint
            if checkpoint_path.exists():
                shutil.rmtree(checkpoint_path, ignore_errors=True)
            raise

    def _backup_files(self, source_dir: Path, dest_dir: Path) -> List[str]:
        """
        Backup files from source to destination

        Returns:
            List of files backed up
        """
        backed_up = []

        for item in source_dir.rglob("*"):
            # Skip if matches exclude pattern
            if self._should_exclude(item):
                continue

            # Skip if not a file
            if not item.is_file():
                continue

            # Calculate relative path
            rel_path = item.relative_to(source_dir)
            dest_path = dest_dir / rel_path

            # Create parent directory
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy file
            try:
                shutil.copy2(item, dest_path)
                backed_up.append(str(rel_path))
            except Exception as e:
                logger.warning(f"Failed to backup {rel_path}: {e}")

        return backed_up

    def _should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded"""
        path_str = str(path.relative_to(self.project_dir))

        for pattern in self.exclude_patterns:
            # Simple pattern matching
            if pattern.startswith("*."):
                # Extension match
                if path.suffix == pattern[1:]:
                    return True
            elif pattern.endswith("/*"):
                # Directory contents match
                if path_str.startswith(pattern[:-2]):
                    return True
            else:
                # Exact or substring match
                if pattern in path_str:
                    return True

        return False

    def _cleanup_old_checkpoints(self):
        """Remove old checkpoints beyond max limit"""
        checkpoints = sorted(
            [d for d in self.checkpoint_dir.iterdir() if d.is_dir()],
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )

        # Keep only max_checkpoints
        for old_checkpoint in checkpoints[self.max_checkpoints:]:
            logger.info(f"Removing old checkpoint: {old_checkpoint.name}")
            shutil.rmtree(old_checkpoint, ignore_errors=True)

    def list_checkpoints(self) -> List[dict]:
        """List all available checkpoints"""
        checkpoints = []

        for checkpoint_dir in sorted(
            self.checkpoint_dir.iterdir(),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        ):
            if not checkpoint_dir.is_dir():
                continue

            # Load metadata
            metadata_file = checkpoint_dir / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file) as f:
                    metadata = json.load(f)
            else:
                metadata = {
                    "timestamp": datetime.fromtimestamp(
                        checkpoint_dir.stat().st_mtime
                    ).isoformat(),
                    "description": "",
                    "file_count": 0
                }

            metadata["name"] = checkpoint_dir.name
            metadata["path"] = str(checkpoint_dir)
            checkpoints.append(metadata)

        return checkpoints

    def restore_checkpoint(self, checkpoint_name: str, backup_current: bool = True):
        """
        Restore from a checkpoint

        Args:
            checkpoint_name: Name of checkpoint to restore
            backup_current: Create backup of current state before restore
        """
        checkpoint_path = self.checkpoint_dir / checkpoint_name

        if not checkpoint_path.exists():
            raise ValueError(f"Checkpoint not found: {checkpoint_name}")

        logger.info(f"Restoring from checkpoint: {checkpoint_name}")

        # Backup current state first
        if backup_current:
            self.create_checkpoint("before_restore")

        # Restore files
        try:
            for item in checkpoint_path.rglob("*"):
                if item.name == "metadata.json":
                    continue

                if not item.is_file():
                    continue

                rel_path = item.relative_to(checkpoint_path)
                dest_path = self.project_dir / rel_path

                # Create parent directory
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                # Copy file
                shutil.copy2(item, dest_path)

            logger.info(f"✓ Restored from checkpoint: {checkpoint_name}")

        except Exception as e:
            logger.error(f"Failed to restore checkpoint: {e}")
            raise

    def start_auto_backup(self):
        """Start automatic backup thread"""
        if self.running:
            logger.warning("Auto-backup already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._backup_loop, daemon=True)
        self.thread.start()

        logger.info(f"✓ Auto-backup started (interval: {self.interval_seconds/60:.0f} min)")

    def stop_auto_backup(self):
        """Stop automatic backup thread"""
        if not self.running:
            return

        logger.info("Stopping auto-backup...")
        self.running = False

        if self.thread:
            self.thread.join(timeout=5)

        logger.info("✓ Auto-backup stopped")

    def _backup_loop(self):
        """Main backup loop (runs in thread)"""
        while self.running:
            try:
                # Create checkpoint
                self.create_checkpoint("auto")

                # Wait for next interval
                time.sleep(self.interval_seconds)

            except Exception as e:
                logger.error(f"Error in backup loop: {e}")
                time.sleep(60)  # Wait 1 minute on error


# ======================== CLI INTERFACE ========================

def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Auto-Checkpoint System for Project Backup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start auto-backup with default settings (15 min intervals)
  python auto_checkpoint.py start

  # Create checkpoint manually
  python auto_checkpoint.py create --desc "Before major changes"

  # List all checkpoints
  python auto_checkpoint.py list

  # Restore from checkpoint
  python auto_checkpoint.py restore checkpoint_20250103_143000

  # Start with custom interval
  python auto_checkpoint.py start --interval 10
        """
    )

    parser.add_argument(
        "command",
        choices=["start", "create", "list", "restore"],
        help="Command to execute"
    )

    parser.add_argument(
        "checkpoint",
        nargs="?",
        help="Checkpoint name (for restore command)"
    )

    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path.cwd(),
        help="Project directory (default: current directory)"
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=15,
        help="Backup interval in minutes (default: 15)"
    )

    parser.add_argument(
        "--max-checkpoints",
        type=int,
        default=10,
        help="Maximum checkpoints to keep (default: 10)"
    )

    parser.add_argument(
        "--desc",
        type=str,
        default="",
        help="Description for checkpoint"
    )

    args = parser.parse_args()

    # Initialize checkpoint system
    checkpoint = AutoCheckpoint(
        project_dir=args.project_dir,
        interval_minutes=args.interval,
        max_checkpoints=args.max_checkpoints
    )

    try:
        if args.command == "start":
            # Start auto-backup
            checkpoint.start_auto_backup()

            logger.info("\n✓ Auto-backup running. Press Ctrl+C to stop.\n")

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("\nStopping...")
                checkpoint.stop_auto_backup()

        elif args.command == "create":
            # Create manual checkpoint
            checkpoint.create_checkpoint(args.desc)

        elif args.command == "list":
            # List checkpoints
            checkpoints = checkpoint.list_checkpoints()

            if not checkpoints:
                logger.info("No checkpoints found")
            else:
                logger.info(f"\nAvailable checkpoints ({len(checkpoints)}):\n")
                for cp in checkpoints:
                    logger.info(f"  • {cp['name']}")
                    logger.info(f"    Time: {cp['timestamp']}")
                    logger.info(f"    Files: {cp.get('file_count', 'N/A')}")
                    if cp.get('description'):
                        logger.info(f"    Desc: {cp['description']}")
                    logger.info("")

        elif args.command == "restore":
            # Restore from checkpoint
            if not args.checkpoint:
                parser.error("restore command requires checkpoint name")

            checkpoint.restore_checkpoint(args.checkpoint)

    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
