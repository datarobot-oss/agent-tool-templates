# Get Data Registry Dataset Tool

This tool is designed to retrieve datasets from the Data Registry using a `dataset_id`. To paginate results, use the `limit` and `offset` parameters. These allow you to retrieve a specific range of rows from the dataset or process the dataset in manageable chunks.

For implementation details, please refer to the [custom_model](./custom_model) directory and `custom.py` file.


## How to call the tool
To call or invoke the tool, send a properly formatted JSON request to the deployed model’s prediction endpoint in DataRobot using its API; the model processes your input and returns a prediction or summary. This can be done programmatically via scripts, command-line tools like `curl`, or integrated into applications.

Please refer to the [making predictions](../README.md#making-predictions) section of documentation for global tools for more technical details on how to call the tool.

### Input structure
When invoking the tool, provide a JSON request as input. The JSON request must include a top-level `payload` object. All parameters listed below should be placed inside this payload object, which will be forwarded to the tool.

**Payload parameters**:
- `dataset_id` (string): The unique ID of the dataset from the DataRobot Data Registry.
- `offset` (integer, optional): The number of rows to skip. Defaults to 0. This parameter is effective only when used with the `limit` parameter.
- `limit` (integer, optional): The maximum number of rows to return. Defaults to None (returns all rows). This parameter is required to enable pagination.

Example:

```json
{
    "payload": {
        "dataset_id": "1234567890abcdef",
        "offset": 0,
        "limit": 3
    }
}
```

### Output structure
The output has the MIME type `text/csv` with `utf-8` encoding and contains the dataset as a CSV-formatted string. 

```text
id,animal,size
1,dog,medium
2,mouse,small
3,lion,big
```


