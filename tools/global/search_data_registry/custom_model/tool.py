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
from functools import lru_cache
from typing import Dict
from typing import List

import datarobot as dr


@lru_cache(maxsize=1000)
def search_data_registry_datasets(search_terms: str = "", limit: int = 20) -> List[Dict[str, str]]:
    """Lists datasets from the DataRobot Data Registry matching the search terms.

    NOTE: DataRobot does not do fuzzy matching so if you do not get the exact results you expect, try a more specific search term.

    Parameters
    ----------
    search_terms : str
        Terms for the search. Leave blank to return all datasets.

    limit : int
        the maximum number of datasets to return. Set to -1 to return all.

    Returns
    -------
    list[dict[str, str]]
        an array of objects with name and dataset_id

    Source
    ______
    datarobot
    """
    client = dr.client.Client()
    params = dict([("searchFor", search_terms)])
    dataset_resp = client.get("catalogItems/", params=params).json()
    datasets = [
        {"dataset_id": r["id"], "dataset_name": r["catalogName"]} for r in dataset_resp["data"]
    ]

    try:
        limit = int(limit)
    except ValueError:
        limit = 20

    if not limit or limit == -1:
        return datasets
    else:
        return datasets[:limit]
