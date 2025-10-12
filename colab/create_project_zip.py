#!/usr/bin/env python3
"""
Create Project Zip for Colab Upload
===================================
Creates a lightweight zip file with all necessary project files for Google Colab.

Usage:
    python colab/create_project_zip.py
    python colab/create_project_zip.py --output custom_name.zip
"""

import os
import sys
import zipfile
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Files to include in zip
INCLUDE_PATTERNS = [
    # Core modules
    'src/__init__.py',
    'src/config.py',
    'src/context_analyzer.py',
    'src/data_management_system.py',
    'src/translation_pipeline.py',
    'src/thai_transcriber.py',
    'src/orchestrator.py',

    # Dictionaries
    'data/dictionaries/thai_idioms.json',
    'data/dictionaries/thai_slang.json',
    'data/dictionaries/forex_terms.json',
    'data/dictionaries/colloquialisms.json',
    'data/dictionaries/metaphors.json',

    # Config files
    'requirements.txt',

    # Documentation
    'colab/README_COLAB.md',
]

# Files to exclude (even if matched by patterns)
EXCLUDE_PATTERNS = [
    '__pycache__',
    '.pyc',
    '.git',
    '.venv',
    'venv',
    '.env',
    '.env.example',
    'logs',
    'output',
    'tests',
    '.pytest_cache',
    '.mypy_cache',
    '.DS_Store',
    'checkpoint',
    '.json.backup',
]


