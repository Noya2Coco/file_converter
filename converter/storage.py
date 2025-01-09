import os
import time
from django.core.files.storage import FileSystemStorage

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        file_path = os.path.join(self.location, name)

        if self.exists(name):
            attempts = 3
            for attempt in range(attempts):
                try:
                    os.remove(file_path)
                    break
                except PermissionError:
                    time.sleep(1)
            else:
                raise PermissionError(f"Cannot remove locked file: {file_path}")
        return name
