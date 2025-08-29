#!/usr/bin/env python3
"""
Website Blocker - Advanced Website Blocking Tool
Created by Umar J
Version: 2.0

A powerful and user-friendly website blocking application with GUI interface,
scheduling features, and advanced management capabilities.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import sys
import platform
import threading
import time
from datetime import datetime, timedelta
import webbrowser
from pathlib import Path
import re
import subprocess

class WebsiteBlocker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Website Blocker - By Umar J")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Modern color scheme
        self.colors = {
            'primary': '#2563eb',
            'primary_dark': '#1d4ed8',
            'secondary': '#64748b',
            'success': '#10b981',
            'danger': '#ef4444',
            'warning': '#f59e0b',
            'bg_primary': '#f8fafc',
            'bg_secondary': '#e2e8f0',
            'text_primary': '#0f172a',
            'text_secondary': '#475569',
            'border': '#cbd5e1'
        }
        
        # Configuration
        self.config_file = "blocker_config.json"
        self.blocked_sites = []
        self.scheduled_blocks = []
        self.is_blocking = False
        
        # Get hosts file path based on OS
        self.hosts_path = self.get_hosts_path()
        self.backup_path = "hosts_backup.txt"
        
        # Load configuration
        self.load_config()
        
        # Set up GUI
        self.setup_gui()
        self.update_status()
        
        # Start scheduler thread
        self.scheduler_thread = threading.Thread(target=self.scheduler_loop, daemon=True)
        self.scheduler_thread.start()

    def get_hosts_path(self):
        """Get the hosts file path based on the operating system"""
        system = platform.system().lower()
        if system == "windows":
            return r"C:\Windows\System32\drivers\etc\hosts"
        else:  # Linux, macOS, Unix-like
            return "/etc/hosts"

    def check_admin_privileges(self):
        """Check if the program is running with admin/root privileges"""
        system = platform.system().lower()
        try:
            if system == "windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            else:
                return os.geteuid() == 0
        except:
            return False

    def request_admin_privileges(self):
        """Request admin privileges if not already running as admin"""
        if self.check_admin_privileges():
            return True
        
        system = platform.system().lower()
        try:
            if system == "windows":
                import ctypes
                ctypes.windll.shell32.ShellExecuteW(
                    None, "runas", sys.executable, " ".join(sys.argv), None, 1
                )
            else:
                # For Unix-like systems, suggest running with sudo
                messagebox.showwarning(
                    "Administrator Required",
                    "This program needs administrator privileges to modify the hosts file.\n"
                    "Please run the program with 'sudo' (Linux/macOS):\n\n"
                    "sudo python3 website_blocker.py"
                )
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Could not request admin privileges: {e}")
            return False

    def setup_gui(self):
        """Set up the graphical user interface"""
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure root
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Tabs
        self.create_block_tab()
        self.create_schedule_tab()
        self.create_settings_tab()
        self.create_about_tab()

    def create_header(self, parent):
        """Create the header section"""
        header_frame = tk.Frame(parent, bg=self.colors['primary'], height=100)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Title and branding
        title_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        title_frame.pack(expand=True, fill=tk.BOTH)
        
        title_label = tk.Label(
            title_frame,
            text="🛡️ Website Blocker",
            font=("Helvetica", 24, "bold"),
            fg="white",
            bg=self.colors['primary']
        )
        title_label.pack(pady=(10, 5))
        
        subtitle_label = tk.Label(
            title_frame,
            text="Advanced Website Blocking Tool - Created by Umar J",
            font=("Helvetica", 10),
            fg="#bfdbfe",
            bg=self.colors['primary']
        )
        subtitle_label.pack()
        
        # Status indicator
        self.status_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        self.status_frame.pack(side=tk.RIGHT, padx=20, pady=20)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="●",
            font=("Helvetica", 20),
            fg=self.colors['danger'],
            bg=self.colors['primary']
        )
        self.status_label.pack()
        
        self.status_text = tk.Label(
            self.status_frame,
            text="Inactive",
            font=("Helvetica", 8),
            fg="white",
            bg=self.colors['primary']
        )
        self.status_text.pack()

    def create_block_tab(self):
        """Create the website blocking tab"""
        block_frame = ttk.Frame(self.notebook)
        self.notebook.add(block_frame, text="Website Blocking")
        
        # Input section
        input_frame = tk.Frame(block_frame, bg="white", relief=tk.RAISED, bd=1)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            input_frame,
            text="Add Website to Block:",
            font=("Helvetica", 12, "bold"),
            bg="white"
        ).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        entry_frame = tk.Frame(input_frame, bg="white")
        entry_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.website_entry = tk.Entry(
            entry_frame,
            font=("Helvetica", 11),
            relief=tk.FLAT,
            bd=5
        )
        self.website_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.website_entry.bind('<Return>', lambda e: self.add_website())
        
        add_btn = tk.Button(
            entry_frame,
            text="Add Website",
            font=("Helvetica", 10, "bold"),
            bg=self.colors['primary'],
            fg="white",
            relief=tk.FLAT,
            padx=20,
            command=self.add_website
        )
        add_btn.pack(side=tk.RIGHT)
        
        # Control buttons
        control_frame = tk.Frame(block_frame, bg="white", relief=tk.RAISED, bd=1)
        control_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        btn_frame = tk.Frame(control_frame, bg="white")
        btn_frame.pack(pady=15)
        
        self.block_btn = tk.Button(
            btn_frame,
            text="🚫 Start Blocking",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['danger'],
            fg="white",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            command=self.toggle_blocking
        )
        self.block_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = tk.Button(
            btn_frame,
            text="🗑️ Clear All",
            font=("Helvetica", 12),
            bg=self.colors['warning'],
            fg="white",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            command=self.clear_all_websites
        )
        clear_btn.pack(side=tk.LEFT)
        
        # Blocked websites list
        list_frame = tk.Frame(block_frame, bg="white", relief=tk.RAISED, bd=1)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(
            list_frame,
            text="Blocked Websites:",
            font=("Helvetica", 12, "bold"),
            bg="white"
        ).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Listbox with scrollbar
        listbox_frame = tk.Frame(list_frame, bg="white")
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.website_listbox = tk.Listbox(
            listbox_frame,
            font=("Helvetica", 10),
            yscrollcommand=scrollbar.set,
            relief=tk.FLAT,
            bd=5,
            selectmode=tk.SINGLE
        )
        self.website_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.website_listbox.yview)
        
        # Remove button
        remove_btn = tk.Button(
            list_frame,
            text="Remove Selected",
            font=("Helvetica", 10),
            bg=self.colors['secondary'],
            fg="white",
            relief=tk.FLAT,
            padx=20,
            command=self.remove_selected_website
        )
        remove_btn.pack(pady=(0, 10))

    def create_schedule_tab(self):
        """Create the scheduling tab"""
        schedule_frame = ttk.Frame(self.notebook)
        self.notebook.add(schedule_frame, text="Scheduling")
        
        # Schedule input section
        input_frame = tk.Frame(schedule_frame, bg="white", relief=tk.RAISED, bd=1)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            input_frame,
            text="Schedule Blocking Sessions:",
            font=("Helvetica", 12, "bold"),
            bg="white"
        ).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Time inputs
        time_frame = tk.Frame(input_frame, bg="white")
        time_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Label(time_frame, text="Start Time:", bg="white").pack(side=tk.LEFT)
        self.start_time_var = tk.StringVar(value="09:00")
        start_time_entry = tk.Entry(time_frame, textvariable=self.start_time_var, width=8)
        start_time_entry.pack(side=tk.LEFT, padx=(5, 20))
        
        tk.Label(time_frame, text="End Time:", bg="white").pack(side=tk.LEFT)
        self.end_time_var = tk.StringVar(value="17:00")
        end_time_entry = tk.Entry(time_frame, textvariable=self.end_time_var, width=8)
        end_time_entry.pack(side=tk.LEFT, padx=(5, 20))
        
        # Days selection
        days_frame = tk.Frame(input_frame, bg="white")
        days_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Label(days_frame, text="Days:", bg="white").pack(anchor=tk.W)
        
        self.days_vars = {}
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        days_checkboxes = tk.Frame(days_frame, bg="white")
        days_checkboxes.pack(fill=tk.X, pady=5)
        
        for day in days:
            var = tk.BooleanVar()
            self.days_vars[day] = var
            cb = tk.Checkbutton(
                days_checkboxes,
                text=day[:3],
                variable=var,
                bg="white"
            )
            cb.pack(side=tk.LEFT, padx=5)
        
        # Add schedule button
        add_schedule_btn = tk.Button(
            input_frame,
            text="Add Schedule",
            font=("Helvetica", 10, "bold"),
            bg=self.colors['success'],
            fg="white",
            relief=tk.FLAT,
            padx=20,
            command=self.add_schedule
        )
        add_schedule_btn.pack(pady=(0, 10))
        
        # Scheduled sessions list
        schedule_list_frame = tk.Frame(schedule_frame, bg="white", relief=tk.RAISED, bd=1)
        schedule_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(
            schedule_list_frame,
            text="Scheduled Sessions:",
            font=("Helvetica", 12, "bold"),
            bg="white"
        ).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Schedule listbox
        schedule_listbox_frame = tk.Frame(schedule_list_frame, bg="white")
        schedule_listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        schedule_scrollbar = tk.Scrollbar(schedule_listbox_frame)
        schedule_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.schedule_listbox = tk.Listbox(
            schedule_listbox_frame,
            font=("Helvetica", 10),
            yscrollcommand=schedule_scrollbar.set,
            relief=tk.FLAT,
            bd=5
        )
        self.schedule_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        schedule_scrollbar.config(command=self.schedule_listbox.yview)
        
        # Remove schedule button
        remove_schedule_btn = tk.Button(
            schedule_list_frame,
            text="Remove Selected Schedule",
            font=("Helvetica", 10),
            bg=self.colors['secondary'],
            fg="white",
            relief=tk.FLAT,
            command=self.remove_selected_schedule
        )
        remove_schedule_btn.pack(pady=(0, 10))

    def create_settings_tab(self):
        """Create the settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Backup section
        backup_frame = tk.Frame(settings_frame, bg="white", relief=tk.RAISED, bd=1)
        backup_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            backup_frame,
            text="Backup & Restore:",
            font=("Helvetica", 12, "bold"),
            bg="white"
        ).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        backup_btn_frame = tk.Frame(backup_frame, bg="white")
        backup_btn_frame.pack(pady=10)
        
        backup_btn = tk.Button(
            backup_btn_frame,
            text="💾 Backup Hosts File",
            font=("Helvetica", 10),
            bg=self.colors['primary'],
            fg="white",
            relief=tk.FLAT,
            padx=20,
            command=self.backup_hosts
        )
        backup_btn.pack(side=tk.LEFT, padx=(10, 5))
        
        restore_btn = tk.Button(
            backup_btn_frame,
            text="📂 Restore Hosts File",
            font=("Helvetica", 10),
            bg=self.colors['warning'],
            fg="white",
            relief=tk.FLAT,
            padx=20,
            command=self.restore_hosts
        )
        restore_btn.pack(side=tk.LEFT, padx=5)
        
        # Import/Export section
        ie_frame = tk.Frame(settings_frame, bg="white", relief=tk.RAISED, bd=1)
        ie_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            ie_frame,
            text="Import/Export Configuration:",
            font=("Helvetica", 12, "bold"),
            bg="white"
        ).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        ie_btn_frame = tk.Frame(ie_frame, bg="white")
        ie_btn_frame.pack(pady=10)
        
        export_btn = tk.Button(
            ie_btn_frame,
            text="📤 Export Config",
            font=("Helvetica", 10),
            bg=self.colors['success'],
            fg="white",
            relief=tk.FLAT,
            padx=20,
            command=self.export_config
        )
        export_btn.pack(side=tk.LEFT, padx=(10, 5))
        
        import_btn = tk.Button(
            ie_btn_frame,
            text="📥 Import Config",
            font=("Helvetica", 10),
            bg=self.colors['secondary'],
            fg="white",
            relief=tk.FLAT,
            padx=20,
            command=self.import_config
        )
        import_btn.pack(side=tk.LEFT, padx=5)

    def create_about_tab(self):
        """Create the about tab"""
        about_frame = ttk.Frame(self.notebook)
        self.notebook.add(about_frame, text="About")
        
        about_content = tk.Frame(about_frame, bg="white", relief=tk.RAISED, bd=1)
        about_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        tk.Label(
            about_content,
            text="🛡️ Website Blocker v2.0",
            font=("Helvetica", 20, "bold"),
            bg="white",
            fg=self.colors['primary']
        ).pack(pady=(30, 10))
        
        # Description
        description = """A powerful and user-friendly website blocking application designed to help you
maintain focus and productivity by blocking distracting websites.

Features:
• Real-time website blocking and unblocking
• Scheduled blocking sessions
• Backup and restore functionality
• Import/Export configurations
• Cross-platform support (Windows, macOS, Linux)
• Modern and intuitive GUI interface
• Admin privileges handling"""
        
        tk.Label(
            about_content,
            text=description,
            font=("Helvetica", 11),
            bg="white",
            justify=tk.LEFT,
            wraplength=600
        ).pack(pady=20, padx=30)
        
        # Author info
        tk.Label(
            about_content,
            text="Created by Umar J",
            font=("Helvetica", 14, "bold"),
            bg="white",
            fg=self.colors['primary']
        ).pack(pady=(20, 5))
        
        tk.Label(
            about_content,
            text="Professional Python Developer & Software Engineer",
            font=("Helvetica", 10),
            bg="white",
            fg=self.colors['secondary']
        ).pack()
        
        # GitHub button (placeholder)
        github_btn = tk.Button(
            about_content,
            text="🔗 View on GitHub",
            font=("Helvetica", 10),
            bg=self.colors['primary'],
            fg="white",
            relief=tk.FLAT,
            padx=30,
            command=lambda: webbrowser.open("https://github.com/yourusername")
        )
        github_btn.pack(pady=20)

    def validate_website(self, website):
        """Validate website URL format"""
        # Remove protocol if present
        website = re.sub(r'^https?://', '', website)
        website = re.sub(r'^www\.', '', website)
        
        # Basic domain validation
        pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        return re.match(pattern, website) is not None, website

    def add_website(self):
        """Add a website to the blocked list"""
        website = self.website_entry.get().strip()
        if not website:
            messagebox.showwarning("Input Error", "Please enter a website URL.")
            return
        
        is_valid, cleaned_website = self.validate_website(website)
        if not is_valid:
            messagebox.showerror("Invalid URL", "Please enter a valid website URL (e.g., facebook.com)")
            return
        
        if cleaned_website not in self.blocked_sites:
            self.blocked_sites.append(cleaned_website)
            self.website_listbox.insert(tk.END, cleaned_website)
            self.website_entry.delete(0, tk.END)
            self.save_config()
            messagebox.showinfo("Success", f"Added {cleaned_website} to blocked list.")
        else:
            messagebox.showwarning("Duplicate", "This website is already in the blocked list.")

    def remove_selected_website(self):
        """Remove selected website from the blocked list"""
        selection = self.website_listbox.curselection()
        if selection:
            website = self.website_listbox.get(selection[0])
            self.blocked_sites.remove(website)
            self.website_listbox.delete(selection[0])
            self.save_config()
            messagebox.showinfo("Success", f"Removed {website} from blocked list.")
        else:
            messagebox.showwarning("No Selection", "Please select a website to remove.")

    def clear_all_websites(self):
        """Clear all websites from the blocked list"""
        if self.blocked_sites:
            if messagebox.askyesno("Confirm", "Are you sure you want to clear all blocked websites?"):
                self.blocked_sites.clear()
                self.website_listbox.delete(0, tk.END)
                self.save_config()
                messagebox.showinfo("Success", "All websites cleared from blocked list.")
        else:
            messagebox.showinfo("Info", "The blocked list is already empty.")

    def toggle_blocking(self):
        """Toggle website blocking on/off"""
        if not self.blocked_sites:
            messagebox.showwarning("No Websites", "Please add websites to block first.")
            return
        
        if not self.check_admin_privileges():
            if not self.request_admin_privileges():
                return
        
        if self.is_blocking:
            self.stop_blocking()
        else:
            self.start_blocking()

    def start_blocking(self):
        """Start blocking websites"""
        try:
            with open(self.hosts_path, 'r') as file:
                hosts_content = file.read()
            
            # Add blocked sites to hosts file
            blocked_entries = []
            for site in self.blocked_sites:
                entries = [
                    f"127.0.0.1 {site}",
                    f"127.0.0.1 www.{site}"
                ]
                blocked_entries.extend(entries)
            
            # Check if sites are already blocked
            new_entries = []
            for entry in blocked_entries:
                if entry not in hosts_content:
                    new_entries.append(entry)
            
            if new_entries:
                with open(self.hosts_path, 'a') as file:
                    file.write('\n# Website Blocker - Umar J\n')
                    for entry in new_entries:
                        file.write(f"{entry}\n")
            
            self.is_blocking = True
            self.update_status()
            self.flush_dns()
            messagebox.showinfo("Success", f"Blocking {len(self.blocked_sites)} websites.")
            
        except PermissionError:
            messagebox.showerror("Permission Error", 
                               "Permission denied. Please run as administrator/root.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start blocking: {e}")

    def stop_blocking(self):
        """Stop blocking websites"""
        try:
            with open(self.hosts_path, 'r') as file:
                lines = file.readlines()
            
            # Remove blocked entries
            filtered_lines = []
            skip_next = False
            
            for line in lines:
                if "# Website Blocker - Umar J" in line:
                    skip_next = True
                    continue
                
                if skip_next and any(site in line for site in self.blocked_sites):
                    continue
                
                if skip_next and line.strip() == "":
                    skip_next = False
                    continue
                
                skip_next = False
                filtered_lines.append(line)
            
            with open(self.hosts_path, 'w') as file:
                file.writelines(filtered_lines)
            
            self.is_blocking = False
            self.update_status()
            self.flush_dns()
            messagebox.showinfo("Success", "Website blocking stopped.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop blocking: {e}")

    def flush_dns(self):
        """Flush DNS cache"""
        system = platform.system().lower()
        try:
            if system == "windows":
                subprocess.run(["ipconfig", "/flushdns"], 
                             capture_output=True, check=True)
            elif system == "darwin":  # macOS
                subprocess.run(["sudo", "dscacheutil", "-flushcache"], 
                             capture_output=True, check=True)
            elif system == "linux":
                # Try different methods for different Linux distributions
                commands = [
                    ["sudo", "systemctl", "restart", "systemd-resolved"],
                    ["sudo", "/etc/init.d/networking", "restart"],
                    ["sudo", "service", "network-manager", "restart"]
                ]
                for cmd in commands:
                    try:
                        subprocess.run(cmd, capture_output=True, check=True)
                        break
                    except:
                        continue
        except Exception:
            pass  # DNS flush failure is not critical

    def add_schedule(self):
        """Add a scheduled blocking session"""
        start_time = self.start_time_var.get()
        end_time = self.end_time_var.get()
        
        # Validate time format
        try:
            datetime.strptime(start_time, "%H:%M")
            datetime.strptime(end_time, "%H:%M")
        except ValueError:
            messagebox.showerror("Invalid Time", "Please use HH:MM format (e.g., 09:00)")
            return
        
        # Get selected days
        selected_days = [day for day, var in self.days_vars.items() if var.get()]
        
        if not selected_days:
            messagebox.showwarning("No Days Selected", "Please select at least one day.")
            return
        
        # Create schedule entry
        schedule = {
            'start_time': start_time,
            'end_time': end_time,
            'days': selected_days
        }
        
        self.scheduled_blocks.append(schedule)
        
        # Update schedule listbox
        schedule_text = f"{start_time}-{end_time}: {', '.join([d[:3] for d in selected_days])}"
        self.schedule_listbox.insert(tk.END, schedule_text)
        
        self.save_config()
        messagebox.showinfo("Success", "Schedule added successfully.")

    def remove_selected_schedule(self):
        """Remove selected schedule"""
        selection = self.schedule_listbox.curselection()
        if selection:
            index = selection[0]
            del self.scheduled_blocks[index]
            self.schedule_listbox.delete(index)
            self.save_config()
            messagebox.showinfo("Success", "Schedule removed.")
        else:
            messagebox.showwarning("No Selection", "Please select a schedule to remove.")

    def scheduler_loop(self):
        """Background thread to check scheduled blocks"""
        while True:
            try:
                current_time = datetime.now()
                current_day = current_time.strftime("%A")
                current_time_str = current_time.strftime("%H:%M")
                
                should_block = False
                for schedule in self.scheduled_blocks:
                    if current_day in schedule['days']:
                        start_time = schedule['start_time']
                        end_time = schedule['end_time']
                        
                        if start_time <= current_time_str <= end_time:
                            should_block = True
                            break
                
                # Auto start/stop blocking based on schedule
                if should_block and not self.is_blocking and self.blocked_sites:
                    self.root.after(0, self.start_blocking)
                elif not should_block and self.is_blocking:
                    # Only stop if it was auto-started by scheduler
                    self.root.after(0, self.stop_blocking)
                
            except Exception:
                pass
            
            time.sleep(60)  # Check every minute

    def backup_hosts(self):
        """Backup the hosts file"""
        try:
            with open(self.hosts_path, 'r') as source:
                content = source.read()
            
            with open(self.backup_path, 'w') as backup:
                backup.write(content)
            
            messagebox.showinfo("Success", f"Hosts file backed up to {self.backup_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to backup hosts file: {e}")

    def restore_hosts(self):
        """Restore the hosts file from backup"""
        if not os.path.exists(self.backup_path):
            messagebox.showerror("Error", "No backup file found.")
            return
        
        if messagebox.askyesno("Confirm", "This will restore the hosts file from backup. Continue?"):
            try:
                with open(self.backup_path, 'r') as backup:
                    content = backup.read()
                
                with open(self.hosts_path, 'w') as hosts:
                    hosts.write(content)
                
                self.is_blocking = False
                self.update_status()
                self.flush_dns()
                messagebox.showinfo("Success", "Hosts file restored from backup.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to restore hosts file: {e}")

    def export_config(self):
        """Export configuration to JSON file"""
        config = {
            'blocked_sites': self.blocked_sites,
            'scheduled_blocks': self.scheduled_blocks,
            'version': '2.0',
            'created_by': 'Umar J'
        }
        
        try:
            filename = f"website_blocker_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as file:
                json.dump(config, file, indent=4)
            
            messagebox.showinfo("Success", f"Configuration exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export configuration: {e}")

    def import_config(self):
        """Import configuration from JSON file"""
        from tkinter import filedialog
        
        filename = filedialog.askopenfilename(
            title="Select Configuration File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'r') as file:
                config = json.load(file)
            
            # Validate config structure
            if 'blocked_sites' in config and 'scheduled_blocks' in config:
                self.blocked_sites = config['blocked_sites']
                self.scheduled_blocks = config['scheduled_blocks']
                
                # Update GUI
                self.refresh_gui()
                self.save_config()
                
                messagebox.showinfo("Success", "Configuration imported successfully.")
            else:
                messagebox.showerror("Error", "Invalid configuration file format.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import configuration: {e}")

    def refresh_gui(self):
        """Refresh GUI with current data"""
        # Update website listbox
        self.website_listbox.delete(0, tk.END)
        for site in self.blocked_sites:
            self.website_listbox.insert(tk.END, site)
        
        # Update schedule listbox
        self.schedule_listbox.delete(0, tk.END)
        for schedule in self.scheduled_blocks:
            schedule_text = f"{schedule['start_time']}-{schedule['end_time']}: {', '.join([d[:3] for d in schedule['days']])}"
            self.schedule_listbox.insert(tk.END, schedule_text)

    def update_status(self):
        """Update the status indicator"""
        if self.is_blocking:
            self.status_label.config(fg=self.colors['success'])
            self.status_text.config(text="Active")
            self.block_btn.config(
                text="✅ Stop Blocking",
                bg=self.colors['success']
            )
        else:
            self.status_label.config(fg=self.colors['danger'])
            self.status_text.config(text="Inactive")
            self.block_btn.config(
                text="🚫 Start Blocking",
                bg=self.colors['danger']
            )

    def load_config(self):
        """Load configuration from JSON file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as file:
                    config = json.load(file)
                    self.blocked_sites = config.get('blocked_sites', [])
                    self.scheduled_blocks = config.get('scheduled_blocks', [])
            except Exception as e:
                print(f"Error loading config: {e}")
                self.blocked_sites = []
                self.scheduled_blocks = []

    def save_config(self):
        """Save configuration to JSON file"""
        config = {
            'blocked_sites': self.blocked_sites,
            'scheduled_blocks': self.scheduled_blocks,
            'version': '2.0',
            'created_by': 'Umar J'
        }
        
        try:
            with open(self.config_file, 'w') as file:
                json.dump(config, file, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.save_config()
            self.root.destroy()

    def run(self):
        """Run the application"""
        # Load initial data into GUI
        self.refresh_gui()
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Center window
        self.center_window()
        
        # Start the GUI main loop
        self.root.mainloop()

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')


def main():
    """Main function to run the Website Blocker application"""
    try:
        app = WebsiteBlocker()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()