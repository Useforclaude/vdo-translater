#!/usr/bin/env python3
"""
Data Management System - Smart External Data Loading
=====================================================
Version: 2.0.0
Author: CodeMaster
Description: Centralized data management with external file support
             No more hardcoding! Everything loads from JSON/YAML files.
"""

import json
import yaml
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    print('⚠️ Watchdog not installed. Auto-reload disabled.')
    Observer = None
    FileSystemEventHandler = object
import hashlib
import logging

logger = logging.getLogger(__name__)


# ======================== DATA STRUCTURES ========================

@dataclass
class DictionaryEntry:
    """Single dictionary entry"""
    thai: str
    english: str
    category: str
    priority: int = 2
    description: Optional[str] = None
    context: Optional[str] = None
    spoken_variations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


# ======================== FILE WATCHER ========================

class DictionaryFileWatcher(FileSystemEventHandler):
    """Watch dictionary files for changes and auto-reload"""
    
    def __init__(self, manager):
        self.manager = manager
        
    def on_modified(self, event):
        if event.src_path.endswith('.json') or event.src_path.endswith('.yaml'):
            logger.info(f"File changed: {event.src_path}")
            self.manager.reload_data()


# ======================== DATA LOADER ========================

class DataLoader:
    """
    Smart data loader that reads from external files
    Supports JSON, YAML, and CSV formats
    """
    
    def __init__(self, data_dir: Path = None):
        """Initialize data loader"""
        self.data_dir = data_dir or Path("data")
        self.cache = {}
        self.last_modified = {}
        
    def load_json(self, filepath: Path, use_cache: bool = True) -> Dict:
        """Load JSON file with caching"""
        filepath = self.data_dir / filepath if not filepath.is_absolute() else filepath
        
        # Check cache
        if use_cache and filepath in self.cache:
            # Check if file modified
            mtime = filepath.stat().st_mtime
            if mtime == self.last_modified.get(filepath):
                return self.cache[filepath]
        
        # Load file
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Update cache
            self.cache[filepath] = data
            self.last_modified[filepath] = filepath.stat().st_mtime
            
            logger.info(f"Loaded: {filepath}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load {filepath}: {e}")
            return {}
    
    def load_yaml(self, filepath: Path, use_cache: bool = True) -> Dict:
        """Load YAML file with caching"""
        filepath = self.data_dir / filepath if not filepath.is_absolute() else filepath
        
        # Check cache
        if use_cache and filepath in self.cache:
            mtime = filepath.stat().st_mtime
            if mtime == self.last_modified.get(filepath):
                return self.cache[filepath]
        
        # Load file
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            # Update cache
            self.cache[filepath] = data
            self.last_modified[filepath] = filepath.stat().st_mtime
            
            logger.info(f"Loaded: {filepath}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load {filepath}: {e}")
            return {}
    
    def save_json(self, data: Dict, filepath: Path, pretty: bool = True):
        """Save data to JSON file"""
        filepath = self.data_dir / filepath if not filepath.is_absolute() else filepath
        
        # Create directory if needed
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                json.dump(data, f, ensure_ascii=False)
        
        logger.info(f"Saved: {filepath}")
    
    def save_yaml(self, data: Dict, filepath: Path):
        """Save data to YAML file"""
        filepath = self.data_dir / filepath if not filepath.is_absolute() else filepath
        
        # Create directory if needed
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        
        logger.info(f"Saved: {filepath}")
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()
        self.last_modified.clear()


# ======================== DICTIONARY MANAGER ========================

