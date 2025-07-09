# Copyright 2025 DataRobot, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import boto3
from botocore.exceptions import ClientError
from typing import BinaryIO, Tuple
from io import BytesIO

from file_storage_backend_generic import FileStorageBackend, StorageError

logger = logging.getLogger(__name__)


class S3FileStorageBackend(FileStorageBackend):
    """Implementation of FileStorageBackend for AWS S3 storage."""

    def __init__(self, bucket_name: str, credentials: dict = None):
        """
        Initialize the S3 file storage backend.

        Args:
            bucket_name: Name of the S3 bucket to use
        """
        self.bucket_name = bucket_name
        self.s3_client = boto3.client("s3")
        if credentials:
            self.s3_client = boto3.client("s3", **credentials)
        else:
            self.s3_client = boto3.client("s3")

        # Verify bucket exists and is accessible
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            raise StorageError(f"Unable to access S3 bucket {bucket_name}: {str(e)}")


    def retrieve_file(self, file_path: str) -> Tuple[BinaryIO, str]:
        """Retrieve a file from S3."""
        try:
            # Download the file into a BytesIO object
            file_content = BytesIO()
            self.s3_client.download_fileobj(self.bucket_name, file_path, file_content)
            file_content.seek(0)

            file_name = extract_file_name(file_path)

            return file_content, file_name

        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                raise FileNotFoundError(f"File not found: {file_path}")
            raise StorageError(f"Failed to retrieve file from S3: {str(e)}") from e
        except Exception as e:
            raise StorageError(f"Failed to retrieve file from S3: {str(e)}") from e


def extract_file_name(input_str: str) -> str:
    """Extract file name from a bucket file path or return string as is if not a URL"""
    return input_str.split("/")[-1] if "/" in input_str else input_str
