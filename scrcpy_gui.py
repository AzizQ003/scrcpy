import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys
from ttkthemes import ThemedTk

class ModernButton(ttk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(style='Modern.TButton')

class ScrcpyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Scrcpy GUI")
        self.root.geometry("500x400")
        
        # Configure styles
        style = ttk.Style()
        style.configure('Modern.TButton', padding=10, font=('Segoe UI', 10))
        style.configure('Modern.TLabel', font=('Segoe UI', 10))
        style.configure('Modern.TCheckbutton', font=('Segoe UI', 10))
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'))
        
        # Create main frame with padding
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Scrcpy Control Panel", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Device selection frame
        device_frame = ttk.LabelFrame(main_frame, text="Device Settings", padding="10")
        device_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(device_frame, text="Device:", style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.device_var = tk.StringVar()
        self.device_combo = ttk.Combobox(device_frame, textvariable=self.device_var, width=30)
        self.device_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Quality settings frame
        quality_frame = ttk.LabelFrame(main_frame, text="Quality Settings", padding="10")
        quality_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(quality_frame, text="Max Resolution:", style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.resolution_var = tk.StringVar(value="1280")
        ttk.Entry(quality_frame, textvariable=self.resolution_var, width=10).grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        ttk.Label(quality_frame, text="Bitrate (Mbps):", style='Modern.TLabel').grid(row=1, column=0, sticky=tk.W, pady=5)
        self.bitrate_var = tk.StringVar(value="8")
        ttk.Entry(quality_frame, textvariable=self.bitrate_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.turn_screen_off = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Turn screen off", variable=self.turn_screen_off, style='Modern.TCheckbutton').grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.stay_awake = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Stay awake", variable=self.stay_awake, style='Modern.TCheckbutton').grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Start button with icon
        start_button = ModernButton(button_frame, text="▶ Start Scrcpy", command=self.start_scrcpy)
        start_button.grid(row=0, column=0, padx=5)
        
        # Refresh button with icon
        refresh_button = ModernButton(button_frame, text="↻ Refresh Devices", command=self.refresh_devices)
        refresh_button.grid(row=0, column=1, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        
        # Initial device refresh
        self.refresh_devices()

    def refresh_devices(self):
        try:
            self.status_var.set("Refreshing devices...")
            self.root.update()
            
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            devices = []
            for line in result.stdout.split('\n')[1:]:
                if '\tdevice' in line:
                    devices.append(line.split('\t')[0])
            self.device_combo['values'] = devices
            if devices:
                self.device_combo.set(devices[0])
                self.status_var.set(f"Found {len(devices)} device(s)")
            else:
                self.status_var.set("No devices found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get devices: {str(e)}")
            self.status_var.set("Error refreshing devices")

    def start_scrcpy(self):
        try:
            device = self.device_var.get()
            if not device:
                messagebox.showerror("Error", "No device selected")
                return
                
            self.status_var.set("Starting Scrcpy...")
            self.root.update()
            
            cmd = ['scrcpy']
            
            # Add device if specified
            if device:
                cmd.extend(['-s', device])
            
            # Add resolution
            if self.resolution_var.get():
                cmd.extend(['--max-size', self.resolution_var.get()])
            
            # Add bitrate
            if self.bitrate_var.get():
                cmd.extend(['--bit-rate', f"{self.bitrate_var.get()}M"])
            
            # Add options
            if self.turn_screen_off.get():
                cmd.append('--turn-screen-off')
            
            if self.stay_awake.get():
                cmd.append('--stay-awake')
            
            subprocess.Popen(cmd)
            self.status_var.set("Scrcpy started successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start scrcpy: {str(e)}")
            self.status_var.set("Error starting Scrcpy")

def main():
    root = ThemedTk(theme="arc")  # Using the 'arc' theme for a modern look
    app = ScrcpyGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 