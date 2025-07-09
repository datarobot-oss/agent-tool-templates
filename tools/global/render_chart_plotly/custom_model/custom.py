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


def test_score_unstructured():
    """Test function for the score_unstructured hook with Plotly."""
    payload = {
        "plotly_spec": """
            {
                "data": [
                    {
                        "type": "scatter",
                        "mode": "markers",
                        "x": {{sepal length (cm)}},
                        "y": {{sepal width (cm)}},
                        "marker": {
                            "color": {{SpeciesNumeric}},
                            "size": 8,
                            "colorscale": "Viridis",
                            "showscale": false
                        },
                        "text": {{Species}}
                    }
                ],
                "layout": {
                    "title": "Scatter Plot for IRIS Dataset",
                    "xaxis": {"title": "Sepal Length (cm)"},
                    "yaxis": {"title": "Sepal Width (cm)"},
                    "width": 600,
                    "height": 400,
                    "hovermode": "closest"
                }
            }
        """,
        "dataset_id": "683ee07e7e96db41ab02b263",
    }

    auth_ctx = {"user": {"id": "12345", "name": "Test User"}, "conns": []}

    data = {"payload": payload, "authorization_context": auth_ctx}

    # Simulate the scoring function
    response_content, response_headers = score_unstructured("model", json.dumps(data))
    print("Response Content:", response_content)
    print("Response Headers:", response_headers)


if __name__ == "__main__":
    test_score_unstructured()
