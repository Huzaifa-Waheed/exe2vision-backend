import os
import shutil
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "uploaded_files"

class FileManager:

    @staticmethod
    def save_file(file: UploadFile) -> str:
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return file_path
