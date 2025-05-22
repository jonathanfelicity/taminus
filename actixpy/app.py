# actixpy/app.py
import actixpy_core
import time # For a small delay to see server messages

class App:
    def __init__(self):
        # In the future, this might initialize Rust-side application state
        print("Initializing ActixPy App...")

    def run(self, host: str = "127.0.0.1", port: int = 8080):
        print(f"Attempting to start server on {host}:{port}")
        try:
            actixpy_core.start_server(host, port)
            # The Rust server starts in a background thread.
            # The Python process would normally exit here if this is the main script.
            # For testing, we can keep it alive for a bit.
            # In a real app, other Python logic or an event loop might keep it alive.
            print(f"Server should be running in the background on http://{host}:{port}")
            print("Python main thread will sleep for a few seconds to allow server to run...")
            print("Try accessing the server URL in your browser or with curl.")
            print("Press Ctrl+C to stop the main Python script (this may not stop the Rust server thread gracefully yet).")
            
            # Keep the main thread alive to observe the server.
            # In a real scenario, this might be an asyncio event loop or similar.
            while True:
                time.sleep(1)

        except ImportError as e:
            print(f"Error importing actixpy_core: {e}")
        except Exception as e:
            print(f"Error starting server: {e}")

if __name__ == "__main__":
    app = App()
    app.run(host="127.0.0.1", port=8000) # Using port 8000 for this example
