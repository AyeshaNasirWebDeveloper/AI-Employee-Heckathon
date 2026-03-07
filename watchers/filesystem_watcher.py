from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import shutil
import time
from datetime import datetime

VAULT_PATH = Path(__file__).parent.resolve()
INBOX = VAULT_PATH / "Inbox"
NEEDS_ACTION = VAULT_PATH / "Needs_Action"

def ensure_directories():
    for directory in [INBOX, NEEDS_ACTION]:
        directory.mkdir(parents=True, exist_ok=True)

def get_unique_filename(destination_dir, filename):
    destination = destination_dir / filename
    if not destination.exists():
        return destination

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
                return

            timestamp = datetime.now().strftime("%H:%M:%S")

            print("\n==============================")
            print(f"[{timestamp}] 📥 New File Detected!")
            print(f"File Name: {source.name}")
            print(f"Location: Inbox")

            dest = get_unique_filename(NEEDS_ACTION, source.name)

            print("➡️  Processing...")
            time.sleep(1)

            shutil.copy2(source, dest)

            print(f"✅ Status: Moved to Needs_Action")
            print(f"New Location: {dest}")
            print("==============================\n")

        except Exception as e:
            print(f"❌ Error: {e}")

ensure_directories()

observer = Observer()
observer.schedule(Handler(), str(INBOX), recursive=False)
observer.start()

print("🤖 AI Employee Watcher Running...")
print("Monitoring Inbox folder...\n")

try:
    while True:
        time.sleep(2)
except KeyboardInterrupt:
    observer.stop()

observer.join()