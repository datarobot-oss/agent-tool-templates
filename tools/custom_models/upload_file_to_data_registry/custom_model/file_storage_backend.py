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
import json
import logging
from env import getenv
from file_storage_backend_generic import FileStorageBackend
from file_storage_backend_s3 import S3FileStorageBackend

logger = logging.getLogger(__name__)


def get_file_storage_backend() -> FileStorageBackend:
    backend_type = getenv("FILE_STORAGE_BACKEND")
    if backend_type == "s3":
        bucket_name = getenv("S3_BUCKET_NAME")
        if not bucket_name:
            raise ValueError("S3_BUCKET_NAME is not set")

        s3_credentials = getenv("S3_CREDENTIALS")
        # When using s3 credential type, we can expect the following format:
        # {
        #     "type": "credential",
        #     "payload": {
        #         "credentialType": "s3",
        #         "awsAccessKeyId": "test key id",
        #         "awsSecretAccessKey": "test secret key",
        #         "awsSessionToken": "test session token"
        #     }
        # }

        s3_credentials_payload = {}
        if s3_credentials:
            if isinstance(s3_credentials, dict):
                s3_credentials_payload = s3_credentials.get("payload", {})
            elif isinstance(s3_credentials, str):
                try:
                    s3_credentials_payload = json.loads(s3_credentials).get("payload", {})
                except json.JSONDecodeError:
                    logger.error("Failed to parse S3 credentials JSON")
                    raise ValueError("Invalid S3 credentials format")

        credentials = {
            "aws_access_key_id": s3_credentials_payload.get("awsAccessKeyId"),
            "aws_secret_access_key": s3_credentials_payload.get("awsSecretAccessKey"),
            "aws_session_token": s3_credentials_payload.get("awsSessionToken"),
        }
        logger.debug(f"Using S3 file storage backend with bucket: {bucket_name}")
        return S3FileStorageBackend(bucket_name, credentials)

    raise ValueError(f"Unsupported file storage backend: {backend_type}")
