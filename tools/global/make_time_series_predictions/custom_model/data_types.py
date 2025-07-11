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
from __future__ import annotations

import json
import logging

logger = logging.getLogger(__name__)


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
