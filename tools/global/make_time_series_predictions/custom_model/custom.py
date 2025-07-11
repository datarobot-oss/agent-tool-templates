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
import datetime
import json
from io import StringIO
from typing import Union

import pandas as pd
import tool
from datarobot.models.model_registry.registered_model import RegisteredModelVersion
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.instrumentation.openai import OpenAIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

instrument_requests = RequestsInstrumentor().instrument()
instrument_aiohttp = AioHttpClientInstrumentor().instrument()
instrument_openai = OpenAIInstrumentor().instrument()


def load_model(input_dir: str):
    """This is called when the model is loaded by DataRobot.
    Custom model hook for loading our the model or artifacts for use by scoring code.
    """
    _ = input_dir
    return "model"


def score_unstructured(model, data: Union[bytes, str], **kwargs):
    """
    This is the main scoring hook invoked by DataRobot during scoring of the unstructured model.

    Args:
        model: Loaded model from load_model() hook.
        data: Incoming JSON data containing tool input parameters
        kwargs: Additional keyword arguments.

    Returns:
        predictions in CSV format, along with headers indicating the content type.
    """
    request = json.loads(data)

    # authorization_context for this tool is not needed because it only calls DataRobot API
    payload = request.get("payload", {})

    # Extract & parse parameters from the payload
    deployment_id = payload["deployment_id"]
    forecast_point = datetime.datetime.strptime(payload["forecast_point"], "%Y-%m-%d %H:%M:%S")
    columns_to_return_with_predictions = payload["columns_to_return_with_predictions"]
    input_data_json_str = payload.get("input_data_json_str")

    input_dataframe = None
    if payload.get("input_dataframe"):
        datafile = StringIO(payload["input_dataframe"])
        input_dataframe = pd.read_csv(datafile)

    leaderboard_model_id = payload["registered_model_version_leaderboard_model_id"]
    rmv = RegisteredModelVersion.create_for_leaderboard_item(model_id=leaderboard_model_id)

    # Call the tool
    csv = tool.make_datarobot_ts_predictions(
        deployment_id=deployment_id,
        forecast_point=forecast_point,
        columns_to_return_with_predictions=columns_to_return_with_predictions,
        input_data_json_str=input_data_json_str,
        input_dataframe=input_dataframe,
        rmv=rmv,
    )

    return csv, {"mimetype": "text/csv", "charset": "utf-8"}
