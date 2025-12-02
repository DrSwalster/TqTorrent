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
    log_file.write_text(log_content, encoding='utf-8')
    print(f"✓ Created: log.txt")
    
    # Version file
    version_content = f"""TqTorrent v1.0.0
Install Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    version_file = base_dir / "Version" / "version.txt"
    version_file.write_text(version_content, encoding='utf-8')
    print(f"✓ Created: version.txt")

def create_desktop_shortcut(base_dir):
    """Create desktop shortcut"""
    try:
        desktop = Path.home() / "Desktop"
        bat_content = f"""@echo off
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
python "{base_dir}\\main.py"
echo.
echo Press any key to exit...
pause >nul
"""
        
        shortcut_path = desktop / "TqTorrent.bat"
        shortcut_path.write_text(bat_content, encoding='utf-8')
        print(f"✓ Desktop shortcut: {shortcut_path}")
        
        # Create main.py
        main_py_content = '''#!/usr/bin/env python3
"""
TqTorrent Main Program
"""

print("="*50)
print("TQTORRENT - MAIN PROGRAM")
print("="*50)
print()
print("Welcome to TqTorrent!")
print()
print("Program installed successfully!")
print("You can modify this file to add your functionality.")
print()
input("Press Enter to exit...")
'''
        
        main_py_path = base_dir / "main.py"
        main_py_path.write_text(main_py_content, encoding='utf-8')
        print(f"✓ Main program: {main_py_path}")
        
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
    print("[1/5] Checking Python installation...")
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
    print("\n[2/5] Installing required libraries...")
    if not install_required_libraries():
        print("⚠ Some libraries may not be installed properly")
        print("You can install them manually later:")
        print("pip install requests beautifulsoup4 psutil pillow")
    
    # Step 3: Create structure
    print("\n[3/5] Creating folder structure...")
    success, result = create_tqtorrent_structure()
    if not success:
        print(f"✗ ERROR: {result}")
        input("\nPress Enter to exit...")
        return
    
    base_dir = result
    
    # Step 4: Create shortcut
    print("\n[4/5] Creating desktop shortcut...")
    if not create_desktop_shortcut(base_dir):
        print("⚠ Could not create desktop shortcut")
    
    # Step 5: Complete
    print("\n[5/5] Setup complete!")
    print("\n" + "="*60)
    print("         SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    print()
    print("TqTorrent has been installed to:")
    print(f"  📁 {base_dir}")
    print()
    print("To launch TqTorrent:")
    print("  1. Double-click 'TqTorrent.bat' on your Desktop")
    print("  2. Or run: python \"{}\\main.py\"".format(base_dir))
    print()
    print("Folder structure created:")
    print("  📁 TqTorrent/")
    print("    📁 Localsaves_by_TqTorrent/saves/")
    print("      📄 config")
    print("      📄 cnf.txt")
    print("    📁 log/")
    print("      📄 log.txt")
    print("    📁 TqManager/")
    print("    📁 Version/")
    print("      📄 version.txt")
    print("    📁 mods/")
    print("    📁 profiles/")
    print("    📁 downloads/")
    print("    📄 main.py")
    print()
    print("="*60)
    
    # Ask to launch
    print()
    choice = input("Launch TqTorrent now? (Y/N): ").strip().upper()
    if choice == 'Y':
        print("\nLaunching TqTorrent...")
        try:
            subprocess.run([sys.executable, str(base_dir / "main.py")])
        except:
            print("Could not launch automatically.")
            print(f"Please run: python \"{base_dir}\\main.py\"")
    
    input("\nPress Enter to exit setup...")

def gui_setup():
    """Run setup with GUI (if tkinter available)"""
    try:
        import tkinter as tk
        from tkinter import ttk, messagebox
    except ImportError:
        print("Tkinter not available, running console setup...")
        console_setup()
        return
    
    # GUI setup code would go here
    # For now, fall back to console
    console_setup()

def main():
    """Main entry point"""
    print("TqTorrent Setup - Starting...")
    
    # Set UTF-8 encoding for Windows
    if sys.platform == "win32":
        os.system("chcp 65001 >nul")
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--console":
        console_setup()
    else:
        # Try GUI, fall back to console
        gui_setup()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"\n\nUnexpected error: {str(e)}")
        print("\nPlease report this error:")
        print(f"Python: {sys.version}")
        print(f"Platform: {sys.platform}")
        input("\nPress Enter to exit...")