class DictionaryManager:
    """
    Centralized dictionary management
    Loads all dictionaries from external files
    """
    
    def __init__(self, data_dir: Path = None, auto_reload: bool = True):
        """
        Initialize dictionary manager
        
        Args:
            data_dir: Directory containing data files
            auto_reload: Enable auto-reload on file changes
        """
        self.data_dir = data_dir or Path("data")
        self.loader = DataLoader(self.data_dir)
        
        # Dictionary storage
        self.forex_terms = {}
        self.colloquialisms = {}
        self.metaphors = {}
        self.custom_terms = {}
        self.patterns = {}
        
        # Indexes for fast lookup
        self.thai_index = {}
        self.english_index = {}
        
        # Load all data
        self.reload_data()
        
        # Setup file watcher
        if auto_reload:
            self.setup_file_watcher()
    
    def reload_data(self):
        """Reload all data from files"""
        logger.info("Reloading dictionary data...")
        
        # Load forex terms
        forex_data = self.loader.load_json(Path("dictionaries/forex_terms.json"))
        self.forex_terms = self._parse_dictionary(forex_data.get("terms", []))
        
        # Load colloquialisms
        colloquial_data = self.loader.load_json(Path("dictionaries/colloquialisms.json"))
        self.colloquialisms = self._parse_dictionary(colloquial_data.get("phrases", []))
        
        # Load metaphors
        metaphor_data = self.loader.load_json(Path("dictionaries/metaphors.json"))
        self.metaphors = metaphor_data.get("domains", {})
        
        # Load custom terms (user additions)
        custom_data = self.loader.load_json(Path("dictionaries/custom_terms.json"))
        self.custom_terms = self._parse_dictionary(custom_data.get("terms", []))
        
        # Load patterns
        pattern_data = self.loader.load_yaml(Path("patterns/speech_patterns.yaml"))
        self.patterns = pattern_data.get("patterns", {})
        
        # Rebuild indexes
        self._rebuild_indexes()
        
        logger.info(f"Loaded {self.get_total_terms()} terms")
    
    def _parse_dictionary(self, items: List[Dict]) -> Dict[str, DictionaryEntry]:
        """Parse dictionary items into DictionaryEntry objects"""
        entries = {}
        
        for item in items:
            entry = DictionaryEntry(
                thai=item.get("thai", ""),
                english=item.get("english", ""),
                category=item.get("category", "general"),
                priority=item.get("priority", 2),
                description=item.get("description"),
                context=item.get("context"),
                spoken_variations=item.get("spoken_variations", []),
                metadata=item.get("metadata", {})
            )
            
            if entry.thai:
                entries[entry.thai] = entry
        
        return entries
    
    def _rebuild_indexes(self):
        """Rebuild lookup indexes"""
        self.thai_index.clear()
        self.english_index.clear()
        
        # Index all dictionaries
        all_dicts = [
            self.forex_terms,
            self.colloquialisms,
            self.custom_terms
        ]
        
        for dictionary in all_dicts:
            for thai, entry in dictionary.items():
                # Thai index
                self.thai_index[thai] = entry
                
                # English index
                if entry.english:
                    self.english_index[entry.english.lower()] = entry
                
                # Variations index
                for variation in entry.spoken_variations:
                    self.thai_index[variation] = entry
    
    def setup_file_watcher(self):
        """Setup automatic file watching"""
        event_handler = DictionaryFileWatcher(self)
        observer = Observer()
        observer.schedule(event_handler, str(self.data_dir), recursive=True)
        observer.start()
        logger.info("File watcher started")
    
    def find_term(self, text: str) -> Optional[DictionaryEntry]:
        """Find a term in any dictionary"""
        # Check Thai index
        if text in self.thai_index:
            return self.thai_index[text]
        
        # Check English index
        if text.lower() in self.english_index:
            return self.english_index[text.lower()]
        
        return None
    
    def add_custom_term(self, entry: DictionaryEntry, save: bool = True):
        """Add a custom term"""
        self.custom_terms[entry.thai] = entry
        
        # Update indexes
        self.thai_index[entry.thai] = entry
        if entry.english:
            self.english_index[entry.english.lower()] = entry
        
        # Save to file
        if save:
            self.save_custom_terms()
    
    def save_custom_terms(self):
        """Save custom terms to file"""
        data = {
            "terms": [
                {
                    "thai": entry.thai,
                    "english": entry.english,
                    "category": entry.category,
                    "priority": entry.priority,
                    "description": entry.description,
                    "context": entry.context,
                    "spoken_variations": entry.spoken_variations,
                    "metadata": entry.metadata
                }
                for entry in self.custom_terms.values()
            ]
        }
        
        self.loader.save_json(data, Path("dictionaries/custom_terms.json"))
    
    def get_total_terms(self) -> int:
        """Get total number of terms"""
        return len(self.thai_index)
    
    def search_terms(self, query: str, limit: int = 10) -> List[DictionaryEntry]:
        """Search for terms containing query"""
        results = []
        query_lower = query.lower()
        
        for entry in self.thai_index.values():
            if (query_lower in entry.thai.lower() or 
                query_lower in entry.english.lower() or
                any(query_lower in var.lower() for var in entry.spoken_variations)):
                results.append(entry)
                
                if len(results) >= limit:
                    break
        
        return results
    
    def export_all(self, filepath: Path):
        """Export all dictionaries to a single file"""
        data = {
            "forex_terms": [self._entry_to_dict(e) for e in self.forex_terms.values()],
            "colloquialisms": [self._entry_to_dict(e) for e in self.colloquialisms.values()],
            "custom_terms": [self._entry_to_dict(e) for e in self.custom_terms.values()],
            "metaphors": self.metaphors,
            "patterns": self.patterns,
            "statistics": {
                "total_terms": self.get_total_terms(),
                "forex_terms": len(self.forex_terms),
                "colloquialisms": len(self.colloquialisms),
                "custom_terms": len(self.custom_terms),
                "exported_at": datetime.now().isoformat()
            }
        }
        
        self.loader.save_json(data, filepath)
    
    def _entry_to_dict(self, entry: DictionaryEntry) -> Dict:
        """Convert entry to dictionary"""
        return {
            "thai": entry.thai,
            "english": entry.english,
            "category": entry.category,
            "priority": entry.priority,
            "description": entry.description,
            "context": entry.context,
            "spoken_variations": entry.spoken_variations,
            "metadata": entry.metadata
        }


