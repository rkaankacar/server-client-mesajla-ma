
import sys
import traceback

print("Debug script started...")

try:
    print("Attempting to import ui.client_ui...")
    from ui.client_ui import ClientUI
    print("Import successful.")

    print("Attempting to initialize ClientUI...")
    app = ClientUI()
    print("Initialization successful.")
    
    print("Attempting to run app...")
    # We won't actually run mainloop() to block, just check if we got here.
    # app.run() 
    print("App is ready to run (test passed).")

except ImportError as e:
    print("\n!!! IMPORT ERROR !!!")
    print(f"Missing module: {e.name}")
    print(f"Full error: {e}")
    traceback.print_exc()
    
    if "Crypto" in str(e):
        print("\nSUGGESTION: You need to install pycryptodome.")
        print("Run: pip install -r requirements.txt")

except Exception as e:
    print("\n!!! RUNTIME ERROR !!!")
    print(f"Error: {e}")
    traceback.print_exc()

input("\nPress Enter to exit...")
