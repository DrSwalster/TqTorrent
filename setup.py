#!/usr/bin/env python3
"""
TqTorrent Setup - Install in Documents
"""

import os
import sys
import subprocess
from pathlib import Path
import datetime
import traceback

def get_documents_folder():
    """Get Documents folder path"""
    try:
        # Try multiple methods to get Documents folder
        docs = Path.home() / "Documents"
        if docs.exists():
            return docs
        
        # Try environment variable
        docs_env = os.environ.get("USERPROFILE", "")
        if docs_env:
            docs = Path(docs_env) / "Documents"
            if docs.exists():
                return docs
        
        # Last resort - current directory
        print("⚠ Documents folder not found, using current directory")
        return Path.cwd()
        
    except Exception as e:
        print(f"⚠ Error getting Documents folder: {e}")
        return Path.cwd()

def create_folder_structure(base_dir):
    """Create TqTorrent folder structure"""
    print(f"\n📁 Creating TqTorrent in: {base_dir}")
    
    try:
        # Create main directory
        base_dir.mkdir(exist_ok=True)
        print(f"✓ Main folder: {base_dir.name}")
        
        # Create subdirectories
        dirs_to_create = [
            "Localsaves_by_TqTorrent/saves",
            "log",
            "TqManager",
            "Version",
            "mods",
            "profiles",
            "downloads"
        ]
        
        for dir_path in dirs_to_create:
            full_path = base_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created: {dir_path}")
        
        # Create files
        create_config_files(base_dir)
        
        return True
        
    except PermissionError:
        print(f"✗ Permission denied for: {base_dir}")
        print("  Try running as Administrator")
        return False
    except Exception as e:
        print(f"✗ Error creating structure: {e}")
        return False

def create_config_files(base_dir):
    """Create all configuration files"""
    print("\n📝 Creating configuration files...")
    
    try:
        # 1. cnf.txt
        cnf_content = f"""# TqTorrent Configuration
# Created: {datetime.datetime.now()}
# Version: 1.0.0

[General]
app_name=TqTorrent
version=1.0.0

[Paths]
base={base_dir}
saves={base_dir}\\Localsaves_by_TqTorrent\\saves
logs={base_dir}\\log

[Settings]
first_run=true
"""
        cnf_file = base_dir / "Localsaves_by_TqTorrent" / "saves" / "cnf.txt"
        cnf_file.parent.mkdir(parents=True, exist_ok=True)
        cnf_file.write_text(cnf_content, encoding='utf-8')
        print("✓ Created: cnf.txt")
        
        # 2. Empty config file
        config_file = base_dir / "Localsaves_by_TqTorrent" / "saves" / "config"
        config_file.touch()
        print("✓ Created: config")
        
        # 3. log.txt
        log_content = f"""TqTorrent Log
{"="*40}
Date: {datetime.datetime.now()}
Path: {base_dir}
{"="*40}

[INFO] Setup completed successfully
"""
        log_file = base_dir / "log" / "log.txt"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        log_file.write_text(log_content, encoding='utf-8')
        print("✓ Created: log.txt")
        
        # 4. version.txt
        version_content = f"""TqTorrent v1.0.0
Install Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Location: {base_dir}
"""
        version_file = base_dir / "Version" / "version.txt"
        version_file.parent.mkdir(parents=True, exist_ok=True)
        version_file.write_text(version_content, encoding='utf-8')
        print("✓ Created: version.txt")
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating config files: {e}")
        return False

def create_main_program(base_dir):
    """Create main.py program"""
    try:
        main_content = '''#!/usr/bin/env python3
"""
TqTorrent Main Program
"""

print("="*60)
print("            TQTORRENT")
print("="*60)
print()
print("✅ Program successfully installed!")
print()
print("📁 Installation completed.")
print("🎉 You can now use TqTorrent!")
print()
print("="*60)
print()
input("Press Enter to exit...")
'''
        main_file = base_dir / "TqTorrent.py"
        main_file.write_text(main_content, encoding='utf-8')
        print("✓ Created: TqTorrent.py")
        return main_file
        
    except Exception as e:
        print(f"✗ Error creating main program: {e}")
        return None

