#!/usr/bin/env python3
"""
Thai→English Video Translation Pipeline
=======================================
Version: 2.0.0

Core modules for translating Thai Forex videos to English SRT subtitles.
"""

__version__ = "2.0.0"
__author__ = "CodeMaster"

# Import main components
try:
    from .config import Config, ConfigMode
    from .context_analyzer import ContextAnalyzer, DocumentType
    from .translation_pipeline import TranslationPipeline, TranscriptionSegment
    from .data_management_system import DataManagementSystem, DictionaryEntry
except ImportError as e:
    # Graceful degradation for partial imports
    print(f"Warning: Some modules not available: {e}")

__all__ = [
    'Config',
    'ConfigMode',
    'ContextAnalyzer',
    'DocumentType',
    'TranslationPipeline',
    'TranscriptionSegment',
    'DataManagementSystem',
    'DictionaryEntry',
]
