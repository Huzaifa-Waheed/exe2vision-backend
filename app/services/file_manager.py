import os
import shutil
import uuid
from fastapi import UploadFile, HTTPException, status

UPLOAD_DIR = "uploaded_files"
ALLOWED_EXTENSIONS = {".exe"}


class FileManager:

    @staticmethod
    def save_file(file: UploadFile) -> str:
        ext = os.path.splitext(file.filename or "")[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type '{ext}'. Only .exe files are accepted."
            )

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Verify PE magic bytes
        with open(file_path, "rb") as f:
            magic = f.read(2)
        if magic != b"MZ":
            os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is not a valid PE executable."
            )

        return file_path
