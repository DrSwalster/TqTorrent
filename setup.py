#!/usr/bin/env python3
"""
TqTorrent Setup - ETS2 Launcher Style
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path
import datetime
import traceback

def check_python_installation():
    """Check if Python is properly installed"""
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True, check=True)
        return True, result.stdout.strip()
    except FileNotFoundError:
        return False, "Python not found in PATH"
    except Exception as e:
        return False, f"Python error: {str(e)}"

def check_and_install_library(lib_name):
    """Check and install a Python library"""
    try:
        # Try to import
        __import__(lib_name)
        return True, f"{lib_name} already installed"
    except ImportError:
        # Try to install
        try:
            print(f"Installing {lib_name}...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", lib_name],
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.returncode == 0:
                return True, f"{lib_name} installed successfully"
            else:
                return False, f"Failed to install {lib_name}: {result.stderr}"
        except subprocess.TimeoutExpired:
            return False, f"Timeout installing {lib_name}"
        except Exception as e:
            return False, f"Error installing {lib_name}: {str(e)}"

def install_required_libraries():
    """Install all required libraries"""
    required_libs = ["requests", "beautifulsoup4", "psutil", "pillow"]
    
    print("\n" + "="*50)
    print("Checking and installing required libraries...")
    print("="*50)
    
    for lib in required_libs:
        success, message = check_and_install_library(lib)
        if success:
            print(f"✓ {message}")
        else:
            print(f"✗ {message}")
    
    print("\nLibrary installation complete!")
    return True

def create_tqtorrent_structure():
    """Create TqTorrent folder structure"""
    try:
        base_dir = Path.home() / "Documents" / "TqTorrent"
        
        print("\n" + "="*50)
        print("Creating TqTorrent folder structure...")
        print("="*50)
        
        # Create main directory
        base_dir.mkdir(exist_ok=True)
        print(f"✓ Main directory: {base_dir}")
        
        # Create subdirectories
        directories = [
            'Localsaves_by_TqTorrent/saves',
            'log',
            'TqManager',
            'Version',
            'mods',
            'profiles',
            'downloads',
            'cache',
            'backups'
        ]
        
        for dir_path in directories:
            full_path = base_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created: {dir_path}")
        
        # Create configuration files
        create_config_files(base_dir)
        
        print("\n" + "="*50)
        print("Folder structure created successfully!")
        print("="*50)
        
        return True, base_dir
        
    except Exception as e:
        return False, f"Error creating structure: {str(e)}"

def create_config_files(base_dir):
    """Create all configuration files"""
    # cnf.txt
    cnf_content = f"""# TqTorrent Configuration
# Created: {datetime.datetime.now()}
# Version: 1.0.0

[General]
app_name=TqTorrent
version=1.0.0
author=DrSwalster
first_run=true

[Paths]
base={base_dir}
saves={base_dir}/Localsaves_by_TqTorrent/saves
logs={base_dir}/log
mods={base_dir}/mods
profiles={base_dir}/profiles

[Settings]
auto_update=true
backup_enabled=true
"""
    
    cnf_file = base_dir / "Localsaves_by_TqTorrent" / "saves" / "cnf.txt"
    cnf_file.parent.mkdir(parents=True, exist_ok=True)
    cnf_file.write_text(cnf_content, encoding='utf-8')
    print(f"✓ Created: cnf.txt")
    
    # Empty config file
    config_file = base_dir / "Localsaves_by_TqTorrent" / "saves" / "config"
    config_file.touch()
    print(f"✓ Created: config")
    
    # Log file
    log_content = f"""TqTorrent Log
{"="*40}
Date: {datetime.datetime.now()}
Version: 1.0.0
{"="*40}

[INFO] Initial setup completed
"""
    log_file = base_dir / "log" / "log.txt"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text(log_content, encoding='utf-8')
    print(f"✓ Created: log.txt")
    
    # Version file
    version_content = f"""TqTorrent v1.0.0
Install Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    version_file = base_dir / "Version" / "version.txt"
    version_file.parent.mkdir(parents=True, exist_ok=True)
    version_file.write_text(version_content, encoding='utf-8')
    print(f"✓ Created: version.txt")

def create_main_program(base_dir):
    """Create main.py program file"""
    try:
        main_content = '''#!/usr/bin/env python3
"""
TqTorrent Main Program
"""

import os
import sys
from pathlib import Path
import datetime

print("="*60)
print("            TQTORRENT - MAIN PROGRAM")
print("="*60)
print()
print("🎉 Congratulations! TqTorrent has been successfully installed!")
print()
print(f"Installation directory: {Path(__file__).parent}")
print(f"Installation date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()
print("📁 Folder structure:")
print("  • Documents/TqTorrent/ - Main directory")
print("  • Documents/TqTorrent/Localsaves_by_TqTorrent/saves/ - Saves and configs")
print("  • Documents/TqTorrent/log/ - Log files")
print("  • Documents/TqTorrent/TqManager/ - Manager files")
print("  • Documents/TqTorrent/Version/ - Version info")
print("  • Documents/TqTorrent/mods/ - Mods directory")
print("  • Documents/TqTorrent/profiles/ - Profiles directory")
print()
print("🚀 What's next:")
print("  1. You can add your Python scripts to this folder")
print("  2. Modify config files in Localsaves_by_TqTorrent/saves/")
print("  3. Check logs in log/ folder")
print()
print("="*60)
print()
input("Press Enter to exit...")
'''
        
        main_file = base_dir / "TqTorrent.py"
        main_file.write_text(main_content, encoding='utf-8')
        print(f"✓ Created: TqTorrent.py")
        
        return main_file
        
    except Exception as e:
        print(f"✗ Error creating main program: {str(e)}")
        return None

