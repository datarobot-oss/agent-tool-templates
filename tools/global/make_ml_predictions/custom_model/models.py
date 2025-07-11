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

from env import config
from openai import AsyncAzureOpenAI
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)


def get_utility_client():
    if not config.OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY is not set. Utility client will not be created.")
        return None

    client_class = AsyncOpenAI
    if config.OPENAI_API_VERSION:
        client_class = AsyncAzureOpenAI

    kwargs = {"api_key": config.OPENAI_API_KEY}
    if config.OPENAI_API_VERSION:
        kwargs["api_version"] = config.OPENAI_API_VERSION

    if config.OPENAI_ENDPOINT:
        kwarg_name = "azure_endpoint" if client_class == AsyncAzureOpenAI else "base_url"
        kwargs[kwarg_name] = config.OPENAI_ENDPOINT

    return client_class(**kwargs)
