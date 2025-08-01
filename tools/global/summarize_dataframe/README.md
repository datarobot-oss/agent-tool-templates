# Summarize DataFrame Tool

This tool is designed to summarize a DataFrame and return the result in a markup format.

For implementation details, please refer to the [custom_model](./custom_model) directory and `custom.py` file.


## How to call the tool
To call or invoke the tool, send a properly formatted JSON request to the deployed model’s prediction endpoint in DataRobot using its API; the model processes your input and returns a prediction or summary. This can be done programmatically via scripts, command-line tools like `curl`, or integrated into applications.

Please refer to the [making predictions](../README.md#making-predictions) section of documentation for global tools for more technical details on how to call the tool.

### Input structure
When invoking the tool, provide a JSON request as input. The JSON request must include a top-level `payload` object. All parameters listed below should be placed inside this payload object, which will be forwarded to the tool.

**Payload parameters**:
- `dataframe` (string): CSV-formatted string with column names in the first row and data in the following rows.

Example:

```json
{
    "payload": {
        "dataframe": "sepal length (cm),sepal width (cm),petal length (cm),petal width (cm)\n5.1,3.5,1.4,0.2\n4.9,3.0,1.4,0.2\n4.7,3.2,1.3,0.2\n4.6,3.1,1.5,0.2\n5.0,3.6,1.4,0.2\n5.4,3.9,1.7,0.4\n4.6,3.4,1.4,0.3\n5.0,3.4,1.5,0.2\n4.4,2.9,1.4,0.2\n4.9,3.1,1.5,0.1\n5.4,3.7,1.5,0.2\n4.8,3.4,1.6,0.2\n4.8,3.0,1.4,0.1\n4.3,3.0,1.1,0.1\n5.8,4.0,1.2,0.2\n5.7,4.4,1.5,0.4\n5.4,3.9,1.3,0.4\n5.1,3.5,1.4,0.3\n5.7,3.8,1.7,0.3\n5.1,3.8,1.5,0.3\n5.4,3.4,1.7,0.2\n5.1,3.7,1.5,0.4\n4.6,3.6,1.0,0.2\n5.1,3.3,1.7,0.5\n4.8,3.4,1.9,0.2\n5.0,3.0,1.6,0.2\n5.0,3.4,1.6,0.4\n5.2,3.5,1.5,0.2\n5.2,3.4,1.4,0.2\n4.7,3.2,1.6,0.2\n4.8,3.1,1.6,0.2\n5.4,3.4,1.5,0.4\n5.2,4.1,1.5,0.1\n5.5,4.2,1.4,0.2\n4.9,3.1,1.5,0.2\n5.0,3.2,1.2,0.2\n5.5,3.5,1.3,0.2\n4.9,3.6,1.4,0.1\n4.4,3.0,1.3,0.2\n5.1,3.4,1.5,0.2\n5.0,3.5,1.3,0.3\n4.5,2.3,1.3,0.3\n4.4,3.2,1.3,0.2\n5.0,3.5,1.6,0.6\n5.1,3.8,1.9,0.4\n4.8,3.0,1.4,0.3\n5.1,3.8,1.6,0.2\n4.6,3.2,1.4,0.2\n5.3,3.7,1.5,0.2\n5.0,3.3,1.4,0.2\n7.0,3.2,4.7,1.4\n6.4,3.2,4.5,1.5\n6.9,3.1,4.9,1.5\n5.5,2.3,4.0,1.3\n6.5,2.8,4.6,1.5\n5.7,2.8,4.5,1.3\n6.3,3.3,4.7,1.6\n4.9,2.4,3.3,1.0\n6.6,2.9,4.6,1.3\n5.2,2.7,3.9,1.4\n5.0,2.0,3.5,1.0\n5.9,3.0,4.2,1.5\n6.0,2.2,4.0,1.0\n6.1,2.9,4.7,1.4\n5.6,2.9,3.6,1.3\n6.7,3.1,4.4,1.4\n5.6,3.0,4.5,1.5\n5.8,2.7,4.1,1.0\n6.2,2.2,4.5,1.5\n5.6,2.5,3.9,1.1\n5.9,3.2,4.8,1.8\n6.1,2.8,4.0,1.3\n6.3,2.5,4.9,1.5\n6.1,2.8,4.7,1.2\n6.4,2.9,4.3,1.3\n6.6,3.0,4.4,1.4\n6.8,2.8,4.8,1.4\n6.7,3.0,5.0,1.7\n6.0,2.9,4.5,1.5\n5.7,2.6,3.5,1.0\n5.5,2.4,3.8,1.1\n5.5,2.4,3.7,1.0\n5.8,2.7,3.9,1.2\n6.0,2.7,5.1,1.6\n5.4,3.0,4.5,1.5\n6.0,3.4,4.5,1.6\n6.7,3.1,4.7,1.5\n6.3,2.3,4.4,1.3\n5.6,3.0,4.1,1.3\n5.5,2.5,4.0,1.3\n5.5,2.6,4.4,1.2\n6.1,3.0,4.6,1.4\n5.8,2.6,4.0,1.2\n5.0,2.3,3.3,1.0\n5.6,2.7,4.2,1.3\n5.7,3.0,4.2,1.2\n5.7,2.9,4.2,1.3\n6.2,2.9,4.3,1.3\n5.1,2.5,3.0,1.1\n5.7,2.8,4.1,1.3\n6.3,3.3,6.0,2.5\n5.8,2.7,5.1,1.9\n7.1,3.0,5.9,2.1\n6.3,2.9,5.6,1.8\n6.5,3.0,5.8,2.2\n7.6,3.0,6.6,2.1\n4.9,2.5,4.5,1.7\n7.3,2.9,6.3,1.8\n6.7,2.5,5.8,1.8\n7.2,3.6,6.1,2.5\n6.5,3.2,5.1,2.0\n6.4,2.7,5.3,1.9\n6.8,3.0,5.5,2.1\n5.7,2.5,5.0,2.0\n5.8,2.8,5.1,2.4\n6.4,3.2,5.3,2.3\n6.5,3.0,5.5,1.8\n7.7,3.8,6.7,2.2\n7.7,2.6,6.9,2.3\n6.0,2.2,5.0,1.5\n6.9,3.2,5.7,2.3\n5.6,2.8,4.9,2.0\n7.7,2.8,6.7,2.0\n6.3,2.7,4.9,1.8\n6.7,3.3,5.7,2.1\n7.2,3.2,6.0,1.8\n6.2,2.8,4.8,1.8\n6.1,3.0,4.9,1.8\n6.4,2.8,5.6,2.1\n7.2,3.0,5.8,1.6\n7.4,2.8,6.1,1.9\n7.9,3.8,6.4,2.0\n6.4,2.8,5.6,2.2\n6.3,2.8,5.1,1.5\n6.1,2.6,5.6,1.4\n7.7,3.0,6.1,2.3\n6.3,3.4,5.6,2.4\n6.4,3.1,5.5,1.8\n6.0,3.0,4.8,1.8\n6.9,3.1,5.4,2.1\n6.7,3.1,5.6,2.4\n6.9,3.1,5.1,2.3\n5.8,2.7,5.1,1.9\n6.8,3.2,5.9,2.3\n6.7,3.3,5.7,2.5\n6.7,3.0,5.2,2.3\n6.3,2.5,5.0,1.9\n6.5,3.0,5.2,2.0\n6.2,3.4,5.4,2.3\n5.9,3.0,5.1,1.8\n"
    }
}
```

### Output structure
The output will be a JSON response with the result containing the summary in the markdown format.

```json
{
    "result": "<markdown>|       |   sepal length (cm) |   sepal width (cm) |   petal length (cm) |   petal width (cm) |\n|:------|--------------------:|-------------------:|--------------------:|-------------------:|\n| count |          150        |         150        |            150      |         150        |\n| mean  |            5.84333  |           3.05733  |              3.758  |           1.19933  |\n| std   |            0.828066 |           0.435866 |              1.7653 |           0.762238 |\n| min   |            4.3      |           2        |              1      |           0.1      |\n| 25%   |            5.1      |           2.8      |              1.6    |           0.3      |\n| 50%   |            5.8      |           3        |              4.35   |           1.3      |\n| 75%   |            6.4      |           3.3      |              5.1    |           1.8      |\n| max   |            7.9      |           4.4      |              6.9    |           2.5      |</markdown>"
}
```