def create_desktop_shortcut(base_dir, main_file):
    """Create desktop shortcut"""
    try:
        desktop = Path.home() / "Desktop"
        
        # Create .bat file shortcut
        bat_content = f'''@echo off
chcp 65001 >nul
title TqTorrent Launcher
color 0A
echo ========================================
echo        TQTORRENT LAUNCHER
echo ========================================
echo.
echo Starting TqTorrent...
echo.
cd /d "{base_dir}"
"{sys.executable}" "{main_file}"
echo.
echo Press any key to exit...
pause >nul
'''
        
        shortcut_path = desktop / "TqTorrent.bat"
        shortcut_path.write_text(bat_content, encoding='utf-8')
        print(f"✓ Desktop shortcut: {shortcut_path}")
        
        # Also create a simple launcher.py
        launcher_content = f'''#!/usr/bin/env python3
"""
TqTorrent Launcher
"""

import subprocess
import sys
import os

print("Launching TqTorrent...")
print(f"Python: {sys.executable}")
print(f"Script: {main_file}")

try:
    subprocess.run([sys.executable, str(main_file)])
except Exception as e:
    print(f"Error: {{e}}")
    input("Press Enter to exit...")
'''
        
        launcher_path = base_dir / "launcher.py"
        launcher_path.write_text(launcher_content, encoding='utf-8')
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating shortcut: {str(e)}")
        return False

def console_setup():
    """Run setup in console mode"""
    print("\n" + "="*60)
    print("         TQTORRENT SETUP ASSISTANT")
    print("="*60)
    print()
    
    # Step 1: Check Python
    print("[1/6] Checking Python installation...")
    success, message = check_python_installation()
    if not success:
        print(f"✗ ERROR: {message}")
        print("\nPlease install Python first:")
        print("1. Download from: https://www.python.org/downloads/")
        print("2. During installation, CHECK 'Add Python to PATH'")
        print("3. Then run this setup again")
        input("\nPress Enter to exit...")
        return
    
    print(f"✓ {message}")
    
    # Step 2: Install libraries
    print("\n[2/6] Installing required libraries...")
    if not install_required_libraries():
        print("⚠ Some libraries may not be installed properly")
        print("You can install them manually later:")
        print("pip install requests beautifulsoup4 psutil pillow")
    
    # Step 3: Create structure
    print("\n[3/6] Creating folder structure...")
    success, result = create_tqtorrent_structure()
    if not success:
        print(f"✗ ERROR: {result}")
        input("\nPress Enter to exit...")
        return
    
    base_dir = result
    
    # Step 4: Create main program
    print("\n[4/6] Creating main program...")
    main_file = create_main_program(base_dir)
    if not main_file:
        print("⚠ Could not create main program file")
        # Create at least an empty file
        try:
            main_file = base_dir / "TqTorrent.py"
            main_file.write_text("# TqTorrent Main Program\n", encoding='utf-8')
            print(f"✓ Created empty: TqTorrent.py")
        except:
            print("✗ Failed to create any main program file")
    
    # Step 5: Create shortcut
    print("\n[5/6] Creating desktop shortcut...")
    if not create_desktop_shortcut(base_dir, main_file):
        print("⚠ Could not create desktop shortcut")
    
    # Step 6: Complete
    print("\n[6/6] Setup complete!")
    print("\n" + "="*60)
    print("         SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    print()
    print("TqTorrent has been installed to:")
    print(f"  📁 {base_dir}")
    print()
    print("To launch TqTorrent:")
    print(f"  1. Double-click 'TqTorrent.bat' on your Desktop")
    if main_file:
        print(f"  2. Or run: \"{sys.executable}\" \"{main_file}\"")
    print()
    print("Created files:")
    print("  • Documents/TqTorrent/TqTorrent.py - Main program")
    print("  • Documents/TqTorrent/launcher.py - Launcher script")
    print("  • Desktop/TqTorrent.bat - Desktop shortcut")
    print("  • Various config files in subfolders")
    print()
    print("="*60)
    
    # Ask to launch
    print()
    choice = input("Launch TqTorrent now? (Y/N): ").strip().upper()
    if choice == 'Y' and main_file:
        print("\nLaunching TqTorrent...")
        print(f"Python: {sys.executable}")
        print(f"Script: {main_file}")
        try:
            # Check if file exists
            if main_file.exists():
                subprocess.run([sys.executable, str(main_file)])
            else:
                print(f"✗ File not found: {main_file}")
                print(f"Please check if the file exists.")
        except Exception as e:
            print(f"✗ Could not launch: {str(e)}")
            print(f"Please run manually: \"{sys.executable}\" \"{main_file}\"")
    elif not main_file:
        print("\n⚠ Main program file was not created.")
        print(f"Please check the folder: {base_dir}")
    
    input("\nPress Enter to exit setup...")

def main():
    """Main entry point"""
    print("TqTorrent Setup - Starting...")
    print(f"Python executable: {sys.executable}")
    print(f"Current directory: {os.getcwd()}")
    
    # Set UTF-8 encoding for Windows
    if sys.platform == "win32":
        os.system("chcp 65001 >nul")
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--console":
        console_setup()
    else:
        console_setup()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"\n\n❌ UNEXPECTED ERROR:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nTraceback:")
        traceback.print_exc()
        print("\nSystem information:")
        print(f"Python: {sys.version}")
        print(f"Platform: {sys.platform}")
        print(f"Executable: {sys.executable}")
        input("\nPress Enter to exit...")
