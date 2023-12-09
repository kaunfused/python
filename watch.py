import time
import subprocess
import platform
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_executed = 0
        self.debounce = 1  # Adjust the debounce time as needed (in seconds)

    def on_modified(self, event):
        current_time = time.time()
        if current_time - self.last_executed > self.debounce and event.src_path.endswith("test.py"):
            print(f"Detected change in {event.src_path}")
            clear_terminal()
            subprocess.run(["python", event.src_path])
            self.last_executed = current_time

def clear_terminal():
    # Clear terminal based on platform (Windows/Linux/Mac)
    system_platform = platform.system()
    if system_platform == "Windows":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
