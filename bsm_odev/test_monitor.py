import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

# Log dizini ve dosyası
LOG_DIR = "/home/ubuntu/bsm/logs"
LOG_FILE = os.path.join(LOG_DIR, "changes.json")
MONITORED_DIR = "/home/ubuntu/bsm/test"

# Değişiklikleri takip eden event handler
class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        self.log_change(event, "modified")

    def on_created(self, event):
        self.log_change(event, "created")

    def on_deleted(self, event):
        self.log_change(event, "deleted")

    def log_change(self, event, event_type):
        if not event.is_directory:  # Sadece dosya değişikliklerini logla
            data = {
                "event": event_type,
                "file_path": event.src_path,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            self.write_log(data)

    def write_log(self, data):
        # JSON formatında log dosyasına yaz
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'w') as f:
                json.dump([], f)  # Boş bir liste başlat
        with open(LOG_FILE, 'r+') as f:
            logs = json.load(f)
            logs.append(data)
            f.seek(0)
            json.dump(logs, f, indent=4)

if __name__ == "__main__":
    print(f"Monitoring changes in {MONITORED_DIR}...")
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, MONITORED_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
