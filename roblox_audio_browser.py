import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import threading
import pygame
from pathlib import Path
import json
import tempfile
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue
import time

class RobloxAudioBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("Roblox Audio Browser")
        self.root.geometry("1100x800")
        self.root.configure(bg="#2b2b2b")
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        
        # Variables
        self.audio_files = []
        self.current_playing = None
        self.temp_audio_file = None
        self.scan_cancelled = False
        self.scan_progress_queue = queue.Queue()
        self.total_files_to_scan = 0
        self.scanned_files_count = 0
        self.is_paused = False
        
        # Default Roblox cache paths
        self.default_paths = [
            os.path.expandvars(r"%LOCALAPPDATA%\Roblox\http"),
	    os.path.expandvars(r"%TEMP%\Roblox\http")
        ]
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="🎵 Roblox Audio Browser", 
            font=("Arial", 20, "bold"),
            fg="#4CAF50",
            bg="#2b2b2b"
        )
        title_label.pack(pady=10)
        
        # Control Frame
        control_frame = tk.Frame(self.root, bg="#2b2b2b")
        control_frame.pack(fill="x", padx=10, pady=5)
        
        # Scan button
        self.scan_button = tk.Button(
            control_frame,
            text="🔍 Scan Roblox Cache",
            command=self.scan_roblox_cache,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=2,
            padx=20,
            pady=5
        )
        self.scan_button.pack(side="left", padx=5)
        
        # Custom folder button
        self.custom_button = tk.Button(
            control_frame,
            text="📁 Browse Custom Folder",
            command=self.browse_custom_folder,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=2,
            padx=20,
            pady=5
        )
        self.custom_button.pack(side="left", padx=5)
        
        # Clear cache button
        self.clear_cache_button = tk.Button(
            control_frame,
            text="🗑️ Clear Cache",
            command=self.clear_cache,
            bg="#FF9800",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=2,
            padx=20,
            pady=5
        )
        self.clear_cache_button.pack(side="left", padx=5)
        
        # Cancel scan button
        self.cancel_button = tk.Button(
            control_frame,
            text="❌ Cancel Scan",
            command=self.cancel_scan,
            bg="#f44336",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=2,
            padx=20,
            pady=5,
            state="disabled"
        )
        self.cancel_button.pack(side="left", padx=5)
        
        # Status label
        self.status_label = tk.Label(
            control_frame,
            text="Ready to scan...",
            fg="#888888",
            bg="#2b2b2b",
            font=("Arial", 10)
        )
        self.status_label.pack(side="right", padx=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.root,
            mode='determinate',
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress.pack(fill="x", padx=10, pady=5)
        
        # Search frame
        search_frame = tk.Frame(self.root, bg="#2b2b2b")
        search_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(
            search_frame,
            text="🔎 Filter:",
            fg="white",
            bg="#2b2b2b",
            font=("Arial", 10)
        ).pack(side="left")
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_files)
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            bg="#404040",
            fg="white",
            insertbackground="white",
            font=("Arial", 10)
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Main frame for listbox and controls
        main_frame = tk.Frame(self.root, bg="#2b2b2b")
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Listbox with scrollbar
        listbox_frame = tk.Frame(main_frame, bg="#2b2b2b")
        listbox_frame.pack(side="left", fill="both", expand=True)
        
        self.listbox = tk.Listbox(
            listbox_frame,
            bg="#404040",
            fg="#E0E0E0",
            selectbackground="#4CAF50",
            selectforeground="white",
            font=("Consolas", 10),
            relief="sunken",
            bd=2,
            activestyle="none"
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)
        
        # Audio controls frame
        controls_frame = tk.Frame(main_frame, bg="#2b2b2b", width=240)
        controls_frame.pack(side="right", fill="y", padx=10)
        controls_frame.pack_propagate(False)
        
        tk.Label(
            controls_frame,
            text="🎵 Audio Controls",
            fg="#4CAF50",
            bg="#2b2b2b",
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        # Play button
        self.play_button = tk.Button(
            controls_frame,
            text="▶️ Play",
            command=self.play_audio,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            width=15,
            pady=5
        )
        self.play_button.pack(pady=5)
        
        # Stop button
        self.stop_button = tk.Button(
            controls_frame,
            text="⏹️ Stop",
            command=self.stop_audio,
            bg="#f44336",
            fg="white",
            font=("Arial", 11, "bold"),
            width=15,
            pady=5
        )
        self.stop_button.pack(pady=5)
        
        # Extract OGG button
        self.extract_button = tk.Button(
            controls_frame,
            text="💾 Extract OGG",
            command=self.extract_selected,
            bg="#FF9800",
            fg="white",
            font=("Arial", 11, "bold"),
            width=15,
            pady=5
        )
        self.extract_button.pack(pady=5)
        
        # Extract Hash button
        self.extract_hash_button = tk.Button(
            controls_frame,
            text="📄 Extract Hash",
            command=self.extract_hash_file,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 11, "bold"),
            width=15,
            pady=5
        )
        self.extract_hash_button.pack(pady=5)
        
        # Volume control
        tk.Label(
            controls_frame,
            text="🔊 Volume",
            fg="white",
            bg="#2b2b2b",
            font=("Arial", 10)
        ).pack(pady=(20, 5))
        
        self.volume_var = tk.DoubleVar(value=0.7)
        volume_scale = tk.Scale(
            controls_frame,
            from_=0.0,
            to=1.0,
            resolution=0.1,
            orient="horizontal",
            variable=self.volume_var,
            command=self.change_volume,
            bg="#404040",
            fg="white",
            highlightbackground="#2b2b2b",
            width=15
        )
        volume_scale.pack(fill="x", padx=5)
        
        # Info panel frame with border
        info_frame = tk.Frame(controls_frame, bg="#2b2b2b", relief="groove", bd=2)
        info_frame.pack(pady=20, padx=5, fill="both", expand=True)
        
        # Info panel title
        info_title = tk.Label(
            info_frame,
            text="📋 File Information",
            fg="#4CAF50",
            bg="#2b2b2b",
            font=("Arial", 10, "bold")
        )
        info_title.pack(pady=(5, 10))
        
        # Main info label
        self.info_label = tk.Label(
            info_frame,
            text="Select an audio file to view details\nDouble-click to play\nRight-click for options",
            fg="#E0E0E0",
            bg="#2b2b2b",
            font=("Consolas", 9),
            wraplength=220,
            justify="left",
            anchor="nw"
        )
        self.info_label.pack(pady=(0, 10), padx=5, fill="both", expand=True)
        
        # Bind double-click to play
        self.listbox.bind("<Double-1>", lambda e: self.play_audio())
        
        # Bind selection change to update info
        self.listbox.bind("<<ListboxSelect>>", self.on_file_select)
        
        # Create context menu
        self.context_menu = tk.Menu(self.root, tearoff=0, bg="#404040", fg="white")
        self.context_menu.add_command(label="▶️ Play Audio", command=self.play_audio)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="💾 Extract as OGG", command=self.extract_selected)
        self.context_menu.add_command(label="📄 Extract Hash File", command=self.extract_hash_file)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📋 Copy File Path", command=self.copy_file_path)
        
        # Bind right-click to context menu
        self.listbox.bind("<Button-3>", self.show_context_menu)
        
    def handle_click_focus(self, event):
        """Handle click events to manage focus properly."""
        # Let the normal click handling occur
        event.widget.focus_set()
    
    def on_play_status_update(self):
        """Update the playing status in info panel."""
        selection = self.listbox.curselection()
        if selection:
            selected_text = self.listbox.get(selection[0])
            selected_file = self.get_selected_file_info(selected_text)
            if selected_file:
                display_name = selected_file['name'][:18] + "..." if len(selected_file['name']) > 18 else selected_file['name']
                size_text = self.format_file_size(selected_file['size'])
                folder_name = selected_file['dir'][:15] + "..." if len(selected_file['dir']) > 15 else selected_file['dir']
                
                playing_info = (
                    f"🎵 NOW PLAYING\n"
                    f"{'─' * 23}\n"
                    f"📄 {display_name}\n"
                    f"💾 {size_text}\n"
                    f"📁 {folder_name}\n"
                    f"{'─' * 23}\n"
                    f"🔊 Vol: {int(self.volume_var.get() * 100)}%"
                )
                self.info_label.config(text=playing_info)
        
    def scan_roblox_cache(self):
        """Scan Roblox cache directories for audio files using multi-threading."""
        self.scan_button.config(state="disabled")
        self.custom_button.config(state="disabled")
        self.clear_cache_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        self.scan_cancelled = False
        self.progress.config(value=0)
        self.status_label.config(text="Preparing scan...")
        
        # Run scan in separate thread to prevent UI freezing
        threading.Thread(target=self._multithreaded_scan, daemon=True).start()
        
        # Start progress monitor
        self.monitor_progress()
        
    def _multithreaded_scan(self):
        """Multi-threaded scanning function."""
        found_files = []
        
        # First pass: count total files to scan
        self.root.after(0, lambda: self.status_label.config(text="Counting files to scan..."))
        total_files = 0
        directories_to_scan = []
        
        for cache_path in self.default_paths:
            if os.path.exists(cache_path) and not self.scan_cancelled:
                for root, dirs, files in os.walk(cache_path):
                    if self.scan_cancelled:
                        break
                    # Filter to only files that could be audio (reasonable size range)
                    potential_files = [f for f in files if 1024 <= self._get_file_size_safe(os.path.join(root, f)) <= 50*1024*1024]  # 1KB to 50MB
                    if potential_files:
                        directories_to_scan.append((root, potential_files))
                        total_files += len(potential_files)
        
        self.total_files_to_scan = total_files
        self.scanned_files_count = 0
        
        if total_files == 0:
            self.root.after(0, lambda: self._update_scan_results([]))
            return
        
        self.root.after(0, lambda: self.status_label.config(text=f"Scanning {total_files} files with {os.cpu_count()} threads..."))
        
        # Multi-threaded scanning
        max_workers = min(os.cpu_count() or 4, 8)  # Use CPU count but cap at 8
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            if self.scan_cancelled:
                return
                
            # Submit all file scanning tasks
            future_to_file = {}
            for root, files in directories_to_scan:
                if self.scan_cancelled:
                    break
                for file in files:
                    if self.scan_cancelled:
                        break
                    file_path = os.path.join(root, file)
                    future = executor.submit(self._scan_file, file_path, root)
                    future_to_file[future] = file_path
            
            # Collect results as they complete
            for future in as_completed(future_to_file):
                if self.scan_cancelled:
                    # Cancel remaining futures
                    for f in future_to_file:
                        f.cancel()
                    break
                    
                try:
                    result = future.result(timeout=5)  # 5 second timeout per file
                    if result:
                        found_files.append(result)
                    
                    self.scanned_files_count += 1
                    
                    # Update progress every 10 files or on last file
                    if self.scanned_files_count % 10 == 0 or self.scanned_files_count >= total_files:
                        progress = (self.scanned_files_count / total_files) * 100
                        self.scan_progress_queue.put(('progress', progress, len(found_files)))
                        
                except Exception as e:
                    self.scanned_files_count += 1
                    # Skip problematic files silently
                    continue
        
        # Update UI in main thread
        if not self.scan_cancelled:
            self.root.after(0, lambda: self._update_scan_results(found_files))
        else:
            self.root.after(0, lambda: self._scan_cancelled())
    
    def _scan_file(self, file_path, root_dir):
        """Scan individual file for audio content."""
        try:
            if self.is_audio_file(file_path):
                return {
                    'path': file_path,
                    'name': os.path.basename(file_path),
                    'size': os.path.getsize(file_path),
                    'dir': os.path.basename(root_dir)
                }
        except:
            pass  # Skip files that can't be read
        return None
    
    def _get_file_size_safe(self, file_path):
        """Safely get file size."""
        try:
            return os.path.getsize(file_path)
        except:
            return 0
    
    def monitor_progress(self):
        """Monitor scanning progress and update UI."""
        try:
            while True:
                try:
                    msg_type, progress, found_count = self.scan_progress_queue.get_nowait()
                    if msg_type == 'progress':
                        self.progress.config(value=progress)
                        self.status_label.config(text=f"Scanned: {self.scanned_files_count}/{self.total_files_to_scan} files | Found: {found_count} audio files")
                except queue.Empty:
                    break
        except:
            pass
        
        # Continue monitoring if scan is still running
        if self.scan_button.cget('state') == 'disabled' and not self.scan_cancelled:
            self.root.after(100, self.monitor_progress)
    
    def cancel_scan(self):
        """Cancel the current scan operation."""
        self.scan_cancelled = True
        self.status_label.config(text="Cancelling scan...")
    
    def _scan_cancelled(self):
        """Handle scan cancellation."""
        self.scan_button.config(state="normal")
        self.custom_button.config(state="normal")
        self.clear_cache_button.config(state="normal")
        self.cancel_button.config(state="disabled")
        self.progress.config(value=0)
        self.status_label.config(text="Scan cancelled")
        self.scan_cancelled = False
        
    def _scan_thread(self):
        """Thread function for scanning."""
        found_files = []
        
        for cache_path in self.default_paths:
            if os.path.exists(cache_path):
                self.root.after(0, lambda p=cache_path: self.status_label.config(
                    text=f"Scanning: {os.path.basename(p)}..."
                ))
                
                for root, dirs, files in os.walk(cache_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        
                        # Check if file contains OGG data
                        if self.is_audio_file(file_path):
                            found_files.append({
                                'path': file_path,
                                'name': file,
                                'size': os.path.getsize(file_path),
                                'dir': os.path.basename(root)
                            })
        
        # Update UI in main thread
        self.root.after(0, lambda: self._update_scan_results(found_files))
        
    def _update_scan_results(self, found_files):
        """Update UI with scan results."""
        self.audio_files = found_files
        self.populate_listbox()
        
        self.progress.config(value=100)
        self.scan_button.config(state="normal")
        self.custom_button.config(state="normal")
        self.clear_cache_button.config(state="normal")
        self.cancel_button.config(state="disabled")
        self.status_label.config(text=f"Scan complete! Found {len(found_files)} audio files")
        
        if not found_files:
            messagebox.showinfo("Scan Complete", "No audio files found in Roblox cache directories.")
        else:
            # Sort files by size (largest first) for better user experience
            self.audio_files.sort(key=lambda x: x['size'], reverse=True)
            self.populate_listbox()
            # Trigger info panel update to show collection stats
            self.on_file_select(None)
        
    def browse_custom_folder(self):
        """Browse for a custom folder to scan."""
        folder_path = filedialog.askdirectory(
            title="Select folder to scan for audio files"
        )
        
        if folder_path:
            self.scan_button.config(state="disabled")
            self.custom_button.config(state="disabled")
            self.clear_cache_button.config(state="disabled")
            self.cancel_button.config(state="normal")
            self.scan_cancelled = False
            self.progress.config(value=0)
            self.status_label.config(text="Preparing custom folder scan...")
            
            # Run scan in separate thread
            threading.Thread(
                target=self._multithreaded_custom_scan,
                args=(folder_path,),
                daemon=True
            ).start()
            
            # Start progress monitor
            self.monitor_progress()
    
    def _multithreaded_custom_scan(self, folder_path):
        """Multi-threaded scanning function for custom folder."""
        found_files = []
        
        # Count files first
        self.root.after(0, lambda: self.status_label.config(text="Counting files in custom folder..."))
        
        all_files = []
        for root, dirs, files in os.walk(folder_path):
            if self.scan_cancelled:
                break
            for file in files:
                file_path = os.path.join(root, file)
                file_size = self._get_file_size_safe(file_path)
                # Filter by size to avoid scanning obviously non-audio files
                if 1024 <= file_size <= 50*1024*1024:  # 1KB to 50MB
                    all_files.append((file_path, root))
        
        self.total_files_to_scan = len(all_files)
        self.scanned_files_count = 0
        
        if not all_files:
            self.root.after(0, lambda: self._update_custom_results([], folder_path))
            return
        
        self.root.after(0, lambda: self.status_label.config(
            text=f"Scanning {len(all_files)} files in custom folder with {os.cpu_count()} threads..."
        ))
        
        # Multi-threaded scanning
        max_workers = min(os.cpu_count() or 4, 8)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            if self.scan_cancelled:
                return
                
            # Submit all file scanning tasks
            future_to_file = {}
            for file_path, root_dir in all_files:
                if self.scan_cancelled:
                    break
                future = executor.submit(self._scan_file, file_path, root_dir)
                future_to_file[future] = file_path
            
            # Collect results as they complete
            for future in as_completed(future_to_file):
                if self.scan_cancelled:
                    for f in future_to_file:
                        f.cancel()
                    break
                    
                try:
                    result = future.result(timeout=5)
                    if result:
                        found_files.append(result)
                    
                    self.scanned_files_count += 1
                    
                    # Update progress
                    if self.scanned_files_count % 10 == 0 or self.scanned_files_count >= len(all_files):
                        progress = (self.scanned_files_count / len(all_files)) * 100
                        self.scan_progress_queue.put(('progress', progress, len(found_files)))
                        
                except Exception:
                    self.scanned_files_count += 1
                    continue
        
        # Update UI in main thread
        if not self.scan_cancelled:
            self.root.after(0, lambda: self._update_custom_results(found_files, folder_path))
        else:
            self.root.after(0, lambda: self._scan_cancelled())
    
    def _scan_custom_thread(self, folder_path):
        """Thread function for scanning custom folder."""
        found_files = []
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                if self.is_audio_file(file_path):
                    found_files.append({
                        'path': file_path,
                        'name': file,
                        'size': os.path.getsize(file_path),
                        'dir': os.path.basename(root)
                    })
        
        # Update UI in main thread
        self.root.after(0, lambda: self._update_custom_results(found_files, folder_path))
    
    def _update_custom_results(self, found_files, folder_path):
        """Update UI with custom scan results."""
        # Sort files by size (largest first)
        found_files.sort(key=lambda x: x['size'], reverse=True)
        self.audio_files = found_files
        self.populate_listbox()
        
        self.progress.config(value=100)
        self.scan_button.config(state="normal")
        self.custom_button.config(state="normal")
        self.clear_cache_button.config(state="normal")
        self.cancel_button.config(state="disabled")
        self.status_label.config(text=f"Custom scan complete! Found {len(found_files)} audio files in {os.path.basename(folder_path)}")
        
        if not found_files:
            messagebox.showinfo("Scan Complete", f"No audio files found in {folder_path}")
        else:
            # Trigger info panel update to show collection stats
            self.on_file_select(None)
    
    def clear_cache(self):
        """Clear Roblox cache directories."""
        # Confirm with user
        result = messagebox.askyesno(
            "Clear Cache", 
            "This will delete all files in Roblox cache directories.\n\n"
            "This action cannot be undone. Are you sure you want to continue?",
            icon='warning'
        )
        
        if not result:
            return
        
        # Stop any playing audio first
        self.stop_audio()
        
        # Clear the current file list
        self.audio_files = []
        self.populate_listbox()
        
        self.status_label.config(text="Clearing Roblox cache...")
        
        # Run clearing in separate thread to avoid blocking UI
        threading.Thread(
            target=self._clear_cache_thread,
            daemon=True
        ).start()
    
    def _clear_cache_thread(self):
        """Thread function for clearing cache directories."""
        cleared_files = 0
        errors = []
        
        for cache_path in self.default_paths:
            if os.path.exists(cache_path):
                self.root.after(0, lambda p=cache_path: self.status_label.config(
                    text=f"Clearing cache: {os.path.basename(p)}..."
                ))
                
                try:
                    # Walk through the directory and delete all files
                    for root, dirs, files in os.walk(cache_path):
                        for file in files:
                            if hasattr(self, 'scan_cancelled') and self.scan_cancelled:
                                return
                            
                            file_path = os.path.join(root, file)
                            try:
                                os.remove(file_path)
                                cleared_files += 1
                                
                                # Update status periodically
                                if cleared_files % 100 == 0:
                                    self.root.after(0, lambda c=cleared_files: self.status_label.config(
                                        text=f"Cleared {c} files..."
                                    ))
                            except Exception as e:
                                errors.append(f"Failed to delete {file}: {str(e)}")
                                continue
                        
                        # Remove empty directories
                        try:
                            # Only remove if directory is empty
                            if not os.listdir(root) and root != cache_path:
                                os.rmdir(root)
                        except:
                            pass  # Ignore errors removing directories
                            
                except Exception as e:
                    errors.append(f"Error accessing {cache_path}: {str(e)}")
        
        # Update UI in main thread
        self.root.after(0, lambda: self._clear_cache_complete(cleared_files, errors))
    
    def _clear_cache_complete(self, cleared_files, errors):
        """Complete the cache clearing operation."""
        if errors:
            error_msg = f"Cache clearing completed with {len(errors)} errors.\n"
            error_msg += f"Cleared {cleared_files} files.\n\n"
            error_msg += "Some errors occurred:\n"
            error_msg += "\n".join(errors[:5])  # Show first 5 errors
            if len(errors) > 5:
                error_msg += f"\n... and {len(errors) - 5} more errors."
            
            messagebox.showwarning("Cache Cleared", error_msg)
        else:
            messagebox.showinfo("Cache Cleared", f"Successfully cleared {cleared_files} files from Roblox cache directories.")
        
        self.status_label.config(text="Cache cleared. Ready to scan...")
    
    def is_audio_file(self, file_path):
        """Check if file contains OGG audio data - optimized version."""
        try:
            # Quick size check first
            file_size = os.path.getsize(file_path)
            if file_size < 1024 or file_size > 50*1024*1024:  # Skip very small or very large files
                return False
            
            # Read larger chunk for better detection but not the entire file
            chunk_size = min(4096, file_size)  # Read up to 4KB
            
            with open(file_path, 'rb') as f:
                data = f.read(chunk_size)
                # Check for OGG header
                if b'OggS' in data:
                    return True
                
                # Also check for other common audio signatures
                if (data.startswith(b'RIFF') and b'WAVE' in data[:20]) or \
                   data.startswith(b'ID3') or \
                   data.startswith(b'\xff\xfb') or data.startswith(b'\xff\xfa'):
                    return True
                    
            return False
        except:
            return False
    
    def contains_ogg(self, file_path):
        """Quick check if file contains OGG data."""
        try:
            with open(file_path, 'rb') as f:
                data = f.read(1024)
                return b'OggS' in data
        except:
            return False
    
    def populate_listbox(self):
        """Populate the listbox with found audio files."""
        self.listbox.delete(0, tk.END)
        
        # Add header with better styling
        header = f"{'FILE NAME':<55} {'SIZE':>10} {'SOURCE':>15} {'TYPE':>8}"
        separator = "═" * 95
        
        self.listbox.insert(tk.END, f"🎵 {header}")
        self.listbox.insert(tk.END, separator)
        
        for i, file_info in enumerate(self.audio_files):
            size_kb = file_info['size'] // 1024
            # Show size in MB if >= 1MB with better formatting
            if size_kb >= 1024:
                size_mb = file_info['size'] / (1024 * 1024)
                size_text = f"{size_mb:.1f}MB"
            else:
                size_text = f"{size_kb}KB"
            
            # Determine file type with icon
            file_type = "🎶 OGG" if self.contains_ogg(file_info['path']) else "📄 DATA"
            
            # Better formatting with improved spacing
            name_part = file_info['name'][:48]
            if len(file_info['name']) > 48:
                name_part = name_part + "..."
            
            # Add visual indicators
            source_icon = "🌐" if file_info['dir'] == "http" else "📁"
            
            # Create formatted row
            row_num = f"{i+1:>3}"
            display_text = f"{row_num}│{name_part:<48}│{size_text:>9}│{source_icon}{file_info['dir']:>14}│{file_type:>12}"
            
            self.listbox.insert(tk.END, display_text)
    
    def filter_files(self, *args):
        """Filter the file list based on search term."""
        search_term = self.search_var.get().lower()
        self.listbox.delete(0, tk.END)
        
        # Add header with better styling
        header = f"{'FILE NAME':<55} {'SIZE':>10} {'SOURCE':>15} {'TYPE':>8}"
        separator = "═" * 95
        
        self.listbox.insert(tk.END, f"🎵 {header}")
        self.listbox.insert(tk.END, separator)
        
        filtered_count = 0
        for file_info in self.audio_files:
            if search_term in file_info['name'].lower() or search_term in file_info['dir'].lower():
                size_kb = file_info['size'] // 1024
                # Show size in MB if >= 1MB with better formatting
                if size_kb >= 1024:
                    size_mb = file_info['size'] / (1024 * 1024)
                    size_text = f"{size_mb:.1f}MB"
                else:
                    size_text = f"{size_kb}KB"
                
                # Determine file type with icon
                file_type = "🎶 OGG" if self.contains_ogg(file_info['path']) else "📄 DATA"
                
                # Better formatting with improved spacing
                name_part = file_info['name'][:48]
                if len(file_info['name']) > 48:
                    name_part = name_part + "..."
                
                # Add visual indicators
                source_icon = "🌐" if file_info['dir'] == "http" else "📁"
                
                # Create formatted row
                filtered_count += 1
                row_num = f"{filtered_count:>3}"
                display_text = f"{row_num}│{name_part:<48}│{size_text:>9}│{source_icon}{file_info['dir']:>14}│{file_type:>12}"
                
                self.listbox.insert(tk.END, display_text)
    
    def get_selected_file_info(self, selected_text):
        """Extract file info from selected display text."""
        # Skip header and separator rows
        if (selected_text.startswith('🎵') or 
            selected_text.startswith('═') or 
            selected_text.startswith('FILENAME') or 
            selected_text.startswith('─') or 
            not selected_text.strip()):
            return None
            
        # Parse the new format: "row│filename│size│source│type"
        if '│' in selected_text:
            parts = selected_text.split('│')
            if len(parts) >= 2:
                # Extract filename (second part, removing extra spaces)
                filename_part = parts[1].strip()
                
                # Remove trailing dots if present
                if filename_part.endswith('...'):
                    filename_part = filename_part[:-3]
                
                # Find the matching file
                for file_info in self.audio_files:
                    # Match by checking if the displayed name matches the start of the actual filename
                    if file_info['name'].startswith(filename_part) or filename_part in file_info['name']:
                        return file_info
        
        # Fallback: try old format parsing for compatibility
        if '.' in selected_text and not selected_text.startswith('🎵'):
            parts = selected_text.split('.', 1)
            if len(parts) >= 2:
                content = parts[1].strip()
                file_name_part = content.split()[0]
                
                if file_name_part.endswith('...'):
                    file_name_part = file_name_part[:-3]
                
                for file_info in self.audio_files:
                    if file_info['name'].startswith(file_name_part) or file_name_part in file_info['name']:
                        return file_info
        
        return None
    
    def play_audio(self):
        """Play the selected audio file."""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an audio file to play.")
            return
        
        # Handle pause/resume if already playing
        if self.current_playing and pygame.mixer.music.get_busy():
            if self.is_paused:
                # Resume
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.play_button.config(text="⏸️ Pause")
                return
            else:
                # Pause
                pygame.mixer.music.pause()
                self.is_paused = True
                self.play_button.config(text="▶️ Resume")
                return
        
        # Get the selected file info
        selected_text = self.listbox.get(selection[0])
        selected_file = self.get_selected_file_info(selected_text)
        
        if not selected_file:
            messagebox.showerror("Error", "Could not find the selected file.")
            return
        
        try:
            # Extract OGG data to temporary file
            if self.temp_audio_file:
                try:
                    os.unlink(self.temp_audio_file)
                except:
                    pass
            
            self.temp_audio_file = self.extract_ogg_to_temp(selected_file['path'])
            
            if self.temp_audio_file:
                pygame.mixer.music.load(self.temp_audio_file)
                pygame.mixer.music.set_volume(self.volume_var.get())
                pygame.mixer.music.play()
                
                self.current_playing = selected_file['name']
                self.is_paused = False
                
                # Use the new status update method
                self.on_play_status_update()
                self.play_button.config(text="⏸️ Pause")
            else:
                messagebox.showerror("Error", "Failed to extract audio data from file.")
                
        except Exception as e:
            messagebox.showerror("Playback Error", f"Could not play audio file:\n{str(e)}")
    
    def stop_audio(self):
        """Stop audio playback."""
        pygame.mixer.music.stop()
        self.current_playing = None
        self.is_paused = False
        self.info_label.config(text="🔇 Playback stopped")
        self.play_button.config(text="▶️ Play")
    
    def change_volume(self, value):
        """Change playback volume."""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_volume(float(value))
            # Update info panel if currently playing
            if self.current_playing and not self.is_paused:
                self.on_play_status_update()
    
    def extract_ogg_to_temp(self, file_path):
        """Extract OGG data from file to temporary file."""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            ogg_start = data.find(b'OggS')
            if ogg_start == -1:
                return None
            
            ogg_data = data[ogg_start:]
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(suffix='.ogg', delete=False)
            temp_file.write(ogg_data)
            temp_file.close()
            
            return temp_file.name
            
        except Exception as e:
            print(f"Error extracting OGG: {e}")
            return None
    
    def extract_selected(self):
        """Extract selected audio file as OGG."""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an audio file to extract.")
            return
        
        # Get the selected file info
        selected_text = self.listbox.get(selection[0])
        selected_file = self.get_selected_file_info(selected_text)
        
        if not selected_file:
            messagebox.showerror("Error", "Could not find the selected file.")
            return
        
        # Ask for save location
        output_path = filedialog.asksaveasfilename(
            title="Save OGG file as...",
            defaultextension=".ogg",
            filetypes=[("OGG Audio", "*.ogg"), ("All Files", "*.*")],
            initialfile=f"{selected_file['name']}.ogg"
        )
        
        if output_path:
            try:
                # Extract OGG data
                with open(selected_file['path'], 'rb') as f:
                    data = f.read()
                
                ogg_start = data.find(b'OggS')
                if ogg_start == -1:
                    messagebox.showerror("Error", "No OGG data found in file.")
                    return
                
                ogg_data = data[ogg_start:]
                
                with open(output_path, 'wb') as f:
                    f.write(ogg_data)
                
                messagebox.showinfo("Success", f"Audio extracted successfully to:\n{output_path}")
                
            except Exception as e:
                messagebox.showerror("Extraction Error", f"Failed to extract audio:\n{str(e)}")
    
    def extract_hash_file(self):
        """Extract selected hash file (raw cache file) as-is."""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a hash file to extract.")
            return
        
        # Get the selected file info
        selected_text = self.listbox.get(selection[0])
        selected_file = self.get_selected_file_info(selected_text)
        
        if not selected_file:
            messagebox.showerror("Error", "Could not find the selected file.")
            return
        
        # Ask for save location - default to hash name without extension
        default_name = selected_file['name']  # No extension added
        output_path = filedialog.asksaveasfilename(
            title="Save hash file as...",
            filetypes=[
                ("Cache Files", "*.cache"),
                ("Hash Files", "*.hash"),
                ("Binary Files", "*.bin"),
                ("All Files", "*.*")
            ],
            initialfile=default_name
        )
        
        if output_path:
            try:
                # Copy the entire hash file as-is
                shutil.copy2(selected_file['path'], output_path)
                
                # Show success message with file info
                file_size = os.path.getsize(output_path)
                size_kb = file_size // 1024
                
                messagebox.showinfo(
                    "Success", 
                    f"Hash file extracted successfully!\n\n"
                    f"File: {os.path.basename(output_path)}\n"
                    f"Size: {size_kb} KB\n"
                    f"Location: {output_path}"
                )
                
            except Exception as e:
                messagebox.showerror("Extraction Error", f"Failed to extract hash file:\n{str(e)}")
    
    def show_context_menu(self, event):
        """Show context menu on right-click."""
        # Select the item under cursor
        index = self.listbox.nearest(event.y)
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(index)
        
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def copy_file_path(self):
        """Copy the selected file's full path to clipboard."""
        selection = self.listbox.curselection()
        if not selection:
            return
        
        # Get the selected file info
        selected_text = self.listbox.get(selection[0])
        selected_file = self.get_selected_file_info(selected_text)
        
        if selected_file:
            self.root.clipboard_clear()
            self.root.clipboard_append(selected_file['path'])
            messagebox.showinfo("Copied", f"File path copied to clipboard:\n{selected_file['path']}")
    
    def on_file_select(self, event):
        """Update info label when a file is selected."""
        selection = self.listbox.curselection()
        if not selection:
            # Show collection statistics when no file is selected
            if hasattr(self, 'audio_files') and self.audio_files:
                total_files = len(self.audio_files)
                total_size = sum(f['size'] for f in self.audio_files)
                size_text = self.format_file_size(total_size)
                
                # Count different formats
                format_counts = {}
                for file in self.audio_files:
                    fmt = self.detect_audio_format(file['path'])
                    format_counts[fmt] = format_counts.get(fmt, 0) + 1
                
                formats_text = "\n".join([f"  • {fmt}: {count}" for fmt, count in sorted(format_counts.items())])
                
                stats_text = (
                    f"📊 COLLECTION STATS\n"
                    f"{'─' * 23}\n"
                    f"📁 Files: {total_files}\n"
                    f"💾 Size: {size_text}\n"
                    f"🎵 Formats:\n{formats_text}"
                )
                self.info_label.config(text=stats_text)
            else:
                self.info_label.config(text="🎵 Select an audio file to view details")
            return
        
        # Get the selected file info
        selected_text = self.listbox.get(selection[0])
        selected_file = self.get_selected_file_info(selected_text)
        
        if selected_file:
            file_path = selected_file['path']
            
            # Calculate size using consistent formatting
            size_text = self.format_file_size(selected_file['size'])
            
            # Get file dates
            try:
                import datetime
                mod_time = os.path.getmtime(file_path)
                mod_date = datetime.datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M")
            except:
                mod_date = "Unknown"
            
            # Estimate audio duration (rough estimate based on file size)
            estimated_duration = self.estimate_audio_duration(selected_file['size'])
            
            # Detect audio format
            audio_format = self.detect_audio_format(file_path)
            
            # Get file extension or hash-like name
            file_name = selected_file['name']
            if '.' in file_name:
                display_name = file_name
            else:
                # Roblox hash file - show truncated hash
                display_name = f"{file_name[:16]}..." if len(file_name) > 16 else file_name
            
            # Build comprehensive info text
            info_text = (
                f"📄 {display_name}\n"
                f"{'─' * 23}\n"
                f"🎵 {audio_format}\n"
                f"📁 {selected_file['dir']}\n"
                f"💾 {size_text}\n"
                f"⏱️ {estimated_duration}\n"
                f"📅 {mod_date}"
            )
            self.info_label.config(text=info_text)
    
    def format_file_size(self, size_bytes):
        """Format file size in human readable format."""
        if size_bytes >= 1024 * 1024 * 1024:  # GB
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
        elif size_bytes >= 1024 * 1024:  # MB
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        elif size_bytes >= 1024:  # KB
            return f"{size_bytes // 1024} KB"
        else:
            return f"{size_bytes} B"
    
    def estimate_audio_duration(self, file_size_bytes):
        """Estimate audio duration based on file size."""
        # Rough estimates for OGG files at common bitrates
        # This is approximate and varies greatly
        if file_size_bytes < 50 * 1024:  # < 50KB
            return "~3-10s"
        elif file_size_bytes < 200 * 1024:  # < 200KB
            return "~10-30s"
        elif file_size_bytes < 500 * 1024:  # < 500KB
            return "~30s-1m"
        elif file_size_bytes < 1024 * 1024:  # < 1MB
            return "~1-2m"
        elif file_size_bytes < 3 * 1024 * 1024:  # < 3MB
            return "~2-5m"
        else:
            return "~5m+"
    
    def detect_audio_format(self, file_path):
        """Detect audio format by checking file headers."""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(16)
                
            if header.startswith(b'OggS'):
                return "OGG Vorbis"
            elif header[4:8] == b'ftyp' or header.startswith(b'\x00\x00\x00'):
                # Could be MP4/M4A
                if b'M4A ' in header or b'mp41' in header:
                    return "M4A/MP4"
                return "MP4/M4A(?)"
            elif header.startswith(b'ID3') or header.startswith(b'\xFF\xFB') or header.startswith(b'\xFF\xF3'):
                return "MP3"
            elif header.startswith(b'RIFF') and b'WAVE' in header[:12]:
                return "WAV"
            elif header.startswith(b'fLaC'):
                return "FLAC"
            else:
                # Check for common audio patterns
                if b'OggS' in header:
                    return "OGG"
                return "Audio (Unknown)"
        except:
            return "Audio File"
    
    def __del__(self):
        """Cleanup temporary files."""
        if hasattr(self, 'temp_audio_file') and self.temp_audio_file:
            try:
                os.unlink(self.temp_audio_file)
            except:
                pass

def main():
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Custom.Horizontal.TProgressbar", background='#4CAF50')
    
    app = RobloxAudioBrowser(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (1100 // 2)
    y = (root.winfo_screenheight() // 2) - (800 // 2)
    root.geometry(f"1100x800+{x}+{y}")

    # Handle closing
    def on_closing():
        pygame.mixer.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()

if __name__ == "__main__":
    main()
