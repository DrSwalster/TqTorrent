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

# Try to import required libraries
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext, font
    from tkinter import PhotoImage
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class ETS2StyleLauncher:
    def __init__(self):
        self.root = None
        self.style = None
        self.current_step = 0
        self.total_steps = 4
        self.base_dir = Path.home() / "Documents" / "TqTorrent"
        self.version = "1.2.0"
        self.setup_complete = False
        
        # Colors similar to ETS2
        self.colors = {
            'bg_dark': '#1a1a2e',
            'bg_medium': '#16213e',
            'bg_light': '#0f3460',
            'accent': '#e94560',
            'text': '#ffffff',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'error': '#F44336'
        }
    
    def setup_codepage(self):
        """Setup Windows codepage"""
        if sys.platform == "win32":
            os.system("chcp 65001 >nul")
    
    def install_python(self):
        """Install Python if not found"""
        try:
            subprocess.run([sys.executable, "--version"], 
                          capture_output=True, text=True, check=True)
            return True, "Python is already installed"
        except:
            # Python not found, need to install
            return False, "Python not found"
    
    def install_library(self, library_name):
        """Install a Python library"""
        try:
            print(f"Installing {library_name}...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", library_name],
                capture_output=True,
                text=True,
                timeout=60
            )
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, f"Timeout installing {library_name}"
        except Exception as e:
            return False, str(e)
    
    def check_requirements(self):
        """Check and install requirements"""
        requirements = {
            'requests': REQUESTS_AVAILABLE,
            'beautifulsoup4': BS4_AVAILABLE,
            'psutil': PSUTIL_AVAILABLE,
            'pillow': False  # Will check later
        }
        
        missing = [lib for lib, avail in requirements.items() if not avail]
        
        # Try to install missing
        for lib in missing:
            success, message = self.install_library(lib)
            if success:
                print(f"✓ Installed {lib}")
            else:
                print(f"✗ Failed to install {lib}: {message}")
        
        return len(missing) == 0
    
    def create_structure(self):
        """Create TqTorrent folder structure"""
        try:
            # Main directory
            self.base_dir.mkdir(exist_ok=True)
            
            # Subdirectories
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
                (self.base_dir / dir_path).mkdir(parents=True, exist_ok=True)
            
            # Create files
            self.create_config_files()
            
            return True, "Structure created successfully"
        except Exception as e:
            return False, f"Error creating structure: {str(e)}"
    
    def create_config_files(self):
        """Create all configuration files"""
        # cnf.txt
        cnf_content = f"""# TqTorrent Configuration
# Created: {datetime.datetime.now()}
# Version: {self.version}

[General]
app_name=TqTorrent
version={self.version}
author=DrSwalster
first_run=true

[Paths]
base={self.base_dir}
saves={self.base_dir}/Localsaves_by_TqTorrent/saves
logs={self.base_dir}/log
mods={self.base_dir}/mods
profiles={self.base_dir}/profiles

[Settings]
auto_update=true
backup_enabled=true
theme=dark
"""
        
        (self.base_dir / "Localsaves_by_TqTorrent" / "saves" / "cnf.txt").write_text(cnf_content, encoding='utf-8')
        
        # Empty config file
        (self.base_dir / "Localsaves_by_TqTorrent" / "saves" / "config").touch()
        
        # Log file
        log_content = f"""TqTorrent Log
{"="*40}
Date: {datetime.datetime.now()}
Version: {self.version}
{"="*40}

[INFO] Initial setup completed
"""
        (self.base_dir / "log" / "log.txt").write_text(log_content, encoding='utf-8')
        
        # Version file
        version_content = f"""TqTorrent v{self.version}
Install Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Build: Release
"""
        (self.base_dir / "Version" / "version.txt").write_text(version_content, encoding='utf-8')
        
        # TqManager config
        manager_content = """[TqManager]
enabled=true
auto_check=true
check_interval=3600

[Features]
mod_management=true
profile_management=true
auto_backup=true
"""
        (self.base_dir / "TqManager" / "config.ini").write_text(manager_content, encoding='utf-8')
    
    def create_desktop_shortcut(self):
        """Create desktop shortcut"""
        desktop = Path.home() / "Desktop"
        bat_content = f"""@echo off
chcp 65001 >nul
title TqTorrent Launcher
color 0A
echo ========================================
echo        TQTORRENT LAUNCHER
echo ========================================
echo.
cd /d "{self.base_dir}"
python "{self.base_dir}\\launcher.py"
pause
"""
        
        (desktop / "TqTorrent.bat").write_text(bat_content, encoding='utf-8')
        
        # Create main launcher
        launcher_content = '''#!/usr/bin/env python3
"""
TqTorrent Main Launcher
"""

import tkinter as tk
from tkinter import ttk
import os
from pathlib import Path

class TqTorrentLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("TqTorrent Launcher")
        self.root.geometry("800x600")
        
        # Create interface
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        header = tk.Frame(self.root, bg="#1a1a2e", height=100)
        header.pack(fill=tk.X)
        
        title = tk.Label(header, text="TQTORRENT", font=("Arial", 24, "bold"),
                        bg="#1a1a2e", fg="white")
        title.pack(pady=20)
        
        # Main content
        main_frame = tk.Frame(self.root, bg="#16213e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Buttons
        buttons = [
            ("Launch TqTorrent", self.launch_main),
            ("Mod Manager", self.open_mod_manager),
            ("Profile Manager", self.open_profile_manager),
            ("Settings", self.open_settings),
            ("Exit", self.root.quit)
        ]
        
        for text, command in buttons:
            btn = tk.Button(main_frame, text=text, font=("Arial", 12),
                           bg="#0f3460", fg="white", padx=20, pady=10,
                           command=command)
            btn.pack(pady=5, fill=tk.X)
    
    def launch_main(self):
        print("Launching TqTorrent...")
    
    def open_mod_manager(self):
        print("Opening Mod Manager...")
    
    def open_profile_manager(self):
        print("Opening Profile Manager...")
    
    def open_settings(self):
        print("Opening Settings...")

if __name__ == "__main__":
    root = tk.Tk()
    app = TqTorrentLauncher(root)
    root.mainloop()
'''
        
        (self.base_dir / "launcher.py").write_text(launcher_content, encoding='utf-8')
    
    def run_assistant(self):
        """Run the setup assistant with GUI"""
        if not TKINTER_AVAILABLE:
            self.run_console_setup()
            return
        
        self.setup_codepage()
        self.root = tk.Tk()
        self.root.title(f"TqTorrent Setup Assistant v{self.version}")
        self.root.geometry("900x700")
        self.root.configure(bg=self.colors['bg_dark'])
        
        # Center window
        self.center_window()
        
        # Set style
        self.setup_style()
        
        # Create interface
        self.create_welcome_screen()
        
        self.root.mainloop()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_style(self):
        """Setup ttk style"""
        self.style = ttk.Style()
        
        # Configure styles
        self.style.theme_use('clam')
        
        # Configure colors
        self.style.configure('TFrame', background=self.colors['bg_dark'])
        self.style.configure('TLabel', background=self.colors['bg_dark'], 
                           foreground=self.colors['text'], font=('Arial', 10))
        self.style.configure('Title.TLabel', font=('Arial', 24, 'bold'))
        self.style.configure('Subtitle.TLabel', font=('Arial', 14))
        
        # Button style
        self.style.configure('Accent.TButton', 
                           background=self.colors['accent'],
                           foreground=self.colors['text'],
                           font=('Arial', 11, 'bold'),
                           padding=10)
        self.style.map('Accent.TButton',
                      background=[('active', '#d43d55')])
    
    def create_welcome_screen(self):
        """Create welcome screen"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="40")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(main_frame, text="TQTORRENT", style='Title.TLabel')
        title.pack(pady=(0, 10))
        
        subtitle = ttk.Label(main_frame, text=f"Setup Assistant v{self.version}", 
                           style='Subtitle.TLabel')
        subtitle.pack(pady=(0, 30))
        
        # Welcome text
        welcome_text = """Welcome to TqTorrent Setup Assistant!