# ======================== DATA FILE TEMPLATES ========================

def create_initial_data_files(data_dir: Path):
    """Create initial data file structure with sample data"""
    
    # Create directories
    (data_dir / "dictionaries").mkdir(parents=True, exist_ok=True)
    (data_dir / "patterns").mkdir(parents=True, exist_ok=True)
    (data_dir / "configs/domains").mkdir(parents=True, exist_ok=True)
    
    # Create forex_terms.json
    forex_terms = {
        "terms": [
            {
                "thai": "แนวรับ",
                "english": "Support",
                "category": "technical",
                "priority": 1,
                "description": "Price support level",
                "spoken_variations": ["ซัพพอร์ต"]
            },
            {
                "thai": "แนวต้าน",
                "english": "Resistance",
                "category": "technical",
                "priority": 1,
                "description": "Price resistance level",
                "spoken_variations": ["รีซิสแตนซ์"]
            }
            # Add more terms...
        ]
    }
    
    with open(data_dir / "dictionaries/forex_terms.json", 'w', encoding='utf-8') as f:
        json.dump(forex_terms, f, ensure_ascii=False, indent=2)
    
    # Create colloquialisms.json
    colloquialisms = {
        "phrases": [
            {
                "thai": "ฝรั่งบอก",
                "english": "As Westerners say",
                "category": "colloquial",
                "context": "introducing_concept",
                "priority": 1
            },
            {
                "thai": "เข้าเนื้อกันดีกว่า",
                "english": "Let's dive into the details",
                "category": "colloquial",
                "context": "transition",
                "priority": 1
            }
            # Add more phrases...
        ]
    }
    
    with open(data_dir / "dictionaries/colloquialisms.json", 'w', encoding='utf-8') as f:
        json.dump(colloquialisms, f, ensure_ascii=False, indent=2)
    
    # Create metaphors.json
    metaphors = {
        "domains": {
            "military": {
                "pattern": "กองทัพ|ทหาร|ยึด|บุก",
                "mappings": {
                    "กองทัพ": "forces",
                    "ทหาร": "traders",
                    "ยึดเมือง": "capture levels"
                }
            },
            "automotive": {
                "pattern": "รถ|เบรค|ยูเทิร์น",
                "mappings": {
                    "เหยียบเบรค": "slowing down",
                    "ยูเทิร์น": "reversing"
                }
            }
        }
    }
    
    with open(data_dir / "dictionaries/metaphors.json", 'w', encoding='utf-8') as f:
        json.dump(metaphors, f, ensure_ascii=False, indent=2)
    
    # Create empty custom_terms.json
    custom_terms = {"terms": []}
    
    with open(data_dir / "dictionaries/custom_terms.json", 'w', encoding='utf-8') as f:
        json.dump(custom_terms, f, ensure_ascii=False, indent=2)
    
    # Create speech_patterns.yaml
    patterns = {
        "patterns": {
            "questions": [
                ".*ไหม$",
                ".*มั้ย$",
                ".*หรือเปล่า$"
            ],
            "continuations": [
                "^และ",
                "^แต่",
                "^หรือ",
                "^ดังนั้น"
            ],
            "fillers": [
                "ครับ",
                "ค่ะ",
                "นะ",
                "อ่า",
                "เอ่อ"
            ]
        }
    }
    
    with open(data_dir / "patterns/speech_patterns.yaml", 'w', encoding='utf-8') as f:
        yaml.dump(patterns, f, allow_unicode=True, default_flow_style=False)
    
    print(f"✅ Created initial data files in {data_dir}")


