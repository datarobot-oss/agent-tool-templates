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
        data: Incoming JSON data containing "dataset_id" in the "payload" key
        kwargs: Additional keyword arguments.

    Returns:
        JSON response with search results
    """
    request = json.loads(data)

    # authorization_context for this tool is not neede because it only calls DataRobot API
    # Extract search parameters from payload
    payload = request.get("payload", {})

    # Call the tool
    df = tool.get_data_registry_dataset(**payload)
    csv = df.to_csv(index=False)

    return csv, {"mimetype": "text/csv", "charset": "utf-8"}


def test_score_unstructured():
    """Test function for the score_unstructured hook."""
    payload = {
        "dataset_id": "65f07dec42d762a299cdebc7",
    }

    auth_ctx = {"user": {"id": "12345", "name": "Test User"}, "conns": []}

    data = {"payload": payload, "authorization_context": auth_ctx}

    response_content, response_headers = score_unstructured("model", json.dumps(data))
    print("Response Content:", response_content)


if __name__ == "__main__":
    test_score_unstructured()
