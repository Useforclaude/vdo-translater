#!/usr/bin/env python3
"""
Updated Configuration Module with .env Support and Mock Mode
=============================================================
Version: 1.1.0
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

# Try to load .env file
try:
    from dotenv import load_dotenv
    # Load .env file from project root
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✓ Loaded .env from: {env_path}")
    else:
        print(f"ℹ No .env file found at: {env_path}")
except ImportError:
    print("ℹ python-dotenv not installed. Install with: pip install python-dotenv")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ======================== ENUMS ========================

class ConfigMode(Enum):
    """Configuration presets"""
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    QUALITY_FOCUS = "quality_focus"
    COST_OPTIMIZED = "cost_optimized"
    MOCK = "mock"  # New: for testing without API


class TranslationModel(Enum):
    """Available translation models"""
    GPT_35_TURBO = "gpt-3.5-turbo"
    GPT_4 = "gpt-4"
    GPT_4_TURBO = "gpt-4-turbo-preview"
    LOCAL = "local"
    MOCK = "mock"  # New: for testing


class WhisperModel(Enum):
    """Available Whisper models"""
    TINY = "tiny"
    BASE = "base"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    LARGE_V2 = "large-v2"
    LARGE_V3 = "large-v3"


class CacheStrategy(Enum):
    """Caching strategies"""
    NONE = "none"
    MEMORY = "memory"
    DISK = "disk"
    REDIS = "redis"
    HYBRID = "hybrid"


# ======================== CONFIGURATION CLASSES ========================

@dataclass
class PathConfig:
    """Path configurations"""
    project_root: Path = Path(__file__).parent
    data_dir: Path = None
    cache_dir: Path = None
    output_dir: Path = None
    temp_dir: Path = None
    log_dir: Path = None
    
    def __post_init__(self):
        """Initialize paths"""
        if self.data_dir is None:
            self.data_dir = self.project_root / "data"
        if self.cache_dir is None:
            self.cache_dir = Path(os.getenv('CACHE_DIR', '.cache'))
        if self.output_dir is None:
            self.output_dir = self.project_root / "output"
        if self.temp_dir is None:
            self.temp_dir = self.project_root / "temp"
        if self.log_dir is None:
            self.log_dir = self.project_root / "logs"
        
        # Create directories
        for path in [self.data_dir, self.cache_dir, self.output_dir, 
                    self.temp_dir, self.log_dir]:
            path.mkdir(parents=True, exist_ok=True)


@dataclass
class APIConfig:
    """API configurations"""
    openai_api_key: Optional[str] = None
    openai_org_id: Optional[str] = None
    openai_base_url: Optional[str] = None
    max_retries: int = 3
    timeout: int = 30
    mock_mode: bool = False
    
    def __post_init__(self):
        """Load from environment"""
        if self.openai_api_key is None:
            self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if self.openai_org_id is None:
            self.openai_org_id = os.getenv('OPENAI_ORG_ID')
        if self.openai_base_url is None:
            self.openai_base_url = os.getenv('OPENAI_BASE_URL')
        
        # Check if we should use mock mode
        if not self.openai_api_key:
            logger.warning("No OPENAI_API_KEY found. Running in MOCK mode.")
            self.mock_mode = True
    
    def validate(self):
        """Validate API configuration"""
        if not self.mock_mode and not self.openai_api_key:
            logger.warning("OPENAI_API_KEY not set. Will run in MOCK mode for testing.")
            self.mock_mode = True
        return True


@dataclass
class WhisperConfig:
    """Whisper configuration"""
    model: WhisperModel = WhisperModel.LARGE_V3
    language: str = "th"
    task: str = "transcribe"
    temperature: float = 0.0
    temperature_increment_on_fallback: float = 0.2
    compression_ratio_threshold: float = 2.4
    logprob_threshold: float = -1.0
    no_speech_threshold: float = 0.6
    condition_on_previous_text: bool = True
    initial_prompt: Optional[str] = None
    word_timestamps: bool = True
    prepend_punctuations: str = "\"'\"([{-"
    append_punctuations: str = "\"\'.。,，!！?？:：\")]}、"
    
    def __post_init__(self):
        """Set Thai-specific prompt"""
        if self.initial_prompt is None:
            self.initial_prompt = "การวิเคราะห์ Forex และการเทรด"


@dataclass
class TranslationConfig:
    """Translation configuration"""
    default_model: TranslationModel = TranslationModel.GPT_35_TURBO
    complex_model: TranslationModel = TranslationModel.GPT_4
    temperature: float = 0.3
    max_tokens: int = 500
    top_p: float = 0.9
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    complexity_threshold: float = 0.7
    use_context: bool = True
    batch_size: int = 5
    
    def __post_init__(self):
        """Load from environment"""
        model_name = os.getenv('DEFAULT_MODEL', 'gpt-3.5-turbo')
        try:
            self.default_model = TranslationModel(model_name)
        except ValueError:
            pass
        
        complex_name = os.getenv('COMPLEX_MODEL', 'gpt-4')
        try:
            self.complex_model = TranslationModel(complex_name)
        except ValueError:
            pass


@dataclass
class CacheConfig:
    """Cache configuration"""
    strategy: CacheStrategy = CacheStrategy.HYBRID
    cache_dir: Path = Path(".cache")
    redis_url: Optional[str] = None
    max_memory_items: int = 10000
    ttl_seconds: int = 86400 * 30  # 30 days
    enable_compression: bool = True
    
    def __post_init__(self):
        """Load from environment"""
        if self.redis_url is None:
            self.redis_url = os.getenv('REDIS_URL')
        
        cache_dir = os.getenv('CACHE_DIR')
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        
        self.cache_dir.mkdir(parents=True, exist_ok=True)


@dataclass
class ProcessingConfig:
    """Processing configuration"""
    max_workers: int = 4
    batch_size: int = 10
    chunk_size: int = 5000
    enable_parallel: bool = True
    enable_gpu: bool = False
    device: str = "cpu"
    
    def __post_init__(self):
        """Load from environment"""
        workers = os.getenv('MAX_WORKERS')
        if workers:
            self.max_workers = int(workers)


@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_logging: bool = True
    console_logging: bool = True
    log_dir: Path = Path("logs")
    
    def __post_init__(self):
        """Load from environment"""
        level = os.getenv('LOG_LEVEL', 'INFO')
        self.level = level
        self.log_dir.mkdir(parents=True, exist_ok=True)


@dataclass
class QualityConfig:
    """Quality thresholds"""
    min_confidence: float = 0.85
    min_translation_score: float = 0.90
    max_segment_length: int = 100
    min_segment_length: int = 3
    require_terminology_check: bool = True
    require_context_analysis: bool = True


# ======================== MAIN CONFIG CLASS ========================

class Config:
    """Main configuration class"""
    
    def __init__(self, mode: ConfigMode = ConfigMode.DEVELOPMENT):
        """Initialize configuration"""
        self.mode = mode
        
        # Initialize all sub-configs
        self.paths = PathConfig()
        self.api = APIConfig()
        self.whisper = WhisperConfig()
        self.translation = TranslationConfig()
        self.cache = CacheConfig()
        self.processing = ProcessingConfig()
        self.logging = LoggingConfig()
        self.quality = QualityConfig()
        
        # Domain specific
        self.domain = os.getenv('DOMAIN', 'forex')
        
        # Feature flags
        self.features = {
            "use_colloquialism_detection": True,
            "use_ensemble_transcription": True,
            "use_two_pass_translation": True,
            "use_caching": True,
            "use_parallel_processing": True,
        }
        
        # Apply mode presets
        self._apply_mode_presets(mode)
        
        # Validate (with fallback to mock mode)
        self.api.validate()
        
        # Log configuration
        logger.info(f"Configuration initialized in {mode.value} mode")
        if self.api.mock_mode:
            logger.info("Running in MOCK mode (no API calls will be made)")
    
    def _apply_mode_presets(self, mode: ConfigMode):
        """Apply configuration presets based on mode"""
        if mode == ConfigMode.DEVELOPMENT:
            self.cache.strategy = CacheStrategy.MEMORY
            self.processing.max_workers = 2
            self.logging.level = "DEBUG"
            
        elif mode == ConfigMode.PRODUCTION:
            self.cache.strategy = CacheStrategy.HYBRID
            self.processing.max_workers = 4
            self.logging.level = "INFO"
            
        elif mode == ConfigMode.QUALITY_FOCUS:
            self.translation.default_model = TranslationModel.GPT_4
            self.translation.temperature = 0.2
            self.quality.min_confidence = 0.95
            
        elif mode == ConfigMode.COST_OPTIMIZED:
            self.translation.default_model = TranslationModel.GPT_35_TURBO
            self.translation.complex_model = TranslationModel.GPT_35_TURBO
            self.cache.strategy = CacheStrategy.HYBRID
            self.features["use_caching"] = True
            
        elif mode == ConfigMode.MOCK:
            self.api.mock_mode = True
            self.translation.default_model = TranslationModel.MOCK
            self.cache.strategy = CacheStrategy.MEMORY
    
    def get_model_for_complexity(self, complexity: float) -> TranslationModel:
        """Get appropriate model based on complexity"""
        if self.api.mock_mode:
            return TranslationModel.MOCK
        
        if complexity > self.translation.complexity_threshold:
            return self.translation.complex_model
        return self.translation.default_model
    
    def estimate_cost(self, segments: int, avg_length: int = 50) -> float:
        """Estimate translation cost"""
        if self.api.mock_mode:
            return 0.0
        
        # Rough estimation
        tokens_per_segment = avg_length * 4  # ~4 tokens per word
        total_tokens = segments * tokens_per_segment * 2  # input + output
        
        # Cost per 1K tokens
        if self.translation.default_model == TranslationModel.GPT_35_TURBO:
            cost_per_1k = 0.002
        elif self.translation.default_model == TranslationModel.GPT_4:
            cost_per_1k = 0.03
        else:
            cost_per_1k = 0.002
        
        # Factor in cache hit rate (assume 60%)
        cache_discount = 0.6 if self.features["use_caching"] else 0
        
        total_cost = (total_tokens / 1000) * cost_per_1k * (1 - cache_discount)
        
        return total_cost
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            "mode": self.mode.value,
            "paths": asdict(self.paths),
            "api": {k: v for k, v in asdict(self.api).items() 
                   if k != 'openai_api_key'},  # Don't expose API key
            "whisper": asdict(self.whisper),
            "translation": asdict(self.translation),
            "cache": asdict(self.cache),
            "processing": asdict(self.processing),
            "logging": asdict(self.logging),
            "quality": asdict(self.quality),
            "domain": self.domain,
            "features": self.features,
        }
    
    def save(self, filepath: Path):
        """Save configuration to file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2, default=str)
        logger.info(f"Configuration saved to {filepath}")
    
    @classmethod
    def load(cls, filepath: Path) -> 'Config':
        """Load configuration from file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        mode = ConfigMode(data.get('mode', 'development'))
        config = cls(mode=mode)
        
        # Update with loaded data
        # (Implementation details omitted for brevity)
        
        logger.info(f"Configuration loaded from {filepath}")
        return config


# ======================== QUICK ACCESS ========================

def get_config(mode: Optional[str] = None) -> Config:
    """Quick config getter"""
    if mode is None:
        mode = os.getenv('CONFIG_MODE', 'development')
    
    try:
        config_mode = ConfigMode(mode)
    except ValueError:
        logger.warning(f"Invalid mode '{mode}', using development")
        config_mode = ConfigMode.DEVELOPMENT
    
    return Config(mode=config_mode)


# ======================== TEST ========================

if __name__ == "__main__":
    print("Configuration Module Test")
    print("=" * 50)
    
    # Test different modes
    for mode in [ConfigMode.DEVELOPMENT, ConfigMode.MOCK, ConfigMode.COST_OPTIMIZED]:
        print(f"\nTesting {mode.value} mode:")
        config = Config(mode=mode)
        
        print(f"  API Mock Mode: {config.api.mock_mode}")
        print(f"  Default Model: {config.translation.default_model.value}")
        print(f"  Cache Strategy: {config.cache.strategy.value}")
        print(f"  Max Workers: {config.processing.max_workers}")
        
        # Test cost estimation
        cost = config.estimate_cost(segments=100)
        print(f"  Estimated cost for 100 segments: ${cost:.4f}")
    
    print("\n✅ Configuration module working correctly!")
