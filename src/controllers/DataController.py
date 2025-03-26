from .BaseController import BaseController
from fastapi import UploadFile
from src.models import ResponseSignal
from .ProjectController import ProjectController
import re
import os


class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576  # convert MB to bytes

    # validate_uploaded_file
    def validate_uploaded_file(self, file: UploadFile):

        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True, ResponseSignal.FILE_UPLOAD_SUCCESS.value

    # generate_unique_filpath
    def generate_unique_filepath(self, original_filename: str, project_id: str):
        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)

        cleaned_filename = self.get_clean_filename(
            original_filename=original_filename,
        )

        new_file_path = os.path.join(
            project_path,
            random_key + "_" + cleaned_filename,
        )

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.koin(
                project_path,
                random_key + "_" + cleaned_filename,
            )

        return new_file_path, random_key + "_" + cleaned_filename

    # get_clean_filename
    def get_clean_filename(self, original_filename: str):

        # removeany special charachters, except underscore and .
        cleaned_filename = re.sub(r"[^\w.]", "", original_filename.strip())

        # replace spaces with underscore
        cleaned_filename = cleaned_filename.replace(" ", "_")

        return cleaned_filename
