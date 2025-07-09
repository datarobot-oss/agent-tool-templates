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
from abc import ABC, abstractmethod
from typing import BinaryIO, Tuple


class FileStorageBackend(ABC):
    """Abstract base class defining the interface for file storage operations."""

    @abstractmethod
    def retrieve_file(self, file_path: str) -> Tuple[BinaryIO, str]:
        """
        Retrieve a file from the storage backend.

        Args:
            file_path: The storage of the file to retrieve

        Returns:
            Tuple[BinaryIO, str]: A tuple containing the file-like object and the file name

        Raises:
            StorageError: If the file cannot be retrieved
            FileNotFoundError: If the file does not exist
        """
        pass


class StorageError(Exception):
    """Base exception for storage-related errors."""

    pass
