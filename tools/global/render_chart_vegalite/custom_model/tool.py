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
import base64
import copy
import json
import logging
from tempfile import NamedTemporaryFile
from typing import Any

import altair as alt
import datarobot as dr
import pandas as pd
import typing_extensions as te
from bson import ObjectId
from markupsafe import Markup
from vega_datasets import data  # noqa: F401

logger = logging.getLogger(__name__)


class ImageB64(Markup):
    """A class for handling base64-encoded images with XML annotations.

    This class extends the Markup class to wrap base64-encoded image data in XML tags
    and provides access to the raw base64 string.

    Parameters
    ----------
    in_obj : str, optional
        The base64-encoded image string to be wrapped, by default ""
    encoding : str or None, optional
        The encoding to use for the text, by default None
    errors : str, optional
        How to handle encoding errors, by default "strict"

    Returns
    -------
    ImageB64
        A new instance of the ImageB64 class with the content wrapped in XML tags

    Attributes
    ----------
    raw_b64 : str
        The raw base64-encoded string without XML tags

    Examples
    --------
    >>> img = ImageB64("base64_encoded_string")
    >>> print(img)
    <imageb64>base64_encoded_string</imageb64>
    >>> print(img.raw_b64)
    base64_encoded_string
    """

    raw_b64: str

    def __new__(
        cls, in_obj: str = "", encoding: str | None = None, errors: str = "strict"
    ) -> te.Self:
        obj = f"""<imageb64>{in_obj}</imageb64>"""
        new_class = super().__new__(cls, obj, encoding, errors)
        new_class.raw_b64 = in_obj
        return new_class


def extract_and_sanitize_json(text: str) -> dict:
    """Extract and sanitize JSON from text that may contain additional content.

    This function attempts to find and parse valid JSON within the input text. If the text
    contains multiple JSON objects, it will attempt to parse each one. If no valid JSON is
    found, it wraps the original text in a dictionary.

    Parameters
    ----------
    text : str
        String that may contain JSON along with other text

    Returns
    -------
    dict
        Parsed JSON object if found and valid, or original text wrapped in a dictionary
        with key 'response'

    Notes
    -----
    The function employs multiple strategies to extract JSON:
    1. Direct parsing of the entire text
    2. Finding and parsing JSON-like substrings enclosed in curly braces
    3. Falling back to wrapping the text in a response dictionary if no valid JSON is found
    """
    # Let's assume the text is already a valid JSON object
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    def find_json_objects(s):
        """Helper function to find potential JSON objects"""
        objects = []
        count = 0
        start = None

        for i, char in enumerate(s):
            if char == "{":
                if count == 0:
                    start = i
                count += 1
            elif char == "}":
                count -= 1
                if count == 0 and start is not None:
                    objects.append(s[start : i + 1])
                    start = None

        return objects

    # Find all potential JSON objects
    json_candidates = find_json_objects(text)

    try:
        # Try to parse each candidate
        for candidate in json_candidates:
            try:
                # Attempt to parse the candidate as JSON
                parsed_json = json.loads(candidate)
                return parsed_json
            except json.JSONDecodeError:
                # If parsing fails, continue to the next candidate
                continue

        # If no valid JSON found in candidates, try to parse the entire text
        return json.loads(text)

    except json.JSONDecodeError:
        # If all attempts fail, return the original text wrapped in a dictionary
        logger.error("No valid JSON found in the text.")
        return {"response": text}


def correct_specification_for_data(spec, dataframe) -> dict:
    """
    Updates the Vega-Lite specification to replace the 'data' field with a named dataset
    if it contains a valid ObjectId, and corrects field capitalization.

    Args:
        spec (dict): The Vega-Lite specification.
        dataframe (pandas.DataFrame): The dataframe containing the data.

    Returns:
        dict: The updated Vega-Lite specification.
    """
    data_field = spec.get("data", "")

    # Replace 'data' field with a named dataset if it contains a valid ObjectId
    if isinstance(data_field, str) and ObjectId.is_valid(data_field):
        spec["data"] = {"name": data_field}

    return correct_field_capitalization(spec, dataframe)


def correct_field_capitalization(spec, dataframe):
    """
    This function checks the field names in the JSON chart specification against
    the column names in the dataframe. If there is a mismatch in capitalization,
    it corrects the field names in the JSON specification.

    Args:
        spec (dict): The JSON chart specification.
        dataframe (pandas.DataFrame): The dataframe containing the data.

    Returns:
        dict: The corrected JSON chart specification.
    """

    # Create a copy of the original specification to avoid modifying the original
    corrected_spec = copy.deepcopy(spec)

    # Get a list of column names in the dataframe
    column_names = dataframe.columns.tolist()

    # Check the encoding field
    if "encoding" in corrected_spec:
        encoding = corrected_spec["encoding"]
        for field, field_spec in encoding.items():
            field_name = field_spec.get("field", "")
            if field_name:
                # Check if the field name matches any column name (case-insensitive)
                matched_column = next(
                    (col for col in column_names if col.lower() == field_name.lower()),
                    None,
                )
                if matched_column:
                    # Update the field name in the specification if capitalization differs
                    if matched_column != field_name:
                        encoding[field]["field"] = matched_column

    return corrected_spec


def get_dataframe_from_data_registry(dataset_id: str) -> pd.DataFrame:
    """Returns a pandas DataFrame from the Data Registry using the provided dataset ID."""
    return dr.Dataset.get(dataset_id).get_as_dataframe()


def vegalite_chart_rendering(vegalite_spec: str) -> str:
    """Returns base64-encoded image of a chart from the input vega-lite specification.

    When you perform an analysis you can generate a vega-lite chart just by passing in
    the specification in JSON. If needed you can pass in the Data Registry "dataset_id"
    as the dataset, and the model will retrieve the data.

    For instance if you pass in the following specification:

    ```
    {
      "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
      "description": "A simple pie chart with labels",
      "data": "661e933c42e38247bda23b8b",
      "mark": {"type": "dots"},
      "encoding": {
        "x": {"field": "A"},
        "y": {"field": "B"}
      },
      "view": {"stroke": null},
      "width": 200,
      "height": 200
    }
    ```

    I will recognize the ObjectId and replace it with the dataset from Data Registry as needed.

    Parameters
    ----------
    vegalite_spec: str
        the vega-lite JSON specification

    Returns
    -------
    str
        the base64 encoded image of the chart
    """

    def get_dataset_object_id(obj: Any):
        """Checks if the given object is a valid MongoDB ObjectId."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if ObjectId.is_valid(v):
                    return v
            else:
                return None
        if isinstance(obj, str):
            if ObjectId.is_valid(obj):
                return obj
            else:
                return None
        return None

    spec = extract_and_sanitize_json(vegalite_spec)

    dataset_id = get_dataset_object_id(spec.get("data", ""))
    if dataset_id is None:
        raise ValueError(
            "The 'data' field in the Vega-Lite specification must contain a valid dataset_id. "
            "Provide either a string representing the ObjectId of the dataset from the Data Registry, "
            "or a dictionary with a named dataset where the value is a valid ObjectId."
        )

    df = get_dataframe_from_data_registry(dataset_id)
    spec = correct_specification_for_data(spec, df)

    # Validate the specification and assign the data
    chart = alt.Chart.from_dict(spec)
    chart.data = df

    with NamedTemporaryFile("+ab", suffix=".png") as ntf:
        chart.save(ntf.name)
        ntf.seek(0)
        chart_b64 = base64.b64encode(ntf.read()).decode()

    return ImageB64(chart_b64)
