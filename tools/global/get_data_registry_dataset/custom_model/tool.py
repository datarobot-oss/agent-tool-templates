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
from typing import Optional

import datarobot as dr
import pandas as pd


def get_data_registry_dataset(
    dataset_id: str, offset: int = 0, limit: Optional[int] = None
) -> pd.DataFrame:
    """Fetches a dataset from the DataRobot Data Registry.

    To paginate results, use the `limit` and `offset` parameters.
    These allow you to retrieve a specific range of rows from the
    dataset or process the dataset in manageable chunks.

    Parameters
    ----------
    dataset_id : str
        the unique dataset id of the dataset from datarobot.
    offset : int, optional
        the number of rows to skip, by default 0.
    limit: int, optional
        the maximum number of rows to return, by default None (returns all rows).

    Returns
    -------
    pd.DataFrame
        the dataset as pandas dataframe

    Source
    ______
    datarobot
    """
    dataset = dr.Dataset.get(dataset_id)
    df = dataset.get_as_dataframe()
    if limit is not None:
        df = df[offset : offset + limit]
    return df