class ProjectZipCreator:
    """Create lightweight project zip for Colab"""

    def __init__(self, project_root: Path, output_path: Path):
        """
        Initialize zip creator

        Args:
            project_root: Root directory of project
            output_path: Output zip file path
        """
        self.project_root = project_root
        self.output_path = output_path
        self.files_added = []
        self.total_size = 0

    def should_include(self, file_path: Path) -> bool:
        """
        Check if file should be included in zip

        Args:
            file_path: File path to check

        Returns:
            True if file should be included
        """
        # Convert to relative path
        try:
            rel_path = file_path.relative_to(self.project_root)
        except ValueError:
            return False

        rel_path_str = str(rel_path)

        # Check exclude patterns
        for pattern in EXCLUDE_PATTERNS:
            if pattern in rel_path_str:
                return False

        # Check include patterns
        for pattern in INCLUDE_PATTERNS:
            if rel_path_str == pattern:
                return True

        return False

    def add_file(self, zip_file: zipfile.ZipFile, file_path: Path):
        """
        Add file to zip

        Args:
            zip_file: ZipFile object
            file_path: File to add
        """
        if not file_path.exists():
            logger.warning(f"File not found (skipping): {file_path}")
            return

        # Get relative path for zip archive
        arcname = file_path.relative_to(self.project_root)

        # Add to zip
        zip_file.write(file_path, arcname=arcname)

        # Track
        size = file_path.stat().st_size
        self.files_added.append(str(arcname))
        self.total_size += size

        logger.debug(f"  Added: {arcname} ({size:,} bytes)")

    def create_readme(self, zip_file: zipfile.ZipFile):
        """
        Add quick start README to zip root

        Args:
            zip_file: ZipFile object
        """
        readme_content = f"""# Thai Video Translator - Colab Package

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 🚀 Quick Start

1. **Upload to Colab**: Upload this entire zip file
2. **Extract**: Will auto-extract in notebook
3. **Upload .env**: Create .env with OPENAI_API_KEY
4. **Run notebook**: Follow instructions in notebook

## 📦 Package Contents

This package includes:

- ✅ Core translation modules (src/)
- ✅ Thai idiom & slang dictionaries (105 idioms, 30 slang)
- ✅ Forex terminology database
- ✅ Context analysis system
- ✅ Smart translation pipeline

**Total files**: {len(self.files_added)}
**Package size**: {self.total_size / 1024:.1f} KB

## 📚 Documentation

See `colab/README_COLAB.md` for complete guide.

## 🔑 Required

- OpenAI API key (for translation)
- Google Colab (free tier OK, GPU recommended)

---

*Happy Translating!* 🎬
"""

        # Add to zip
        zip_file.writestr('README.txt', readme_content)
        logger.info("  Added: README.txt")

    def create_zip(self) -> Path:
        """
        Create project zip file

        Returns:
            Path to created zip file
        """
        logger.info("=" * 60)
        logger.info("Creating Colab Project Zip")
        logger.info("=" * 60)

        # Ensure output directory exists
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        # Create zip
        with zipfile.ZipFile(self.output_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:

            logger.info("\nAdding files...")

            # Add all included files
            for pattern in INCLUDE_PATTERNS:
                file_path = self.project_root / pattern

                if file_path.exists():
                    if file_path.is_file():
                        self.add_file(zip_file, file_path)
                    else:
                        # Directory - add all files
                        for f in file_path.rglob('*'):
                            if f.is_file() and self.should_include(f):
                                self.add_file(zip_file, f)
                else:
                    logger.warning(f"Pattern not found (skipping): {pattern}")

            # Add README
            logger.info("\nAdding README...")
            self.create_readme(zip_file)

        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("ZIP CREATED SUCCESSFULLY")
        logger.info("=" * 60)
        logger.info(f"Output: {self.output_path}")
        logger.info(f"Total files: {len(self.files_added)}")
        logger.info(f"Total size: {self.total_size / 1024:.1f} KB ({self.total_size / (1024*1024):.2f} MB)")

        # File list summary
        logger.info(f"\nIncluded files:")
        for category in ['src/', 'data/', 'colab/', 'requirements.txt']:
            matching = [f for f in self.files_added if f.startswith(category)]
            if matching:
                logger.info(f"  {category}: {len(matching)} files")

        return self.output_path

    def verify_zip(self) -> bool:
        """
        Verify zip file integrity

        Returns:
            True if zip is valid
        """
        logger.info("\nVerifying zip file...")

        try:
            with zipfile.ZipFile(self.output_path, 'r') as zip_file:
                # Test zip
                bad_file = zip_file.testzip()
                if bad_file:
                    logger.error(f"Corrupt file in zip: {bad_file}")
                    return False

                # Check critical files
                critical_files = [
                    'src/orchestrator.py',
                    'src/thai_transcriber.py',
                    'data/dictionaries/thai_idioms.json',
                    'requirements.txt',
                    'README.txt'
                ]

                for critical in critical_files:
                    if critical not in zip_file.namelist():
                        logger.error(f"Missing critical file: {critical}")
                        return False

                logger.info("✅ Zip file is valid")
                return True

        except zipfile.BadZipFile as e:
            logger.error(f"Bad zip file: {e}")
            return False


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Create Colab project zip file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create default zip in colab/ directory
  python colab/create_project_zip.py

  # Custom output path
  python colab/create_project_zip.py -o my_project.zip

  # Verbose mode
  python colab/create_project_zip.py -v
        """
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=None,
        help='Output zip file path (default: colab/project.zip)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output (show all files)'
    )

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Determine project root
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_path = project_root / 'colab' / 'project.zip'

    try:
        # Create zip
        creator = ProjectZipCreator(project_root, output_path)
        zip_path = creator.create_zip()

        # Verify
        if creator.verify_zip():
            logger.info("\n" + "=" * 60)
            logger.info("SUCCESS!")
            logger.info("=" * 60)
            logger.info(f"\n📦 Colab package ready: {zip_path}")
            logger.info(f"\nNext steps:")
            logger.info(f"1. Open Colab notebook: colab/thai_video_translator.ipynb")
            logger.info(f"2. Upload this zip file: {zip_path.name}")
            logger.info(f"3. Follow notebook instructions")
            logger.info(f"\n🚀 Happy translating!")
            sys.exit(0)
        else:
            logger.error("\n❌ Zip verification failed")
            sys.exit(1)

    except Exception as e:
        logger.error(f"\n❌ Failed to create zip: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
