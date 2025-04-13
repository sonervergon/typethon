import os
import shutil
import uuid
from pathlib import Path
from typing import BinaryIO, List, Optional

from fastapi import UploadFile

from core.config import BASE_DIR, UPLOAD_DIR


class FileStorage:
    def __init__(self):
        self.upload_dir = Path(BASE_DIR) / UPLOAD_DIR
        # Ensure upload directory exists
        os.makedirs(self.upload_dir, exist_ok=True)

    def save_file(self, file: UploadFile, subdir: Optional[str] = None) -> str:
        """
        Save an uploaded file to the filesystem
        Returns the relative path to the saved file
        """
        # Generate a unique filename
        file_extension = self._get_extension(file.filename)
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        # Determine the target directory
        target_dir = self.upload_dir
        if subdir:
            target_dir = target_dir / subdir
            os.makedirs(target_dir, exist_ok=True)

        # Define the full path to the file
        file_path = target_dir / unique_filename

        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Return the relative path from the upload directory
        if subdir:
            return f"{subdir}/{unique_filename}"
        return unique_filename

    def save_binary(
        self, content: BinaryIO, filename: str, subdir: Optional[str] = None
    ) -> str:
        """
        Save binary content to the filesystem
        Returns the relative path to the saved file
        """
        # Determine the target directory
        target_dir = self.upload_dir
        if subdir:
            target_dir = target_dir / subdir
            os.makedirs(target_dir, exist_ok=True)

        # Define the full path to the file
        file_path = target_dir / filename

        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(content, buffer)

        # Return the relative path from the upload directory
        if subdir:
            return f"{subdir}/{filename}"
        return filename

    def get_file_path(self, file_path: str) -> Path:
        """Get full path to a file"""
        result: Path = self.upload_dir / file_path
        return result

    def delete_file(self, file_path: str) -> bool:
        """Delete a file by path"""
        full_path = self.get_file_path(file_path)
        if full_path.exists():
            full_path.unlink()
            return True
        return False

    def list_files(self, subdir: Optional[str] = None) -> List[str]:
        """List files in a directory"""
        target_dir = self.upload_dir
        if subdir:
            target_dir = target_dir / subdir

        if not target_dir.exists():
            return []

        return [f.name for f in target_dir.iterdir() if f.is_file()]

    def file_exists(self, file_path: str) -> bool:
        """Check if a file exists"""
        return self.get_file_path(file_path).exists()

    def _get_extension(self, filename: Optional[str]) -> str:
        """Extract file extension including the dot"""
        if not filename:
            return ""
        return os.path.splitext(filename)[1]


# Singleton instance
_file_storage = None


def get_file_storage() -> FileStorage:
    """Dependency to get FileStorage instance"""
    global _file_storage
    if _file_storage is None:
        _file_storage = FileStorage()
    return _file_storage