This assistant will guide you through the installation process.

We will:
1. Check Python installation
2. Install required libraries
3. Create folder structure
4. Configure TqTorrent

Click 'Start Setup' to begin."""
        
        text_widget = tk.Text(main_frame, height=8, width=60, wrap=tk.WORD,
                            bg=self.colors['bg_medium'], fg=self.colors['text'],
                            font=('Arial', 10), relief=tk.FLAT, bd=0)
        text_widget.insert('1.0', welcome_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(pady=20, padx=20)
        
        # Progress info
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(pady=20)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, 
                                          variable=self.progress_var,
                                          maximum=100, length=400,
                                          mode='determinate')
        self.progress_bar.pack()
        
        self.progress_label = ttk.Label(progress_frame, text="Ready to start")
        self.progress_label.pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        start_btn = ttk.Button(button_frame, text="Start Setup",
                             command=self.start_setup_process,
                             style='Accent.TButton')
        start_btn.pack(side=tk.LEFT, padx=10)
        
        exit_btn = ttk.Button(button_frame, text="Exit",
                            command=self.root.quit)
        exit_btn.pack(side=tk.LEFT, padx=10)
    
    def start_setup_process(self):
        """Start the setup process in a separate thread"""
        self.progress_label.config(text="Starting setup...")
        self.progress_var.set(10)
        
        # Run setup in thread to avoid freezing GUI
        setup_thread = threading.Thread(target=self.run_setup_steps)
        setup_thread.daemon = True
        setup_thread.start()
    
    def run_setup_steps(self):
        """Run all setup steps"""
        steps = [
            ("Checking Python...", self.check_python_step),
            ("Installing libraries...", self.install_libraries_step),
            ("Creating structure...", self.create_structure_step),
            ("Finalizing...", self.finalize_step)
        ]
        
        for i, (step_name, step_func) in enumerate(steps):
            # Update progress in GUI thread
            self.root.after(0, self.update_progress, 
                          step_name, int((i / len(steps)) * 100))
            
            # Run step
            success, message = step_func()
            
            if not success:
                self.root.after(0, self.show_error, f"Step failed: {message}")
                return
        
        # Complete
        self.root.after(0, self.setup_complete_screen)
    
    def update_progress(self, message, value):
        """Update progress bar and label"""
        self.progress_label.config(text=message)
        self.progress_var.set(value)
        self.root.update_idletasks()
    
    def check_python_step(self):
        """Step 1: Check Python"""
        success, message = self.install_python()
        return success, message
    
    def install_libraries_step(self):
        """Step 2: Install libraries"""
        success = self.check_requirements()
        return success, "Libraries installed" if success else "Failed to install libraries"
    
    def create_structure_step(self):
        """Step 3: Create structure"""
        success, message = self.create_structure()
        return success, message
    
    def finalize_step(self):
        """Step 4: Finalize"""
        self.create_desktop_shortcut()
        self.setup_complete = True
        return True, "Setup completed"
    
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Setup Error", message)
    
    def setup_complete_screen(self):
        """Show setup complete screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = ttk.Frame(self.root, padding="40")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Success icon/text
        success_label = ttk.Label(main_frame, text="✓", 
                                font=('Arial', 48, 'bold'),
                                foreground=self.colors['success'])
        success_label.pack(pady=20)
        
        title = ttk.Label(main_frame, text="Setup Complete!", 
                         font=('Arial', 24, 'bold'))
        title.pack(pady=10)
        
        # Summary
        summary = f"""TqTorrent has been successfully installed!

Location: {self.base_dir}

What was installed:
• Python and required libraries
• TqTorrent folder structure
• Configuration files
• Desktop shortcut

You can now launch TqTorrent from your desktop."""
        
        text_widget = tk.Text(main_frame, height=10, width=70, wrap=tk.WORD,
                            bg=self.colors['bg_medium'], fg=self.colors['text'],
                            font=('Arial', 10), relief=tk.FLAT)
        text_widget.insert('1.0', summary)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(pady=20, padx=20)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        launch_btn = ttk.Button(button_frame, text="Launch TqTorrent",
                              command=self.launch_tqtorrent,
                              style='Accent.TButton')
        launch_btn.pack(side=tk.LEFT, padx=10)
        
        close_btn = ttk.Button(button_frame, text="Close",
                             command=self.root.quit)
        close_btn.pack(side=tk.LEFT, padx=10)
    
    def launch_tqtorrent(self):
        """Launch TqTorrent"""
        try:
            desktop_shortcut = Path.home() / "Desktop" / "TqTorrent.bat"
            if desktop_shortcut.exists():
                os.startfile(desktop_shortcut)
        except:
            pass
        self.root.quit()
    
    def run_console_setup(self):
        """Fallback to console setup"""
        self.setup_codepage()
        
        print("\n" + "="*50)
        print("TQTORRENT SETUP ASSISTANT")
        print("="*50)
        print()
        
        # Step 1: Check Python
        print("Step 1/4: Checking Python...")
        success, message = self.install_python()
        print(f"  {message}")
        
        # Step 2: Install libraries
        print("\nStep 2/4: Installing libraries...")
        if self.check_requirements():
            print("  ✓ Libraries installed")
        else:
            print("  ⚠ Some libraries may not be installed")
        
        # Step 3: Create structure
        print("\nStep 3/4: Creating structure...")
        success, message = self.create_structure()
        print(f"  {message}")
        
        # Step 4: Finalize
        print("\nStep 4/4: Finalizing...")
        self.create_desktop_shortcut()
        print("  ✓ Desktop shortcut created")
        
        print("\n" + "="*50)
        print("SETUP COMPLETE!")
        print("="*50)
        print(f"\nTqTorrent installed to: {self.base_dir}")
        print("\nLaunch from: Desktop\\TqTorrent.bat")
        print("\nPress Enter to exit...")
        input()

def main():
    """Main entry point"""
    launcher = ETS2StyleLauncher()
    
    # Check if console mode requested
    if len(sys.argv) > 1 and sys.argv[1] == "--console":
        launcher.run_console_setup()
    else:
        launcher.run_assistant()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSetup cancelled.")
    except Exception as e:
        print(f"\nError: {e}")
        input("Press Enter to exit...")
