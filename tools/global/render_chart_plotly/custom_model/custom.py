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
from typing import Union

import tool
from opentelemetry.instrumentation.requests import RequestsInstrumentor

instrument_requests = RequestsInstrumentor().instrument()


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
        data: Incoming JSON data containing tool parameters
        kwargs: Additional keyword arguments.

    Returns:
         JSON response with rendered PlotlyChart object as a result.
    """
    request = json.loads(data)
    # authorization_context for this tool is not needed because it only calls DataRobot API
    # Extract search parameters from payload
    payload = request.get("payload", {})

    result = tool.plotly_chart_rendering(**payload)
    response = {"result": result}

    return json.dumps(response), {"mimetype": "application/json", "charset": "utf-8"}
