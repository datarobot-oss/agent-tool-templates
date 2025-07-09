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
from io import StringIO
from typing import Union

import pandas as pd
import tool
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor

instrument_requests = RequestsInstrumentor().instrument()
instrument_botocore = BotocoreInstrumentor().instrument()


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
        JSON response with search results
    """
    request = json.loads(data)

    # authorization_context for this tool is not needed because it only calls DataRobot API
    payload = request.get("payload", {})

    # Extract & parse parameters from the payload
    file_path = payload.get("file_path")
    dataframe = None
    if payload.get("dataframe"):
        datafile = StringIO(payload["dataframe"])
        dataframe = pd.read_csv(datafile)
    file_name = payload.get("file_name")

    created_dataset_id = tool.upload_file_to_data_registry(
        file_path=file_path,
        dataframe=dataframe,
        file_name=file_name,
    )
    response = {"dataset_id": created_dataset_id}

    return json.dumps(response), {"mimetype": "application/json", "charset": "utf-8"}


def test_score_unstructured():
    """Test function for the score_unstructured hook."""
    # test with a dataframe
    df = pd.DataFrame({"Name": ["Alice", "Bob", "Cid"], "Age": [28, 22, 42]})
    payload = {
        "file_name": "tool_test_dataframe.csv",
        "dataframe": df.to_csv(index=False),
    }
    auth_ctx = {"user": {"id": "12345", "name": "Test User"}, "conns": []}
    data = {"payload": payload, "authorization_context": auth_ctx}
    response_content, response_headers = score_unstructured("model", json.dumps(data))
    print("Response Content:", response_content)

    # test with s3 storage and renaming the file
    payload = {
        "file_path": "tool_tests/datasets/ts_multi_head.csv",
        "file_name": "tool_test_s3_storage.csv",
    }
    auth_ctx = {"user": {"id": "12345", "name": "Test User"}, "conns": []}
    data = {"payload": payload, "authorization_context": auth_ctx}
    response_content, response_headers = score_unstructured("model", json.dumps(data))
    print("Response Content:", response_content)


if __name__ == "__main__":
    test_score_unstructured()
