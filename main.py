
import tkinter as tk
from tkinter import ttk
import threading
import time
import random

try:
    import pyautogui
except ImportError:
    print("pyautogui not installed. Please install it using: pip install pyautogui")
    pyautogui = None

class MouseMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Mover")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        self.is_moving = False
        self.move_thread = None
        
        self.setup_ui()
        
        # Disable pyautogui failsafe for smoother operation
        if pyautogui:
            pyautogui.FAILSAFE = False
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Mouse Mover", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Status: Stopped", font=("Arial", 10))
        self.status_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Start button
        self.start_button = ttk.Button(
            main_frame, 
            text="Start Moving", 
            command=self.start_moving,
            style="Green.TButton"
        )
        self.start_button.grid(row=2, column=0, padx=(0, 10), pady=5, sticky="ew")
        
        # Stop button
        self.stop_button = ttk.Button(
            main_frame, 
            text="Stop Moving", 
            command=self.stop_moving,
            state="disabled",
            style="Red.TButton"
        )
        self.stop_button.grid(row=2, column=1, padx=(10, 0), pady=5, sticky="ew")
        
        # Movement settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0), sticky="ew")
        
        # Movement interval
        ttk.Label(settings_frame, text="Interval (seconds):").grid(row=0, column=0, sticky="w")
        self.interval_var = tk.StringVar(value="2")
        interval_spinbox = ttk.Spinbox(
            settings_frame, 
            from_=1, 
            to=10, 
            textvariable=self.interval_var,
            width=10
        )
        interval_spinbox.grid(row=0, column=1, padx=(10, 0))
        
        # Movement range
        ttk.Label(settings_frame, text="Movement range:").grid(row=1, column=0, sticky="w", pady=(5, 0))
        self.range_var = tk.StringVar(value="50")
        range_spinbox = ttk.Spinbox(
            settings_frame, 
            from_=10, 
            to=200, 
            textvariable=self.range_var,
            width=10
        )
        range_spinbox.grid(row=1, column=1, padx=(10, 0), pady=(5, 0))
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        settings_frame.columnconfigure(1, weight=1)
        
        # Style configuration
        style = ttk.Style()
        style.configure("Green.TButton", foreground="green")
        style.configure("Red.TButton", foreground="red")
    
    def start_moving(self):
        if not pyautogui:
            self.status_label.config(text="Error: pyautogui not installed")
            return
        
        # Immediate UI feedback
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_label.config(text="Status: Starting...")
        self.root.update()  # Force immediate UI update
        
        self.is_moving = True
        
        # Start movement in a separate thread
        self.move_thread = threading.Thread(target=self.move_mouse_loop, daemon=True)
        self.move_thread.start()
        
        # Update status after thread starts
        self.root.after(100, lambda: self.status_label.config(text="Status: Moving cursor..."))
    
    def stop_moving(self):
        # Immediate UI feedback
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Status: Stopping...")
        self.root.update()  # Force immediate UI update
        
        self.is_moving = False
        
        # Restore UI after stopping
        self.root.after(200, lambda: (
            self.start_button.config(state="normal"),
            self.status_label.config(text="Status: Stopped")
        ))
    
    def move_mouse_loop(self):
        try:
            interval = float(self.interval_var.get())
            movement_range = int(self.range_var.get())
        except ValueError:
            interval = 2.0
            movement_range = 50
        
        while self.is_moving:
            try:
                # Get current mouse position
                current_x, current_y = pyautogui.position()
                
                # Generate random movement within range
                dx = random.randint(-movement_range, movement_range)
                dy = random.randint(-movement_range, movement_range)
                
                new_x = current_x + dx
                new_y = current_y + dy
                
                # Ensure new position is within screen bounds
                screen_width, screen_height = pyautogui.size()
                new_x = max(0, min(new_x, screen_width - 1))
                new_y = max(0, min(new_y, screen_height - 1))
                
                # Move mouse smoothly with shorter duration
                pyautogui.moveTo(new_x, new_y, duration=0.1)
                
                # Wait for the specified interval with responsive checking
                start_time = time.time()
                while time.time() - start_time < interval and self.is_moving:
                    time.sleep(0.1)  # Check every 100ms for stop signal
                
            except Exception as e:
                print(f"Error moving mouse: {e}")
                break
    
    def on_closing(self):
        self.stop_moving()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = MouseMoverApp(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
