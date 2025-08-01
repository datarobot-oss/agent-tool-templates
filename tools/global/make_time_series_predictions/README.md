# Make Time-Series Predictions Tool

This tool is designed make time-series predictions using a custom model deployed in DataRobot.

For implementation details, please refer to the [custom_model](./custom_model) directory and `custom.py` file.


## How to call the tool
To call or invoke the tool, send a properly formatted JSON request to the deployed model’s prediction endpoint in DataRobot using its API; the model processes your input and returns a prediction or summary. This can be done programmatically via scripts, command-line tools like `curl`, or integrated into applications.

Please refer to the [making predictions](../README.md#making-predictions) section of documentation for global tools for more technical details on how to call the tool.

### Input structure
When invoking the tool, provide a JSON request as input. The JSON request must include a top-level `payload` object. All parameters listed below should be placed inside this payload object, which will be forwarded to the tool.

**Payload parameters**:
- `deployment_id` (string): The DataRobot deployment ID to request predictions from.
- `columns_to_return_with_predictions` (array of strings, required): A list of columns from the input data to merge back onto the output data for reference.
- `input_data_json_str` (string): A JSON-formatted array of rows to use for generating predictions.
- `input_dataframe` (string): A CSV-formatted string or a DataFrame cache ID to use for predictions.

- Example:

```json
{
    "payload": {
        "deployment_id": "68357303660a79b4805c6d61", 
        "forecast_point": "2014-01-01 00:00:05", 
        "columns_to_return_with_predictions": [
            "xtime", 
            "xmoney", 
            "xbool"
        ],
        "input_dataframe": "xdate,xtime,xint,xfloat,xcat,xtext,xmoney,xperc,xbool\n2014-01-01 00:00:00,2014-01-01 00:00:00,5,123.181023543,France,disloyal Lacy torching comparability Danelaw,$5.00,12%,True\n2014-01-02 00:00:00,2014-01-01 00:00:01,136,124.309099557,Australia,lawgiver's incomparable fulminated Micheal dew's,$136.00,12%,False\n2014-01-03 00:00:00,2014-01-01 00:00:02,145,95.1656058176,Australia,Hollywood's cynic's institutions hurrays excavators,$145.00,10%,False\n2014-01-04 00:00:00,2014-01-01 00:00:03,184,131.199256363,Australia,undecipherable tagging comedienne's Mennen civies,$184.00,13%,False\n2014-01-05 00:00:00,2014-01-01 00:00:04,23,106.306457123,Russia,congruent before flycatchers jabbering Velázquez,$23.00,11%,False\n2014-01-06 00:00:00,2014-01-01 00:00:05,97,107.082387522,Russia,handsomeness confederated misspelling chiropractics smart's,$97.00,11%,False\n2014-01-07 00:00:00,2014-01-01 00:00:06,183,130.165420105,France,detoxification unwieldiest viscera motorcyclist combustibility,$183.00,13%,False\n2014-01-08 00:00:00,2014-01-01 00:00:07,170,83.9755323187,Russia,suite's loudmouthed capacitance anaesthetized whoopee,$170.00,8%,False\n2014-01-09 00:00:00,2014-01-01 00:00:08,140,80.5545227328,Australia,Turin's debacle's tingling's hallucinogens Khoikhoi's,$140.00,8%,True\n",
        "registered_model_version_leaderboard_model_id": "68347697e8f9ed17461526b4"
    }
}
```

### Output structure
The output has the MIME type `text/csv` with `utf-8` encoding and contains the dataframe with predictions. The output will include the columns specified in `columns_to_return_with_predictions` along with the predictions generated by the model. 

```text
xtime,xmoney,xbool,prediction
2014-01-01 00:00:00,5.00,True,123.18
2014-01-01 00:00:01,136.00,False,124.31
2014-01-01 00:00:02,145.00,False,95.17
2014-01-01 00:00:03,184.00,False,131.20
2014-01-01 00:00:04,23.00,False,106.31
2014-01-01 00:00:05,97.00,False,107.08
2014-01-01 00:00:06,183.00,False,130.17
2014-01-01 00:00:07,170.00,False,83.98
2014-01-01 00:00:08,140.00,True,80.55
```
