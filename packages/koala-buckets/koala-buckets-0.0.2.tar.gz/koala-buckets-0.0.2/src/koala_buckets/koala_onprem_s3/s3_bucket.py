import requests
import logging

from io import BytesIO


class S3Bucket:

    def __init__(self, url: str, bucket_name: str, access_key: str, secret_key: str):
        self._url = url
        self._bucket_name = bucket_name
        self._access_key = access_key
        self._secret_key = secret_key
        self._logger = self._create_logger()

    @property
    def bucket_name(self):
        return self._bucket_name

    def read_file(self, folder: str, file: str) -> bytes:
        url = self._get_url(bucket_name=self.bucket_name, folder=folder, file=file)
        headers = self._get_headers()

        self._logger.info(f"Reading {folder}/{file} from {self.bucket_name}...")
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            self._logger.info(f"Failed to read '{folder}/{file}' from '{self.bucket_name}'.")
            raise error
        else:
            self._logger.info(f"Successfully read '{folder}/{file}' from '{self.bucket_name}'.")
            return response.content

    def upload_buffer(self, source_buffer: BytesIO, target_folder: str, target_file: str) -> None:
        url = self._get_url(bucket_name=self.bucket_name, folder=target_folder, file=target_file)
        headers = self._get_headers()

        self._logger.info(f"Uploading  to '{target_folder}/{target_file}' to '{self.bucket_name}'...")
        try:
            response = requests.put(url=url, data=source_buffer, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            self._logger.info(f"Failed to upload  to  '{self.bucket_name}'.")
            raise error
        else:
            self._logger.info(f"Successfully uploaded   to '{self.bucket_name}'.")

    def upload_file(self, source_file: str, target_folder: str, target_file: str) -> None:
        url = self._get_url(bucket_name=self.bucket_name, folder=target_folder, file=target_file)
        headers = self._get_headers()

        self._logger.info(f"Uploading '{source_file}' to '{target_folder}/{target_file}' to '{self.bucket_name}'...")
        try:
            with open(source_file, "rb") as file:
                content_as_bytes = file.read()
        except FileNotFoundError as file_not_found_error:
            self._logger.info(f"Could not find file '{source_file}'.")
            raise file_not_found_error

        try:
            response = requests.put(url=url, data=content_as_bytes, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as request_error:
            self._logger.info(f"Failed to upload  '{source_file}' to  '{self.bucket_name}'.")
            raise request_error
        else:
            self._logger.info(f"Successfully uploaded  '{source_file}' to '{self.bucket_name}'.")

    def _get_headers(self) -> dict:
        return {'S3-ACCESS-KEY': self._access_key,
                'S3-SECRET-KEY': self._secret_key}

    def _create_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)

        logger.addHandler(handler)

        logger.info(f"Created instance of S3Bucket for '{self.bucket_name}' bucket.")

        return logger

    def _get_url(self, bucket_name: str, folder: str, file: str) -> str:
        return f"{self._url}/{bucket_name}/{folder}/{file}"
