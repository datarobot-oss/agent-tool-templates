# Render Plotly Chart Tool

This tool is designed to generate Plotly charts based on the dataset from the AI catalog.

For implementation details, please refer to the [custom_model](./custom_model) directory and `custom.py` file.


## How to call the tool
To call or invoke the tool, send a properly formatted JSON request to the deployed model’s prediction endpoint in DataRobot using its API; the model processes your input and returns a prediction or summary, and this can be done programmatically via scripts, command-line tools like `curl`, or integrated into applications.

Please refer to the [making predictions](../README.md#making-predictions) section of documentation for global tools for more technical details on how to call the tool.

### Input structure
When invoking the tool, provide a JSON request as input. The JSON request must include a top-level `payload` object. All parameters listed below should be placed inside this payload object, which will be forwarded to the tool.

**Payload parameters**:
- `plotly_spec` (string): The Plotly JSON specification, serialized as a string.  
  You can reference columns from the dataframe (loaded from AI Catalog using the `dataset_id` parameter) by wrapping them in double curly braces, e.g., `{{column_name}}`. Example usage, where `{{x}}` and `{{y}}` will be replaced with the actual data from the dataset:

  ```json
  {
    "data": [
      {
        "type": "scatter",
        "mode": "markers",
        "x": {{x}},   // replaced with the contents of the `x` column
        "y": {{y}}    // replaced with the contents of the `y` column
      }
    ],
    "layout": {
      "title": "Scatterplot with 5 Random Points"
      // ...
    }
  }
- `datset_id` (string): The ID of the dataset in the AI catalog. It identifies an existing dataset within AI Catalog.
- `max_samples` (integer, optional, default 10000): The maximum number of samples to use.

Example:

```json
{
  "payload": {
    "plotly_spec": "{\n  \"data\": [\n    {\n      \"type\": \"scatter\",\n      \"mode\": \"markers\",\n      \"x\": {{sepal length (cm)}},\n      \"y\": {{sepal width (cm)}},\n      \"marker\": {\n        \"color\": {{SpeciesNumeric}},\n        \"size\": 8,\n        \"colorscale\": \"Viridis\",\n        \"showscale\": false\n      },\n      \"text\": {{Species}}\n    }\n  ],\n  \"layout\": {\n    \"title\": \"Scatter Plot for IRIS Dataset\",\n    \"xaxis\": {\"title\": \"Sepal Length (cm)\"},\n    \"yaxis\": {\"title\": \"Sepal Width (cm)\"},\n    \"width\": 600,\n    \"height\": 400,\n    \"hovermode\": \"closest\"\n  }\n}",
    "dataset_id": "683ee07e7e96db41ab02b263",
    "max_samples": 500
  }
}
```

### Output structure
The response will be a JSON object with a single key, `result`. The value is a string containing the Plotly chart object, serialized as JSON and wrapped in `<plotly>` markup. This can be directly rendered or further processed as needed.

```json
{
  "result": "<plotly>...plotly JSON chart object as a string...</plotly>"
}
```
