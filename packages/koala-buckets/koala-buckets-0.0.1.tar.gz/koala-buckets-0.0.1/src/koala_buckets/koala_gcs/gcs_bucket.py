import logging

from io import BytesIO
from google.cloud import storage, exceptions
from google.oauth2 import service_account


class GCSBucket:

    def __init__(self, bucket_name: str, credentials: dict):
        self._bucket_name = bucket_name
        self._creds = self._create_credentials(credentials)
        self._client = storage.Client(self._creds.project_id, credentials=self._creds)
        self._bucket = self._client.get_bucket(self._bucket_name)
        self._logger = self._create_logger()

    def upload_from_file(self, source_file: str, target_file: str, target_folder: str = None) -> None:
        blob = self._create_blob(target_file, target_folder)

        self._logger.info(f"Uploading file {source_file} to {self._bucket_name}...")
        blob.upload_from_filename(filename=source_file)
        self._logger.info(f"Successfully uploaded file {source_file} from {self._bucket_name}.")

    def upload_from_buffer(self, source_buffer: BytesIO, target_file: str, target_folder: str = None) -> None:
        blob = self._create_blob(target_file, target_folder)

        self._logger.info(f"Uploading  buffer to {self._bucket_name}...")
        blob.upload_from_string(data=source_buffer.getvalue())
        self._logger.info(f"Successfully uploaded buffer to {self._bucket_name}.")

    def read_file(self, file: str, folder: str = None) -> bytes:
        blob = self._create_blob(file, folder)

        self._logger.info(f"Reading file {blob.name} from {self._bucket_name}...")
        try:
            data = blob.download_as_string()
        except exceptions.NotFound:
            self._logger.error(f"File {blob.name} NOT found in {self._bucket_name}!")
        else:
            self._logger.info(f"Successfully read file {blob.name} from {self._bucket_name}.")
            return data

    def list_content(self, prefix: str = None) -> list:
        blobs = [blob.name for blob in self._bucket.list_blobs(prefix=prefix)]
        return blobs

    def delete_file(self, target_file: str, target_folder: str = None) -> None:
        blob = self._create_blob(target_file, target_folder)

        self._logger.info(f"Deleting file {blob.name} from {self._bucket_name}...")
        try:
            blob.delete()
        except exceptions.NotFound:
            self._logger.error(f"File {blob.name} NOT found in {self._bucket_name}!")
        else:
            self._logger.info(f"Successfully deleted file {blob.name} from {self._bucket_name}.")

    def _create_blob(self, file: str, folder: str = None) -> storage.Blob:
        path = self._create_path(file, folder)
        return self._bucket.blob(path)

    def _create_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)

        logger.addHandler(handler)

        logger.info(f"Created instance of GCSBucket for '{self._bucket_name}' bucket.")

        return logger

    @staticmethod
    def _create_credentials(credentials: dict):
        creds = service_account.Credentials.from_service_account_info(credentials)

        return creds

    @staticmethod
    def _create_path(file: str, folder: str = None):
        if folder is not None:
            path = f"{folder}/{file}"
        else:
            path = f"{file}"

        return path