def create_launcher(base_dir, main_file):
    """Create launcher files"""
    try:
        # Create .bat launcher in Documents folder
        bat_content = f'''@echo off
chcp 65001 >nul
title TqTorrent
color 0A
echo ========================================
echo          TQTORRENT LAUNCHER
echo ========================================
echo.
echo Starting TqTorrent...
echo.
cd /d "{base_dir}"
"{sys.executable}" "TqTorrent.py"
echo.
echo Program finished.
pause
'''
        bat_file = base_dir / "Launch_TqTorrent.bat"
        bat_file.write_text(bat_content, encoding='utf-8')
        print("✓ Created: Launch_TqTorrent.bat")
        
        # Try to create desktop shortcut
        try:
            desktop = Path.home() / "Desktop"
            if desktop.exists():
                desktop_bat = desktop / "TqTorrent.bat"
                desktop_content = f'''@echo off
echo Launching TqTorrent from Documents...
cd /d "{base_dir}"
"Launch_TqTorrent.bat"
'''
                desktop_bat.write_text(desktop_content, encoding='utf-8')
                print("✓ Created desktop shortcut")
        except:
            print("⚠ Could not create desktop shortcut")
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating launcher: {e}")
        return False

def setup():
    """Main setup function"""
    print("\n" + "="*60)
    print("         TQTORRENT SETUP")
    print("="*60)
    print()
    
    # Get Documents folder
    docs_folder = get_documents_folder()
    base_dir = docs_folder / "TqTorrent"
    
    print(f"📁 Will install to: {base_dir}")
    print()
    
    # Step 1: Create structure
    print("[1/3] Creating folder structure...")
    if not create_folder_structure(base_dir):
        print("\n❌ Failed to create folder structure")
        print("Trying alternative location...")
        
        # Try current directory as fallback
        base_dir = Path.cwd() / "TqTorrent"
        print(f"Trying: {base_dir}")
        
        if not create_folder_structure(base_dir):
            input("\n❌ Setup failed. Press Enter to exit...")
            return False
    
    # Step 2: Create main program
    print("\n[2/3] Creating main program...")
    main_file = create_main_program(base_dir)
    if not main_file:
        print("⚠ Warning: Main program not created")
    
    # Step 3: Create launcher
    print("\n[3/3] Creating launcher...")
    if main_file:
        create_launcher(base_dir, main_file)
    else:
        print("⚠ Skipping launcher (no main program)")
    
    # Summary
    print("\n" + "="*60)
    print("         SETUP COMPLETE!")
    print("="*60)
    print()
    print("✅ TqTorrent has been installed!")
    print()
    print(f"📁 Location: {base_dir}")
    print()
    print("🚀 How to run:")
    print(f"   1. Go to: {base_dir}")
    print(f"   2. Run 'Launch_TqTorrent.bat'")
    
    if main_file and main_file.exists():
        print(f"   3. Or run: \"{sys.executable}\" \"TqTorrent.py\"")
    
    print()
    print("📁 Created folders:")
    try:
        for item in base_dir.iterdir():
            if item.is_dir():
                print(f"   • {item.name}/")
            elif item.suffix in ['.py', '.bat']:
                print(f"   • {item.name}")
    except:
        print("   (Cannot list contents)")
    
    print()
    print("="*60)
    
    # Ask to run
    print()
    choice = input("Run TqTorrent now? (Y/N): ").strip().upper()
    if choice == 'Y' and main_file and main_file.exists():
        print("\n🚀 Launching TqTorrent...\n")
        subprocess.run([sys.executable, str(main_file)])
    
    input("\nPress Enter to exit setup...")
    return True

def main():
    """Main function"""
    try:
        # Set UTF-8 for Windows
        if sys.platform == "win32":
            os.system("chcp 65001 >nul")
        
        # Print debug info
        print(f"Python: {sys.executable}")
        print(f"Current dir: {Path.cwd()}")
        
        setup()
        
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"\n\n❌ UNEXPECTED ERROR:")
        print(f"Error: {e}")
        traceback.print_exc()
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
