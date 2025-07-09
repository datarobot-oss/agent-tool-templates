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
import logging
import re

import datarobot as dr
import pandas as pd
import plotly.graph_objects as go
import typing_extensions as te
from bson import ObjectId
from markupsafe import Markup

logger = logging.getLogger(__name__)


class PlotlyChart(Markup):
    """A class for handling Plotly charts with XML annotations.

    This class extends the Markup class to wrap Plotly charts in XML tags for proper
    rendering in the streaming output.
    """

    raw_plot: str

    def __new__(
        cls, in_obj: str = "", encoding: str | None = None, errors: str = "strict"
    ) -> te.Self:
        obj = f"""<plotly>{in_obj}</plotly>"""
        new_class = super().__new__(cls, obj, encoding, errors)
        new_class.raw_plot = in_obj
        return new_class


def find_placeholders(spec_str: str) -> list[str]:
    """Finds all placeholders in the spec string

    Placeholders are column names from a dataframe that are wrapped with double curly braces.
    """
    return re.findall(r"\{\{(.*?)\}\}", spec_str)


def get_dataframe_from_data_registry(dataset_id: str) -> pd.DataFrame:
    """Returns a pandas DataFrame from the Data Registry using the provided dataset ID."""
    return dr.Dataset.get(dataset_id).get_as_dataframe().dropna()


def validate_plotly_spec(plotly_spec: str) -> None:
    """Validates the Plotly specification by attempting to create a Plotly figure."""
    try:
        # Parse the JSON specification
        spec = json.loads(plotly_spec)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in Plotly specification: {str(e)}")

    try:
        # Attempt to create a Plotly figure to validate the spec
        go.Figure(spec)
    except Exception as e:
        raise ValueError(f"Invalid Plotly specification: {str(e)}")


def plotly_chart_rendering(plotly_spec: str, dataset_id: str, max_samples: int = 10000) -> str:
    """Returns a PlotlyChart object from the input Plotly specification.
    When you perform an analysis you can generate a Plotly chart by passing
    in the specification in JSON.

    Do not escape the plotly_spec string.

    You need to pass in a "dataset_id" to this function, which identifies an
    existing dataset within Data Registry. Then you can reference columns from the
    dataframe by wrapping them in double curly braces. For instance if you pass
    in the following specification:

    ```
    plotly_spec='''
    {
        "data": [
            {
                "type": "scatter",
                "mode": "markers",
                "x": {{x}},
                "y": {{y}}
            }
        ],
        "layout": {
            "title": "Scatterplot with 5 Random Points",
            ...
        }
    }
    ''',
    dataset_id="683ee07e7e96db41ab02b263",
    ```

    The plot will automatically be rendered in the frontend. You do not need to write out the resulting plot yourself.

    Parameters
    ----------
    plotly_spec: str
        the Plotly JSON specification.
    dataset_id: str
        the dataset_id of the Data Registry dataset to use.
    max_samples: int
        the maximum number of samples to use. Default is 10000.

    Returns
    -------
    PlotlyChart
        A PlotlyChart object containing the rendered chart
    """
    if not ObjectId.is_valid(dataset_id):
        raise ValueError(
            "Parameter 'dataset_id' must be a valid ObjectId of an existing dataset in the Data Registry."
        )

    logger.debug(f"Retrieving dataset {dataset_id} from Data Registry")

    # Retrieve the dataset from Data Registry for visualization
    try:
        df = get_dataframe_from_data_registry(dataset_id)
        if max_samples and len(df) > max_samples:
            df = df.sample(max_samples, random_state=42)
            logger.debug(f"Sampled dataset to {max_samples} rows")
    except Exception as e:
        logger.exception(f"Failed to retrieve dataset: {str(e)}")
        raise ValueError(f"Failed to retrieve dataset {dataset_id}: {str(e)}")

    # Process placeholders
    placeholders = find_placeholders(plotly_spec)
    if not placeholders:
        raise ValueError("No {{placeholders}} found in the Plotly specification")

    # Validate all placeholders exist in dataframe
    missing_columns = [p for p in placeholders if p not in df.columns]
    if missing_columns:
        raise ValueError(f"Columns not found in dataset: {', '.join(missing_columns)}")

    # Replace placeholders with data
    processed_spec = plotly_spec
    for placeholder in placeholders:
        placeholder_data = json.dumps(df[placeholder].to_list())
        processed_spec = processed_spec.replace("{{" + placeholder + "}}", placeholder_data)

    # Ensure the processed spec is valid JSON and can be rendered by Plotly
    validate_plotly_spec(processed_spec)

    return PlotlyChart(json.dumps(processed_spec))
