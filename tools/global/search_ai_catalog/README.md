# Search AI Catalog Tool

This tool is designed to search for datasets in the AI Catalog using a search query. It returns a list of datasets that match the query.

For implementation details, please refer to the [custom_model](./custom_model) directory and `custom.py` file.

## How to call the tool
To call or invoke the tool, send a properly formatted JSON request to the deployed model’s prediction endpoint in DataRobot using its API; the model processes your input and returns a prediction or summary. This can be done programmatically via scripts, command-line tools like `curl`, or integrated into applications.

Please refer to the [making predictions](../README.md#making-predictions) section of documentation for global tools for more technical details on how to call the tool.

### Input structure
When invoking the tool, provide a JSON request as input. The JSON request must include a top-level `payload` object. All parameters listed below should be placed inside this payload object, which will be forwarded to the tool.

**Payload parameters**:
- `search_terms` (string): Search terms to filter datasets. Leave empty to return all datasets.
- `limit` (integer, optional, default: 20): Maximum number of datasets to return. Use `-1` to return all.

Example:

```json
{
    "payload": {
        "search_terms": "iris",
        "limit": 10
    }
}
```

### Output structure
The output will be a JSON response with the result containing the summary in the markdown format.

```json
{
  "result": [
    {
      "dataset_id": "686cecb57210ef64110120b9",
      "dataset_name": "iris-full.csv"
    },
    {
      "dataset_id": "686ced017210ef64110120ba",
      "dataset_name": "iris-train.csv"
    }
  ]
}
```
