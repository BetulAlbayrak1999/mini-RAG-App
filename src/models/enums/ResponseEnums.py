from enum import Enum


class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_successfully"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    PROCESSING_FAILED = "process_failed"
    PROCESSING_SUCCESS = "process_success"
