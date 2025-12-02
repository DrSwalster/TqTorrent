#!/usr/bin/env python3
"""
TqTorrent - Main Setup Program
Interface similar to ETS2 Launcher
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
import datetime

# Try to import tkinter for GUI
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    print("Note: GUI mode not available (tkinter not installed)")

class TqTorrentLauncher:
    def __init__(self):
        self.base_dir = Path.home() / "Documents" / "TqTorrent"
        self.version = "1.0.0"
        
    def setup_codepage(self):
        """Setup Windows codepage for Russian text"""
        if sys.platform == "win32":
            os.system("chcp 65001 >nul")
    
    def check_python_libraries(self):
        """Check and install required libraries"""
        required = ["requests", "beautifulsoup4", "psutil"]
        missing = []
        
        for lib in required:
            try:
                __import__(lib)
            except ImportError:
                missing.append(lib)
        
        return missing
    
    def install_library(self, library):
        """Install a Python library"""
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])
            return True
        except subprocess.CalledProcessError:
            return False
    
    def create_folder_structure(self):
        """Create TqTorrent folder structure"""
        print("\n" + "="*50)
        print("Creating TqTorrent folder structure...")
        print("="*50)
        
        try:
            # Main folders
            folders = [
                self.base_dir,
                self.base_dir / "Localsaves_by_TqTorrent" / "saves",
                self.base_dir / "log",
                self.base_dir / "TqManager",
                self.base_dir / "Version",
                self.base_dir / "mods",
                self.base_dir / "profiles",
                self.base_dir / "downloads"
            ]
            
            for folder in folders:
                folder.mkdir(parents=True, exist_ok=True)
                print(f"✓ Created: {folder}")
            
            # Create files
            self.create_config_files()
            
            print("\n" + "="*50)
            print("Folder structure created successfully!")
            print(f"Location: {self.base_dir}")
            print("="*50)
            
            return True
            
        except Exception as e:
            print(f"\n✗ Error creating structure: {e}")
            return False
    
    def create_config_files(self):
        """Create configuration files"""
        # cnf.txt
        cnf_content = f"""# TqTorrent Configuration File
# Created: {datetime.datetime.now()}
# Version: {self.version}

[General]
app_name=TqTorrent
version={self.version}
author=DrSwalster
github=https://github.com/DrSwalster/TqTorrent

[Paths]
base_dir={self.base_dir}
saves_dir={self.base_dir}/Localsaves_by_TqTorrent/saves
logs_dir={self.base_dir}/log
mods_dir={self.base_dir}/mods
profiles_dir={self.base_dir}/profiles

[Settings]
first_run=true
auto_update=true
check_interval=3600
"""
        
        with open(self.base_dir / "Localsaves_by_TqTorrent" / "saves" / "cnf.txt", "w", encoding="utf-8") as f:
            f.write(cnf_content)
        
        # Empty config file
        with open(self.base_dir / "Localsaves_by_TqTorrent" / "saves" / "config", "w", encoding="utf-8") as f:
            f.write("")
        
        # Log file
        log_content = f"""TQTORRENT LOG FILE
{"="*50}
Created: {datetime.datetime.now()}
Version: {self.version}
Python: {sys.version}
Platform: {sys.platform}
{"="*50}

[INFO] Initial setup completed
"""
        
        with open(self.base_dir / "log" / "log.txt", "w", encoding="utf-8") as f:
            f.write(log_content)
        
        # Version file
        version_content = f"""TqTorrent v{self.version}
Build Date: {datetime.datetime.now().strftime("%Y-%m-%d")}
Install Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Author: DrSwalster
GitHub: https://github.com/DrSwalster/TqTorrent

[Changelog]
v1.0.0 - Initial release
- Folder structure creation
- Basic configuration
- Logging system
"""
        
        with open(self.base_dir / "Version" / "version.txt", "w", encoding="utf-8") as f:
            f.write(version_content)
        
        # TqManager config
        manager_content = """[TqManager]
enabled=true
auto_check_updates=true
update_interval=86400
backup_enabled=true
max_backups=10

[Modules]
mod_manager=true
profile_manager=true
download_manager=true
settings_manager=true
"""
        
        with open(self.base_dir / "TqManager" / "manager_config.ini", "w", encoding="utf-8") as f:
            f.write(manager_content)
        
        print("✓ Configuration files created")
    
    def show_welcome_message(self):
        """Show welcome message"""
        welcome = f"""