# ======================== SIMPLE API ========================

class SimpleDictionaryAPI:
    """Simple API for easy dictionary access"""
    
    def __init__(self, data_dir: Path = None):
        """Initialize API"""
        self.manager = DictionaryManager(data_dir)
    
    def translate(self, text: str) -> str:
        """Simple translation lookup"""
        entry = self.manager.find_term(text)
        if entry:
            return entry.english
        return text
    
    def add(self, thai: str, english: str, category: str = "custom"):
        """Add new term"""
        entry = DictionaryEntry(
            thai=thai,
            english=english,
            category=category
        )
        self.manager.add_custom_term(entry)
    
    def search(self, query: str) -> List[Dict]:
        """Search terms"""
        results = self.manager.search_terms(query)
        return [
            {"thai": e.thai, "english": e.english, "category": e.category}
            for e in results
        ]
    
    def reload(self):
        """Reload all dictionaries"""
        self.manager.reload_data()


# ======================== USAGE EXAMPLE ========================

def example_usage():
    """Example of using the data management system"""
    
    print("=" * 60)
    print("📚 Smart Dictionary Management System")
    print("=" * 60)
    
    # Setup data directory
    data_dir = Path("data")
    
    # Create initial files if not exist
    if not (data_dir / "dictionaries/forex_terms.json").exists():
        print("\n📁 Creating initial data files...")
        create_initial_data_files(data_dir)
    
    # Initialize manager
    print("\n🚀 Initializing Dictionary Manager...")
    manager = DictionaryManager(data_dir, auto_reload=True)
    
    print(f"✅ Loaded {manager.get_total_terms()} terms")
    
    # Test finding terms
    print("\n🔍 Testing term lookup:")
    test_terms = ["แนวรับ", "support", "ฝรั่งบอก"]
    
    for term in test_terms:
        entry = manager.find_term(term)
        if entry:
            print(f"  • {term} → {entry.english} ({entry.category})")
        else:
            print(f"  • {term} → Not found")
    
    # Test adding custom term
    print("\n➕ Adding custom term:")
    custom = DictionaryEntry(
        thai="พินบาร์",
        english="Pin bar",
        category="price_action",
        priority=1,
        spoken_variations=["พิน บาร์", "ปินบาร์"]
    )
    manager.add_custom_term(custom)
    print(f"  Added: {custom.thai} → {custom.english}")
    
    # Test search
    print("\n🔎 Searching for 'บาร์':")
    results = manager.search_terms("บาร์", limit=5)
    for entry in results:
        print(f"  • {entry.thai} → {entry.english}")
    
    # Simple API example
    print("\n" + "=" * 60)
    print("🎯 Simple API Example:")
    print("=" * 60)
    
    api = SimpleDictionaryAPI(data_dir)
    
    # Translate
    print("\n📝 Translation:")
    print(f"  แนวต้าน → {api.translate('แนวต้าน')}")
    
    # Add term
    api.add("โมเมนตัม", "Momentum", "technical")
    print("\n✅ Added new term via API")
    
    # Search
    print("\n🔍 Search results for 'โม':")
    results = api.search("โม")
    for r in results[:3]:
        print(f"  • {r['thai']} → {r['english']}")
    
    # Export all
    print("\n💾 Exporting all dictionaries...")
    manager.export_all(Path("all_dictionaries.json"))
    print("  Exported to all_dictionaries.json")


if __name__ == "__main__":
    example_usage()
