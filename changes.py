import os
import json
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def get_file_metadata(path):

    metadata = {}
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            stat = os.stat(filepath)
            metadata[stat.st_ino] = {
                "File name": filename,
                "File size": stat.st_size,
                "path": filepath,
                "Date of creation": time.ctime(stat.st_ctime),
                "last modified": time.ctime(stat.st_mtime),
                "operation type": "present",
                "Inode number": stat.st_ino
            }
    return metadata


class Watcher:
    def __init__(self, directory):
        self.directory = directory
        self.event_handler = FileHandler()
        self.observer = Observer()
        self.last_save_time = None  # variable to track the time of the last JSON file saved

    def run(self):
        self.observer.schedule(self.event_handler, self.directory, recursive=True)
        self.observer.start()
        try:
            while True:
                current_time = time.localtime()
                if self.last_save_time is None or current_time.tm_min % 1 == 0 and self.last_save_time.tm_min != current_time.tm_min:
                    # check if 10 minutes have passed since last save or if it's the first save
                    self.save_to_json_file(current_time)
                    self.last_save_time = current_time  # update last_save_time
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def save_to_json_file(self, current_time):
        json_filename = time.strftime("%H_%M_changes.json", current_time)
        with open('C:\workspace\HPE\changes\\' + json_filename, "w") as f:
            json.dump(self.event_handler.file_data, f, indent=4)
        self.event_handler.file_data = {}  # reset file_data

class FileHandler(FileSystemEventHandler):
    def __init__(self):
        self.file_data = {}
        super().__init__()

    def on_created(self, event):
        if not event.is_directory:
            data = self.get_file_details(event.src_path, "creation")
            self.file_data[str(data["Inode number"])] = data

    def on_modified(self, event):
        if not event.is_directory:
            data = self.get_file_details(event.src_path, "modification")
            self.file_data[str(data["Inode number"])] = data

    def on_deleted(self, event):
        if not event.is_directory:
            data = self.get_file_details(event.src_path, "deletion")
            self.file_data[str(data["Inode number"])] = data

    def get_file_details(self, path, operation_type, inode_number=None):
        file_name = os.path.basename(path)
        if operation_type == "deletion":
            file_size = None
            path = None
            date_created = None
            last_modified = None
            inode_number = None
        else:
            file_size = os.stat(path).st_size
            date_created = time.ctime(os.path.getctime(path))
            last_modified = time.ctime(os.path.getmtime(path))
            inode_number = os.stat(path).st_ino
        data = {
            "File name": file_name,
            "File size": file_size,
            "path": path,
            "Date of creation": date_created,
            "last modified": last_modified,
            "operation type": operation_type,
            "Inode number": inode_number
        }
        return data

if __name__ == '__main__':

    path=r"C:\workspace\HPE\test"
    metadata = get_file_metadata(path)
    with open("C:\workspace\HPE\initial.json", "w") as f:
        json.dump(metadata, f, indent=4)

    w = Watcher(directory=path)
    w.run()
