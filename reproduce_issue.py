import tkinter as tk
import time

print("Starting reproduction script...")
try:
    root = tk.Tk()
    print("Root created.")
    root.withdraw()
    print("Root withdrawn.")

    dialog = tk.Toplevel(root)
    print("Dialog created.")
    dialog.title("Test Dialog")
    tk.Label(dialog, text="If you see this, it works!").pack(padx=20, pady=20)
    
    # Mimic the ClientUI logic
    dialog.transient(root)
    print("Transient set.")
    dialog.grab_set()
    print("Grab set.")
    
    print("Waiting for window...")
    root.wait_window(dialog)
    print("Dialog closed.")
    
    root.destroy()
    print("Root destroyed.")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("Script finished.")
