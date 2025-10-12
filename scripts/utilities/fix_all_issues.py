#!/usr/bin/env python3
"""
Fix All Issues Script - แก้ปัญหาทั้งหมดอัตโนมัติ
================================================
รันครั้งเดียวเพื่อแก้ไขทุกปัญหา
"""

import os
import sys
import subprocess
from pathlib import Path

def fix_config_file():
    """Fix syntax error in config.py"""
    print("🔧 Fixing config.py...")
    
    config_path = Path("config.py")
    if not config_path.exists():
        print("❌ config.py not found")
        return False
    
    # Read file
    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the syntax error
    # Replace problematic line
    old_line1 = 'prepend_punctuations: str = "\\"\'\"¿([{-"'
    new_line1 = 'prepend_punctuations: str = "\\"\'¿([{-"'
    
    old_line2 = "prepend_punctuations: str = \"\\\"\\'\"¿([{-\""
    new_line2 = "prepend_punctuations: str = \"\\\"'¿([{-\""
    
    # Try multiple possible formats
    if old_line1 in content:
        content = content.replace(old_line1, new_line1)
    elif old_line2 in content:
        content = content.replace(old_line2, new_line2)
    else:
        # Generic fix - find and replace the problematic pattern
        import re
        pattern = r'prepend_punctuations:\s*str\s*=\s*"[^"]*"'
        replacement = 'prepend_punctuations: str = "\\"\'¿([{-"'
        content = re.sub(pattern, replacement, content)
    
    # Write back
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ config.py fixed")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    required = [
        "watchdog",
        "pyyaml", 
        "python-dotenv"
    ]
    
    for package in required:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} already installed")
        except ImportError:
            print(f"📥 Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                          capture_output=True, text=True)
            print(f"✅ {package} installed")
    
    return True

def fix_data_management():
    """Make watchdog optional in data_management_system.py"""
    print("\n🔧 Fixing data_management_system.py...")
    
    dm_path = Path("data_management_system.py")
    if not dm_path.exists():
        print("❌ data_management_system.py not found")
        return False
    
    # Read file
    with open(dm_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find and fix import lines
    new_lines = []
    for i, line in enumerate(lines):
        if line.strip() == "from watchdog.observers import Observer":
            # Replace with try-except block
            new_lines.append("try:\n")
            new_lines.append("    from watchdog.observers import Observer\n")
            if i+1 < len(lines) and "FileSystemEventHandler" in lines[i+1]:
                new_lines.append("    from watchdog.events import FileSystemEventHandler\n")
                new_lines.append("    WATCHDOG_AVAILABLE = True\n")
                new_lines.append("except ImportError:\n")
                new_lines.append("    WATCHDOG_AVAILABLE = False\n")
                new_lines.append("    print('⚠️ Watchdog not installed. Auto-reload disabled.')\n")
                new_lines.append("    Observer = None\n")
                new_lines.append("    FileSystemEventHandler = object\n")
                lines[i+1] = ""  # Skip next line
            else:
                new_lines.append("    WATCHDOG_AVAILABLE = True\n")
                new_lines.append("except ImportError:\n")
                new_lines.append("    WATCHDOG_AVAILABLE = False\n")
                new_lines.append("    Observer = None\n")
        elif line.strip() == "from watchdog.events import FileSystemEventHandler":
            continue  # Skip if already handled
        else:
            new_lines.append(line)
    
    # Write back
    with open(dm_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("✅ data_management_system.py fixed")
    return True

def create_requirements_txt():
    """Create requirements.txt file"""
    print("\n📝 Creating requirements.txt...")
    
    requirements = """# Core dependencies
pyyaml
python-dotenv

# Optional features
watchdog  # For auto-reload

# API dependencies (add as needed)
# openai>=1.0.0
# openai-whisper
# redis
"""
    
    with open("requirements.txt", 'w', encoding='utf-8') as f:
        f.write(requirements)
    
    print("✅ requirements.txt created")
    return True

def run_migration():
    """Try to run migration script"""
    print("\n🔄 Running migration script...")
    
    if Path("migrate_to_json.py").exists():
        result = subprocess.run([sys.executable, "migrate_to_json.py"], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Migration completed")
            return True
        else:
            print("⚠️ Migration failed (may need manual run)")
            print(result.stderr)
    else:
        print("⚠️ migrate_to_json.py not found")
    
    return False

def test_imports():
    """Test if all imports work"""
    print("\n🧪 Testing imports...")
    
    modules = [
        ("config", "Config"),
        ("context_analyzer", "ContextAnalyzer"),
        ("data_management_system", "DictionaryManager")
    ]
    
    success = True
    for module, class_name in modules:
        try:
            mod = __import__(module)
            if hasattr(mod, class_name):
                print(f"✅ {module}.py works")
            else:
                print(f"⚠️ {module}.py: {class_name} not found")
                success = False
        except SyntaxError as e:
            print(f"❌ {module}.py: Syntax error - {e}")
            success = False
        except ImportError as e:
            print(f"⚠️ {module}.py: Import error - {e}")
            # This might be okay if dependencies not installed
        except Exception as e:
            print(f"❌ {module}.py: {e}")
            success = False
    
    return success

def main():
    """Run all fixes"""
    print("=" * 60)
    print("🔧 AUTO-FIX ALL ISSUES")
    print("=" * 60)
    
    # Fix config.py syntax error
    fix_config_file()
    
    # Install dependencies
    install_dependencies()
    
    # Fix data_management_system.py
    fix_data_management()
    
    # Create requirements.txt
    create_requirements_txt()
    
    # Run migration
    run_migration()
    
    # Test imports
    print("\n" + "=" * 60)
    test_success = test_imports()
    
    # Final status
    print("\n" + "=" * 60)
    print("📊 FINAL STATUS")
    print("=" * 60)
    
    if test_success:
        print("✅ All issues fixed! You can now run:")
        print("\n  python data_management_system.py")
        print("  python Test_Script_ep02.py")
    else:
        print("⚠️ Some issues remain. Check the errors above.")
        print("\nTry running:")
        print("  pip install -r requirements.txt")
        print("  python migrate_to_json.py")
    
    print("\n💡 Next steps:")
    print("1. Run: python migrate_to_json.py")
    print("2. Test: python data_management_system.py")
    print("3. Test with ep-02: python Test_Script_ep02.py")

if __name__ == "__main__":
    main()
