from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import shutil
import time

# Use current directory as the vault path
VAULT_PATH = Path(__file__).parent.resolve()
INBOX = VAULT_PATH / "Inbox"
NEEDS_ACTION = VAULT_PATH / "Needs_Action"

def ensure_directories():
    """Ensure required directories exist."""
    for directory in [INBOX, NEEDS_ACTION]:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"Ensured directory exists: {directory}")

def get_unique_filename(destination_dir, filename):
    """Generate a unique filename to avoid overwrites."""
    destination = destination_dir / filename
    if not destination.exists():
        return destination
    
    # Split filename and extension
    stem = destination.stem
    suffix = destination.suffix
    counter = 1
    
    while True:
        new_filename = f"{stem}_{counter}{suffix}"
        new_destination = destination_dir / new_filename
        if not new_destination.exists():
            return new_destination
        counter += 1

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        try:
            source = Path(event.src_path)
            if not source.exists():
                print(f"Source file no longer exists: {source}")
                return
                
            dest = get_unique_filename(NEEDS_ACTION, source.name)
            shutil.copy2(source, dest)
            print(f"Moved {source.name} to Needs_Action as {dest.name}")
        except Exception as e:
            print(f"Error processing file {event.src_path}: {e}")

# Ensure directories exist before starting the observer
ensure_directories()

observer = Observer()
observer.schedule(Handler(), str(INBOX), recursive=False)
observer.start()

print("Watcher running...")

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    observer.stop()

observer.join()

observer = Observer()
observer.schedule(Handler(), str(INBOX), recursive=False)
observer.start()

print("Watcher running...")

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    observer.stop()

observer.join()