╔══════════════════════════════════════════════╗
║           WELCOME TO TQTORRENT               ║
║                    v{self.version:<10}               ║
╚══════════════════════════════════════════════╝

This setup will:
1. Check Python installation
2. Install required libraries
3. Create folder structure
4. Configure TqTorrent

Press Enter to continue or Ctrl+C to cancel...
"""
        print(welcome)
        input()
    
    def run_console_setup(self):
        """Run setup in console mode"""
        self.setup_codepage()
        
        self.show_welcome_message()
        
        # Check libraries
        print("\n" + "="*50)
        print("Checking Python libraries...")
        print("="*50)
        
        missing = self.check_python_libraries()
        if missing:
            print(f"\nMissing libraries: {', '.join(missing)}")
            print("Installing missing libraries...")
            
            for lib in missing:
                print(f"\nInstalling {lib}...")
                if self.install_library(lib):
                    print(f"✓ {lib} installed successfully")
                else:
                    print(f"✗ Failed to install {lib}")
                    
            print("\n✓ Library installation completed")
        else:
            print("✓ All required libraries are installed")
        
        # Create folder structure
        if not self.create_folder_structure():
            print("\n✗ Failed to create folder structure")
            input("\nPress Enter to exit...")
            return
        
        # Final message
        print("\n" + "="*50)
        print("SETUP COMPLETED SUCCESSFULLY!")
        print("="*50)
        print(f"\nTqTorrent has been installed to:")
        print(f"  {self.base_dir}")
        
        print("\nFolder structure:")
        print(f"  📁 {self.base_dir.name}/")
        print(f"    📁 Localsaves_by_TqTorrent/")
        print(f"      📁 saves/")
        print(f"        📄 config")
        print(f"        📄 cnf.txt")
        print(f"    📁 log/")
        print(f"      📄 log.txt")
        print(f"    📁 TqManager/")
        print(f"      📄 manager_config.ini")
        print(f"    📁 Version/")
        print(f"      📄 version.txt")
        print(f"    📁 mods/")
        print(f"    📁 profiles/")
        print(f"    📁 downloads/")
        
        print("\n" + "="*50)
        print("You can now use TqTorrent!")
        print("="*50)
        
        # Create desktop shortcut
        self.create_desktop_shortcut()
        
        input("\nPress Enter to exit...")
    
    def create_desktop_shortcut(self):
        """Create desktop shortcut"""
        desktop = Path.home() / "Desktop"
        shortcut = desktop / "TqTorrent.bat"
        
        shortcut_content = f"""@echo off
chcp 65001 >nul
echo ============================================
echo          TQTORRENT LAUNCHER
echo ============================================
echo.
cd /d "{self.base_dir}"
python "{self.base_dir}\\TqTorrent.py"
pause
"""
        
        with open(shortcut, "w", encoding="utf-8") as f:
            f.write(shortcut_content)
        
        # Create main TqTorrent.py file
        main_program = self.base_dir / "TqTorrent.py"
        main_content = """#!/usr/bin/env python3
"""
TqTorrent - Main Program
"""

import os
import sys
from pathlib import Path

def main():
    print("="*50)
    print("TQTORRENT - MAIN PROGRAM")
    print("="*50)
    print()
    print("Welcome to TqTorrent!")
    print()
    print("This is the main program.")
    print("You can modify this file to add your functionality.")
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
"""
        
        with open(main_program, "w", encoding="utf-8") as f:
            f.write(main_content)
        
        print(f"\n✓ Desktop shortcut created: {shortcut}")
        print(f"✓ Main program created: {main_program}")
    
    def run_gui_setup(self):
        """Run setup with GUI (if tkinter available)"""
        if not TKINTER_AVAILABLE:
            print("GUI not available, running console setup...")
            self.run_console_setup()
            return
        
        # GUI setup would go here
        # For now, fall back to console
        self.run_console_setup()

def main():
    """Main entry point"""
    launcher = TqTorrentLauncher()
    
    # Check if GUI requested
    if len(sys.argv) > 1 and sys.argv[1] == "--gui" and TKINTER_AVAILABLE:
        launcher.run_gui_setup()
    else:
        launcher.run_console_setup()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"\n\nError during setup: {e}")
        input("Press Enter to exit...")
