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
from __future__ import annotations

from logging import getLogger
from typing import Optional

import datarobot as dr
import pandas as pd
from file_storage_backend import get_file_storage_backend

logger = getLogger(__name__)


def upload_file_to_data_registry(
    file_path: Optional[str] = None,
    dataframe: Optional[pd.DataFrame] = None,
    file_name: Optional[str] = None,
) -> str:
    """Uploads a file to the Data Registry.

    You must provide either a file path or a dataframe.

    Parameters
    ----------
    file_path : str
        the path of the file (e.g., csv, xlsx, zip, etc.) in the file storage to upload
    dataframe : pd.DataFrame
        a pandas dataframe to upload
    file_name : str
        name of the target file to create in the Data Registry

    Returns
    -------
    str
        dataset ID of the uploaded file in the Data Registry
    """
    if not file_path and dataframe is None:
        raise ValueError("You must provide either a dataframe or an file_path")

    file_data = None
    if file_path:
        logger.info("Retrieving file from storage backend")
        backend = get_file_storage_backend()
        file_data, original_file_name = backend.retrieve_file(file_path)
        try:
            if file_name:
                file_data.name = file_name
            else:
                file_data.name = original_file_name
        except:
            pass

    if file_data:
        logger.info("Creating dataset from loaded file data")
        dataset = dr.Dataset.create_from_file(filelike=file_data)
        return dataset.id
    elif dataframe is not None:
        logger.info("Creating dataset from provided dataframe")
        dataset = dr.Dataset.create_from_in_memory_data(
            data_frame=dataframe, fname=file_name
        )
        return dataset.id
    else:
        raise ValueError("Couldn't load file or dataframe")
