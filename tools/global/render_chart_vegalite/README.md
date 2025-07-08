# Render Vega-Lite Chart Tool

This tool is designed to generate Vega-Lite charts based on the dataset from the AI catalog. 

For implementation details, please refer to the [custom_model](./custom_model) directory and `custom.py` file.


## How to call the tool
To call or invoke the tool, send a properly formatted JSON request to the deployed model’s prediction endpoint in DataRobot using its API; the model processes your input and returns a prediction or summary, and this can be done programmatically via scripts, command-line tools like `curl`, or integrated into applications.

Please refer to the [making predictions](../README.md#making-predictions) section of documentation for global tools for more technical details on how to call the tool.

### Input structure
When invoking the tool, provide a JSON request as input. The JSON request must include a top-level `payload` object. All parameters listed below should be placed inside this payload object, which will be forwarded to the tool.

**Payload parameters**:
- `vegalite_spec` (string): (string): The Vega-Lite JSON specification, serialized as a string. This specification defines the chart to be rendered. If the `data` field contains an AI Catalog `dataset_id`, the tool will automatically fetch the dataset and generate the chart.  

Example:

```json
{
    "payload": {
        "vegalite_spec": '{"$schema": "https://vega.github.io/schema/vega-lite/v5.json", "description": "A simple point chart for the IRIS dataset", "data": "683ee07e7e96db41ab02b263", "mark": {"type": "point"}, "encoding": {"x": {"field": "sepal length (cm)", "type": "quantitative"}, "y": {"field": "sepal width (cm)", "type": "quantitative"}, "color": {"field": "species", "type": "nominal"}}, "width": 400, "height": 300}'}
    }
}
```

### Output structure
The output will be a JSON response with the result containing a base64-encoded image of the chart, wrapped in the markup.

```json
{
  "result": "<imageb64>...base64-encoded contents of the chart image...</imageb64>" 
}
```
