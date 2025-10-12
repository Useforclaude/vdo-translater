#!/usr/bin/env python3
"""
Batch Processor - Process multiple videos in parallel/sequence
==============================================================
Process multiple video files through the translation pipeline with progress tracking.

Features:
- Sequential or parallel processing
- Resume from last checkpoint
- Progress tracking with ETA
- Cost estimation and limits
- Detailed batch reports
- Error recovery

Usage:
    python scripts/batch_process.py input_dir/
    python scripts/batch_process.py input_dir/ -j 4 --mode production
    python scripts/batch_process.py manifest.json --resume
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from concurrent.futures import ProcessPoolExecutor, as_completed
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)
logger = logging.getLogger(__name__)

# Local imports
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from src.orchestrator import VideoTranslationOrchestrator, OrchestratorResult
    from src.config import ConfigMode
    from src.context_analyzer import DocumentType
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    logger.error("Make sure you're running from project root")
    sys.exit(1)


# ======================== DATA STRUCTURES ========================

@dataclass
class BatchJob:
    """Single batch job"""
    index: int
    video_path: Path
    output_dir: Path
    status: str = "pending"  # pending, processing, completed, failed
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    error: Optional[str] = None
    result: Optional[Dict] = None


@dataclass
class BatchProgress:
    """Batch processing progress"""
    total_jobs: int
    completed: int
    failed: int
    in_progress: int
    pending: int
    total_cost: float
    total_duration: float
    start_time: datetime
    estimated_finish: Optional[datetime] = None


@dataclass
class BatchReport:
    """Complete batch processing report"""
    batch_id: str
    start_time: datetime
    end_time: datetime
    total_duration: float
    total_videos: int
    successful: int
    failed: int
    total_cost: float
    average_cost_per_video: float
    jobs: List[BatchJob]


# ======================== BATCH PROCESSOR ========================

class BatchProcessor:
    """Process multiple videos in batch"""

    def __init__(
        self,
        config_mode: ConfigMode = ConfigMode.PRODUCTION,
        whisper_model: str = "large-v3",
        device: str = "cpu",
        max_workers: int = 1,
        max_cost: Optional[float] = None
    ):
        """
        Initialize batch processor

        Args:
            config_mode: Pipeline configuration mode
            whisper_model: Whisper model name
            device: Device for Whisper (cpu/cuda)
            max_workers: Maximum parallel workers (1 = sequential)
            max_cost: Maximum total cost limit (None = unlimited)
        """
        self.config_mode = config_mode
        self.whisper_model = whisper_model
        self.device = device
        self.max_workers = max_workers
        self.max_cost = max_cost

        self.batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.checkpoint_file = Path(f".batch_checkpoint_{self.batch_id}.json")

        logger.info("=" * 70)
        logger.info("Batch Processor Initialized")
        logger.info("=" * 70)
        logger.info(f"Mode: {config_mode.value}")
        logger.info(f"Whisper model: {whisper_model}")
        logger.info(f"Device: {device}")
        logger.info(f"Max workers: {max_workers}")
        if max_cost:
            logger.info(f"Max cost limit: ${max_cost:.2f}")

    def discover_videos(
        self,
        input_path: Path,
        extensions: List[str] = None
    ) -> List[Path]:
        """
        Discover video files in directory or from manifest

        Args:
            input_path: Directory path or manifest JSON
            extensions: Video file extensions to include

        Returns:
            List of video file paths
        """
        if extensions is None:
            extensions = ['.mp4', '.avi', '.mkv', '.mov', '.webm', '.flv', '.m4v']

        videos = []

        # Check if manifest JSON
        if input_path.is_file() and input_path.suffix == '.json':
            logger.info(f"Loading manifest: {input_path}")
            with open(input_path, 'r') as f:
                manifest = json.load(f)

            # Extract chunk paths from manifest
            if 'chunks' in manifest:
                for chunk in manifest['chunks']:
                    chunk_path = Path(chunk['output_path'])
                    if chunk_path.exists():
                        videos.append(chunk_path)
            else:
                logger.warning("No chunks found in manifest")

        # Check if directory
        elif input_path.is_dir():
            logger.info(f"Scanning directory: {input_path}")
            for ext in extensions:
                videos.extend(input_path.glob(f"*{ext}"))
                videos.extend(input_path.glob(f"*{ext.upper()}"))

            videos = sorted(set(videos))  # Remove duplicates and sort

        else:
            raise ValueError(f"Invalid input: {input_path}")

        logger.info(f"Found {len(videos)} video files")
        return videos

    def create_jobs(
        self,
        videos: List[Path],
        output_dir: Path
    ) -> List[BatchJob]:
        """
        Create batch jobs from video list

        Args:
            videos: List of video paths
            output_dir: Output directory

        Returns:
            List of BatchJob objects
        """
        jobs = []
        for i, video_path in enumerate(videos):
            job = BatchJob(
                index=i,
                video_path=video_path,
                output_dir=output_dir / video_path.stem
            )
            jobs.append(job)

        return jobs

    def process_single(
        self,
        job: BatchJob,
        doc_type: DocumentType = DocumentType.TUTORIAL
    ) -> BatchJob:
        """
        Process single video job

        Args:
            job: BatchJob to process
            doc_type: Document type

        Returns:
            Updated BatchJob with results
        """
        job.status = "processing"
        job.start_time = datetime.now()

        try:
            # Initialize orchestrator
            orchestrator = VideoTranslationOrchestrator(
                whisper_model=self.whisper_model,
                config_mode=self.config_mode,
                device=self.device
            )

            # Process video
            result = orchestrator.process_video(
                input_path=job.video_path,
                output_dir=job.output_dir,
                doc_type=doc_type
            )

            job.end_time = datetime.now()

            if result.success:
                job.status = "completed"
                job.result = result.stats
            else:
                job.status = "failed"
                job.error = result.error

        except Exception as e:
            job.status = "failed"
            job.error = str(e)
            job.end_time = datetime.now()
            logger.error(f"Job {job.index} failed: {e}")

        return job

    def save_checkpoint(self, jobs: List[BatchJob]):
        """Save checkpoint for resume capability"""
        checkpoint = {
            'batch_id': self.batch_id,
            'timestamp': datetime.now().isoformat(),
            'jobs': [
                {
                    'index': job.index,
                    'video_path': str(job.video_path),
                    'output_dir': str(job.output_dir),
                    'status': job.status,
                    'error': job.error,
                    'result': job.result
                }
                for job in jobs
            ]
        }

        with open(self.checkpoint_file, 'w') as f:
            json.dump(checkpoint, f, indent=2)

    def load_checkpoint(self, checkpoint_path: Path) -> List[BatchJob]:
        """Load checkpoint for resume"""
        with open(checkpoint_path, 'r') as f:
            checkpoint = json.load(f)

        jobs = []
        for job_data in checkpoint['jobs']:
            job = BatchJob(
                index=job_data['index'],
                video_path=Path(job_data['video_path']),
                output_dir=Path(job_data['output_dir']),
                status=job_data['status'],
                error=job_data.get('error'),
                result=job_data.get('result')
            )
            jobs.append(job)

        logger.info(f"Loaded checkpoint: {checkpoint_path}")
        logger.info(f"  Batch ID: {checkpoint['batch_id']}")
        logger.info(f"  Total jobs: {len(jobs)}")
        completed = sum(1 for j in jobs if j.status == 'completed')
        logger.info(f"  Completed: {completed}/{len(jobs)}")

        return jobs

    def process_batch(
        self,
        jobs: List[BatchJob],
        doc_type: DocumentType = DocumentType.TUTORIAL
    ) -> BatchReport:
        """
        Process batch of jobs

        Args:
            jobs: List of BatchJob objects
            doc_type: Document type

        Returns:
            BatchReport with results
        """
        start_time = datetime.now()
        total_cost = 0.0

        logger.info("\n" + "=" * 70)
        logger.info(f"Starting batch processing: {len(jobs)} videos")
        logger.info("=" * 70)

        # Filter pending jobs
        pending_jobs = [j for j in jobs if j.status == "pending"]
        completed_jobs = [j for j in jobs if j.status == "completed"]

        if not pending_jobs:
            logger.info("All jobs already completed!")
            end_time = datetime.now()
            return self._create_report(jobs, start_time, end_time)

        logger.info(f"Pending: {len(pending_jobs)}, Already completed: {len(completed_jobs)}")

        # Sequential processing
        if self.max_workers == 1:
            for i, job in enumerate(pending_jobs, 1):
                logger.info(f"\n[{i}/{len(pending_jobs)}] Processing: {job.video_path.name}")

                # Check cost limit
                if self.max_cost and total_cost >= self.max_cost:
                    logger.warning(f"Cost limit reached: ${total_cost:.2f} >= ${self.max_cost:.2f}")
                    job.status = "skipped"
                    job.error = "Cost limit reached"
                    continue

                job = self.process_single(job, doc_type)

                # Update cost
                if job.result and 'estimated_cost' in job.result:
                    total_cost += job.result['estimated_cost']

                # Save checkpoint
                self.save_checkpoint(jobs)

                # Progress report
                completed = sum(1 for j in jobs if j.status == "completed")
                failed = sum(1 for j in jobs if j.status == "failed")
                logger.info(f"Progress: {completed}/{len(jobs)} completed, {failed} failed")
                logger.info(f"Total cost so far: ${total_cost:.4f}")

        # Parallel processing
        else:
            logger.info(f"Processing in parallel with {self.max_workers} workers...")

            with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_job = {
                    executor.submit(self.process_single, job, doc_type): job
                    for job in pending_jobs
                }

                for future in as_completed(future_to_job):
                    job = future_to_job[future]

                    try:
                        result_job = future.result()

                        # Update job in list
                        for i, j in enumerate(jobs):
                            if j.index == result_job.index:
                                jobs[i] = result_job
                                break

                        # Update cost
                        if result_job.result and 'estimated_cost' in result_job.result:
                            total_cost += result_job.result['estimated_cost']

                        # Save checkpoint
                        self.save_checkpoint(jobs)

                        # Progress
                        completed = sum(1 for j in jobs if j.status == "completed")
                        failed = sum(1 for j in jobs if j.status == "failed")
                        logger.info(f"Progress: {completed}/{len(jobs)} completed, {failed} failed")

                    except Exception as e:
                        logger.error(f"Job {job.index} failed: {e}")

        end_time = datetime.now()
        return self._create_report(jobs, start_time, end_time)

    def _create_report(
        self,
        jobs: List[BatchJob],
        start_time: datetime,
        end_time: datetime
    ) -> BatchReport:
        """Create batch report"""
        successful = sum(1 for j in jobs if j.status == "completed")
        failed = sum(1 for j in jobs if j.status == "failed")
        total_cost = sum(
            j.result.get('estimated_cost', 0) for j in jobs
            if j.result and 'estimated_cost' in j.result
        )

        report = BatchReport(
            batch_id=self.batch_id,
            start_time=start_time,
            end_time=end_time,
            total_duration=(end_time - start_time).total_seconds(),
            total_videos=len(jobs),
            successful=successful,
            failed=failed,
            total_cost=total_cost,
            average_cost_per_video=total_cost / len(jobs) if jobs else 0,
            jobs=jobs
        )

        return report

    def save_report(self, report: BatchReport, output_path: Path):
        """Save batch report to JSON"""
        report_dict = {
            'batch_id': report.batch_id,
            'start_time': report.start_time.isoformat(),
            'end_time': report.end_time.isoformat(),
            'total_duration_seconds': report.total_duration,
            'total_videos': report.total_videos,
            'successful': report.successful,
            'failed': report.failed,
            'total_cost': report.total_cost,
            'average_cost_per_video': report.average_cost_per_video,
            'jobs': [
                {
                    'index': job.index,
                    'video': str(job.video_path),
                    'output_dir': str(job.output_dir),
                    'status': job.status,
                    'error': job.error,
                    'result': job.result
                }
                for job in report.jobs
            ]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, indent=2, ensure_ascii=False)

        logger.info(f"Report saved: {output_path}")


# ======================== CLI INTERFACE ========================

def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description="Batch process multiple videos through translation pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all videos in directory (sequential)
  python scripts/batch_process.py input_dir/

  # Parallel processing with 4 workers
  python scripts/batch_process.py input_dir/ -j 4

  # Production mode with cost limit
  python scripts/batch_process.py input_dir/ --mode production --max-cost 50.00

  # Process from manifest (from split_video.py)
  python scripts/batch_process.py video_chunks_manifest.json

  # Resume from checkpoint
  python scripts/batch_process.py --resume .batch_checkpoint_20250103_123456.json
        """
    )

    parser.add_argument(
        'input',
        type=Path,
        nargs='?',
        help='Input directory or manifest JSON file'
    )

    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=Path('batch_output'),
        help='Output directory (default: batch_output/)'
    )

    parser.add_argument(
        '-j', '--jobs',
        type=int,
        default=1,
        help='Number of parallel workers (default: 1 = sequential)'
    )

    parser.add_argument(
        '-m', '--model',
        type=str,
        default='large-v3',
        help='Whisper model (default: large-v3)'
    )

    parser.add_argument(
        '--mode',
        type=str,
        default='production',
        choices=['development', 'production', 'quality_focus', 'cost_optimized', 'mock'],
        help='Pipeline mode (default: production)'
    )

    parser.add_argument(
        '--device',
        type=str,
        default='cpu',
        choices=['cpu', 'cuda'],
        help='Device for Whisper (default: cpu)'
    )

    parser.add_argument(
        '--doc-type',
        type=str,
        default='tutorial',
        choices=['tutorial', 'analysis', 'news', 'commentary', 'mixed'],
        help='Document type (default: tutorial)'
    )

    parser.add_argument(
        '--max-cost',
        type=float,
        help='Maximum total cost limit in USD'
    )

    parser.add_argument(
        '--resume',
        type=Path,
        help='Resume from checkpoint file'
    )

    parser.add_argument(
        '--report',
        type=Path,
        help='Save report to file (default: batch_report_<timestamp>.json)'
    )

    args = parser.parse_args()

    try:
        # Mode mapping
        mode_map = {
            'development': ConfigMode.DEVELOPMENT,
            'production': ConfigMode.PRODUCTION,
            'quality_focus': ConfigMode.QUALITY_FOCUS,
            'cost_optimized': ConfigMode.COST_OPTIMIZED,
            'mock': ConfigMode.MOCK
        }
        config_mode = mode_map[args.mode]

        # Doc type mapping
        doc_type_map = {
            'tutorial': DocumentType.TUTORIAL,
            'analysis': DocumentType.ANALYSIS,
            'news': DocumentType.NEWS,
            'commentary': DocumentType.COMMENTARY,
            'mixed': DocumentType.MIXED
        }
        doc_type = doc_type_map[args.doc_type]

        # Initialize processor
        processor = BatchProcessor(
            config_mode=config_mode,
            whisper_model=args.model,
            device=args.device,
            max_workers=args.jobs,
            max_cost=args.max_cost
        )

        # Resume mode
        if args.resume:
            if not args.resume.exists():
                logger.error(f"Checkpoint not found: {args.resume}")
                sys.exit(1)

            jobs = processor.load_checkpoint(args.resume)
            report = processor.process_batch(jobs, doc_type)

        # Normal mode
        else:
            if not args.input:
                parser.print_help()
                sys.exit(1)

            if not args.input.exists():
                logger.error(f"Input not found: {args.input}")
                sys.exit(1)

            # Discover videos
            videos = processor.discover_videos(args.input)

            if not videos:
                logger.error("No videos found!")
                sys.exit(1)

            # Create jobs
            jobs = processor.create_jobs(videos, args.output)

            # Process
            report = processor.process_batch(jobs, doc_type)

        # Print summary
        logger.info("\n" + "=" * 70)
        logger.info("BATCH PROCESSING COMPLETE")
        logger.info("=" * 70)
        logger.info(f"Total videos: {report.total_videos}")
        logger.info(f"Successful: {report.successful}")
        logger.info(f"Failed: {report.failed}")
        logger.info(f"Total duration: {timedelta(seconds=int(report.total_duration))}")
        logger.info(f"Total cost: ${report.total_cost:.4f}")
        logger.info(f"Average cost/video: ${report.average_cost_per_video:.4f}")

        # Save report
        if args.report:
            report_path = args.report
        else:
            report_path = Path(f"batch_report_{processor.batch_id}.json")

        processor.save_report(report, report_path)

        # Clean up checkpoint
        if processor.checkpoint_file.exists():
            processor.checkpoint_file.unlink()
            logger.info("Checkpoint cleaned up")

        sys.exit(0 if report.failed == 0 else 1)

    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Batch processing interrupted")
        logger.info("Run with --resume to continue from checkpoint")
        sys.exit(130)
    except Exception as e:
        logger.error(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
