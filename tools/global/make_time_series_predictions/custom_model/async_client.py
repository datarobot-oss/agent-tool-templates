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

import aiohttp
import datarobot as dr
from env import config

HEADERS = dr.Client(token=config.DATAROBOT_API_TOKEN, endpoint=config.DATAROBOT_ENDPOINT).headers


async def arequest(method, url, params=dict(), data=dict()):
    if url.startswith("http"):
        pass
    else:
        url = f"{config.DATAROBOT_ENDPOINT.rstrip('/')}/{url.lstrip('/')}"
    async with aiohttp.ClientSession() as session:
        async with session.request(
            method, url, headers=HEADERS, params=params, json=data
        ) as response:
            data = await response.json()
            return response, data


async def get_deployments():
    resp, data = await arequest("GET", "deployments/", params={"limit": 100})
    deployments = data["data"]
    while next_url := data.get("next"):
        resp, data = await arequest("GET", next_url)
        if resp.status == 200:
            deployments.extend(data["data"])
        else:
            raise Exception(f"Failed to get deployments: {resp.status}")
    return deployments


async def get_deployment_by_id(deployment_id):
    resp, data = await arequest("GET", f"deployments/{deployment_id}/")
    if resp.status == 200:
        return data
    else:
        raise Exception(f"Failed to get deployment: {resp.status}")


async def get_deployment_features(deployment_id):
    resp, data = await arequest("GET", f"deployments/{deployment_id}/features")
    if resp.status == 200:
        return data["data"]
    else:
        raise Exception(f"Failed to get deployment features: {resp.status}")
